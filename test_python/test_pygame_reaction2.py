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
        for event in events:
            if event.type == pygame.JOYHATMOTION:
                print("十字キー座標")
                print("("+str((j.get_hat(0))[0])+","+str((j.get_hat(0))[1])+")")
            elif event.type == pygame.JOYAXISMOTION:
                if abs((j.get_axis(0))) >= 0.5 or abs((j.get_axis(1))) >= 0.5:
                    print("左スティック座標")
                    print("("+str(j.get_axis(0))+","+ str(j.get_axis(1))+")")
                    
                elif abs((j.get_axis(2))) >= 0.5 or abs((j.get_axis(3))) >= 0.5:
                    print("右スティック座標")
                    print("("+str(j.get_axis(2))+","+ str(j.get_axis(3))+")")
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()