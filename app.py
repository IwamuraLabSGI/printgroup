#!/usr/bin/env python
from flask import Flask, render_template, request
from datetime import datetime
import numpy as np
import cv2
import os
import appink
import appakaze
import appretrieve
import DBDB
import appregist

app = Flask(__name__, static_url_path="", static_folder="./templates/IMG")

# 処理した画像ファイルの保存先
IMG_DIR = "static"
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR + IMG_DIR

# 保存先のパスがなければ作成
if not os.path.isdir(IMG_PATH):
    os.mkdir(IMG_PATH)


@app.route('/', methods=['GET', 'POST'])
def index():
    start_time = datetime.now()
    all_time = 0
    print("開始時間： ", start_time)
    # TODO: 同時アクセスがあったときに不具合が発生する
    appink.imageclear()
    time = '画像入力待ち'
    img_name = ""
    Hantei = 0
    ID = 0
    LLAH = [[[0, 1], [2, 3], [4, 5]], [[6, 7], [8, 9], [10, 11]], [[12, 13], [14, 15], [16, 17]]]
    AKAZE = [0] * 9
    n = 0
    if request.method == 'POST':
        # 画像をロード
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
            # TODO: IDからstaticフォルダないの画像を特定して渡すのではなくメモリの画像情報を共有する
            appink.main(ID, img)
            LLAH = appretrieve.retrieve_all(ID)
            for i in range(3):
                for j in range(3):
                    if LLAH[i][j][0] != 0:
                        AKAZE[n] = appakaze.AKAZEmain(LLAH[i][j][0], img)
                    n = n + 1
            Hantei = max(AKAZE)
            end_time = datetime.now()
            all_time = end_time - start_time
            print("終了時間： ", end_time)
            print("処理時間： ", all_time)
            time = "画像入力待ち ⇨ 真贋判定開始 ⇨ 真贋判定終了(画像左から入力画像、CMY、AKAZE判定)"
    # 画像の保存

    return render_template('index.html', img_name=img_name, Hantei=Hantei, time=time, alltime=all_time, LLAH=LLAH,
                           AKAZE=AKAZE)


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
            ID = DBDB.NewID()
            appink.main(ID, img)
            appink.register(ID, img)
            appregist.registall(ID)
            time = "登録画像待ち ⇨ 登録が完了しました(左から順に入力画像、CMY画像)"
    # 画像の保存

    return render_template('form.html', img_name=img_name, time=time, ID=ID)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
