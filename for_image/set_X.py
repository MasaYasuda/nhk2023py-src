import numpy as np

import images4 as images3
import cv2
import math
import phase
import movement as moves
import IandD
import time
def shot_jyunbi(Center_X,Center_Y,pipe,border_Phase,border_PID,CON_PID):
    global H_fil
    global Hue
    global Hue_wide
    global h,w
    global Y
    L_log=0
    R_log=0
    L_I=0
    R_I=0
    L_D=0
    R_D=0
    count=0
    st=time.time()
    while time.time()-st<10:
        count+=1

        #PhaseX to Zero

        #インポート
        frames = pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        img = np.asanyarray(color_frame.get_data())

        #定数
        Y_max_half=0.674#デフォルトで半分の値
        X_max_half=1.19822#デフォルトで半分の値


        #画像処理
        img2, lines ,stats_nonuse,centroids_nonuse = images3.images_4return(img,H_fil,Hue,Hue_wide)
        #画面全体の塊認識をなくす
        stats=stats_nonuse
        centroids=centroids_nonuse
        kazu_of_blob=centroids.shape[0]

        if kazu_of_blob!=0:
            #狙うべきポールを特定 kouho_numに格納
            i=0
            Center_X_short=centroids[0][0]
            Center_Y_short=centroids[0][1]
            Center_X_gosa=Center_X_short-Center_X
            Center_Y_gosa=Center_Y_short-Center_Y
            gosa=math.sqrt( ( (Center_X_gosa)**2+(Center_Y_gosa)**2 )/2 )
            gosa_log=gosa
            kouho_num=i
            i=1

            while i<kazu_of_blob:
                Center_X_short=centroids[i][0]
                Center_Y_short=centroids[i][1]
                Center_X_gosa=Center_X_short-Center_X
                Center_Y_gosa=Center_Y_short-Center_Y
                gosa=math.sqrt( ( (Center_X_gosa)**2+(Center_Y_gosa)**2 )/2 )

                if gosa<gosa_log:
                    gosa_log=gosa
                    kouho_num=i
                i+=1
            #横位置を揃える
            phase_X=phase.HighToTheta((centroids[kouho_num][0]),int(w/2),Y_max_half)
            L_move,R_move=moves.phase(phase_X,border_Phase,CON_PID,L_I,R_I,L_D,R_D)
            

            #終了判定
                        
            L_I,R_I,L_D,R_D=IandD.IAndD(L_move,R_move,L_log,R_log,L_I,R_I)
            L_log=L_move
            R_log=R_move
            
            I=(abs(L_I)+abs(R_I))/2
            D=(abs(L_D)+abs(R_D))/2
            
            phase_Y=phase.HighToTheta((stats[kouho_num][1]),int(h/2),Y_max_half)

            Reach=Y/(math.cos(phase_X)*math.tan(phase_Y))

            gosa=Reach*phase_X#[mm]
            #しきい値は調整すること！
            if gosa<30 & I<0.5 & D<0.5:
                return 2,phase_Y
        

            
        """

        stats_T=np.array(stats.T,dtype=int)
        centroids_T=np.array(centroids.T,dtype=int)
        Stats_Centroids_T=np.array((centroids_T[0],stats_T[1]),dtype=int)
        Stats_Centroids=np.array(Stats_Centroids_T.T,dtype=int)



        """


