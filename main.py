import nhk23
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
        print("右スティック座標")
        print("("+str(j.get_axis(2))+","+ str(j.get_axis(3))+")")
        x=j.get_axis(0)
        y=j.get_axis(1)*(-1)
        rot=0
        v=nhk23.Vector()
        v.calc_move(v,x,y)
        v.calc_rot(v,rot)

        m=nhk23.Motor("omni")
        m.omni_setup(100,500,1,1,1000,1)
        m.calc_move_speed(v.move)
        m.calc_rot_speed(v.rot)
        m.compression_speed()
        print(m.omni_speed)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()




