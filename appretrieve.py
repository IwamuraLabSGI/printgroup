import DBDB
import appproc
from llah.descriptor_extractor import DescriptorExtractor


def retrieve_all(ID):
    print("特徴点抽出中 (上からシアン・マゼンダ・イエロー)")
    Cyankey = appproc.detectFeatures(1, "./templates/CyanIMG/" + str(ID) + ".jpg")
    Magendakey = appproc.detectFeatures(2, "./templates/MagendaIMG/" + str(ID) + ".jpg")
    Yellowkey = appproc.detectFeatures(3, "./templates/YellowIMG/" + str(ID) + ".jpg")
    print("特徴量算出中 (上からシアン・マゼンダ・イエロー)")
    descriptor_extractor = DescriptorExtractor(6, 1)
    Cyandescriptors = descriptor_extractor.OLDextract(Cyankey)
    Magendadescriptors = descriptor_extractor.OLDextract(Magendakey)
    Yellowdescriptors = descriptor_extractor.OLDextract(Yellowkey)
    print("LLAHでの検索中 (上からシアン・マゼンダ・イエロー)")
    cyan = DBDB.retrieveFeature(1, Cyandescriptors)
    magenda = DBDB.retrieveFeature(2, Magendadescriptors)
    yellow = DBDB.retrieveFeature(3, Yellowdescriptors)
    print("シアンの第1候補：", cyan[0][0], ".jpg マッチングスコア：", cyan[0][1])
    print("シアンの第2候補：", cyan[1][0], ".jpg マッチングスコア：", cyan[1][1])
    print("シアンの第3候補：", cyan[2][0], ".jpg マッチングスコア：", cyan[2][1])
    print("マゼンダの第1候補：", magenda[0][0], ".jpg マッチングスコア：", magenda[0][1])
    print("マゼンダの第2候補：", magenda[1][0], ".jpg マッチングスコア：", magenda[1][1])
    print("マゼンダの第3候補：", magenda[2][0], ".jpg マッチングスコア：", magenda[2][1])
    print("イエローの第1候補：", yellow[0][0], ".jp マッチングスコア：", yellow[0][1])
    print("イエローの第2候補：", yellow[1][0], ".jpg マッチングスコア：", yellow[1][1])
    print("イエローの第3候補：", yellow[2][0], ".jpg マッチングスコア；", yellow[2][1])
    LLAHanswer = []
    LLAHanswer.append(list(cyan))
    LLAHanswer.append(list(magenda))
    LLAHanswer.append(list(yellow))
    return LLAHanswer
