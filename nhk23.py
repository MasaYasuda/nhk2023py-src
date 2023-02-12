import math
import serial
import struct
class Vector:
  '''
  HOW TO USE Vector class
  
  vector=nhk23.Vector() # make instance
  move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
  
  ********
  move : [a1,a2,a3,a4] -1~1
  rot : [ROT,ROT,ROT,ROT] -1~1
  ********
  '''
  def __init__ (self):
    self.move =[0]
    self.rot =[0]
  
  def calc_move(self,x,y):
    r = math.sqrt(x**2 + y**2) 
    if abs(r)<0.2:
      r=0
    r = max(-1, min(r, 1))
    theta = math.atan2(y, x) # rad
    
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    self.move = [x - y, x + y, -x + y, -x - y]
    return
  
  def calc_rot(self,rot):
    if abs(rot)<0.2:
      rot=0
    rot = max(-1, min(rot, 1))
    self.rot = [rot,rot,rot,rot]
    return
  
  def calc_vector(self,x,y,rot):
    self.calc_move(x,y)
    self.calc_rot(rot)
    return self.move , self.rot
  
class Motor:
  '''
  HOW TO USE Motor class
  
  ########## For 4 omni wheels ##########
  
  motor=nhk23.Motor("omni") # make instance
  motor.omni_setup(diamiter,diagonal,max_move,max_rot,max_wheel_speed,gear_ratio)
  output = motor.calc_omni_output(move,rot)  # move,rot is "Vector.move","Vector.rot"
     
  ********
  diamiter: mm
  diagonal: mm
  max_move: m/s
  max_rot : rpm
  max_wheel_speed : rpm
  gear_ratio : [b1,b2,b3,b4] (signed) # if the encoder rotates faster than wheel -> b1,b2,b3,b4 >1
  
  output : [a1,a2,a3,a4] rpm # "output" is the target value for encoder
  
  # 4輪オムニ車体が時計回りに回転するとき全出力は正
  ********
  
  ########## For roller(single) ##########
  
  motor=nhk23.Motor("roller") # make instance
  motor.roller_setup(diamiter,max_spin,gear_ratio)
  output = motor.calc_roller_output(spin) # spin: -1~1 

  ********
  diamiter: mm
  max_spin : m/s
  gear_ratio : (signed) # if the encoder rotates faster than wheel -> b1,b2,b3,b4 >1
  
  output : rpm  # "output" is the target value for encoder
  ********
  
  '''
  def __init__(self,type): 
    
    if type == "omni":
      self.__wheel_diameter = 0 # mm
      self.__omni_diagonal = 0 # mm
      self.__max_move_speed = 0 # m/s
      self.__max_rot_speed = 0 # rpm
      self.__compress_rate =0.5 # 0~1
      self.__max_wheel_speed = 0 #rpm
      self.__omni_enc_gear_ratio = [1,1,1,1] #符号付き encoderのほうが早く(多く)回る:　ratio>1
      
      self.omni_move_speed = [0,0,0,0] # rpm
      self.omni_rot_speed = [0,0,0,0] # rpm
      self.omni_speed = [0,0,0,0] # rpm
      self.omni_enc_target =[0,0,0,0] #rpm
   
    elif type == "roller":
      self.__roller_diameter = 0 # mm
      self.__max_spin_speed = 0 # m/s
      self.__roller_enc_gear_ratio = 1 #符号付き
      
      self.roller_speed = 0 # rpm
      self.roller_enc_target = 0
    
  ## FOR 4 OMNI WHEELS ########################
  
  def omni_setup(self,diamiter,diagonal,max_move,max_rot,max_wheel_speed,gear_ratio):
    self.__wheel_diameter = diamiter
    self.__omni_diagonal = diagonal
    self.__max_move_speed = max_move
    self.__max_rot_speed = max_rot
    self.__max_wheel_speed = max_wheel_speed
    self.__omni_enc_gear_ratio = gear_ratio
    
  def calc_move_speed(self,move): # move: generated by Vector.move()
    for i in range(0,4):
      self.omni_move_speed[i]=self.__max_move_speed * move[i] *30000 / self.__wheel_diameter/ 2 /math.pi # N[rpm]=30*v[m/s]/(r[mm]*pi)
    return
  
  def calc_rot_speed(self,rot):
    for i in range(0,4):
      self.omni_rot_speed[i]=self.__max_rot_speed * rot[i]*self.__omni_diagonal/2 /self.__wheel_diameter/2 # v[m/s]=ω*r=ω'*r'
    return
  
  def compression_speed(self):
    check_ratio=1
    for i in range(0,4):
      self.omni_speed[i] = self.omni_move_speed[i] + self.omni_rot_speed[i]
      if self.omni_speed[i] > self.__max_wheel_speed:
        check_ratio = min[check_ratio , self.__max_wheel_speed/self.omni_speed[i] ]
    if check_ratio<1:
      for i in range(0,4):
        self.omni_speed[i] = check_ratio* (self.omni_move_speed[i] + self.omni_rot_speed[i])
    return
  
  def calc_omni_enc_target(self):
    for i in range(0,4):
      self.omni_enc_target[i] = self.__omni_enc_gear_ratio[i]*self.omni_speed[i]
    return
  
  def calc_omni_output(self,move,rot):
    self.calc_move_speed(move)
    self.calc_rot_speed(rot)
    self.compression_speed()
    self.calc_omni_enc_target()
    return self.omni_enc_target
  
  ## FOR ROLLER #########################
    
  def roller_setup(self,diamiter,max_spin,gear_ratio):
    self.__roller_diameter = diamiter
    self.__max_spin_speed = max_spin
    self.__roller_enc_gear_ratio = gear_ratio
    
  def calc_roller_speed(self,spin): # spin: -1~1
    self.roller_speed=self.__max_spin_speed * spin *30000 / self.__roller_diameter /math.pi # N[rpm]=30*v[m/s]/(r[mm]*pi)
    return
  def calc_roller_enc_target(self):
    self.roller_enc_target = self.__roller_enc_gear_ratio * self.roller_speed
    return
  
  def calc_roller_output(self,spin):
    self.calc_roller_speed(spin)
    self.calc_roller_enc_target()
    return self.roller_enc_target
  
  
class Transmitter (serial.Serial):
  """
  HOW TO USE Transmiter class
  
  ## AUTOMATIC

  transmitter = nhk23.Transmitter("COM3", 115200)
  motor_num_array=[0,1,2,3,4,5]
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
  
  
    
    
  