import cv2
import numpy as np
import pyrealsense2 as rs


def printing(X):
    print(X)

def printposition(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(str(x)+","+str(y))
        cv2.rectangle(img,(x-50,y-50),(x+50,y+50),(0,0,0),-1)
        print("end")
    print(flags)

def averages(event,x,y,flags,param):
    if flags== 1:
        average = 0.0
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        average += img_hsv[y,x]
        r = 5
        count=1
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

        ave0=average[0]
        ave0=(ave0-10)*(-40)+532
        gra1=ave0.astype(np.uint16)
        gra2=x+20
        cv2.circle(glaf,(gra2,gra1),2,(100,100,0),-1)


# カメラの設定
conf = rs.config()
# RGB
conf.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# 距離
#conf.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

# stream開始
pipe = rs.pipeline()
profile = pipe.start(conf)

cnt = 0

#windowの設定
cv2.namedWindow("Win_a", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Win_a", 400, 300)

print("setup ended")

glaf=np.ones((552,1320,3),dtype=np.uint8)*255
cv2.line(glaf,(20,20),(20,532),(0,0,0),2)
cv2.line(glaf,(20,532),(1300,532),(0,0,0),2)

for i in range(13):
    y1=532-40*i
    x2=20+i*100
    cv2.line(glaf,(20,y1),(10,y1),(0,0,0),2)
    cv2.line(glaf,(x2,532),(x2,542),(0,0,0),2)

cv2.createTrackbar("Track",
                   "Win_a",
                    128,
                    255,
                    printing)

cv2.setMouseCallback("Win_a",
                    averages)


while True:
    frames = pipe.wait_for_frames()

    # frameデータを取得
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    # 画像データに変換
    img = np.asanyarray(color_frame.get_data())
    # 距離情報をカラースケール画像に変換する
    #depth_color_frame = rs.colorizer().colorize(depth_frame)
    #depth_image = np.asanyarray(depth_color_frame.get_data())
    #画像処理

    cv2.imshow("Win_a",img)

    #表示
    if cv2.waitKey(1)==27:
        break

cv2.imwrite("./filtered_images/plot_H.png",glaf)
cv2.destroyAllWindows