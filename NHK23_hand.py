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
    dynamixel_1=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,1,2138,3803)
    dynamixel_2=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,2,324,2115)
    dynamixel_1.enable_torque()
    dynamixel_2.enable_torque()

    R_hand_value=0.634
    L_hand_value=0.355

    while True:
        events = pygame.event.get()
        print("左スティック座標")
        print(str(j.get_axis(0)))
        print("右スティックx座標")
        print(str(j.get_axis(3)))

        L_order=j.get_axis(0)
        if abs(L_order)<0.2:
            L_order=0
        R_order=j.get_axis(3)
        if abs(R_order)<0.2:
            R_order=0

        R_hand_value=R_hand_value+R_order*0.03
        R_hand_value=max(0,min(R_hand_value,1))
        L_hand_value=L_hand_value+L_order*0.03
        L_hand_value=max(0,min(L_hand_value,1))

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