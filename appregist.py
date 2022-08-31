from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dt
import sys
import DBDB
import appproc
from mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
from llah.descriptor_extractor import DescriptorExtractor
from llah.keypoint import Keypoint


args = sys.argv


def registall(ID):
    print("特徴点抽出中 (上からシアン・マゼンダ・イエロー)")
    Cyankey = appproc.register_features(ID, 1, "./templates/CyanIMG/" + str(ID) + ".jpg")
    Magendakey = appproc.register_features(ID, 2, "./templates/MagendaIMG/" + str(ID) + ".jpg")
    Yellowkey = appproc.register_features(ID, 3, "./templates/YellowIMG/" + str(ID) + ".jpg")
    print("特徴量算出中 (上からシアン・マゼンダ・イエロー)")
    descriptor_extractor = DescriptorExtractor(6, 1)
    Cyandescriptors = descriptor_extractor.OLDextract(Cyankey)
    Magendadescriptors = descriptor_extractor.OLDextract(Magendakey)
    Yellowdescriptors = descriptor_extractor.OLDextract(Yellowkey)
    DBDB.RegisterFeature(1,ID,Cyandescriptors)
    DBDB.RegisterFeature(2,ID,Magendadescriptors)
    DBDB.RegisterFeature(3,ID,Yellowdescriptors)
    return None

