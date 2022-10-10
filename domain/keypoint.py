import numpy as np
from PIL import Image

import llah


class CmykKeypointExtractor:
    @classmethod
    def extract(cls, img: np.ndarray):
        # TODO: 線形変換で明るさ調整

        imgCMYGetter = ImgCMYGetter(img)

        cyan_img = imgCMYGetter.get_cyan()
        cyan_keypoints = llah.KeypointExtractor.extract(cyan_img[:, :, 2])

        magenta_img = imgCMYGetter.get_magenta()
        magenta_keypoints = llah.KeypointExtractor.extract(magenta_img[:, :, 2])

        yellow_img = imgCMYGetter.get_yellow()
        yellow_keypoints = llah.KeypointExtractor.extract(yellow_img[:, :, 2])

        return {
            'cyan': cyan_keypoints,
            'magenta': magenta_keypoints,
            'yellow': yellow_keypoints,
        }


class ImgCMYGetter:
    hsv_img: np.ndarray

    def __init__(self, rgb_img: np.ndarray):
        self.hsv_img = np.array(Image.fromarray(rgb_img, 'RGB').convert('HSV'), np.uint8)

    def get_cyan(self):
        cyan_filter = ImgCMYGetter.get_cyan_filter(self.hsv_img)
        cyan_img = np.copy(self.hsv_img)
        cyan_img[:, :, 0] = cyan_img[:, :, 0] * cyan_filter
        cyan_img[:, :, 1] = cyan_img[:, :, 1] * cyan_filter
        cyan_img[:, :, 2] = cyan_img[:, :, 2] * cyan_filter
        return cyan_img

    def get_magenta(self):
        magenta_filter = ImgCMYGetter.get_magenta_filter(self.hsv_img)
        magenta_img = np.copy(self.hsv_img)
        magenta_img[:, :, 0] = magenta_img[:, :, 0] * magenta_filter
        magenta_img[:, :, 1] = magenta_img[:, :, 1] * magenta_filter
        magenta_img[:, :, 2] = magenta_img[:, :, 2] * magenta_filter
        return magenta_img

    def get_yellow(self):
        yellow_filter = ImgCMYGetter.get_yellow_filter(self.hsv_img)
        yellow_img = np.copy(self.hsv_img)
        yellow_img[:, :, 0] = yellow_img[:, :, 0] * yellow_filter
        yellow_img[:, :, 1] = yellow_img[:, :, 1] * yellow_filter
        yellow_img[:, :, 2] = yellow_img[:, :, 2] * yellow_filter
        return yellow_img

    @classmethod
    def get_cyan_filter(cls, img: np.ndarray):
        hue = img[:, :, 0]
        hue_center = 180 / 360 * 256
        hue_width_lower = 80 / 360 * 256
        hue_width_upper = 60 / 360 * 256
        hue_filter = (hue > (hue_center - hue_width_lower)) * (hue < (hue_center + hue_width_upper))

        saturation = img[:, :, 1]
        saturation_lower_limit = 40
        saturation_filter = saturation > saturation_lower_limit

        value = img[:, :, 2]
        value_lower_limit = 60
        value_higher_limit = 240
        value_filter = (value > value_lower_limit) * (value < value_higher_limit)

        return hue_filter * saturation_filter * value_filter

    @classmethod
    def get_magenta_filter(cls, img: np.ndarray):
        hue = img[:, :, 0]
        hue_1_center = 300 / 360 * 256
        hue_1_width_lower = 60 / 360 * 256
        hue_1_width_upper = 60 / 360 * 256
        hue_1_filter = (hue >= (hue_1_center - hue_1_width_lower)) * (hue <= (hue_1_center + hue_1_width_upper))
        hue_2_center = 0 / 360 * 256
        hue_2_width_lower = 0 / 360 * 256
        hue_2_width_upper = 25 / 360 * 256
        hue_2_filter = (hue >= (hue_2_center - hue_2_width_lower)) * (hue <= (hue_2_center + hue_2_width_upper))
        hue_filter = (hue_1_filter + hue_2_filter) > 0

        saturation = img[:, :, 1]
        saturation_lower_limit = 80
        saturation_filter = saturation > saturation_lower_limit

        value = img[:, :, 2]
        value_lower_limit = 80
        value_filter = value > value_lower_limit

        return hue_filter * saturation_filter * value_filter

    @classmethod
    def get_yellow_filter(cls, img: np.ndarray):
        hue = img[:, :, 0]
        hue_center = 60 / 360 * 256
        hue_width = 30
        hue_filter = (hue > (hue_center - hue_width)) * (hue < (hue_center + hue_width))

        saturation = img[:, :, 1]
        saturation_lower_limit = 70
        saturation_filter = saturation > saturation_lower_limit

        value = img[:, :, 2]
        value_lower_limit = 80
        value_filter = value > value_lower_limit

        return hue_filter * saturation_filter * value_filter


