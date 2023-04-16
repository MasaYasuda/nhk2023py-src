import v1_nhk23
import time

try:
    mode=[50,50,0,0,0,0]
    dir=[0,0,0,0,0,0]
    lev=[0,0,0,0,0,0]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega2",115200,mode,dir,lev)
    time.sleep(0.5)
    while 1: 
        Transmitter.reset_input_buffer()
        Transmitter.write_air_single(0,1)
        Transmitter.write_air_single(1,0)
        time.sleep(2)
        Transmitter.reset_input_buffer()
        Transmitter.write_air_single(0,0)
        Transmitter.write_air_single(1,1)
        time.sleep(2)

except KeyboardInterrupt:
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
    

