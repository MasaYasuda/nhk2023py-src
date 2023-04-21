import cv2
import numpy as np


def averages(img,x,y):
    average = 0.0
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    average += img_hsv[y,x]
    r = 12
    count=0
    for i in range(r):
        for j in range(r):
            average+=img_hsv[y+j+1,x+i+1]
            average+=img_hsv[y-j-1,x-i-1]
            average+=img_hsv[y+j+1,x-i-1]
            average+=img_hsv[y-j-1,x+i+1]
            count+=4

    average /= count
    print("("+str(x)+","+str(y)+")")
    print("average:"+str(average))
    cv2.rectangle(img,(x+r+1,y+r+1),(x-r-1,y-r-1),(0,0,0),-1)
    return img

img4 = cv2.imread("filtered_images/de_pole3.png")


print("img4")
averages(img4,647,288)
averages(img4,647,238)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", 640, 480)

cv2.imshow("img",img4)
while True:
    if cv2.waitKey(30) == 27:
        break
cv2.destroyAllWindows

#1-797,380
#173,177
#2-677,354
#3-248,409
#1149,144