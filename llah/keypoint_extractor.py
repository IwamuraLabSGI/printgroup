import cv2
import numpy as np
from llah.keypoint import Keypoint


class KeypointExtractor:
    @classmethod
    def extract(cls, img: np.ndarray):
        if img.ndim != 2:
            raise ValueError('引数の画像が1チェンネルではありません')
        if img.dtype != 'uint8':
            img = img.astype(np.uint8)
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda cnt: cv2.contourArea(cnt) >= 50, contours))

        keypoints: list[Keypoint] = []
        for counter in contours:
            moments = cv2.moments(counter, False)
            center_x: float = 0
            center_y: float = 0
            # TODO: 分母が0になるような場合を確認
            if moments['m00'] != 0:
                center_x = moments['m10'] / moments['m00']
                center_y = moments['m01'] / moments['m00']
            keypoint = Keypoint(
                center_x,
                center_y,
                cv2.contourArea(counter)
            )
            # 同じ重心を持った特徴点を排除
            # TODO: sizeが大きい方で置換の方が良いかも？今はサイズ使ってないのでよき。
            duplicated = list(filter(lambda item: item.distance_from(keypoint) == 0, keypoints))
            if len(duplicated) == 0:
                keypoints.append(keypoint)
        return keypoints
