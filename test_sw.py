import v1_nhk23
import time

try:
    mode=[100,0,0,0,0,0]
    dir=[0,0,0,0,0,0]
    lev=[1,1,1,1,1,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    time.sleep(0.5)
    while 1: 
        st=time.time()
        while time.time()-st<4:
          Transmitter.reset_input_buffer()
          Transmitter.write_motor_single(0,0.25)
          time.sleep(0.1)
        st=time.time()
        while time.time()-st<4:
          Transmitter.reset_input_buffer()
          Transmitter.write_motor_single(0,-0.6)
          time.sleep(0.1)
        

except KeyboardInterrupt:
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
    

