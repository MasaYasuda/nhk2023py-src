import nhk23
import time
import os
import used_testfiles.kbhit as kbhit
kb=kbhit.KBHit()

try:    
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    dynamixel_1=nhk23.Dynamixel("/dev/link-PORT7",57600 ,1,2500,3800)
    dynamixel_2=nhk23.Dynamixel("/dev/link-PORT7",57600 ,2,500,1870)

    while True:
        if kb.kbhit():
            break
        dynamixel_1.read_position()
        dynamixel_2.read_position()


        time.sleep(0.5)
    
    print("プログラムを終了します")
    dynamixel_1.close_port()
    dynamixel_2.close_port()

except KeyboardInterrupt:
    print("プログラムを終了します")
    dynamixel_1.close_port()
    dynamixel_2.close_port()


