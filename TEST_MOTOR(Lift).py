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
    mode_array=[20,100,100,100,100,100]
    direction_config_array =[0,0,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[0,0,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    while True:
        ## Get Inputs
        events = pygame.event.get()
        print("十字キー座標")
        print(str((j.get_hat(0))[1]))

        speed_encoder_rpm=((j.get_hat(0))[1])*10

        transmitter.write_single_auto(0,speed_encoder_rpm)
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    transmitter.write_all_auto([0,1,2,3],motor.omni_enc_target)
    j.quit()
    transmitter.close()
    

