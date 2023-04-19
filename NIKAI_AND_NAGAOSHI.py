import v1_nhk23
import pygame
import time
import os
try:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()

    time.sleep(2)

    print("コントローラのボタンを押してください")
    while True:
        st=time.time()
        while time.time()-st<1:
          ## Get Inputs
          events = pygame.event.get()
          if (j.get_hat(0)[1]==1):
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if (j.get_hat(0)[1]==0):
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if (j.get_hat(0)[1]==1):
                    print("DOUBLE TOUCH")
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
            
          if j.get_button(0)==1:
            tmp_index=0
            st2=time.time()
            while time.time()-st2<0.5:
              events = pygame.event.get()
              if j.get_button(0)==0:
                tmp_index=1
                break
            if tmp_index==0:
              print("STAY PRESS")
              time.sleep(0.1)
          
          if j.get_button(3)==1:
            print("SHIKAKU_TOUCH")
            st2=time.time()
            while time.time()-st2<0.3:
              events = pygame.event.get()
              if j.get_button(3)==0:
                st3=time.time()
                while time.time()-st3<0.3:
                  events = pygame.event.get()
                  if j.get_button(3)==1:
                    print("四角二回押し")
                    time.sleep(0.3)
                    break
                  time.sleep(0.05)
              time.sleep(0.05)
            time.sleep(0.05)
            
          time.sleep(0.01)
            
            
        print("OFF")
        



except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()
    




"""
CHANGE MODE <  > -> < 0 >
全出力無効
"""
if j.get_button(9)==1:
  print("OPTION BUTTON")
  OP_MODE=0
  Transmitter.reset_data_all()
  time.sleep(0.12)
  break
  
"""
CHANGE MODE <  > -> < 1 >
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
          time.sleep(0.3)
          break
        time.sleep(0.05)
    time.sleep(0.05)
  time.sleep(0.05)
  
  
"""
CHANGE MODE <  > -> < 2 >
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
          time.sleep(0.3)
          break
        time.sleep(0.05)
    time.sleep(0.05)
  time.sleep(0.05)


"""
CHANGE MODE <  > -> < 3 >
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
          time.sleep(0.3)
          break
        time.sleep(0.05)
    time.sleep(0.05)
  time.sleep(0.05)