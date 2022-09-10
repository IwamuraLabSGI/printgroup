import numpy as np
from PIL import Image


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

Points = list[Point]

class ImgPainter:

    @classmethod
    def paint_points(cls, img: np.ndarray, points: Points, radius: int, hue: int):
        image = Image.fromarray(img, 'L').convert('HSV')
        for point in points:
            for x in range(point.x - radius, point.x + radius):
                for y in range(point.y - radius, point.y + radius):
                    if 0 < x < image.width and 0 < y < image.height:
                        image.putpixel((x, y), (hue, 255, 255))
        return np.array(image)
