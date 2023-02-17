'''
joystickでハンドの開閉を調節する
'''

import pygame
import nhk23
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print("コントローラのボタンを押してください")
    # id 1 =右手　　id 2 = 左手
    dynamixel_1=nhk23.Dynamixel("COM3",115200,1,2500,3800)
    dynamixel_1.enable_torque()
    dynamixel_2=nhk23.Dynamixel("COM3",115200,2,500,1870)
    dynamixel_2.enable_torque()

    R_hand_value=0.5
    L_hand_value=0.5

    while True:
        events = pygame.event.get()
        print("左スティック座標")
        print(str(j.get_axis(0)))
        print("右スティックx座標")
        print(str(j.get_axis(3)))

        R_hand_value=R_hand_value+j.get_axis(3)*0.001
        L_hand_value=L_hand_value+j.get_axis(3)*0.001

        dynamixel_1.write_position(R_hand_value)
        dynamixel_2.write_position(L_hand_value)
        
        dynamixel_1.read_position()
        dynamixel_1.read_position()

        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    dynamixel_1.close_port()
    dynamixel_2.close_port()