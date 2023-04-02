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
    
    mode=[10,10,0,0,0,0]
    direction_config =[3,3,0,0,0,0] #回転が逆だったら3にする
    forward_level=[1,1,1,1,1,1]
    
    transmitter = v1_nhk23.Transmitter("/dev/ArduinoMega1", 115200,mode,direction_config,forward_level)
    goal_position=0
    
    while True:
        transmitter.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        for event in events:
          if event.type ==pygame.JOYHATMOTION: # 変化があった時のみ反応する
            goal_position+=1000*(j.get_hat(0))[1]
            time.sleep(0.05)
            
        transmitter.write_motor_single(0,goal_position)
        time.sleep(0.05)
        transmitter.write_motor_single(1,goal_position)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    init_array=[0,0,0,0,0,0]
    transmitter.write_motor_all(init_array)
    transmitter.close()
    