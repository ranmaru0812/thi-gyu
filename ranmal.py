import cv2
import numpy as np

img = cv2.imread("/mnt/c/Users/n1290134.STCN2/Pictures/thi-gyu/ojimaru.jpg")
h,w = img.shape[:2]
rot_mat = cv2.getRotationMatrix2D((w/2,h/2),40,1)
img_afn2 = cv2.warpAffine(img, rot_mat,(w,h)) 
cv2.imshow('image', img_afn2)
cv2.waitKey(0)
cv2.destroyAllWindows()


