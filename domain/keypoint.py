import numpy as np
from PIL import Image

import llah


class CmykKeypointExtractor:
    @classmethod
    def extract(cls, img: np.ndarray):
        # Image.fromarray(img, mode='RGB').save('dist/target/original.png')

        # TODO: 線形変換で明るさ調整

        imgCMYGetter = ImgCMYGetter(img)
        # Image.fromarray(imgCMYGetter.hsv_img, 'HSV').convert('RGB').save('dist/target/cmyk.png')

        cyan_img = imgCMYGetter.get_cyan()
        # Image.fromarray(cyan_img, "HSV").convert('RGB').save('dist/target/cyan.png')

        cyan_keypoints = llah.KeypointExtractor.extract(cyan_img[:, :, 2])
        # cyan_points = list(map(lambda keypoint: Point(math.floor(keypoint.x), math.floor(keypoint.y)), cyan_keypoints))
        # Image.fromarray(
        #     ImgPainter.paint_points(cyan_img[:, :, 2], cyan_points, 4, 255),
        #     'HSV'
        # ).convert('RGB').save('dist/target/cyan_point.png')

        magenta_img = imgCMYGetter.get_magenta()
        # Image.fromarray(magenta_img, "HSV").convert('RGB').save('dist/target/magenta.png')

        magenta_keypoints = llah.KeypointExtractor.extract(magenta_img[:, :, 2])
        # magenta_points = list(
        #     map(lambda keypoint: Point(math.floor(keypoint.x), math.floor(keypoint.y)), magenta_keypoints))
        # Image.fromarray(
        #     ImgPainter.paint_points(magenta_img[:, :, 2], magenta_points, 4, 255),
        #     'HSV'
        # ).convert('RGB').save('dist/target/magenta_point.png')

        yellow_img = imgCMYGetter.get_yellow()
        # Image.fromarray(yellow_img, "HSV").convert('RGB').save('dist/target/yellow.png')

        yellow_keypoints = llah.KeypointExtractor.extract(yellow_img[:, :, 2])
        # yellow_points = list(
        #     map(lambda keypoint: Point(math.floor(keypoint.x), math.floor(keypoint.y)), yellow_keypoints))
        # Image.fromarray(
        #     ImgPainter.paint_points(yellow_img[:, :, 2], yellow_points, 4, 255),
        #     'HSV'
        # ).convert('RGB').save('dist/target/yellow_point.png')

        return {
            'cyan': cyan_keypoints,
            'magenta': magenta_keypoints,
            'yellow': yellow_keypoints,
        }


class ImgCMYGetter:
    hsv_img: np.ndarray

    def __init__(self, rgb_img: np.ndarray):
        hsv_img = np.array(Image.fromarray(rgb_img, 'RGB').convert('HSV'), np.uint8)
        s_filter = hsv_img[:, :, 1] > 70
        v_filter = hsv_img[:, :, 2] > 80
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
        return cyan_img

    def get_magenta(self):
        magenta_filter = ImgCMYGetter.get_magenta_filter_from_hue(self.hsv_img[:, :, 0])
        magenta_img = np.copy(self.hsv_img)
        magenta_img[:, :, 0] = magenta_img[:, :, 0] * magenta_filter
        magenta_img[:, :, 1] = magenta_img[:, :, 1] * magenta_filter
        magenta_img[:, :, 2] = magenta_img[:, :, 2] * magenta_filter
        return magenta_img

    def get_yellow(self):
        yellow_filter = ImgCMYGetter.get_yellow_filter_from_hue(self.hsv_img[:, :, 0])
        yellow_img = np.copy(self.hsv_img)
        yellow_img[:, :, 0] = yellow_img[:, :, 0] * yellow_filter
        yellow_img[:, :, 1] = yellow_img[:, :, 1] * yellow_filter
        yellow_img[:, :, 2] = yellow_img[:, :, 2] * yellow_filter
        return yellow_img

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


