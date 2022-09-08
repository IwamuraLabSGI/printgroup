import math

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from llah.keypoint_extractor import KeypointExtractor
from llah.descriptor_extractor import DescriptorExtractor


class Feature:
    EFFECTIVE_DECIMAL_DIGIT = 3

    @classmethod
    def __discretize(cls, val: float):
        if val > 1:
            val = 1 / val
        result = math.floor(val * (10 ** cls.EFFECTIVE_DECIMAL_DIGIT))
        return result

    @classmethod
    def get_from_descriptor(cls, descriptor: list[float]):
        discretized_elements: list[float] = []
        for elem in descriptor:
            discretized_elements.append(Feature.__discretize(elem))

        feature = 0
        discretized_elements.sort()
        for i, elem in enumerate(discretized_elements):
            feature += elem * ((10 ** cls.EFFECTIVE_DECIMAL_DIGIT) ** i)
        return feature


def adjust_luminance(img: np.ndarray):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # 線形変換
    min_lum = img.min()
    max_lum = img.max()
    return (img - min_lum) * (255 / (max_lum - min_lum))


def filter_cyan(img):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # TODO: 平滑化などの前処理
    img_filter = img > 120
    return img * img_filter


def filter_magenta(img):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # TODO: 平滑化などの前処理
    img_filter = img > 120
    return img * img_filter


def filter_yellow(img):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # TODO: 平滑化などの前処理
    img_filter = img > 120
    return img * img_filter


def get_features(img: np.ndarray):
    keypoints = KeypointExtractor.extract(img)
    descriptor_extractor = DescriptorExtractor(6, 2)
    descriptors = descriptor_extractor.extract(keypoints)
    features: list[float] = []
    for descriptor in descriptors:
        features.append(Feature.get_from_descriptor(descriptor))
    return features


def get_cyan_filter_from_hue(hue: np.ndarray):
    cyan = 180 / 360 * 256
    width = 30
    return (hue > (cyan - width)) * (hue < (cyan + width))


def get_magenta_filter_from_hue(hue: np.ndarray):
    magenta = 300 / 360 * 256
    width = 30
    return (hue > (magenta - width)) * (hue < (magenta + width))


def get_yellow_filter_from_hue(hue: np.ndarray):
    yellow = 60 / 360 * 256
    width = 30
    return (hue > (yellow - width)) * (hue < (yellow + width))


def get_cmy_features_from_img(img):
    hsv_img = img.convert("HSV")
    hsv_img_data = np.array(hsv_img, np.uint8)

    # h_unique, h_counts = np.unique(hsv_img_data[:, :, 0], return_counts=True)
    # plt.bar(h_unique, h_counts, width=1.0)
    # plt.show()

    s_filter = hsv_img_data[:, :, 1] > 70
    v_filter = hsv_img_data[:, :, 2] > 50
    hsv_img_data[:, :, 0] = hsv_img_data[:, :, 0] * s_filter
    hsv_img_data[:, :, 1] = hsv_img_data[:, :, 1] * s_filter
    hsv_img_data[:, :, 2] = hsv_img_data[:, :, 2] * s_filter
    hsv_img_data[:, :, 0] = hsv_img_data[:, :, 0] * v_filter
    hsv_img_data[:, :, 1] = hsv_img_data[:, :, 1] * v_filter
    hsv_img_data[:, :, 2] = hsv_img_data[:, :, 2] * v_filter
    # Image.fromarray(hsv_img_data, "HSV").show()

    cyan_filter = get_cyan_filter_from_hue(hsv_img_data[:, :, 0])
    cyan_img_data = np.copy(hsv_img_data)
    cyan_img_data[:, :, 0] = cyan_img_data[:, :, 0] * cyan_filter
    cyan_img_data[:, :, 1] = cyan_img_data[:, :, 1] * cyan_filter
    cyan_img_data[:, :, 2] = cyan_img_data[:, :, 2] * cyan_filter
    # cyan_img = Image.fromarray(cyan_img_data, "HSV")
    # cyan_img.show()

    magenta_filter = get_magenta_filter_from_hue(hsv_img_data[:, :, 0])
    magenta_img_data = np.copy(hsv_img_data)
    magenta_img_data[:, :, 0] = magenta_img_data[:, :, 0] * magenta_filter
    magenta_img_data[:, :, 1] = magenta_img_data[:, :, 1] * magenta_filter
    magenta_img_data[:, :, 2] = magenta_img_data[:, :, 2] * magenta_filter
    # magenta_img = Image.fromarray(magenta_img_data, "HSV")
    # magenta_img.show()

    yellow_filter = get_yellow_filter_from_hue(hsv_img_data[:, :, 0])
    yellow_img_data = np.copy(hsv_img_data)
    yellow_img_data[:, :, 0] = yellow_img_data[:, :, 0] * yellow_filter
    yellow_img_data[:, :, 1] = yellow_img_data[:, :, 1] * yellow_filter
    yellow_img_data[:, :, 2] = yellow_img_data[:, :, 2] * yellow_filter
    # yellow_img = Image.fromarray(yellow_img_data, "HSV")
    # yellow_img.show()

    return {
        'cyan': get_features(cyan_img_data[:, :, 2]),
        'magenta': get_features(magenta_img_data[:, :, 2]),
        'yellow': get_features(yellow_img_data[:, :, 2]),
    }
