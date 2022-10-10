import os.path
import threading

import numpy as np
from PIL import Image
import sys

import llah
import utils
from repository.mysql.qr_code import QRCode as QRCodeRepo
from schema.mysql import load_mysql
from service.qr_code import QRCode as QRCodeSvc
from domain import CmykKeypointExtractor, FeatureCalculator
import model.mysql as mysql_model


def main():
    args = sys.argv
    target_file_paths: list[str] = []
    if os.path.isfile(args[1]):
        target_file_paths.append(args[1])
    else:
        target_file_paths = utils.list_img_paths_in_dir(args[1])

    for file_path in target_file_paths:
        print(f'add qr code: {file_path}')
        add_qr_code(file_path)


def add_qr_code(file_path: str):
    mysql = load_mysql()
    mysql.connect()
    qr_code_repo = QRCodeRepo(mysql)
    qr_code_svc = QRCodeSvc(qr_code_repo)

    with Image.open(file_path) as img:
        cmy_keypoints = CmykKeypointExtractor.extract(np.array(img, dtype=np.uint8))

        descriptor_extractor = llah.DescriptorExtractor(6, 2)

        cyan_descriptors = descriptor_extractor.extract(cmy_keypoints.get('cyan'))
        magenta_descriptors = descriptor_extractor.extract(cmy_keypoints.get('magenta'))
        yellow_descriptors = descriptor_extractor.extract(cmy_keypoints.get('yellow'))

        cyan_features = FeatureCalculator.calc(cyan_descriptors)
        magenta_features = FeatureCalculator.calc(magenta_descriptors)
        yellow_features = FeatureCalculator.calc(yellow_descriptors)

        # cyan_features = descriptor_extractor.old_extract(cmy_keypoints.get('cyan'))
        # magenta_features = descriptor_extractor.old_extract(cmy_keypoints.get('magenta'))
        # yellow_features = descriptor_extractor.old_extract(cmy_keypoints.get('yellow'))

        features: mysql_model.QRCodeFeatures = []
        for cmy_feature in cyan_features:
            features.append(mysql_model.QRCodeFeature(
                feature=cmy_feature,
                color=mysql_model.QRCodeFeatureColor.cyan
            ))
        for cmy_feature in magenta_features:
            features.append(mysql_model.QRCodeFeature(
                feature=cmy_feature,
                color=mysql_model.QRCodeFeatureColor.magenta
            ))
        for cmy_feature in yellow_features:
            features.append(mysql_model.QRCodeFeature(
                feature=cmy_feature,
                color=mysql_model.QRCodeFeatureColor.yellow
            ))

        qr_code_svc.add(
            file_name=os.path.basename(file_path),
            features=features
        )


if __name__ == '__main__':
    main()
