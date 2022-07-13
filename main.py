import numpy as np

from mysql import MySQL, MySQLConfig
from repository.mysql.qr_code import QRCode as QRCodeRepo
from service.qr_code import QRCode as QRCodeSvc
import sys
from llah.keypoint_extractor import KeypointExtractor
from llah.descriptor_extractor import DescriptorExtractor
from PIL import Image


def adjust_luminance(img: np.ndarray):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # 線形変換
    min_lum = img.min()
    max_lum = img.max()
    return (img - min_lum) * (255 / (max_lum - min_lum))


mysqlConfig = MySQLConfig(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='qr_auth'
)

mysql = MySQL(mysqlConfig)
mysql.connect()
qrCodeRepo = QRCodeRepo(mysql)
qrCodeSvc = QRCodeSvc(qrCodeRepo)

args = sys.argv
with Image.open(args[1]) as img:
    # グレーの領域を白に
    hsv_img = img.convert("HSV")
    hsv_img_data = np.asarray(hsv_img, np.uint8)
    v_img_data = hsv_img_data[:, :, 2]
    v_img_data = adjust_luminance(v_img_data)
    img_data = np.asarray(img, np.uint8)
    img_filter = v_img_data > 170
    reverted_img_filter = np.logical_not(img_filter)
    filtered_img_data = np.zeros(img_data.shape)
    filtered_img_data[:, :, 0] = img_data[:, :, 0] * img_filter + reverted_img_filter * 255
    filtered_img_data[:, :, 1] = img_data[:, :, 1] * img_filter + reverted_img_filter * 255
    filtered_img_data[:, :, 2] = img_data[:, :, 2] * img_filter + reverted_img_filter * 255
    img = Image.fromarray(np.uint8(filtered_img_data))

    cmyk_img = img.convert('CMYK')
    cmyk_img_data = np.asarray(cmyk_img, np.uint8)

    # cyan抽出
    c_img_data = cmyk_img_data[:, :, 0]
    c_img_data = adjust_luminance(c_img_data)
    # TODO: 平滑化などの前処理
    c_img_filter = c_img_data > 120
    c_img_data = c_img_data * c_img_filter

    keypoints = KeypointExtractor.extract(c_img_data)
    descriptor_extractor = DescriptorExtractor(5, 2)
    descriptors = descriptor_extractor.extract(keypoints)
    # TODO: ハッシュ計算考える
    features = list(map(lambda item: sum(item), descriptors))
    qrCodeSvc.add(features)





