import v1_nhk23
import time

try:
    Diff=v1_nhk23.DiffDrive(127,254,0.4,30,28)
    mode=[100,100,0,0,0,0]
    dir=[0,0,0,0,0,0]
    lev=[0,0,1,1,1,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    time.sleep(0.5)
    while 1: 
        Transmitter.reset_input_buffer()
        R_speed,L_speed=Diff.calc_speed_radicon(0,1)
        Transmitter.write_motor_single(0,R_speed)
        Transmitter.write_motor_single(1,L_speed)
        time.sleep(3)
        Transmitter.reset_input_buffer()
        R_speed,L_speed=Diff.calc_speed_radicon(0,0)
        Transmitter.write_motor_single(0,R_speed)
        Transmitter.write_motor_single(1,L_speed)
        time.sleep(3)
        Transmitter.reset_input_buffer()
        R_speed,L_speed=Diff.calc_speed_radicon(1,0)
        Transmitter.write_motor_single(0,R_speed)
        Transmitter.write_motor_single(1,L_speed)
        time.sleep(3)

except KeyboardInterrupt:
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
    

