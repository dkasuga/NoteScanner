# NoteScanner
- This is a very simple OCR app. It transcribes the text in the image to .txt file or converts codes on a book to .cpp file. You can also directly access the URLs in the images.

- This is my work for a software development contest during software-2 class.


## How to use
1. Execute main.py and you see the movie recorded by face WebCam.
2. Put something you want to transcribe and press 'p', and the screen freezes.
3. Use the mouse pointer to enclose the area you want to read.
4. Press the follwing key, and each of them corresponds to the save format.
    - 't' read texts as simple texts and save them as .txt file

    | input                                                                | output                                                               |
    | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
    | ![](https://github.com/dkasuga/NoteScanner/blob/master/img/img2.png) | ![](https://github.com/dkasuga/NoteScanner/blob/master/img/out1.png) |

    - 'u' read texts as URL and open the page in your web browser.

    | input                                                                | output                                                               |
    | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
    | ![](https://github.com/dkasuga/NoteScanner/blob/master/img/img3.png) | ![](https://github.com/dkasuga/NoteScanner/blob/master/img/out3.png) |

    - 'c' read texts as C++ codes and make .cpp file

    | input                                                                | output                                                               |
    | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
    | ![](https://github.com/dkasuga/NoteScanner/blob/master/img/img1.png) | ![](https://github.com/dkasuga/NoteScanner/blob/master/img/out2.png) |

## Dependencies
- opencv
- numpy
- selenium
- requests
- Depends on Google Cloud Vision API. You have to register for the service and get an API key, which should be set to API_KEY in main.py
