# program to capture single image from webcam in python

import cv2
import os
from datetime import datetime


def get():
    user = os.getenv("USERPROFILE")
    time = str(datetime.now().day) + '' + str(datetime.now().month) + '' + str(datetime.now().year) + '' + str(datetime.now().second)
    filename = user + "\\Desktop\\" + time + ".png"

    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()

    cv2.imshow("SayCheese", image)
    cv2.imwrite(filename, image)
    # cv2.waitKey(0)
    os.system(filename)
    cv2.destroyWindow("SayCheese")