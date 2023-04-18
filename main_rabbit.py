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
    mode=[100,100,20,20,20,20]
    dir=[0,0,2,1,3,1]
    lev=[1,1,1,1,1,1]
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
    mode=[0,0,0,0,0,0]
    dir=[0,0,2,1,3,1]
    lev=[1,1,1,1,1,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega1",115200,mode,dir,lev)
    # ------------------------------------------------
    
    # ANYTHING ELSE --------------------------------------------
    OP_MODE=0
    Transmitter.reset_input_buffer()
    # ------------------------------------------------
    
    # OP_MODE < 0 > ----------------------------------
    while OP_MODE==0:
      print("-----------------------------------")
      print("          OP_MODE < 0 > ")
      print("-----------------------------------")
      
      # Arduino全出力無効
      Transmitter.reset_data_all()
      # 高速送信======(この外は遅い送信)
      st=time.time()
      while time.time()-st<0.1:
        Transmitter.reset_input_buffer()
        Transmitter.write_motor_single(2,0.25)
        time.sleep(0.1)
      # CHANGE MODE < 0 > -> < 1 >
      if 1:
        OP_MODE=1
        Transmitter.reset_data_single(4,20)
        Transmitter.reset_data_single(5,20)
        time.sleep(0.05)
      # CHANGE MODE < 0 > -> < 2 >
      if 2:
        OP_MODE=2
        Transmitter.reset_data_single(1,100)
        time.sleep(0.02)
      # CHANGE MODE < 0 > -> < 3 >
      if 3:
        OP_MODE=3
        Transmitter.reset_data_single(0,100)
        Transmitter.reset_data_single(1,100)
        Transmitter.reset_data_single(2,20)
        Transmitter.reset_data_single(3,20)
        Transmitter.reset_data_single(2,20)
        Transmitter.reset_data_single(3,20)
        time.sleep(0.12)
        # MAX上昇
        Transmitter.write_motor_single(1,-1) 
        # ローラー回転開始
        speed=roller.calc_speed(0.7) 
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(3,speed)
        time.sleep(0.06)
      
      Transmitter.reset_input_buffer()
        
    # ------------------------------------------------
    
    # OP_MODE < 1 > ----------------------------------
    while OP_MODE==1:
      print("-----------------------------------")
      print("          OP_MODE < 1 > ")
      print("-----------------------------------")
        
      ## Get Inputs
      events = pygame.event.get()
      
      ##### VECTOR CALCLATION
      
      move=v1_nhk23.joy_threshold(j.get_axis(1)*(-1)*(1.0),0.4)
      rot=v1_nhk23.joy_threshold(j.get_axis(3)*(1),0.4)
      
      R_value,L_value=diffdrive.calc_speed(move,rot)
      
      R_speed,L_speed=Diff.calc_speed()
      
      # CHANGE MODE < 0 > -> < 1 >
      if 1:
        Transmitter.reset_data_single(4,20)
        Transmitter.reset_data_single(5,20)
        time.sleep(0.05)
      # CHANGE MODE < 0 > -> < 2 >
      if 2:
        Transmitter.reset_data_single(1,100)
        time.sleep(0.02)
      # CHANGE MODE < 0 > -> < 3 >
      if 3:
        Transmitter.reset_data_single(0,100)
        Transmitter.reset_data_single(1,100)
        Transmitter.reset_data_single(2,20)
        Transmitter.reset_data_single(3,20)
        Transmitter.reset_data_single(2,20)
        Transmitter.reset_data_single(3,20)
        time.sleep(0.12)
        # MAX上昇
        Transmitter.write_motor_single(1,-1) 
        # ローラー回転開始
        speed=roller.calc_speed(0.7) 
        Transmitter.write_motor_single(2,speed)
        Transmitter.write_motor_single(3,speed)
        time.sleep(0.06)
        
        Transmitter.reset_input_buffer()
      
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
    

