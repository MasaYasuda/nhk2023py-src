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
    # id 1 =右手　　id 2 = 左手
    dynamixel_1=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,1,2138,3803)
    dynamixel_2=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,2,324,2115)
    dynamixel_1.enable_torque()
    dynamixel_2.enable_torque()

    transmitter = nhk23.Transmitter("/dev/ArduinoMega2", 115200)
    mode_array=[0,100,100,100,100,100]
    direction_config_array =[3,0,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[1,0,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    R_hand_value=0.634
    L_hand_value=0.355

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

        print("左スティック座標")
        print(str(j.get_axis(0)))
        print("右スティックx座標")
        print(str(j.get_axis(3)))

        L_order=j.get_axis(0)
        if abs(L_order)<0.1:
            L_order=0
        R_order=j.get_axis(3)
        if abs(R_order)<0.1:
            R_order=0

        R_hand_value=R_hand_value+R_order*0.015
        R_hand_value=max(0,min(R_hand_value,1))
        L_hand_value=L_hand_value+L_order*0.015
        L_hand_value=max(0,min(L_hand_value,1))

        dynamixel_1.write_position(R_hand_value)
        dynamixel_2.write_position(L_hand_value)
        
        dynamixel_1.read_position()
        dynamixel_1.read_position()
        if lift_order!=0 :
            transmitter.write_single_auto(0,lift_order*(-1)*0.5)
            time.sleep(0.05)
        elif lift_order==0 and lift_order_past!=0:
            transmitter.write_single_auto(0,lift_order*(-1)*0.5)
            time.sleep(0.05)
        lift_order_past=lift_order
        time.sleep(0.005)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    dynamixel_1.disable_torque()
    dynamixel_2.disable_torque()
    dynamixel_1.close_port()
    dynamixel_2.close_port()


