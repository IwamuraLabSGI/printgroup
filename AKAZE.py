from turtle import distance
import cv2
import sys
import numpy as np
args = sys.argv

def main(args):
    img1 = cv2.imread(args[1])
    img2 = cv2.imread(args[2])
    akaze = cv2.AKAZE_create()                                
    kp1, des1 = akaze.detectAndCompute(img1, None)
    kp2, des2 = akaze.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1,des2)
    
    "ここのratioを変更すると、マッチング率が変わる"
    good = []
    for m in matches:
        print(m.distance)
        print("")
        if m.distance < 20:
            good.append([m])

    print(len(good))

    img_akaze = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
    cv2.imwrite(args[1] + "and" + args[2] +".jpg", img_akaze)

main(args)