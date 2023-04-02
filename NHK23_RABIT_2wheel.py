import v1_nhk23
import pygame
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    ##### TRANSMITTER SETUP

    transmitter = v1_nhk23.Transmitter("/dev/ArduinoMega1", 115200)

    # If speed pid
    mode_array=[0,0,100,100,100,100]
    direction_config_array =[3,3,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[1,1,1,1,1,1]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    print("コントローラのボタンを押してください")
    while True:
        transmitter.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        
        ##### VECTOR CALCLATION
        move=v1_nhk23.joy_threshold(j.get_axis(1)*(-1),0.1)
        rotation=v1_nhk23.joy_threshold(j.get_axis(3)*0.3,0.1)
        # 運動学（簡易版）の計算
        R_value = move - rot
        L_value = move + rot

        # 大きすぎる値（1以上）のとき圧縮する
        R_abs = abs(R_value)  # 絶対値を求める
        L_abs = abs(L_value)  # 絶対値を求める

        if R_abs > 1 or L_abs > 1:
            if R_abs >= L_abs:
                R_value = R_value / R_abs  # 圧縮
                L_value = L_value / R_abs  # 圧縮
            elif R_abs < L_abs:
                R_value = R_value / L_abs
                L_value = L_value / L_abs

        ##### TRANSMIT 
        transmitter.write_single_auto(0,R_value)
        time.sleep(0.05)
        transmitter.write_single_auto(1,L_value)
        time.sleep(0.05)



except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    init_array=[0,0,0,0,0,0]
    transmitter.write_all_auto([0,1,2,3,4,5],init_array)
    transmitter.close()
    