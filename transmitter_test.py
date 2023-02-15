import serial
import struct
import nhk23
import time

transmitter = nhk23.Transmitter("COM6", 115200)

try:
  while True:
    motor_num=5
    speed=1
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(5)
except:
  transmitter.close()
    
  