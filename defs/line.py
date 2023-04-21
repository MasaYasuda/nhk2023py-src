import cv2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#edge抽出

def lines(img_Color,img_blobed,h,w):

    h_50 = h/6
    w_50 = w/6

    h_w_large = (h_50 + w_50)/2
    h_w_noise = h_w_large/2

    img_blobed = cv2.Canny(img_blobed,h_w_noise,h_w_large)

#lineを弾く
#    lines = cv2.HoughLines((img_blobed),1,np.pi/180,50,min_theta=np.pi-0.15,max_theta=0.15)
    line = cv2.HoughLines((img_blobed),1,np.pi/360,90)

    if line is None:
        print("No lines")
        return img_Color,None
    
    const1 = 0

    for i in line:
        theta = i[0][1]
        if theta <0.2 or theta > 2.9959:
            const1 += 1
    
    lines = np.ones((const1,2), np.float16)*255

    const1 = 0

    #print(line)

    for j in line:
        theta = j[0][1]
        if theta <0.15 or theta > 2.9959:
            print(str(j[0][0]) +"  "+ str(j[0][1]))
            print(str(lines[const1][0]) +"  "+ str(lines[const1][1]))
            lines[const1][0] = j[0][0]
            lines[const1][1] = j[0][1]
            #print(str(j[0][0]) +"  "+ str(j[0][1]))
            #print(str(lines[const1][0]) +"  "+ str(lines[const1][1]))

            const1 += 1

#    if line == None:
#        return img_Color,None


    # i = [ [[rho0 theta0]] [[rho1 theta1]] ... ] 二重括弧のため　i[0][0]

#    lines2 = np.zeros((lines.shape[1],2), dtype = np.uint8)

#    print(lines)

    for k in lines[:]:
        
        rho = k[0]
        theta = k[1]

#        rho = 0
#        theta = 3.0
        
        a = np.cos(theta)
        b = np.sin(theta)
        
        X0 = rho * a
        Y0 = rho * b
        
        X1 = int( X0 - (-1000 * b) )
        Y1 = int( Y0 - (1000 * a) )
        
        X2 = int( X0 + (-1000 * b) )
        Y2 = int( Y0 + (1000 * a) )
        
        cv2.line(img_Color,(X1,Y1),(X2,Y2),(255,0,0),1)
    
    return img_Color, line
        

#img_Color = cv2.imread("filtered_images/img_lines2.png")
#img_blobed = cv2.imread("filtered_images/img_lines1.png")

#h, w = img_blobed.shape[:2]

#img_Color, line = lines(img_Color, img_blobed, h, w)

#cv2.imwrite("./filtered_images/lined.png", img_Color)