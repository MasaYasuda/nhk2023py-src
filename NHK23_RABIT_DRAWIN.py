import v1_nhk23
import pygame
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print("コントローラのボタンを押してください")
    ##### TRANSMITTER SETUP
    
    mode=[100,0,0,0,0,0]
    direction_config =[3,3,0,0,0,0] #回転が逆だったら3にする
    forward_level=[1,1,1,1,1,1]
    
    transmitter = v1_nhk23.Transmitter("/dev/ArduinoMega1", 115200,mode,direction_config,forward_level)

    while True:
        transmitter.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        
        ##### VECTOR CALCLATION
        
        value=v1_nhk23.joy_threshold(j.get_axis(1)*(-1)*0.3,0.1)
        
        ##### TRANSMIT 
        transmitter.write_motor_single(0,value)
        time.sleep(0.05)


except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    init_array=[0,0,0,0,0,0]
    transmitter.write_motor_all(init_array)
    transmitter.close()
    