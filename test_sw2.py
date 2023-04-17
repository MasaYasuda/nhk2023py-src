import v1_nhk23
import time

try:
    #[引き込み、昇降、発射上、発射下]
    roller=v1_nhk23.SingleDrive(100,10,2.77)
    mode=[100,100,20,20,0,0]
    dir=[0,0,2,1,0,0]
    lev=[1,1,1,1,1,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    time.sleep(0.5)
    
    st=time.time()
    while time.time()-st<5:
      Transmitter.reset_input_buffer()
      Transmitter.write_motor_single(1,-0.75)
      time.sleep(0.1)
    
    speed=roller.calc_speed(0.5)
    Transmitter.write_motor_single(2,speed)
    Transmitter.write_motor_single(2,speed)
    time.sleep(0.5)
    Transmitter.write_motor_single(3,speed)
    Transmitter.write_motor_single(3,speed)
    
    time.sleep(2)
    
    st=time.time()
    for i in range(0,4):
      #index reset
      Transmitter.reset_data_single(1,100)
      Transmitter.reset_data_single(1,100)
      Transmitter.reset_data_single(1,100)
      #上昇
      
      st=time.time()
      while time.time()-st<2:
        Transmitter.reset_input_buffer()
        Transmitter.write_motor_single(1,-0.75)
        time.sleep(0.1)
      #戻し
      st=time.time()
      while time.time()-st<1:
        Transmitter.reset_input_buffer()
        Transmitter.write_motor_single(0,-0.75)
        time.sleep(0.1)
      #引き込み
      st=time.time()
      while time.time()-st<2:
        Transmitter.reset_input_buffer()
        Transmitter.write_motor_single(0,0.75)
        time.sleep(0.1)
      
    #停止
    Transmitter.write_motor_single(2,0)
    Transmitter.write_motor_single(2,0)
    Transmitter.write_motor_single(3,0)
    Transmitter.write_motor_single(3,0)
    time.sleep(1)
    
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
      
        

except KeyboardInterrupt:
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
    

