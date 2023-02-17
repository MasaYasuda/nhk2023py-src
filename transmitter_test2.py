import serial
import struct
import nhk23
import time

transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)

try:
  while True:
    motor_num_array=[0,1,2,3,4,5]
    values=[-0.0,0.2,0.4,0.6,0.8,1.0]
    transmitter.write_all_auto(motor_num_array,values)
    time.sleep(3)

    motor_num_array=[0,1,2,3,4,5]
    values=[-140,0.2,0.4,0.6,0.8,1.0]
    transmitter.write_all_auto(motor_num_array,values)
    time.sleep(3)

    motor_num_array=[0,1,2,3,4,5]
    values=[-20,0.2,0.4,0.6,0.8,1.0]
    transmitter.write_all_auto(motor_num_array,values)
    time.sleep(3)

    

except:
  motor_num_array=[0,1,2,3,4,5]
  values=[-0,0,0,0,0,0]
  transmitter.write_all_auto(motor_num_array,values)
  transmitter.close()
    
  
