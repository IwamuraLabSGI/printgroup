from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dt
import sys

args = sys.argv


def AKAZEmain(ID, query, img):
    print("AKAZE中", query)
    img1 = img
    img2 = cv2.imread("./templates/RegistIMG/" + str(query) + ".jpg")
    x1 = int(img1.shape[0] * (1280 / img1.shape[1]))
    x2 = int(img2.shape[0] * (1280 / img2.shape[1]))
    img1 = cv2.resize(img1, dsize=(1280, x1))
    img2 = cv2.resize(img2, dsize=(1280, x2))
    akaze = cv2.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(img1, None)
    kp2, des2 = akaze.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    "ここのratioを変更すると、マッチング率が変わる"
    good = []
    for m in matches:
        if m.distance < 20:
            good.append([m])

    img_akaze = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
    if (len(good) > 20):
        cv2.imwrite("./templates/IMG/AKAZE.jpg", img_akaze)
    else:
        cv2.imwrite("./templates/IMG/FakeAKAZE.jpg", img_akaze)
    print(len(good))
    return len(good)
