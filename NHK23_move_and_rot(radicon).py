'''
前進と回転のみ
2つのArduinoでわける
ArduinoMega 1 -> 1 , 2  
ArduinoMega 2 -> 0 , 3
'''


import nhk23
import pygame
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    ##### VECTOR SETUP
    
    vector=nhk23.Vector() # make instance
    
    ##### MOTOR SETUP

    motor=nhk23.Motor("omni") # make instance
    
    ##### TRANSMITTER SETUP

    transmitter12 = nhk23.Transmitter("/dev/ArduinoMega1", 115200)
    transmitter03 = nhk23.Transmitter("/dev/ArduinoMega2", 115200)

    # If speed pid
    mode_array12=[0,0,0,0,100,100]
    direction_config_array12 =[0,3,3,0,0,0] #回転が逆だったら3にする
    forward_direction_array12=[0,0,0,0,0,0]
    transmitter12.write_config_all(mode_array12,direction_config_array12,forward_direction_array12)
    mode_array03=[0,0,0,0,100,100]

    direction_config_array03 =[0,3,3,0,0,0] #回転が逆だったら3にする
    forward_direction_array03=[0,0,0,0,0,0]
    transmitter03.write_config_all(mode_array12,direction_config_array12,forward_direction_array12)
    print("コントローラのボタンを押してください")
    while True:
        transmitter12.reset_input_buffer()
        transmitter03.reset_input_buffer()
        ## Get Inputs
        events = pygame.event.get()
        print("十字y座標")
        print(str((j.get_hat(0))[1]))
        y=(j.get_hat(0))[1]
        if abs(y)<0.1:
            y=0
        x=0

        print("右スティックx座標")
        print(str(j.get_axis(3)))
        
        ##### VECTOR CALCLATION
        
        rotation=j.get_axis(3)
        move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
        
        ##### MOTOR CALCLATION
        omni_output = motor.calc_omni_output_for_radicon(move,rot)  # move,rot is "Vector.move","Vector.rot"
        for i in range(0,4):
            omni_output[i]=omni_output[i]*0.5
        print(omni_output)
        
        ##### TRANSMIT 
        transmitter12.write_single_auto(0,omni_output[0])
        time.sleep(0.1)
        transmitter12.write_single_auto(1,omni_output[1])
        time.sleep(0.1)
        transmitter03.write_single_auto(0,omni_output[2])
        time.sleep(0.1)
        transmitter03.write_single_auto(1,omni_output[3])
        time.sleep(0.1)


except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0,0,0]
    transmitter12.write_all_auto([0,1,2,3,4,5],init_array)
    transmitter03.write_all_auto([0,1,2,3,4,5],init_array)
    j.quit()
    transmitter12.close()
    transmitter03.close()
    