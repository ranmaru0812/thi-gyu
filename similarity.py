#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import cv2

def main():
    image_path = "img/tigyu1.jpg"

    # グレースケールとして、file読込み
    image_gray = cv2.imread(image_path,0)

    # カスケード分類器の特徴量を取得.
    # 私の場合、/usr/local/share/OpenCV 以下に複数installされていました
    cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")

    # detectMultiScale() の引数の意味は、きちんとは理解していません
    facerect = cascade.detectMultiScale(image_gray,
                                        scaleFactor=1.1,
                                        minNeighbors=1,
                                        minSize=(50,50))
    if len(facerect) == 0:
        return
    
    print("face detected !!")
    print(facerect)

    #検出した顔を四角で描画
    for rect in facerect:
        cv2.rectangle(image_gray,
                      tuple(rect[0:2]),
                      tuple(rect[0:2]+rect[2:4]),
                      (255, 255, 255),
                      thickness=2)
    # 結果保存
    cv2.imwrite("detected.jpg", image_gray)


if __name__ == '__main__':
    main()