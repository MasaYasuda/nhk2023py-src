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
        ## Get Inputs
        events = pygame.event.get()
        print("R2の押し込み量")
        print(j.get_axis(5))
        
        spin=(j.get_axis(5)+1)/2
        if spin<0.2:
            spin=0

        transmitter.write_single_auto(0,spin)
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    transmitter.write_single_auto(0,0)
    j.quit()
    transmitter.close()
    




