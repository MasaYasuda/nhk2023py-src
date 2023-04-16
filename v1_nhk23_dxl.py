"""Dynamixel操作用クラス
"""
import os

###### 触らない
if os.name == 'nt':
    import msvcrt
else:
    import sys, tty, termios
from dynamixel_sdk import * # Uses Dynamixel SDK library
###############

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

