import pygame
import v1_dxl
import v1_nhk23
import time
import os



# joystick setup ---------------------------------
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
# ------------------------------------------------

# Dyamixel setup ---------------------------------
ID_RHAND=1
ID_LHAND=2
RHAND_LIMIT=[2500,3800]
LHAND_LIMIT=[500,1870]
Dxl=v1_dxl.Dynamixel("/dev/ttyUSB0",57600)
Dxl.set_mode_position(ID_RHAND)
Dxl.set_mode_position(ID_LHAND)
Dxl.set_min_max_position(ID_RHAND,RHAND_LIMIT[0],RHAND_LIMIT[1])
Dxl.set_min_max_position(ID_LHAND,LHAND_LIMIT[0],LHAND_LIMIT[0])
# トルクオン
Dxl.disable_torque(ID_RHAND)
Dxl.disable_torque(ID_LHAND)
# ------------------------------------------------
# ハンド開閉
dxl_r=Dxl.read_position(ID_RHAND)
dxl_l=Dxl.read_position(ID_LHAND)


while 1:
  print(str(Dxl.read_position(ID_RHAND))+","+str(Dxl.read_position(ID_LHAND)))

