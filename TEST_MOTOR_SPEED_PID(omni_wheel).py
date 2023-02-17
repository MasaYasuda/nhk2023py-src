import nhk23
import pygame
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    ##### VECTOR SETUP
    
    vector=nhk23.Vector() # make instance
    
    ##### MOTOR SETUP
    motor=nhk23.Motor("omni") # make instance
    motor.omni_setup(5,50,0.0001,0.1,1000,[1,1,1,1])
    
    ##### TRANSMITTER SETUP
    
    transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)
    # If speed pid
    mode_array=[20,20,20,20,100,100]
    direction_config_array =[2,1,1,2,0,0] #回転が逆だったら3にする
    forward_direction_array=[0,0,0,0,0,0]
    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

    
    print("コントローラのボタンを押してください")
    
    while True:
        ## Get Inputs
        events = pygame.event.get()
        print("左スティック座標")
        print("("+str(j.get_axis(0))+","+ str((-1)*j.get_axis(1))+")")
        print("右スティックx座標")
        print(str(j.get_axis(3)))
        
        ##### VECTOR CALCLATION
        x=j.get_axis(0)
        y=j.get_axis(1)*(-1)
        rotation=j.get_axis(3)
        move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
        
        ##### MOTOR CALCLATION
        omni_output = motor.calc_omni_output(move,rot)  # move,rot is "Vector.move","Vector.rot"
        print(omni_output)
        
        ##### TRANSMIT 
        transmitter.write_all_auto([0,1,2,3],motor.omni_enc_target)

        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0]
    transmitter.write_all_auto([0,1,2,3],init_array)
    j.quit()
    transmitter.close()
    




