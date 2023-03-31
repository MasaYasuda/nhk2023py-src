# CORRECT

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

    transmitter = nhk23.Transmitter("/dev/ArduinoMega1", 115200)
    mode_array=[100,100,100,0,100,100]
    direction_config_array =[0,0,0,3,0,0] #回転が逆だったら3にする
    forward_direction_array=[0,0,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    lift_order=0
    lift_order_past=0
    while True:
        transmitter.reset_input_buffer()

        events = pygame.event.get()
        print("十字y座標")
        print(str((j.get_hat(0))[1]))
        lift_order=(j.get_hat(0))[1]
        if abs(lift_order)<0.1:
            lift_order=0

        print(str(lift_order))

        if lift_order!=0 :
            transmitter.write_single_auto(3,lift_order*(-1)*0.5)
            time.sleep(0.05)
        elif lift_order==0 and lift_order_past!=0:
            transmitter.write_single_auto(3,lift_order*(-1)*0.5)
            time.sleep(0.05)
        lift_order_past=lift_order
        time.sleep(0.005)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()

