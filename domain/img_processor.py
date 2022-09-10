import numpy as np


class ImgProcessor:
    @classmethod
    def adjust_luminance(cls, img: np.ndarray):
        if img.ndim != 2:
            raise ValueError('引数の画像がgray-scaleではありません')
        # 線形変換
        min_lum = img.min()
        max_lum = img.max()
        return (img - min_lum) * (255 / (max_lum - min_lum))