import numpy as np
import cv2
import imutils
import math
from imutils.object_detection import non_max_suppression
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

def dline(a, b, h, g, u_people, i_people):
    f = h/u_people
    f2 = g/i_people
    f = ((f2*g/2)^2 + (g*f)^2)**(1/2)
    fg = ((f*f + f2*f2)**(1/2))**(1/2)
    return fg

def coord(a, dline2):
    x = dline2*math.cos(a)
    y = dline2*math.sin(a)
    return x,y

class Data:
    x_ = 0
    y_ = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('{} {}'.format(Data.x_, Data.y_).encode())


serv = HTTPServer(("0.0.0.0", 8080), Handler)
serv_t = threading.Thread(target=serv.serve_forever)
serv_t.daemon = True
serv_t.start()

cv2.namedWindow("img", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


while 1:
    ret, img = cap.read()
    img = imutils.resize(img, width=min(300, img.shape[1]))
    orig = img.copy()

    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4),
                                            padding=(8, 8), scale=1.05)


    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 255), 2)
        Data.x_, Data.y_ = coord(53, dline(53, 47, 2, 3, xA - xB, yA - yB))

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
