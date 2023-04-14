import v1_nhk23
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    ##### TRANSMITTER SETUP
    
    mode=[100,100,0,0,0,0]
    direction_config =[0,0,0,0,0,0] #回転が逆だったら3にする
    forward_level=[1,1,1,1,1,1] 
    
    transmitter = v1_nhk23.Transmitter("/dev/ttyACM0", 115200,mode,direction_config,forward_level)
    diffdrive=v1_nhk23.DiffDrive()
    time.sleep(1)
    print("コントローラのボタンを押してください")
    while True:
        transmitter.reset_input_buffer()
        
        R_value,L_value=diffdrive.calc_speed_radicon(0.5,0)
        transmitter.write_motor_single(0,R_value)
        transmitter.write_motor_single(1,L_value)
        time.sleep(1)
        R_value,L_value=diffdrive.calc_speed_radicon(0,0)
        transmitter.write_motor_single(0,R_value)
        transmitter.write_motor_single(1,L_value)
        time.sleep(1)



except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0,0,0]
    transmitter.write_motor_all(init_array)
    transmitter.close()
    
