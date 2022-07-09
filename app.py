#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
import numpy as np
import cv2
import os
from datetime import datetime as dt
import sys
import appink
import appakaze
import appproc
import DBDB
args = sys.argv

app = Flask(__name__, static_url_path="",static_folder="./templates/IMG")

# 処理した画像ファイルの保存先
IMG_DIR = "static"
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR + IMG_DIR

# 保存先のパスがなければ作成
if not os.path.isdir(IMG_PATH):
    os.mkdir(IMG_PATH)

# グレースケール変換
def rgb_to_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

@app.route('/', methods=['GET', 'POST'])
def index():
    starttime = datetime.now()
    alltime = 0
    print("開始時間： ",starttime)
    appink.imageclear()
    time = '画像入力待ち'
    img_name = ""
    Hantei = 0
    ID = 0
    if request.method == 'POST':
    # 画像をロード
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
    # グレースケール変換
            time = "画像入力待ち　⇨ 真贋判定開始"
            appink.main(ID,img)
            appproc.detectall(ID)
            Hantei = appakaze.AKAZEmain(ID,img)
            endtime = datetime.now()
            alltime = endtime - starttime
            print("終了時間： ",endtime)
            print("処理時間： ",alltime)
            time = "画像入力待ち ⇨ 真贋判定開始 ⇨ 真贋判定終了(画像左から入力画像、CMY、AKAZE判定)"
    # 画像の保存


    return render_template('index.html', img_name=img_name,Hantei= Hantei,time=time,alltime=alltime)

@app.route('/form', methods=['GET', 'POST'])
def form():
    appink.imageclear()
    ID = 0
    time = "登録画像待ち"
    img_name = ""
    if request.method == 'POST':
    # 画像をロード
        
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
    # グレースケール変換
            time = "画像入力待ち ⇨ 真贋判定開始"
            ID = DBDB.NewID()
            appink.main(ID,img)
            appink.register(ID,img)
            appproc.registall(ID)
            time = "登録画像待ち ⇨ 登録が完了しました(左から順に入力画像、CMY画像)"
    # 画像の保存

    return render_template('form.html', img_name=img_name,time=time,ID=ID)

if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)