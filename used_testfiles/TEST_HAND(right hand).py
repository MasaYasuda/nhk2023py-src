# CORRECT

'''
joystickで右ハンドの開閉を調節する
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
    # id 1 =右手
    dynamixel_1=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,1,2500,3800)
    dynamixel_1.enable_torque()
    R_hand_value=0.5

    while True:
        events = pygame.event.get()
        print("右スティックx座標")
        print(str(j.get_axis(3)))
        order=j.get_axis(3)
        if abs(order)<0.2:
            order=0
        
        R_hand_value=R_hand_value+order*0.05
        R_hand_value=max(0,min(R_hand_value,1))

        dynamixel_1.write_position(R_hand_value)
        
        dynamixel_1.read_position()

        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    dynamixel_1.close_port()



