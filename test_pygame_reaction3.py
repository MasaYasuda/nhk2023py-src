# CORRECT

import pygame
import time
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print("コントローラのボタンを押してください")
try:
    state=0
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYHATMOTION: # 発射用ローラー 
                if (j.get_hat(0))[1]==1:
                    emit_order=emit_order+0.2
                    time.sleep(0.1)
                elif (j.get_hat(0))[1]==-1:
                    emit_order=emit_order-0.2
                    time.sleep(0.1)
        emit_order=max(0,min(emit_order,1))
        print(str(emit_order))
                
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()