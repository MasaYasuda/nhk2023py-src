import v1_nhk23
import time

try:
    roller=v1_nhk23.SingleDrive(100,10,2.77)
    mode=[20,20,20,0,0,0]
    dir=[2,1,2,0,0,0]
    lev=[1,1,1,1,1,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    time.sleep(0.5)
    while 1: 
        Transmitter.reset_input_buffer()
        speed=roller.calc_speed(0.7)
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(1,speed)
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(1,speed)
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(1,speed)
        time.sleep(20)
        Transmitter.reset_input_buffer()
        speed=roller.calc_speed(0.0)
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(1,speed)
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(1,speed)
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(1,speed)
        time.sleep(10)
        
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
    

