import serial
import struct
import nhk23
import time

transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)

try:
  while True:
    motor_num=3
    value=10
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(0.5)
    
    motor_num=0
    value=100
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(0.5)
except:
  transmitter.close()
    
  