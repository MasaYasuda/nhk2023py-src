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
    mode_array=[0,100,100,100,100,0]
    direction_config_array =[0,0,0,0,0,0]# speed pidの時でチェック済み
    forward_direction_array=[1,1,1,0,0,1]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    while True:
        
        events = pygame.event.get()
        # 引き込み操作
        print("十字y座標")
        print(str((j.get_hat(0))[1]))
        drawin_order=(j.get_hat(0))[1]

        '''## Get Inputs
        print("R2")
        order=(j.get_axis(5)+1)/2
        if abs(order)<0.1:
            order=0
        print(str(order))
        
        output = motor.calc_roller_output(order) # spin: -1~1    

        transmitter.write_single_auto(0,output*0.67)
        time.sleep(0.1)
        transmitter.write_single_auto(1,output*0.67)
        time.sleep(0.1)'''
        transmitter.write_single_auto(0,drawin_order*1.0)
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
    

