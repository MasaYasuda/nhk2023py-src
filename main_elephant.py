"""自動射出のプログラム
昇降（上昇）→ローラー加速→引き込み→上昇の繰り返し



"""

import v1_nhk23
import pygame
import v1_dxl
import time
import os

try:
    """ MEMOS
    [引込み、昇降、発射上、発射下,右足回り、左足回り]
    
    Mega4:[右前足、左前足、左後足、右後足、]
    Mega5:
    mode=[100,100,20,20,20,20]
    dir=[0,0,2,1,3,1]
    lev=[1,1,1,1,1,1]
    Arduino.../dev/ArduinoMega1
    分解度 [any,any,256,256,512,512]
    FFPIDgain:
      any,any,{0.032,0,0.0003,0},{0.022,0,0.0003,0},{0,0,0.01,0},{0,0,0.01,0}
    Integral Limit:
      any,any,500000,500000,100000,100000
    PWM all MAX=240
    """
    # ANYTHING ELSE --------------------------------------------
    P_DRAWIN=0
    P_LIFT=1
    P_ROLLER1=2
    P_ROLLER2=3
    P_RWHEEL=4
    P_LWHEEL=5
    ID_RHAND=1
    ID_LHAND=2
    RHAND_LIMIT=[2500,3800]
    LHAND_LIMIT=[500,1870]
    
    OP_MODE=0
    RING_NUM=10 #最初の数
    RING_COUNT=10 #現在の数（※　RINGCNUMと同じ値にする。）
    
    dxl_r=0
    dxl_l=0
    
    
    # ------------------------------------------------

    # joystick setup ---------------------------------
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    # ------------------------------------------------
    
    # Dyamixel setup ---------------------------------
    Dxl=v1_dxl.Dynamixel("/dev/ttyUSB0",57600)
    Dxl.set_mode_position(ID_RHAND)
    Dxl.set_mode_position(ID_LHAND)
    Dxl.set_min_max_position(ID_RHAND,RHAND_LIMIT[0],RHAND_LIMIT[1])
    Dxl.set_min_max_position(ID_LHAND,LHAND_LIMIT[0],LHAND_LIMIT[1])
    # トルクオン
    Dxl.enable_torque(ID_RHAND)
    Dxl.enable_torque(ID_LHAND)
    # ------------------------------------------------
    
    # Arduino (rappini Roller,Diff) setup ------------
    Roller=v1_nhk23.SingleDrive(100,3,2.77)
    Diff=v1_nhk23.DiffDrive(127,254,0.4,30,28)
    mode=[0,0,0,0,0,0]
    dir=[0,0,2,1,3,1]
    lev=[0,1,0,0,0,1]
    Transmitter=v1_nhk23.Transmitter("/dev/ArduinoMega2",115200,mode,dir,lev)
    # ------------------------------------------------
    
    
    Transmitter.reset_input_buffer()
    while 1:
      # OP_MODE < 0 > ----------------------------------
      while OP_MODE==0:
        print("-----------------------------------")
        print("          OP_MODE < 0 > ")
        print("-----------------------------------")
        
        # Arduino全出力無効
        Transmitter.reset_data_all()
        
        # 高速送信======(この外は遅い送信)
        st=time.time()
        while time.time()-st<1:
          ## Get Inputs
          events = pygame.event.get()
          
          """
          CHANGE MODE < 0 > -> < 1 >
          足回り起動
          """
          if j.get_button(3)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(3)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(3)==1:
                    print("四角二回押し")
                    OP_MODE=1
                    time.sleep(2)
                    Transmitter.reset_data_single(P_RWHEEL,20) 
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.3)
                    Transmitter.reset_data_single(P_RWHEEL,20) 
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
            
          """
          CHANGE MODE < 0 > -> < 2 >
          昇降起動
          """
          if j.get_button(2)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(2)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(2)==1:
                    print("三角二回押し")
                    OP_MODE=2
                    Transmitter.reset_data_single(P_LIFT,100)

                    dxl_r=Dxl.read_position(ID_RHAND)
                    dxl_l=Dxl.read_position(ID_LHAND)
                    time.sleep(0.5)
                    Transmitter.reset_data_single(P_LIFT,100)

                    dxl_r=Dxl.read_position(ID_RHAND)
                    dxl_l=Dxl.read_position(ID_LHAND)
                    time.sleep(0.5)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
            
          """
          CHANGE MODE < 0 > -> < 3 >
          引込、昇降、ローラー、足回り起動＆ローラー回転開始
          """
          if j.get_button(1)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(1)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(1)==1:
                    print("丸二回押し")
                    
                    OP_MODE=3
                    Transmitter.reset_data_single(P_DRAWIN,100)
                    Transmitter.reset_data_single(P_LIFT,100)
                    Transmitter.reset_data_single(P_ROLLER1,20)
                    Transmitter.reset_data_single(P_ROLLER2,20)
                    Transmitter.reset_data_single(P_RWHEEL,20)
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.12)
                    Transmitter.reset_data_single(P_DRAWIN,100)
                    Transmitter.reset_data_single(P_LIFT,100)
                    Transmitter.reset_data_single(P_ROLLER1,20)
                    Transmitter.reset_data_single(P_ROLLER2,20)
                    Transmitter.reset_data_single(P_RWHEEL,20)
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.12)
                    
                    # ローラー回転開始
                    speed=Roller.calc_speed(0.7) 
                    Transmitter.write_motor_single(P_ROLLER1,speed)
                    Transmitter.write_motor_single(P_ROLLER2,speed)
                    speed=Roller.calc_speed(0.7) 
                    Transmitter.write_motor_single(P_ROLLER1,speed)
                    Transmitter.write_motor_single(P_ROLLER2,speed)
                    
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
          time.sleep(0.01)
        Transmitter.reset_input_buffer()
          
      # ------------------------------------------------
      
      
      # OP_MODE < 1 > ----------------------------------
      while OP_MODE==1:
        print("-----------------------------------")
        print("          OP_MODE < 1 > ")
        print("-----------------------------------")
          
        # 移動出力　ジョイスティックRL (R1,L1同時押し中で微調整モード)
        events = pygame.event.get()
        
        move=v1_nhk23.joy_threshold(j.get_axis(1)*(-1)*(1.0),0.2)
        rot=v1_nhk23.joy_threshold(j.get_axis(3)*(1),0.2)
        if j.get_button(4)==1 and j.get_button(5)==1 :
          move=move/2
          rot=rot/2
        R_speed,L_speed=Diff.calc_speed(move,rot)
        Transmitter.write_motor_single(P_RWHEEL,R_speed)
        Transmitter.write_motor_single(P_LWHEEL,L_speed)
        
        # 高速送信======(この外は遅い送信)
        st=time.time()
        while time.time()-st<0.1:
          ## Get Inputs
          events = pygame.event.get()
                  
          """
          CHANGE MODE < 1 > -> < 0 >
          全出力無効
          """
          if j.get_button(9)==1:
            print("OPTION BUTTON")
            OP_MODE=0
            Transmitter.reset_data_all()
            time.sleep(0.12)
            break
            
            
          """
          CHANGE MODE < 1 > -> < 2 > 
          移動無効、昇降有効
          """
          if j.get_button(2)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(2)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(2)==1:
                    print("三角二回押し")
                    OP_MODE=2
                    Transmitter.reset_data_single(P_RWHEEL,0)
                    Transmitter.reset_data_single(P_LWHEEL,0)
                    Transmitter.reset_data_single(P_LIFT,100)
                    Transmitter.reset_data_single(P_RWHEEL,0)
                    Transmitter.reset_data_single(P_LWHEEL,0)
                    Transmitter.reset_data_single(P_LIFT,100)

                    dxl_r=Dxl.read_position(ID_RHAND)
                    dxl_l=Dxl.read_position(ID_LHAND)
                    time.sleep(0.3)
                    dxl_r=Dxl.read_position(ID_RHAND)
                    dxl_l=Dxl.read_position(ID_LHAND)
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)


          """
          CHANGE MODE < 1 > -> < 3 >
          引込、昇降、ローラー有効＆ローラー加速
          """
          if j.get_button(1)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(1)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(1)==1:
                    print("丸二回押し")
                    OP_MODE=3
                    Transmitter.reset_data_single(P_DRAWIN,100)
                    Transmitter.reset_data_single(P_LIFT,100)
                    Transmitter.reset_data_single(P_ROLLER1,20)
                    Transmitter.reset_data_single(P_ROLLER2,20)
                    time.sleep(0.12)
                    Transmitter.reset_data_single(P_DRAWIN,100)
                    Transmitter.reset_data_single(P_LIFT,100)
                    Transmitter.reset_data_single(P_ROLLER1,20)
                    Transmitter.reset_data_single(P_ROLLER2,20)
                    time.sleep(0.12)
                    
                    # ローラー回転開始
                    speed=Roller.calc_speed(0.7) 
                    Transmitter.write_motor_single(P_ROLLER1,speed)
                    Transmitter.write_motor_single(P_ROLLER2,speed)
                    time.sleep(0.3)
                    Transmitter.write_motor_single(P_ROLLER1,speed)
                    Transmitter.write_motor_single(P_ROLLER2,speed)
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
          time.sleep(0.01)
        Transmitter.reset_input_buffer()
        
      # ------------------------------------------------
      
      
      # OP_MODE < 2 > ----------------------------------
      while OP_MODE==2:
        print("-----------------------------------")
        print("          OP_MODE < 2 > ")
        print("-----------------------------------")
        
        # ハンド送信　ジョイスティックRL
        events = pygame.event.get()
        # 昇降　十字上下
        Transmitter.write_motor_single(P_LIFT,(j.get_hat(0))[1]*(-1)*0.5)
        
        # ハンド開閉
        tmp_r=(v1_nhk23.joy_threshold(j.get_axis(3)*(1),0.2))*50
        tmp_l=(v1_nhk23.joy_threshold(j.get_axis(0)*(1),0.2))*50
        if j.get_button(4)==1 and j.get_button(5)==1 :
          tmp_r=tmp_r/2
          tmp_l=tmp_l/2
        dxl_r=int(max(RHAND_LIMIT[0],min(RHAND_LIMIT[1],dxl_r+tmp_r)) )
        dxl_l=int(max(LHAND_LIMIT[0],min(LHAND_LIMIT[1],dxl_l+tmp_l)) )
        Dxl.write_position(ID_RHAND,dxl_r)
        time.sleep(0.02)
        Dxl.write_position(ID_LHAND,dxl_l)

        # 高速送信======(この外は遅い送信)
        st=time.time()
        while time.time()-st<0.05:
          ## Get Inputs
          events = pygame.event.get()
          """
          CHANGE MODE < 2 > -> < 0 >
          全出力無効
          """
          if j.get_button(9)==1:
            print("OPTION BUTTON")
            OP_MODE=0
            Transmitter.reset_data_all()
            time.sleep(0.12)
            break
            
          """
          CHANGE MODE < 2 > -> < 1 >
          昇降無効、移動有効
          """
          if j.get_button(3)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(3)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(3)==1:
                    print("四角二回押し")
                    OP_MODE=1
                    Transmitter.reset_data_single(P_LIFT,0)
                    Transmitter.reset_data_single(P_RWHEEL,20)
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.3)
                    Transmitter.reset_data_single(P_LIFT,0)
                    Transmitter.reset_data_single(P_RWHEEL,20)
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
            
          """
          CHANGE MODE < 2 > -> < 3 >
          引込、ローラー、移動有効＆ローラー加速
          """
          if j.get_button(1)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(1)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(1)==1:
                    print("丸二回押し")
                    OP_MODE=3
                    Transmitter.reset_data_single(P_DRAWIN,100)
                    Transmitter.reset_data_single(P_ROLLER1,20)
                    Transmitter.reset_data_single(P_ROLLER2,20)
                    Transmitter.reset_data_single(P_RWHEEL,20)
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.12)
                    Transmitter.reset_data_single(P_DRAWIN,100)
                    Transmitter.reset_data_single(P_ROLLER1,20)
                    Transmitter.reset_data_single(P_ROLLER2,20)
                    Transmitter.reset_data_single(P_RWHEEL,20)
                    Transmitter.reset_data_single(P_LWHEEL,20)
                    time.sleep(0.12)
                    # ローラー回転開始
                    speed=Roller.calc_speed(0.7) 
                    Transmitter.write_motor_single(P_ROLLER1,speed)
                    Transmitter.write_motor_single(P_ROLLER2,speed)
                    time.sleep(0.06)
                    Transmitter.write_motor_single(P_ROLLER1,speed)
                    Transmitter.write_motor_single(P_ROLLER2,speed)
                    time.sleep(0.06)
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
          time.sleep(0.01)
            
        Transmitter.reset_input_buffer()
      # ------------------------------------------------
      
      
      
      # OP_MODE < 3 > ----------------------------------
      while OP_MODE==3:
        print("-----------------------------------")
        print("          OP_MODE < 3 > ")
        print("-----------------------------------")
        
        # 向き調整(移動)　(R1,L1同時押し中で微調整モード)
        events = pygame.event.get()
        
        move=v1_nhk23.joy_threshold(j.get_axis(1)*(-1)*(0.5),0.1)
        rot=v1_nhk23.joy_threshold(j.get_axis(3)*(0.5),0.1)
        if j.get_button(4)==1 and j.get_button(5)==1 :
          move=move/2
          rot=rot/2
        R_speed,L_speed=Diff.calc_speed(move,rot)
        Transmitter.write_motor_single(P_RWHEEL,R_speed)
        Transmitter.write_motor_single(P_LWHEEL,L_speed)
        
        
        # 高速送信======(この外は遅い送信)
        st=time.time()
        while time.time()-st<0.1:
          # Get Input
          events = pygame.event.get()   
            
          """
          CHANGE MODE < 3 > -> < 0 >
          全出力無効
          """
          if j.get_button(9)==1:
            print("OPTION BUTTON")
            OP_MODE=0
            Transmitter.reset_data_all()
            time.sleep(0.12)
            break
            
          """
          CHANGE MODE < 3 > -> < 1 >
          引込、昇降、ローラー無効＆ローラー回転停止
          """
          if j.get_button(3)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(3)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(3)==1:
                    print("四角二回押し")
                    OP_MODE=1
                    Transmitter.write_motor_single(P_ROLLER1,0)
                    Transmitter.write_motor_single(P_ROLLER2,0)
                    Transmitter.reset_data_single(P_DRAWIN,0)
                    Transmitter.reset_data_single(P_LIFT,0)
                    time.sleep(0.3)
                    Transmitter.write_motor_single(P_ROLLER1,0)
                    Transmitter.write_motor_single(P_ROLLER2,0)
                    Transmitter.reset_data_single(P_DRAWIN,0)
                    Transmitter.reset_data_single(P_LIFT,0)
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
            
            
          """
          CHANGE MODE < 3 > -> < 2 >
          引込、ローラー、足回り無効＆ローラー回転停止
          """
          if j.get_button(2)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(2)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(2)==1:
                    print("三角二回押し")
                    OP_MODE=2
                    Transmitter.write_motor_single(P_ROLLER1,0)
                    Transmitter.write_motor_single(P_ROLLER2,0)
                    Transmitter.reset_data_single(P_DRAWIN,0)
                    Transmitter.reset_data_single(P_RWHEEL,0)
                    Transmitter.reset_data_single(P_LWHEEL,0)
                    time.sleep(0.3)
                    
                    Transmitter.write_motor_single(P_ROLLER1,0)
                    Transmitter.write_motor_single(P_ROLLER2,0)
                    Transmitter.reset_data_single(P_DRAWIN,0)
                    Transmitter.reset_data_single(P_RWHEEL,0)
                    Transmitter.reset_data_single(P_LWHEEL,0)
                    time.sleep(0.3)
                    Dxl.enable_torque(ID_RHAND)
                    Dxl.enable_torque(ID_LHAND)
                    dxl_r=Dxl.read_position(ID_RHAND)
                    dxl_l=Dxl.read_position(ID_LHAND)
                    time.sleep(0.1)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
          
          
          """
          自動上昇 十字上２回押し
          """
          if (j.get_hat(0))[1]==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if (j.get_hat(0)[1]==0):
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if (j.get_hat(0)[1]==1):
                    print("HAT DOUBLE TOUCH")
                    Transmitter.write_motor_single(P_LIFT,-1)
                    Transmitter.write_motor_single(P_LIFT,-1)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)

          """"
          自動上昇停止
          """
          if (j.get_hat(0))[1]==-1:
            print("HAT UNDER")
            Transmitter.write_motor_single(P_LIFT,0)
            Transmitter.write_motor_single(P_LIFT,0)
            Transmitter.write_motor_single(P_LIFT,0)
            time.sleep(0.2)
            
          
          """
          xボタン 二回押し発射
          """
          if j.get_button(0)==1:
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(0)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if (j.get_button(0)==1):
                    print("×ボタン二回押し")
                    if RING_COUNT>0:
                      
                      if RING_COUNT==RING_NUM:
                        #ラッピニ戻し
                        st=time.time()
                        while time.time()-st<1:
                          Transmitter.reset_input_buffer()
                          Transmitter.write_motor_single(P_DRAWIN,-0.75)
                          time.sleep(0.1)
                        
                      
                      #ラッピニ引き込み
                      st=time.time()
                      while time.time()-st<2:
                        Transmitter.reset_input_buffer()
                        Transmitter.write_motor_single(P_DRAWIN,0.75)
                        time.sleep(0.1)
                        
                      #ラッピニ戻し
                      st=time.time()
                      while time.time()-st<1:
                        Transmitter.reset_input_buffer()
                        Transmitter.write_motor_single(P_DRAWIN,-0.75)
                        time.sleep(0.1)
                        
                      RING_COUNT=RING_COUNT-1
                      
                      if RING_COUNT>0:
                        #上昇
                        st=time.time()
                        while time.time()-st<1:
                          Transmitter.reset_input_buffer()
                          Transmitter.write_motor_single(P_LIFT,-1)
                          time.sleep(0.1)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
          
          time.sleep(0.01)          
        Transmitter.reset_input_buffer()
    # ------------------------------------------------


except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    
    Transmitter.reset_data_all()
    Transmitter.reset_data_all()
    time.sleep(1)
    Transmitter.close()

    Dxl.disable_torque(ID_RHAND)
    Dxl.disable_torque(ID_LHAND)
    time.sleep(0.3)
    Dxl.close_port()

