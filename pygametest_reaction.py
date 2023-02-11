import pygame
import time
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print("コントローラのボタンを押してください")
try:
    while True:
        events = pygame.event.get()
        print("十字キー座標")
        print("("+str((j.get_hat(0))[0])+","+str((j.get_hat(0))[1])+")")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()