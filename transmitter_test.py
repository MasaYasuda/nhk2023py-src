import serial
import struct
import nhk23
import time

transmitter = nhk23.Transmitter("COM6", 115200)

try:
  while True:
    motor_num=5
    value=0.1
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(1)
    
    motor_num=5
    value=0.0
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(1)
    
    motor_num=5
    value=0.5
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(1)
    
    motor_num=5
    value=0.0
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(1)
    
    motor_num=5
    value=1
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(1)
    
    motor_num=5
    value=0.0
    transmitter.store_single_target_values(motor_num,value)
    transmitter.write_single(motor_num)
    time.sleep(1)
except:
  transmitter.close()
    
  