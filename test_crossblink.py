import nhk23
import pygame
import time
import os

order=[0,0,0,0]
count=0
try:
    transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)
    
    while True:
        for i in range(0,4):
            if i==count:
                order[i]=1
            else:
                order[i]=0
    

        transmitter.write_all_auto([0,1,2,3],order)
        count=count+1
        if count==4:
            count=0
        time.sleep(1)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    transmitter.close()
