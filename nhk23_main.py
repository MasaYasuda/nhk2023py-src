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
    vector=nhk23.Vector() # make instance
    motor=nhk23.Motor("omni") # make instance
    motor.omni_setup(5,50,0.0001,0.1,1000,[1,1,1,1])
    #motor2=nhk23.Motor("roller") # make instance
    #motor2.roller_setup(50,1,1)
    transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)
    
    while True:
        ## Get Inputs
        events = pygame.event.get()
        print("左スティック座標")
        print("("+str(j.get_axis(0))+","+ str((-1)*j.get_axis(1))+")")
        print("右スティックx座標")
        print(str(j.get_axis(3)))
        
        '''
        print("R2の押し込み量")
        print(j.get_axis(5))
        '''
        
        x=j.get_axis(0)
        y=j.get_axis(1)*(-1)
        rotation=j.get_axis(3)
        spin=(j.get_axis(5)+1)/2
        if spin<0.2:
            spin=0
        
        move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
        omni_output = motor.calc_omni_output(move,rot)  # move,rot is "Vector.move","Vector.rot"
        print(omni_output)
        '''
        spin_output = motor2.calc_roller_output(spin) # spin: -1~1 
        print(spin_output)
        '''
        transmitter.write_all_auto([0,1,2,3],motor.omni_enc_target)

        # transmitter.write_single_auto(5,motor2.roller_enc_target)
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    transmitter.write_all_auto([0,1,2,3],motor.omni_enc_target)
    j.quit()
    transmitter.close()
    




