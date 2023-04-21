import cv2
import numpy as np

def shirushi(img_num,h,nLabels,stats,centroids):
    for i in range(1, nLabels):
        
#        xc = int(centroids[i][0])
#        yc = int(centroids[i][1])

        haba = stats[i][2]
        takasa = stats[i][3]

        hidariue = (stats[i][0],stats[i][1])
        migishita = (stats[i][0]+haba,stats[i][1]+takasa)

        xc = int(stats[i][0]+haba/2)
        yc = int(stats[i][1]+takasa/2)

        if haba>takasa:
            small=takasa
            scale = (takasa*0.8)/25
        
        else :
            small=haba
            scale = (haba*0.8)/25



        font = cv2.FONT_HERSHEY_COMPLEX
        r1 = small/2
        r2 = int(r1)
        color = (0, 0,0)
        moji_iti_hoseiX = int((scale*20) /2)
        moji_iti_hoseiY = int((scale*20) /2)
        moji_hutosa = int(small/15)

        #img3=np.ndarray(img_num)
        #img3=np.zeros(img_num.shape,dtype=np.uint8)
        img3=img_num
        cv2.rectangle(img3,hidariue,migishita,(0,0,0),2)
        cv2.circle(img3, (xc,yc), r2,(255,0,255),-1)
        cv2.putText(img3, str(i), (xc-moji_iti_hoseiX,yc+moji_iti_hoseiY), font, scale, color, moji_hutosa, cv2.LINE_AA)

    return img_num
"""
img4=cv2.imread("./programs/images/H_filter.png")
nLabels=2
stats=((600,200,100,100),(600,200,100,100))
centroids=((650,250))
h=720
img2=shirushi(img4,h,nLabels,stats,centroids)
"""