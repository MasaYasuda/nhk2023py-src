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
    
    transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)
    # If speed pid
    mode_array=[0,100,100,100,100,100]
    direction_config_array =[0,0,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[0,0,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    while True:
        #transmitter.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        print("右スティックy座標")
        print(str((-1)*j.get_axis(4)))
        order=(-1)*j.get_axis(4)
        if abs(order)<0.2:
            order=0

        transmitter.write_single_auto(0,order*0.5)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    transmitter.write_single_auto(0,0)
    j.quit()
    transmitter.close()
    

