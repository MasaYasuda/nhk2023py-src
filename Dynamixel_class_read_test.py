import nhk23
import time
import os
import kbhit
kb=kbhit.KBHit()

try:    
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    dynamixel_1=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,1,2500,3800)

    while True:
        if kb.kbhit():
            break
        dynamixel_1.read_position()
    
    print("プログラムを終了します")
    dynamixel_1.close_port()

except KeyboardInterrupt:
    print("プログラムを終了します")
    dynamixel_1.close_port()


