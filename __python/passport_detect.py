import cv2
from PIL import Image
import pytesseract
import time
import re

cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

banner = cv2.imread('banner.jpg')
banner1 = cv2.imread('banner1.jpg')

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('window', gray)
    img_pil = Image.fromarray(gray)


    txt = pytesseract.image_to_string(img_pil, lang='rus')
    if 'ОПЯКИН' in txt and 'РОМАН' in txt and 'СЕРГЕЕВИЧ' in txt and '14.02.1999' in txt:
        print('passport of Roma')
        cv2.imshow('window', banner)
        while 1:
            k = cv2.waitKey(30) & 0xff
            time.sleep(3)
            break


    if 'САТАЕВ' in txt and 'ЭМИЛЬ' in txt and 'РОБЕРТОВИЧ' in txt and '01.11.1999' in txt:
        print('passport of Emil')
        cv2.imshow('window', banner1)
        while 1:
            k = cv2.waitKey(30) & 0xff
            time.sleep(3)
            break

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break