from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dt
import sys
import DBDB
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
    cx = [0] * len(contours)
    cy = [0] * len(contours)
    for i in range(len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if(M['m00']>50):
            cx[i] = int(M['m10']/M['m00'])
            cy[i] = int(M['m01']/M['m00'])
            cv2.circle(image, (cx[i],cy[i]), 4, 100, 2, 4)
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
    
    return None

def detectFeatures(ID,color,image):
    image = cv2.imread(image)
    if image.shape[2]==3:
        grayimage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    else:
        grayimage = image
    retC, invImage = cv2.threshold(grayimage,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(invImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pointID = 0
    cx = [0] * len(contours)
    cy = [0] * len(contours)
    for i in range(len(contours)):
        cnt = contours[i]
        M = cv2.moments(cnt)
        if(M['m00']>50):
            cx[i] = int(M['m10']/M['m00'])
            cy[i] = int(M['m01']/M['m00'])
            cv2.circle(image, (cx[i],cy[i]), 4, 100, 2, 4)
    if color==1:
        image_1 = cv2.drawContours(image, contours, -1, (255,255, 0), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procCyan.jpg', image_1)
        
    elif color==2:
        image_1 = cv2.drawContours(image, contours, -1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procMagenda.jpg', image_1)
    else:
        image_1 = cv2.drawContours(image, contours, -1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imwrite('./templates/IMG/procYellow.jpg', image_1)
    
    return None

def detectall(ID):
    print("特徴点抽出中")
    detectFeatures(ID,1,"./templates/IMG/Cyan.jpg")
    detectFeatures(ID,2,"./templates/IMG/Yellow.jpg")
    detectFeatures(ID,3,"./templates/IMG/Magenda.jpg")
    return None

def registall(ID):
    print("特徴点登録中")
    registFeatures(ID,1,"./templates/IMG/Cyan.jpg")
    registFeatures(ID,2,"./templates/IMG/Yellow.jpg")
    registFeatures(ID,3,"./templates/IMG/Magenda.jpg")
    return None

