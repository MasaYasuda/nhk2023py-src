import v1_nhk23
import time

try:
    Diff=v1_nhk23.DiffDrive(127,254,0.5,30,28)
    mode=[100,100,0,0,0,0]
    dir=[0,0,0,0,0,0]
    lev=[0,0,0,0,0,0]
    Transmitter=v1_nhk23.Transmitter("/dev/ttyACM0",115200,mode,dir,lev)
    time.sleep(0.5)
    while 1:    
        Transmitter.reset_input_buffer()
        Transmitter.write_motor_single(0,0.5)
        time.sleep(1)
        Transmitter.write_motor_single(0,0)
        time.sleep(1)
except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0,0,0]
    Transmitter.write_motor_all(init_array)
    Transmitter.close()
    

