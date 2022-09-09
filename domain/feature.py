import math
import numpy as np
from PIL import Image
import llah


# TODO: imgはnp.ndarrayで受け取るようにする
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

    @classmethod
    def get_cmy_features_from_img(cls, img):
        imgCMYGetter = ImgCMYGetter(img)

        cyan_img = imgCMYGetter.get_cyan()
        # cyan_img = Image.fromarray(cyan_img, "HSV")
        # cyan_img.show()

        magenta_img = imgCMYGetter.get_magenta()
        # magenta_img = Image.fromarray(magenta_img, "HSV")
        # magenta_img.show()

        yellow_img = imgCMYGetter.get_yellow()
        # yellow_img = Image.fromarray(yellow_img, "HSV")
        # yellow_img.show()

        return {
            'cyan': Feature.get_features(cyan_img),
            'magenta': Feature.get_features(magenta_img),
            'yellow': Feature.get_features(yellow_img),
        }

    @classmethod
    def get_features(cls, img: np.ndarray):
        keypoints = llah.KeypointExtractor.extract(img)
        descriptor_extractor = llah.DescriptorExtractor(6, 2)
        descriptors = descriptor_extractor.extract(keypoints)
        features: list[float] = []
        for descriptor in descriptors:
            features.append(Feature.get_from_descriptor(descriptor))
        return features


class ImgCMYGetter:
    hsv_img: np.ndarray

    def __init__(self, rgb_img: np.ndarray):
        hsv_img = np.array(rgb_img.convert('HSV'), np.uint8)
        s_filter = hsv_img[:, :, 1] > 70
        v_filter = hsv_img[:, :, 2] > 50
        hsv_img[:, :, 0] = hsv_img[:, :, 0] * s_filter
        hsv_img[:, :, 1] = hsv_img[:, :, 1] * s_filter
        hsv_img[:, :, 2] = hsv_img[:, :, 2] * s_filter
        hsv_img[:, :, 0] = hsv_img[:, :, 0] * v_filter
        hsv_img[:, :, 1] = hsv_img[:, :, 1] * v_filter
        hsv_img[:, :, 2] = hsv_img[:, :, 2] * v_filter
        self.hsv_img = hsv_img

    def get_cyan(self):
        cyan_filter = ImgCMYGetter.get_cyan_filter_from_hue(self.hsv_img[:, :, 0])
        cyan_img = np.copy(self.hsv_img)
        cyan_img[:, :, 0] = cyan_img[:, :, 0] * cyan_filter
        cyan_img[:, :, 1] = cyan_img[:, :, 1] * cyan_filter
        cyan_img[:, :, 2] = cyan_img[:, :, 2] * cyan_filter
        return cyan_img[:, :, 2]

    def get_magenta(self):
        magenta_filter = ImgCMYGetter.get_magenta_filter_from_hue(self.hsv_img[:, :, 0])
        magenta_img = np.copy(self.hsv_img)
        magenta_img[:, :, 0] = magenta_img[:, :, 0] * magenta_filter
        magenta_img[:, :, 1] = magenta_img[:, :, 1] * magenta_filter
        magenta_img[:, :, 2] = magenta_img[:, :, 2] * magenta_filter
        return magenta_img[:, :, 2]

    def get_yellow(self):
        yellow_filter = ImgCMYGetter.get_yellow_filter_from_hue(self.hsv_img[:, :, 0])
        yellow_img = np.copy(self.hsv_img)
        yellow_img[:, :, 0] = yellow_img[:, :, 0] * yellow_filter
        yellow_img[:, :, 1] = yellow_img[:, :, 1] * yellow_filter
        yellow_img[:, :, 2] = yellow_img[:, :, 2] * yellow_filter
        return yellow_img[:, :, 2]

    @classmethod
    def get_cyan_filter_from_hue(cls, hue: np.ndarray):
        cyan = 180 / 360 * 256
        width = 30
        return (hue > (cyan - width)) * (hue < (cyan + width))

    @classmethod
    def get_magenta_filter_from_hue(cls, hue: np.ndarray):
        magenta = 300 / 360 * 256
        width = 30
        return (hue > (magenta - width)) * (hue < (magenta + width))

    @classmethod
    def get_yellow_filter_from_hue(cls, hue: np.ndarray):
        yellow = 60 / 360 * 256
        width = 30
        return (hue > (yellow - width)) * (hue < (yellow + width))
