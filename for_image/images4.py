import cv2
from defs import color_filter_X
import defs.blob as blob
from defs import shirushi
import defs.line as line
import numpy as np

def images_4return(img,H_fil,Hue,Hue_wide):
    #print(img.shape)

    Hue_low=Hue-Hue_wide
    Hue_upp=Hue+Hue_wide

    #setup
    h,w = img.shape[:2]
    img_HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #img_Blur=cv2.blur(img,(3,3))
    H,S,V=cv2.split(img_HSV)
    #H=H.astype(np.float16)
    
#    cv2.imwrite("./filtered_images/de_pole4.png", img)

    #カメラの補正(Hue)
#    H_fil=H.astype(np.int16)+H_fil
    H_Re=H+H_fil
    img_HSV=cv2.merge((H_Re,S,V))
    #たまに落ちるエラーはここ!!
    img_Re=cv2.cvtColor(img_HSV,cv2.COLOR_HSV2BGR)
    cv2.imwrite("./filtered_images/de_pole3.png", img_Re)



    #ポールの色を抽出
    img_Color = color_filter_X.color_filter_X(img_Re,img_HSV, (int(Hue_low),100,100),(int(Hue_upp),255,255))
    #print("Color has ended")
    #return img_Color,0,0,0

    img_G = cv2.cvtColor(img_Color, cv2.COLOR_BGR2GRAY)
    #print("Grey has ended")
    #return img_G,0,0,0

    #2値化
    border = 2
    ret, img_G = cv2.threshold(img_G, border, 255, cv2.THRESH_BINARY)
    #print("judge has ended")

#    return img,(0,0),(0,0),(0,0)

#    cv2.imwrite("./filtered_images/img_lines1.png",img_G)

    #塊検出
    nLabels, img_no_use, stats, centroids= blob.blobs(img_G,1000)
    print("blob has ended")

    #img=line.lines(img,img3,h,w)

    #番号割り振り画像作成
    img = shirushi.shirushi(img,h,nLabels,stats,centroids)
    print("shirushi has ended")


#    cv2.imwrite("./filtered_images/img_lines2.png",img)

    lines = np.zeros(1)

#    img, lines = line.lines(img,img3,h,w)
#    print("line has ended")

    return img, lines, stats[1:], centroids[1:]



#img = cv2.imread("programs/images/H_filter.png")
#print(img.shape)
#cv2.imwrite("./filtered_images/7_img_numbered.png", img)
#cv2.imshow("img",img)