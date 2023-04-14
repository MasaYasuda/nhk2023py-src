import v1_nhk23
import time

try:
    Diff=v1_nhk23.DiffDrive(127,254,0.5,30,28)
    mode=[10,10,0,0,0,0]
    dir=[2,0,0,0,0,0]
    lev=[0,0,0,0,0,0]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    time.sleep(0.5)
    while 1:    
        Transmitter.reset_input_buffer()
        Transmitter.write_motor_single(0,2000)
        Transmitter.write_motor_single(1,2000)
        time.sleep(3)
        Transmitter.write_motor_single(0,0)
        Transmitter.write_motor_single(1,0)
        time.sleep(3)

except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0,0,0]
    Transmitter.write_motor_all(init_array)
    Transmitter.close()
    

