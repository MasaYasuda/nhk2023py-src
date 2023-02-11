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
        print("十字キー座標")
        print("("+str((j.get_hat(0))[0])+","+str((j.get_hat(0))[1])+")")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
x=0.6
y=0.8
rot=0
v=nhk23.Vector
v.calc_move(v,x,y)
v.calc_rot(v,rot)

m=nhk23.Motor("omni")
m.omni_setup(100,500,1,1,1000,1)
m.calc_move_speed(v.move)
m.calc_rot_speed(v.rot)
m.compression_speed()
print(m.omni_speed)



