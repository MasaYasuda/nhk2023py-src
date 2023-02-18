import nhk23
import pygame
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    ##### TRANSMITTER SETUP

    transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)

    # If speed pid
    mode_array=[0,100,100,100,100,100]
    direction_config_array =[3,1,1,2,0,0] #回転が逆だったら3にする
    forward_direction_array=[0,0,0,0,0,0]
    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    while True:
        transmitter.reset_input_buffer()
        transmitter.write_single_auto(0 , 0.0)
        time.sleep(3)

        transmitter.write_single_auto(0 , 0.33)
        time.sleep(3)

        transmitter.write_single_auto(0 , 0.66)
        time.sleep(3)

        transmitter.write_single_auto(0 , 1.0)
        time.sleep(3)

        transmitter.write_single_auto(0 , 0.66)
        time.sleep(3)

        transmitter.write_single_auto(0 , 0.33)
        time.sleep(3)


except:
    print("プログラムを終了します")
    init_array=[0,0,0,0]
    transmitter.write_all_auto([0,1,2,3],init_array)
    transmitter.close()
    




