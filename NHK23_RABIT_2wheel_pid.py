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
    
    mode=[20,20,0,0,0,0]
    direction_config =[2,0,0,0,0,0] #回転が逆だったら3にする
    forward_level=[1,1,1,1,1,1] 
    
    transmitter = v1_nhk23.Transmitter("/dev/ttyACM0", 115200,mode,direction_config,forward_level)
    diffdrive=v1_nhk23.DiffDrive(127,254,0.4,10,28)
    time.sleep(2)

    print("コントローラのボタンを押してください")
    while True:
        transmitter.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        
        ##### VECTOR CALCLATION
        
        move=v1_nhk23.joy_threshold(j.get_axis(1)*(-1)*(1.0),0.4)
        rot=v1_nhk23.joy_threshold(j.get_axis(3)*(1),0.4)
        R_value,L_value=diffdrive.calc_speed(move,rot)
        
        print(move,rot)
        # print(R_value,L_value)
        ##### TRANSMIT 
        #transmitter.write_motor_single(0,R_value)
        #transmitter.write_motor_single(1,L_value)
        time.sleep(0.05)



except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    init_array=[0,0,0,0,0,0]
    transmitter.write_motor_all(init_array)
    transmitter.close()
    