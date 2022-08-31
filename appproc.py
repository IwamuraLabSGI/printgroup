from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dt
import sys
import DBDB
from mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
from llah.descriptor_extractor import DescriptorExtractor
from llah.keypoint import Keypoint


args = sys.argv

def registFeatures(ID,color,image):
    image = cv2.imread(image)
    if image.shape[2]==3:
        grayimage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        grayimage = image
    retC, invImage = cv2.threshold(grayimage,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(invImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointID = 0
    j=0
    cx = [0] * len(contours)
    cy = [0] * len(contours)
    for i in range(len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if(M['m00']>50):
            cx[j] = int(M['m10']/M['m00'])
            cy[j] = int(M['m01']/M['m00'])
            cv2.circle(image, (cx[i],cy[i]), 4, 100, 2, 4)
            j=j+1
    if color==1:
        image_1 = cv2.drawContours(image, contours, -1, (255,255, 0), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procCyan.jpg', image_1)
        DBDB.Register(1,ID,cx,cy)
    elif color==2:
        image_1 = cv2.drawContours(image, contours, -1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procMagenda.jpg', image_1)
        DBDB.Register(2,ID,cx,cy)
    else:
        image_1 = cv2.drawContours(image, contours, -1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procYellow.jpg', image_1)
        DBDB.Register(3,ID,cx,cy)
    print("カラー：",color,"　総特徴点数：",j)
    points = np.zeros((j, 3))
    for i in range(j):
        points[i][0]=cx[i]
        points[i][1]=cy[i]
        points[i][2]=100
    keypoints = list(map(lambda key: Keypoint(key[0], key[1], key[2]), points))
    return keypoints

def detectFeatures(ID,color,image):
    image = cv2.imread(image)
    if image.shape[2]==3:
        grayimage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        grayimage = image
    retC, invImage = cv2.threshold(grayimage,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(invImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointID = 0
    j=0
    cx = [0] * len(contours)
    cy = [0] * len(contours)
    for i in range(len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if(M['m00']>50):
            cx[j] = int(M['m10']/M['m00'])
            cy[j] = int(M['m01']/M['m00'])
            cv2.circle(image, (cx[i],cy[i]), 4, 100, 2, 4)
            j=j+1
    if color==1:
        image_1 = cv2.drawContours(image, contours, -1, (255,255, 0), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procCyan.jpg', image_1)
        
    elif color==2:
        image_1 = cv2.drawContours(image, contours, -1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procMagenda.jpg', image_1)
    else:
        image_1 = cv2.drawContours(image, contours, -1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procYellow.jpg', image_1)
    points = np.zeros((j, 3))
    for i in range(j):
        points[i][0]=cx[i]
        points[i][1]=cy[i]
        points[i][2]=100
    keypoints = list(map(lambda key: Keypoint(key[0], key[1], key[2]), points))
    print("カラー：",color,"　総特徴点数：",j)
    return keypoints
