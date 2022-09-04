import DBDB
import appproc
from llah.descriptor_extractor import DescriptorExtractor


def register_all(ID):
    print("特徴点抽出中 (上からシアン・マゼンダ・イエロー)")
    Cyankey = appproc.register_features(ID, 1, "./templates/CyanIMG/" + str(ID) + ".jpg")
    Magendakey = appproc.register_features(ID, 2, "./templates/MagendaIMG/" + str(ID) + ".jpg")
    Yellowkey = appproc.register_features(ID, 3, "./templates/YellowIMG/" + str(ID) + ".jpg")

    print("特徴量算出中 (上からシアン・マゼンダ・イエロー)")
    descriptor_extractor = DescriptorExtractor(6, 1)
    Cyandescriptors = descriptor_extractor.OLDextract(Cyankey)
    Magendadescriptors = descriptor_extractor.OLDextract(Magendakey)
    Yellowdescriptors = descriptor_extractor.OLDextract(Yellowkey)

    DBDB.register_feature(1, ID, Cyandescriptors)
    DBDB.register_feature(2, ID, Magendadescriptors)
    DBDB.register_feature(3, ID, Yellowdescriptors)

    return None
