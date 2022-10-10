import math
import os
import sys

import numpy as np
from PIL import Image

import llah
import utils
from domain.img_painter import Point, ImgPainter
from domain.keypoint import ImgCMYGetter

args = sys.argv
target_file_paths: list[str] = []
if os.path.isfile(args[1]):
    target_file_paths.append(args[1])
else:
    target_file_paths = utils.list_img_paths_in_dir(args[1])

for file_path in target_file_paths:
    with Image.open(file_path) as img:
        file_name = os.path.basename(file_path)
        output_dir_path = os.path.join(f'dist/preprocess_image/{file_name}')

        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)

        img = np.array(img, dtype=np.uint8)
        imgCMYGetter = ImgCMYGetter(img)

        Image.fromarray(img, mode='RGB').save(f'{output_dir_path}/original.png')

        cyan_img = imgCMYGetter.get_cyan()
        Image.fromarray(cyan_img, "HSV").convert('RGB').save(f'{output_dir_path}/cyan.png')

        cyan_keypoints = llah.KeypointExtractor.extract(cyan_img[:, :, 2])
        cyan_points = list(map(lambda keypoint: Point(math.floor(keypoint.x), math.floor(keypoint.y)), cyan_keypoints))
        Image.fromarray(
            ImgPainter.paint_points(cyan_img[:, :, 2], cyan_points, 4, 255),
            'HSV'
        ).convert('RGB').save(f'{output_dir_path}/cyan_point.png')

        magenta_img = imgCMYGetter.get_magenta()
        Image.fromarray(magenta_img, "HSV").convert('RGB').save(f'{output_dir_path}/magenta.png')

        magenta_keypoints = llah.KeypointExtractor.extract(magenta_img[:, :, 2])
        magenta_points = list(
            map(lambda keypoint: Point(math.floor(keypoint.x), math.floor(keypoint.y)), magenta_keypoints))
        Image.fromarray(
            ImgPainter.paint_points(magenta_img[:, :, 2], magenta_points, 4, 255),
            'HSV'
        ).convert('RGB').save(f'{output_dir_path}/magenta_point.png')

        yellow_img = imgCMYGetter.get_yellow()
        Image.fromarray(yellow_img, "HSV").convert('RGB').save(f'{output_dir_path}/yellow.png')

        yellow_keypoints = llah.KeypointExtractor.extract(yellow_img[:, :, 2])
        yellow_points = list(
            map(lambda keypoint: Point(math.floor(keypoint.x), math.floor(keypoint.y)), yellow_keypoints))
        Image.fromarray(
            ImgPainter.paint_points(yellow_img[:, :, 2], yellow_points, 4, 255),
            'HSV'
        ).convert('RGB').save(f'{output_dir_path}/yellow_point.png')

