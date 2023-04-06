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
    while True:
        ## Get Inputs
        events = pygame.event.get()
        
        ##### VECTOR CALCLATION
        
        move=v1_nhk23.joy_threshold(j.get_axis(1)*(-1)*(1.0),0.3)
        rot=v1_nhk23.joy_threshold(j.get_axis(3)*0.5,0.3)
        
        print(move)
        time.sleep(0.05)



except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    