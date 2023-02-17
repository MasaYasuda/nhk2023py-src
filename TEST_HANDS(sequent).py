'''
1、ボタンを押して、左ハンドを定位置まで持って来る
2、自動で右手を操作できるようになる
3、ボタンを押して、両手を定位置まで持ってくる
4、もう一度ボタンを押して終了
'''

import pygame
import nhk23
import time
import os
import msvcrt
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    # id 1 =右手　　id 2 = 左手
    dynamixel_1=nhk23.Dynamixel("COM3",115200,1,2500,3800)
    dynamixel_1.enable_torque()
    dynamixel_2=nhk23.Dynamixel("COM3",115200,2,500,1870)
    dynamixel_2.enable_torque()

    R_hand_value=0.0
    L_hand_value=0.0

    while True:

        ########## 1 ###########################

        print("PRESS ANY BUTTONS")
        while 1:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN: #ボタンが押された場合
                    if j.get_button(0) or j.get_button(1) or j.get_button(2) or j.get_button(3):
                        break
        dynamixel_2.write_position()
        time.sleep(0.1)

        ########## 2 ###########################

        print("ADJUST RIGHT HAND , AND THEN PRESS ANY BUTTONS")
        while 1:
            events = pygame.event.get()
            print("右スティックx座標")
            print(str(j.get_axis(3)))
            R_hand_value=R_hand_value+j.get_axis(3)*0.001
            dynamixel_1.write_position(R_hand_value)
            dynamixel_1.read_position()
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN: #ボタンが押された場合
                    if j.get_button(0) or j.get_button(1) or j.get_button(2) or j.get_button(3):
                        break
        time.sleep(0.1)

        ########## 3 ############################

        dynamixel_1.write_position()
        dynamixel_2.write_position()
        time.sleep(0.1)

        ########## 4 #######################
        
        print("PRESS ANY KEYS or BUTTONS , AND THEN FIN")

        while 1:
            if msvcrt.kbhit():
                break
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN: #ボタンが押された場合
                    if j.get_button(0) or j.get_button(1) or j.get_button(2) or j.get_button(3):
                        break
    
    print("プログラムを終了します")
    j.quit()
    dynamixel_1.close_port()
    dynamixel_2.close_port()

except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    dynamixel_1.close_port()
    dynamixel_2.close_port()