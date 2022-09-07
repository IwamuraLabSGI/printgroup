import math

import numpy as np
from PIL import Image

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


def adjust_cyan(img):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # TODO: 平滑化などの前処理
    img = adjust_luminance(img)
    img_filter = img > 120
    return img * img_filter


def adjust_magenta(img):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # TODO: 平滑化などの前処理
    img = adjust_luminance(img)
    img_filter = img > 120
    return img * img_filter


def adjust_yellow(img):
    if img.ndim != 2:
        raise ValueError('引数の画像がgray-scaleではありません')
    # TODO: 平滑化などの前処理
    img = adjust_luminance(img)
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


def get_cmy_features_from_img(img):
    # グレーの領域を白に
    hsv_img = img.convert("HSV")
    hsv_img_data = np.asarray(hsv_img, np.uint8)
    # h_unique, h_counts = np.unique(hsv_img_data[:, :, 0], return_counts=True)
    # plt.bar(h_unique, h_counts, width=1.0)
    # plt.show()
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

    cyan_img = adjust_cyan(cmyk_img_data[:, :, 0])
    cyan_features = get_features(cyan_img)
    magenta_img = adjust_magenta(cmyk_img_data[:, :, 1])
    magenta_features = get_features(magenta_img)
    yellow_img = adjust_yellow(cmyk_img_data[:, :, 2])
    yellow_features = get_features(yellow_img)

    return {
        'cyan': cyan_features,
        'magenta': magenta_features,
        'yellow': yellow_features,
    }
