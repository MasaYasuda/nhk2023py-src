
import math
import serial
import struct
import os

###### 触らない
if os.name == 'nt':
    import msvcrt
else:
    import sys, tty, termios
from dynamixel_sdk import * # Uses Dynamixel SDK library
###############

def joy_threshold(value,threshold):
  """絶対値がしきい値以下の場合は0にする

  Parameters
  ----------
  value : any
      対象の値
  threshold : any
      しきい値

  Returns
  -------
  value : any
      処理後の値
  """
  if abs(value)<threshold:
    value=0
  return value

def calc_vector(x,y):
  """
  座標から単位円のベクトルを求める。
  
  Parameters
  ---------
  x : float
    -1~1で示される移動のx座標 
  y : float
    -1~1で示される移動のy座標 

  Returns
  ---------
  r : float
    0~1 で示される半径
  theta : float
    弧度法(rad)で示される0~2*pi
  """
  r = math.sqrt(x**2 + y**2) 
  r = max(-1, min(r, 1))
  theta = math.atan2(y, x) # rad
  
  return r,theta 
  
 
class SingleDrive:
  def __init__(self,diameter,max_velocity,gear_ratio):
    """単一モーター回転量計算

    Parameters
    ----------
    diameter : float
      直径[mm]
    max_velocity : float
      最大の速さ[m/s]
    gear_ratio : float
      最終的な出力回転量と観測エンコーダーの回転量の比
      =エンコーダーの観測回転量/出力1回転
    """
    self.__DIAMETER=diameter
    self.__MAX_VELOCITY=max_velocity
    self.__GEAR_RATIO=gear_ratio
  
  def calc_speed(self,power):
    """エンコーダーの目標観測回転量の算出
    
    Parameters
    -----------
    power : float
     -1~1で示される回転量の大きさ
    
    Return
    ---------
    speed : float
      エンコーダーの目標観測回転量[rpm]
    """
    velocity=self.__MAX_VELOCITY * power * 2 *30000 / self.__DIAMETER /math.pi # N[rpm]=30*v[m/s]/(r[mm]*pi)
    speed = self.__GEAR_RATIO * velocity
    return speed

class OmniDrive:
  def __init__(self,diameter=0.0,diagonal=0.0,max_move=0.0,max_rot=0.0,gear_ratio=0.0):
    """4輪オムニ制御用各モーター回転量計算

    Parameters
    ----------
    diameter : float, optional
        直径[mm], by default 0.0
    diagonal : float, optional
        対角線長[mm], by default 0.0
    max_move : float, optional
        最大移動速度[m/s], by default 0.0
    max_rot : float, optional
        最大旋回速度[rpm], by default 0.0
    gear_ratio : float, optional
        最終的な出力回転量と観測エンコーダーの回転量の比
        =エンコーダーの観測回転量/出力1回転
        , by default 0.0
    """
    self.__DIAMETER =diameter
    self.__DIAGONAL=diagonal
    self.__MAX_MOVE=max_move
    self.__MAX_ROT=max_rot
    self.__GEAR_RATIO=gear_ratio
    
  def calc_speed_radicon(self,r,theta,rot):
    """
    ラジコン制御用各エンコーダーの目標観測回転量の算出
    配列は右前、左前、左後、右後 の順

    Parameters
    ----------
    r : float
        ベクトルの強さ。-1~1
    theta : float
        偏角[rad]
    rot : float
        旋回の強さ。-1~1

    Returns
    -------
    speed : list [float] *4
      各モーターの回転の強度-1~1
    """
    x = r * math.cos(theta)/math.sqrt(2)
    y = r * math.sin(theta)/math.sqrt(2)
    move = [x - y, x + y, -x + y, -x - y]
    
    check_ratio=1
    speed = [0] * 4
    
    for i in range(0,4):
      speed[i] = move[i] + rot
      if speed[i] > 1:
        check_ratio = min(check_ratio , 1/speed[i] )
    if check_ratio<1:
      for i in range(0,4):
        speed[i] = check_ratio* (move[i] + rot)
        
    return speed
  
  def calc_speed(self,r,theta,rot):
    """フィードバック制御用各エンコーダーの目標観測回転量の算出
    配列は右前、左前、左後、右後 の順

    Parameters
    ----------
    r : float
        -1~1
    theta : float
        [rad]
    rot : float
        -1~1
        
    Returns
    -------
    speed : list[float]*4
        エンコーダーの目標観測回転量
    """
    x = r * math.cos(theta)/math.sqrt(2)
    y = r * math.sin(theta)/math.sqrt(2)
    move = [x - y, x + y, -x + y, -x - y]
    speed=[0]*4
    
    for i in range(0,4):
      speed[i]=self.__MAX_MOVE * move[i] * 2 * 30000 / self.__DIAMETER /math.pi # N[rpm]=30*v[m/s]/(r[mm]*pi)
      speed[i]+=self.__MAX_ROT * rot *self.__DIAGONAL/ self.__DIAMETER # v[m/s]=ω*r=ω'*r'
    
    return speed
    
    

class DiffDrive:
  """差動二輪制御用モーター回転量計算

  Parameters
  ----------
  __DIAMETER :float
  __DISTANCE : float
  __MAX_MOVE :  float
  __MAX_ROT : float
  __GEAR_RATIO :int
    最終的なタイヤの回転量と観測エンコーダーの回転量の比

  """
  def __init__(self,diameter=0.0,distance=0.0,max_move=0.0,max_rot=0.0,gear_ratio=0.0):
    """差動二輪制御用モーター回転量計算

    Parameters
    ----------
    diameter : float, optional
        直径[mm], by default 0.0
    distance : float, optional
        対角線長[mm], by default 0.0
    max_move : float, optional
        最大移動速度[m/s], by default 0.0
    max_rot : float, optional
        最大旋回速度[rpm], by default 0.0
    gear_ratio : float, optional
        最終的な出力回転量と観測エンコーダーの回転量の比
        =エンコーダーの観測回転量/出力1回転
        , by default 0.0
    """
    
    self.__DIAMETER =diameter
    self.__DISTANCE=distance
    self.__MAX_MOVE=max_move
    self.__MAX_ROT=max_rot
    self.__GEAR_RATIO=gear_ratio
    
  def calc_speed_radicon(self,move,rot):
    """ラジコン制御用各エンコーダーの目標観測回転量の算出

    Parameters
    ----------
    move : float
        -1~1で示される前後移動の強さ
    rot : float
        -1~1で示される回転運動の強さ
        
    Returns 
    ----------
    R_speed :
      -1~1で示される右車輪の回転量の大きさ 
    L_speed :
      -1~1で示される左車輪の回転量の大きさ
      
    """
    R_speed = move - rot
    L_speed = move + rot

    # 大きすぎる値（1以上）のとき圧縮する
    R_abs = abs(R_speed)  # 絶対値を求める
    L_abs = abs(L_speed)  # 絶対値を求める

    if R_abs > 1 or L_abs > 1:
        if R_abs >= L_abs:
            R_speed = R_speed / R_abs  # 圧縮
            L_speed = L_speed / R_abs  # 圧縮
        elif R_abs < L_abs:
            R_speed = R_speed / L_abs
            L_speed = L_speed / L_abs
            
    return R_speed,L_speed
    
  def calc_speed(self,move,rot):
    return 0
  
  
class Transmitter (serial.Serial):
  """
  
  Parameters
  -------------
  __ADDR_MOTOR : int
  __ADDR_MODE : int
  __ADDR_DIRECTION_CONFIG : int
  __ADDR_FORWARD_LEVEL : int

  """
  
  def __init__(self, port, baudrate,mode,direction_config,forward_level):
    """Slaveマイコンへの目標値送信

    Parameters
    ----------
    port : String
        ポート番号又はデバイスファイル名
    baudrate : int
        通信速度
    mode : list[int]*6
        モードの指定(0:ラジコン/10:位置型PID/20:速度型PID/100:出力無効)
    direction_config : list[int]*6
        To know the config number, please refer to this ""
    forward_level : list[int]*6
        正回転の場合のDIRピンのレベル(0 or 1)
    """
    super().__init__(port, baudrate) # 基底クラスのコンストラクタをオーバーライド
    self.__ADDR_MOTOR=0
    self.__ADDR_MODE=200
    self.__ADDR_DIRECTION_CONFIG=210
    self.__ADDR_FORWARD_LEVEL=220
    
    #mode等の初期設定
    self.__write_all(self.__ADDR_MODE,mode)
    self.__write_all(self.__ADDR_DIRECTION_CONFIG,direction_config)
    self.__write_all(self.__ADDR_FORWARD_LEVEL,forward_level)
    
    
  def __write_single(self,addr_direct,value):
    """_summary_

    Parameters
    ----------
    addr_direct : int
        指定するArduino側のADDR（厳密には設定番号）
    value : float

    Returns
    -------
    data : list[int,byte,float]
      送信値(バイナリではない)
    """
    # 1Byte目は固定値0xFF
    # 2Byte目は1Byteデータ（数値）
    # 3~6Byte目はfloat型数値
    # 7Byte目はチェックサム（開始宣言バイト0xFFも含む）
    
    data = [0xFF, addr_direct.to_bytes(1,"big"),float(value)]
    packet = struct.pack('>Bcf', *data)
    checksum=sum(packet) & 0xFF
    self.write(packet)
    self.write(checksum)
    print(packet,checksum)
    
    
    return data
  
  def __write_all(self,addr,value):
    """

    Parameters
    ----------
    addr : int
     書き込むアドレス (0番目)
    value : list[float]*6
     各値
     
    """
    for i in range (0,6):
      self.__write_single(i+addr,value[i])
      
  def write_motor_single(self,num,value):
    """1つのモーターの目標値を送信する

    Parameters
    ----------
    num : int
        モーター番号
    value : float
        目標値

    """
    if num>5:
      return 0
    data=self.__write_single(num,value)
    
  def write_motor_all(self,value):
    """全てのモーターの目標値を送信する

    Parameters
    ----------
    value : list[float]*6
        目標値の配列
    """
    self.__write_all(self.__ADDR_MOTOR,value)
    


class Dynamixel:
  def __init__(self,port,baudrate,id,min_position,max_position):
    if os.name == 'nt':
        def getch():
            return msvcrt.getch().decode()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        def getch():
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        
    #********* DYNAMIXEL Model definition *********
    self.__MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430
    self.__ADDR_TORQUE_ENABLE          = 64
    self.__ADDR_GOAL_POSITION          = 116
    self.__ADDR_PRESENT_POSITION       = 132
    self.__ADDR_MAXIMUM_POSITION_VALUE = 48
    self.__ADDR_MINIMUM_POSITION_VALUE = 52
    self.__MINIMUM_POSITION_VALUE  = min_position         # ダイナミクセルの最小値は0
    self.__MAXIMUM_POSITION_VALUE  = max_position      # ダイナミクセルの最小値は4095
    self.__BAUDRATE                    = baudrate
    self.__PROTOCOL_VERSION            = 2.0
    self.__ID                      = id  # Factory default ID of all DYNAMIXEL is 1
    self.__DEVICENAME                  = port  # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"

    self.__now_goal_position=0
    self.__now_goal_position_value=0
    self.__portHandler = PortHandler(self.__DEVICENAME)
    self.__packetHandler = PacketHandler(self.__PROTOCOL_VERSION)

    # Open port
    if self.__portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()

    # Set port baudrate
    if self.__portHandler.setBaudRate(self.__BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()
    
    # Write Max Position Limit
    dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(self.__portHandler, self.__ID, self.__ADDR_MAXIMUM_POSITION_VALUE, self.__MAXIMUM_POSITION_VALUE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
    print("SET MAX POSITION")
    
    # Write Min Position Limit
    dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(self.__portHandler, self.__ID, self.__ADDR_MINIMUM_POSITION_VALUE, self.__MINIMUM_POSITION_VALUE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
    print("SET MIN POSITION")
    
    
  def enable_torque(self):
    """トルクをONにする
    """
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(self.__portHandler, self.__DXL_ID, self.__ADDR_TORQUE_ENABLE,1)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")
  
  def disable_torque(self):
    """トルクをオフにする
    """
    dxl_comm_result, dxl_error = self.__packetHandler.write1ByteTxRx(self.__portHandler, self.__DXL_ID, self.__ADDR_TORQUE_ENABLE,0)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % self.__packetHandler.getRxPacketError(dxl_error))   
  
  def write_position(self,value):
    """目標位置を書き込む

    Parameters
    ----------
    value : float
        0(MinPositionLimit)~1(MaxPositionLimit)で示される位置の値
    """
    self.__now_goal_position_value = max(0, min(value, 1)) # value: 0~1
    position=(self.__MAXIMUM_POSITION_VALUE*self.__now_goal_position_value)+(1-self.__now_goal_position_value)*self.__MINIMUM_POSITION_VALUE
    self.__now_goal_position = int(position)  # position: 0~4095
    dxl_comm_result, dxl_error = self.__packetHandler.write4ByteTxRx(self.__portHandler, self.__ID, self.__ADDR_GOAL_POSITION, self.__now_goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
    print("SET POSITION")
    print("[ID:%03d]  GoalPos:%03d  Value:%03f" % (self.__DXL_ID, self.__now_goal_position,self.__now_goal_position_value))
    
        
  def read_position(self): 
    """現在の位置の読みとり

    Returns
    -------
    dxl_present_position : int
      0~4095までの値
    present_position_value : float
      0(MinPositionLimit)~1(MaxPositionLimit)で示される現在位置の値
      
    """
    dxl_present_position, dxl_comm_result, dxl_error = self.__packetHandler.read4ByteTxRx(self.__portHandler, self.__DXL_ID, self.__ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % self.__packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % self.__packetHandler.getRxPacketError(dxl_error))
        
    present_position_value=(dxl_present_position-self.__DXL_MINIMUM_POSITION_VALUE)/(self.__DXL_MAXIMUM_POSITION_VALUE-self.__DXL_MINIMUM_POSITION_VALUE)
    print("[ID:%03d]  GoalPos:%03d  PresPos:%03d  Value:%03f" % (self.__DXL_ID, self.__now_goal_position, dxl_present_position,present_position_value))
    
    return dxl_present_position,present_position_value
    
  def close_port(self):
    """ポートを閉じる
    """
    self.__portHandler.closePort()