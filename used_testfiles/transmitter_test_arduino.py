import math
import serial
import struct
import os
import time

class Transmitter (serial.Serial):
  """
  this class is specified for ArduinoMegaMotorSlave.

  HOW TO USE Transmiter class
  


  ## AUTOMATIC

  transmitter = nhk23.Transmitter("COM3", 115200)
  motor_num_array=[0,1,2,3,4,5]
  # If speed pid
  mode_array=[20,20,20,20,20,20]
  direction_config_array =[0,0,0,0,0,0]
  forward_direction_array=[0,0,0,0,0,0]

  transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)

  values=[10,10,10,10,10,10]
  transmitter.write_all_auto(motor_num_array,values)
  transmitter.close()  ## DON'T FORGET!!
  
  ************
  # 1Byte目は固定値0xFF
  # 2Byte目は1Byteデータ（数値）
  # 3~6Byte目はfloat型数値
  ************
  
  ## SINGLE ORDER
  
  transmitter = nhk23.Transmitter("COM3", 115200)
  motor_num=3
  value=10
  transmitter.write_single_auto(motor_num,value)
  transmitter.close()   ## DON'T FORGET!!
  
  """
  
  def __init__(self, port, baudrate):
        super().__init__(port, baudrate) # 基底クラスのコンストラクタをオーバーライド
        self.target_values = [0,0,0,0,0,0]
        self.target_mode =[100,100,100,100,100,100]
        self.target_direction_config=[0,0,0,0,0,0]
        self.target_forward_direction=[0,0,0,0,0,0]
        
  def store_single_target_values(self,motor_num,value):  # motor_num starts 0 (max 5)
    self.target_values[motor_num]=float(value)
    
  def store_all_taget_values(self,motor_num_array,values):
    for i in range(0,len(motor_num_array)):
      self.target_values[motor_num_array[i]]=float(values[i])
  
      
  def write_single(self,motor_num):
    # 1Byte目は固定値0xFF
    # 2Byte目は1Byteデータ（数値）
    # 3~6Byte目はfloat型数値
    data = [0xFF, motor_num.to_bytes(1,"big"),self.target_values[motor_num]]
    packet = struct.pack('>Bcf', *data)
    self.write(packet)
    print(data)
    print(str(packet))
    return data
  
  def write_reset_null(self):
    # 1Byte目は固定値0xFF
    # 2Byte目は1Byteデータ（数値）
    # 3~6Byte目はfloat型数値
    NULL=0.0
    print("POINT 0")
    data = [0x00, 0x00,NULL]
    print("POINT 1")
    packet = struct.pack('>BBf', *data)
    print("POINT 2")
    self.write(packet)
    print("POINT 3")
    print(data)
    print("POINT 4")
    print(str(packet))
    print("POINT 5")
    return data
  
  def write_all(self):
    for i in range(0,6):
      self.write_single(i)
      
  def write_all_auto(self,motor_num_array,values):
    self.store_all_taget_values(motor_num_array,values)
    self.write_all()
    return 
  
  def write_single_auto(self,motor_num,value):
    self.store_single_target_values(motor_num,value)
    self.write_single(motor_num)
    return 
  
  def write_mode_auto(self,mode_array):
    '''
    motor_num=0 to 5
    define mode num  =100 to 105
    
    mode:
    0... radio controll ->
    10... position pid
    20... speed pid
    100(default) ... output disabled

    '''
    for i in range(0,6):
      self.target_mode[i]=float(mode_array[i])
      # 1Byte目は固定値0xFF
      # 2Byte目は1Byteデータ（数値）
      # 3~6Byte目はfloat型数値
      data = [0xFF, (i+100).to_bytes(1,"big"),self.target_mode[i]]
      packet = struct.pack('>Bcf', *data)
      self.write(packet)
      print(data)
      print(str(packet))
  
  def write_direction_config(self,config_array):
    '''
    motor_num = 0 to 5
    config_num = 200 to 205
    
    To know the config number, please refer to this ""

    '''
    for i in range(0,6):
      self.target_direction_config[i]=float(config_array[i])
      # 1Byte目は固定値0xFF
      # 2Byte目は1Byteデータ（数値）
      # 3~6Byte目はfloat型数値
      data = [0xFF, (i+200).to_bytes(1,"big"),self.target_direction_config[i]]
      packet = struct.pack('>Bcf', *data)
      self.write(packet)
      print(data)
      print(str(packet))
    
  def write_forward_direction(self,forward_direction_array):
    for i in range(0,6):
      self.target_forward_direction[i]=float(forward_direction_array[i])
      # 1Byte目は固定値0xFF
      # 2Byte目は1Byteデータ（数値）
      # 3~6Byte目はfloat型数値
      data = [0xFF, (i+210).to_bytes(1,"big"),self.target_forward_direction[i]]
      packet = struct.pack('>Bcf', *data)
      self.write(packet)
      print(data)
      print(str(packet))

  def write_config_all(self,mode_array,config_array,forward_direction_array):
    self.write_mode_auto(mode_array)
    self.write_direction_config(config_array)
    self.write_forward_direction(forward_direction_array)
    print("Configured")



try:
    transmitter = Transmitter("COM3", 115200)
    # If speed pid
    mode_array=[0,0,0,0,100,100]
    direction_config_array =[0,0,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[0,0,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)
    index=0
    while True:
        transmitter.reset_input_buffer()
        transmitter.write_single_auto(0,index*(-0.5))
        transmitter.write_single_auto(1,index*(-0.5))
        transmitter.write_single_auto(2,index*(-0.5))
        transmitter.write_single_auto(3,index*(-0.5))
        transmitter.write_single_auto(4,index*(-0.5))
        transmitter.write_single_auto(5,index*(-0.5))
        time.sleep(1)
        index=1-index
        
except KeyboardInterrupt:
    print("プログラムを終了します")
    transmitter.write_single_auto(0,0)
    transmitter.write_single_auto(1,0)
    transmitter.write_single_auto(2,0)
    transmitter.write_single_auto(3,0)
    transmitter.write_single_auto(4,0)
    transmitter.write_single_auto(5,0)
    transmitter.close()
    

