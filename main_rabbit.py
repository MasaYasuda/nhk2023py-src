"""自動射出のプログラム
昇降（上昇）→ローラー加速→引き込み→上昇の繰り返し
"""

import v1_nhk23
import pygame
import v1_nhk23_dxl
import time
import os

try:
    """ MEMOS
    [引込み、昇降、発射上、発射下,右足回り、左足回り]
    Arduino.../dev/ArduinoMega1
    分解度 [any,any,256,256,512,512]
    FFPIDgain:
      any,
      any,
      {0.032,0,0.0003,0},
      {0.022,0,0.0003,0},
      {0,0,0.01,0},
      {0,0,0.01,0}
    Integral Limit:
      any,
      any,
      500000,
      500000,
      100000,
      100000
    PWM all MAX=240
    """
    # joystick setup ---------------------------------
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    # ------------------------------------------------
    
    # Dyamixel setup ---------------------------------
    # トルクオン
    # ------------------------------------------------
    
    # Arduino (rappini Roller,Diff) setup ------------
    roller=v1_nhk23.SingleDrive(100,10,2.77)
    Diff=v1_nhk23.OmniDrive(127,254,0.4,30,28)
    # [引込み、昇降、発射上、発射下,右足回り、左足回り]
    mode=[100,100,20,20,20,20]
    dir=[0,0,2,1,3,1]
    lev=[1,1,1,1,1,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    # ------------------------------------------------
    
    # var --------------------------------------------
    OP_MODE=0
    # ------------------------------------------------
    
    # OP_MODE < 0 > ----------------------------------
    while OP_MODE==0:
      print("-----------------------------------")
      print("          OP_MODE < 0 > ")
      print("-----------------------------------")
      """ MEMO
      while : 
        Arduino全出力無効(RESET)
        
      ※ Dynamixelトルクはそのまま
      
      Change Mode 0 -> 1
        予約なし
      Change Mode 0 -> 2,3 
        不可
      
      """
      # Arduino全出力無効
      
      # CHANGE MODE < 0 > -> < 1 >
      
      # CHANGE MODE < 0 > -> < 3 >
      
      
    # ------------------------------------------------
    
    # OP_MODE < 1 > ----------------------------------
    while OP_MODE==1:
      print("-----------------------------------")
      print("          OP_MODE < 1 > ")
      print("-----------------------------------")
      """ MEMO
      while 1:
        タイヤ速度送信
      
      Change Mode 1 -> 0
        
      Change Mode 1-> 2 
        
      Change Mode 1-> 3 
        不可
      
      """
      
    # ------------------------------------------------
    
    # OP_MODE < 2 > ----------------------------------
    while OP_MODE==2:
      print("-----------------------------------")
      print("          OP_MODE < 2 > ")
      print("-----------------------------------")
    # ------------------------------------------------
    
    # OP_MODE < 3 > ----------------------------------
    while OP_MODE==3:
      print("-----------------------------------")
      print("          OP_MODE < 3 > ")
      print("-----------------------------------")
      
    # ------------------------------------------------
    

except KeyboardInterrupt:
    print("プログラムを終了します")
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()
    

