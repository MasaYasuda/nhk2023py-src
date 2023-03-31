import nhk23
import pygame
import time
import os

try:
    #########

    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print("コントローラのボタンを押してください")
    
    #########

    motor=nhk23.Motor("roller") # make instance
    motor.roller_setup(100,10,2.77)

    #########
    
    transmitter = nhk23.Transmitter("/dev/ArduinoMega2", 115200)
    # If speed pid
    mode_array=[20,20,100,100,100,100]
    direction_config_array =[3,0,0,0,0,0]# speed pidの時でチェック済み
    forward_direction_array=[1,1,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    while True:
        ## Get Inputs
        events = pygame.event.get()
        print("R2")
        order=(j.get_axis(5)+1)/2
        if abs(order)<0.1:
            order=0
        print(str(order))
        
        output = motor.calc_roller_output(order) # spin: -1~1    

        transmitter.write_single_auto(0,output*0.5)
        time.sleep(0.1)
        transmitter.write_single_auto(1,output*0.5)
        time.sleep(0.1)
        transmitter.reset_input_buffer()
        time.sleep(0.1)

        
except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0]
    transmitter.write_all_auto([0,1,2,3],init_array)
    j.quit()
    transmitter.close()
    transmitter
    

