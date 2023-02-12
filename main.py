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
        ## Get Inputs
        events = pygame.event.get()
        print("右スティック座標")
        print("("+str(j.get_axis(2))+","+ str(j.get_axis(3))+")")
        print("右スティックx座標")
        print(str(j.get_axis(3)))
        print("R2の押し込み量")
        print(j.get_axis(5))
        
        x=j.get_axis(0)
        y=j.get_axis(1)*(-1)
        rotation=j.get_axis(3)
        spin=(j.get_axis(5)+1)/2
        if spin<0.2:
            spin=0
        
        vector=nhk23.Vector() # make instance
        move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
        
        motor=nhk23.Motor("omni") # make instance
        motor.omni_setup(100,500,1,1,1000,1)
        omni_output = motor.calc_omni_output(move,rot)  # move,rot is "Vector.move","Vector.rot"
        print(omni_output)
        
        motor2=nhk23.Motor("roller") # make instance
        motor2.roller_setup(50,1000,1)
        output = motor2.calc_roller_output(spin) # spin: -1~1 
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()




