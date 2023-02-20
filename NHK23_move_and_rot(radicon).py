'''
4つのArduino  すべてポート

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

    transmitter0 = nhk23.Transmitter("/dev/ArduinoMega1", 115200)
    #transmitter1 = nhk23.Transmitter("/dev/ArduinoMega2", 115200)
    #transmitter2 = nhk23.Transmitter("/dev/ArduinoMega3", 115200)
    #transmitter3 = nhk23.Transmitter("/dev/ArduinoMega4", 115200)

    # If speed pid
    mode_array=[0,0,0,0,100,100]
    direction_config_array0 =[0,0,0,0,0,0] #回転が逆だったら3にする
    #direction_config_array1 =[0,0,0,0,0,0] #回転が逆だったら3にする
    #direction_config_array2 =[3,0,0,0,0,0] #回転が逆だったら3にする
    #direction_config_array3 =[3,0,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[1,1,1,1,1,1]

    transmitter0.write_config_all(mode_array,direction_config_array0,forward_direction_array)
    #transmitter1.write_config_all(mode_array,direction_config_array1,forward_direction_array)
    #transmitter2.write_config_all(mode_array,direction_config_array2,forward_direction_array)
    #transmitter3.write_config_all(mode_array,direction_config_array3,forward_direction_array)

    print("コントローラのボタンを押してください")
    while True:
        transmitter0.reset_input_buffer()
        #transmitter1.reset_input_buffer()
        #transmitter2.reset_input_buffer()
        #transmitter3.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        print("左スティック座標")
        print("("+str(j.get_axis(0))+","+ str((-1)*j.get_axis(1))+")")
        x=j.get_axis(0)
        y=j.get_axis(1)*(-1)

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
        transmitter0.write_single_auto(0,omni_output[0])
        time.sleep(0.1)
        transmitter0.write_single_auto(1,omni_output[1])
        time.sleep(0.1)
        transmitter0.write_single_auto(2,omni_output[2])
        time.sleep(0.1)
        transmitter0.write_single_auto(3,omni_output[3])
        time.sleep(0.1)


except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    init_array=[0,0,0,0,0,0]
    transmitter0.write_all_auto([0,1,2,3,4,5],init_array)
    #transmitter1.write_all_auto([0,1,2,3,4,5],init_array)
    #transmitter2.write_all_auto([0,1,2,3,4,5],init_array)
    #transmitter3.write_all_auto([0,1,2,3,4,5],init_array)
    transmitter0.close()
    #transmitter1.close()
    #transmitter2.close()
    #transmitter3.close()
    