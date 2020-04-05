# coding: UTF-8
from PIL import Image
import sys

import cv2
#import webbrowser #webブラウザを起動できるように

# -*- coding: utf-8 -*-
from selenium import webdriver

import numpy as np
#自前で用意したマウスの制御クラス
import mouse

import requests
import json #Google Cloud Vision APIのために必要
import base64  # 画像はbase64でエンコードする必要があるため
import copy #mutableなオブジェクトの深いコピー
import subprocess   #pythonからUNIXコマンドを実行

#GCVAPIの利用のために必要なAPI key
API_KEY = "" # YOUR OWN API KEY


#マウスによる範囲選択枠書き込みの保存フレーム
temp_frame = None
#pre_frame = None
#change_frame = None

#Googleの画像認識を使用するための関数
def text_detection(image_path):
    api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)
    with open(image_path, "rb") as img:
        image_content = base64.b64encode(img.read())
        req_body = json.dumps({
            'requests': [{
                'image': {
                    'content': image_content.decode('utf-8')  # base64でエンコードしたものをjsonにするためdecodeする
                },
                'features': [{
                    'type': 'TEXT_DETECTION'
                }]
            }]
        })
        res = requests.post(api_url, data=req_body)
        return res.json()   #東洋経済でいま話題のjsonファイルを返す


def main():
    cap = cv2.VideoCapture(0)

    #表示するwindows名
    cv2.namedWindow("input window")

    cap.set(15, 0.8)

    drawing = False #クリックされているときTrue
    ix, iy, x, y = -1, -1, -1, -1   #範囲選択の矩形の対角点の座標

    #
    mouseData = mouse.mouseParam("input window")

    #カメラのモード。Trueのとき映像キャプチャ、falseのとき静止撮影
    mode = True


    while(True):
        #キーボードの入力待ち
        key = cv2.waitKey(1) & 0xFF
        # qが押された場合は終了する
        if  key == ord('q'):        #81:   #q
            break

        #映像キャプチャモード
        if mode == True:
            # フレームをキャプチャする
            ret, frame = cap.read()
            cv2.imshow("input window",frame)

            #p（photo）で静止撮影モード
            if key == ord('p'):     #:80:   #p
                mode = False
                tmp_frame = copy.deepcopy(frame)    #現在のキャプチャ画像を静止画像として保存。深いコピー

        #静止撮影モード
        elif mode == False:
            cv2.imshow("input window", frame)

            #マウスが左クリックされたとき
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                drawing = True  #範囲選択モード開始
                ix, iy = mouseData.getX(), mouseData.getY()

            #マウスが動いているとき（ドラッグ中）
            elif mouseData.getEvent() == cv2.EVENT_MOUSEMOVE:
                if drawing == True: #範囲選択中なら
                    frame = copy.deepcopy(tmp_frame)    #現在のフレームを保存した静止画像にしてから
                    cv2.rectangle(frame, (ix,iy), (mouseData.getX(), mouseData.getY()), (0,255,0), 2)   #その上に長方形を新規に書き込み

            #マウスの左クリックが離れたら
            elif mouseData.getEvent() == cv2.EVENT_LBUTTONUP:
                drawing = False #範囲選択モード終了 範囲選択決定
                x, y = mouseData.getX(), mouseData.getY()   #範囲選択決定の座標に現在のマウスの座標を入れる

            #m（movie）が押されたら映像キャプチャモードに
            if key == ord('m'):     #77:   #m
                mode = True
                ix, iy, x, y = -1, -1, -1, -1

            if key== ord('t'):      #.txtファイルの作成
                make_textfile(tmp_frame, ix, iy, x, y)

            if key == ord('u'):     #URLへのアクセス
                open_url(tmp_frame, ix, iy, x, y)

            if key == ord('c'):     #.cppファイルの作成
                make_cppfile(tmp_frame, ix, iy, x, y)

    cap.release()
    cv2.destroyAllWindows()




#.txtファイルの作成
def make_textfile(frame, ix, iy, x, y):
    roi = frame[iy:y, ix:x] #フレームから選択範囲だけを切り取り
    cv2.imwrite("text.png",roi) #png画像として書き出し

    img_path = "text.png"   #書き出した画像ファイルのパス
    res_json = text_detection(img_path) #そのパスをAPIにわたす
    res_text = res_json["responses"][0]["textAnnotations"][0]["description"]    #返ってきた結果をテキストに
    print(res_text) #一応ターミナルでprint
    with open("text.txt", "w", encoding = "utf-8") as f:    #.txtファイルに書き込み
        f.write(res_text)

    #ターミナルの呼び出しコマンドを使ってアプリで開く
    args = ['open', 'text.txt']
    try:
        print(subprocess.check_call(args))  #作った.txtファイルをmac標準テキストエディタで開く
    except:
        print("Error.")

#以下2つもだいたい同じ

def open_url(frame, ix, iy, x, y):
    roi = frame[iy:y, ix:x]
    cv2.imwrite("url.png",roi)

    img_path = "url.png"
    res_json = text_detection(img_path)
    url = res_json["responses"][0]["textAnnotations"][0]["description"]

    correct_url = url.replace(' ', '_') #時々誤認識としてスペースが入るので、アンダーバーに置換
    browser = webdriver.Chrome('/Users/d_kasuga/Library/Mobile Documents/com~apple~CloudDocs/software/GCVA/chromedriver')   #Chromeのドライバー取得
    browser.get(correct_url)    #ブラウザーでURLを開く

    print("correct_url")
    with open("url.txt", "w", encoding = "utf-8") as f:
        f.write(correct_url)

def make_cppfile(frame, ix, iy, x, y):
    roi = frame[iy:y, ix:x]
    cv2.imwrite("cppfile.png",roi)

    img_path = "cppfile.png"
    res_json = text_detection(img_path)
    res_text = res_json["responses"][0]["textAnnotations"][0]["description"]
    with open("cppfile.cpp", "w", encoding = "utf-8") as f:
        f.write(res_text)

    args = ['code', 'cppfile.cpp']
    try:
        print(subprocess.check_call(args))  #作った.cppファイルをcodeで開く
    except:
        print("Error.")

if __name__ == "__main__":
    main()
