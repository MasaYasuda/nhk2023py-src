'''
前後+回転
or 
左右移動+回転
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

    transmitter = nhk23.Transmitter("/dev/ArduinoMega1", 115200)

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
        print("左スティック座標")
        print("("+str(j.get_axis(0))+","+ str((-1)*j.get_axis(1))+")")

        print("右スティックx座標")
        print(str(j.get_axis(3)))
        
        ##### VECTOR CALCLATION
<<<<<<< HEAD
        x=0
        y=0
        rotation=0
        # x=j.get_axis(0)
        y=j.get_axis(1)*(-1)

        rotation=j.get_axis(3)*0.3
=======
        x=j.get_axis(0)
        y=j.get_axis(1)*(-1)
        rotation=j.get_axis(3)
>>>>>>> 3f79c9d46e371156a2d054b3ad2865cb7e894275
        move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
        
        ##### MOTOR CALCLATION
        omni_output = motor.calc_omni_output_for_radicon(move,rot)  # move,rot is "Vector.move","Vector.rot"
        for i in range(0,4):
            omni_output[i]=omni_output[i]*1
        print(omni_output)
        
        ##### TRANSMIT 
<<<<<<< HEAD
        transmitter.write_single_auto(0,omni_output[0])
        transmitter.write_single_auto(1,omni_output[1])
        time.sleep(0.2)
=======
        for i in range(0,4):
            transmitter.write_single_auto(i,omni_output[i])
            time.sleep(0.1)
>>>>>>> 3f79c9d46e371156a2d054b3ad2865cb7e894275



except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    init_array=[0,0,0,0,0,0]
    transmitter.write_all_auto([0,1,2,3,4,5],init_array)
    transmitter.close()
    