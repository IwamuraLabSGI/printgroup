from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dt
import sys

args = sys.argv


def colorInk(src, dst, ch1Lower, ch1Upper, ch2Lower, ch2Upper, ch3Lower, ch3Upper):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    lower = [0, 0, 0]
    upper = [0, 0, 0]
    lower[0] = ch1Lower
    lower[1] = ch2Lower
    lower[2] = ch3Lower
    upper[0] = ch1Upper
    upper[1] = ch2Upper
    upper[2] = ch3Upper
    hsv = [0, 0, 0]
    size = src.shape
    tmp = src
    for y in range(0, size[0]):
        for x in range(0, size[1]):
            hsv[0] = src[y, x][0]
            hsv[1] = src[y, x][1]
            hsv[2] = src[y, x][2]

            if lower[0] <= upper[0]:
                if lower[0] <= hsv[0] and hsv[0] <= upper[0] and lower[1] <= hsv[1] and hsv[1] <= upper[1] and lower[
                    2] <= hsv[2] and hsv[2] <= upper[2]:
                    src[y, x][0] = src[y, x][0]
                    src[y, x][1] = src[y, x][1]
                    src[y, x][2] = src[y, x][2]

                else:
                    src[y, x][0] = 0
                    src[y, x][1] = 0
                    src[y, x][2] = 0
            else:
                if lower[0] <= hsv[0] or hsv[0] <= upper[0]:
                    if lower[1] <= hsv[1] and hsv[1] <= upper[1] and lower[2] <= hsv[2] and hsv[2] <= upper[2]:
                        src[y, x][0] = src[y, x][0]
                        src[y, x][1] = src[y, x][1]
                        src[y, x][2] = src[y, x][2]

                else:
                    src[y, x][0] = 0
                    src[y, x][1] = 0
                    src[y, x][2] = 255

    src = cv2.cvtColor(src, cv2.COLOR_HSV2BGR)
    return src


def imageclear():
    cv2.imwrite("./templates/IMG/AKAZE.jpg", 0)
    cv2.imwrite("./templates/IMG/FakeAKAZE.jpg", 0)
    cv2.imwrite("./templates/IMG/INPUT.jpg", 0)
    cv2.imwrite("./templates/IMG/Cyan.jpg", 0)
    cv2.imwrite("./templates/IMG/Magenda.jpg", 0)
    cv2.imwrite("./templates/IMG/Yellow.jpg", 0)
    cv2.imwrite("./templates/IMG/procCyan.jpg", 0)
    cv2.imwrite("./templates/IMG/procMagenda.jpg", 0)
    cv2.imwrite("./templates/IMG/procYellow.jpg", 0)


def colorExtraction1(src, dst,
                     ch1Lower, ch1Upper,
                     ch2Lower, ch2Upper,
                     ch3Lower, ch3Upper):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    lower = [0, 0, 0]
    upper = [0, 0, 0]
    TEKIOU = 0
    akazu = 0
    bkazu = 0
    lower[0] = ch1Lower
    lower[1] = ch2Lower
    lower[2] = ch3Lower
    upper[0] = ch1Upper
    upper[1] = ch2Upper
    upper[2] = ch3Upper
    hsv = [0, 0, 0]
    size = src.shape
    tmp = np.zeros([size[0], size[1]])
    for y in range(0, size[0]):
        for x in range(0, size[1]):
            hsv[0] = src[y, x][0]
            hsv[1] = src[y, x][1]
            hsv[2] = src[y, x][2]

            if lower[0] <= upper[0]:
                if lower[0] <= hsv[0] and hsv[0] <= upper[0] and lower[1] <= hsv[1] and hsv[1] <= upper[1] and lower[
                    2] <= hsv[2] and hsv[2] <= upper[2]:
                    tmp[y, x] = 255
                    akazu = abs(hsv[0] - 90)
                    bkazu = bkazu + 1
                    TEKIOU = TEKIOU + akazu
                else:
                    tmp[y, x] = 0
            else:
                if lower[0] <= hsv[0] or hsv[0] <= upper[0]:
                    if lower[1] <= hsv[1] and hsv[1] <= upper[1] and lower[2] <= hsv[2] and hsv[2] <= upper[2]:
                        tmp[y, x] = 255
                    akazu = abs(hsv[0] - 90)
                    bkazu = bkazu + 1
                    TEKIOU = TEKIOU + akazu
                else:

                    tmp[y, x] = 0

    return TEKIOU / bkazu


def register(ID, img):
    x = int(img.shape[0] * (1280 / img.shape[1]))
    img = cv2.resize(img, dsize=(1280, x))
    cv2.imwrite("./templates/RegistIMG/" + str(ID) + ".jpg", img)


# TODO: 引数でIDからpathを作って最適化した画像を保存するのではなく、画像情報を返す。
# TODO: 使用していない処理、変数を消す。
def main(ID, img):
    x = int(img.shape[0] * (1280 / img.shape[1]))
    img = cv2.resize(img, dsize=(1280, x))
    "1.原画像の入力"
    print("入力中")
    cv2.imwrite("./templates/IMG/INPUT.jpg", img)
    src = img
    src_img_orig = src
    print("The Ink Process: ")
    alpha = 1.0
    size = src.shape

    "2.コントラスト調整①-線形変換"
    print("線形変換")
    Max = [0, 0, 0]
    Min = [255, 255, 255]

    "3.コントラスト調整②-積和演算"
    print("積和演算")
    alpha = 1.0
    AVR = [0, 0, 0]
    CC = [0, 0, 0]
    beta = [0, 0, 0]
    new2_img = np.zeros([size[0], size[1]])

    "4.画像の先鋭化フィルター"
    print("先鋭中")
    k = 1.0
    sharpningKernel8 = np.array([[k, k, k], [k, 1 + (8 * k * -1), k], [k, k, k]])

    "5.画像の彩度の算出(白抜き画像の生成)"
    print("白抜き中")
    Hue = 0.0
    white = np.zeros([size[0], size[1]])

    "6.インク抽出処理とビット反転"
    print("インク抽出")
    x_Cyan = 0.0
    y_Cyan = 0.0
    x_MY = 0.0
    y_MY = 0.0
    x_Cyan = Hue
    y_Cyan = (-1.043 * x_Cyan) + 186.44
    x_MY = Hue
    y_Cyan = (1.429 * x_MY) + 25.71
    img_Cyan = np.zeros([size[0], size[1], size[2]])
    img_Cyan = colorInk(src, img_Cyan, 90, 150, 70, 255, 180, 255)
    img_Magenda = np.zeros([size[0], size[1], size[2]])
    img_Magenda = colorInk(src, img_Magenda, 150, 255, 60, 255, 180, 255)
    img_Yellow = np.zeros([size[0], size[1], size[2]])
    img_Yellow = colorInk(src, img_Yellow, 15, 65, 60, 255, 180, 255)

    "7.グレースケール変換"
    print("グレースケール")
    img_Cyan = cv2.cvtColor(img_Cyan, cv2.COLOR_BGR2GRAY)
    img_Magenda = cv2.cvtColor(img_Magenda, cv2.COLOR_BGR2GRAY)
    img_Yellow = cv2.cvtColor(img_Yellow, cv2.COLOR_BGR2GRAY)

    "8.適応2値化"
    print("適応")
    img_Cyan = cv2.adaptiveThreshold(img_Cyan, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 0)
    img_Magenda = cv2.adaptiveThreshold(img_Magenda, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 0)
    img_Yellow = cv2.adaptiveThreshold(img_Yellow, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 0)

    "9.2値化"
    print("通常")
    retC, img_Cyan = cv2.threshold(img_Cyan, 127, 255, cv2.THRESH_BINARY)
    retM, img_Magenda = cv2.threshold(img_Magenda, 127, 255, cv2.THRESH_BINARY)
    retY, img_Yellow = cv2.threshold(img_Yellow, 127, 255, cv2.THRESH_BINARY)

    "10.出力画像の保存"
    print("保存")
    out = [0, 0, 0, 0]
    out[0] = "./templates/CyanIMG/" + str(ID) + ".jpg"
    out[1] = "./templates/MagendaIMG/" + str(ID) + ".jpg"
    out[2] = "./templates/YellowIMG/" + str(ID) + ".jpg"
    cv2.imwrite(out[0], img_Cyan)
    cv2.imwrite(out[1], img_Magenda)
    cv2.imwrite(out[2], img_Yellow)

    return None
