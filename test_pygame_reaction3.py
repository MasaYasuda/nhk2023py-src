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
            if event.type == pygame.JOYHATMOTION:
                if (j.get_hat(0))[1]==1:
                    state=state+1
                    print("state="+str(state))
                    time.sleep(0.1)
                elif (j.get_hat(0))[1]==-1:
                    state=state-1
                    print("state="+str(state))
                    time.sleep(0.1)
            elif event.type == pygame.JOYBUTTONDOWN: #ボタンが押された場合
                if j.get_button(0):
                    print("四角ボタンが押されました")
                    time.sleep(0.1)
                
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()