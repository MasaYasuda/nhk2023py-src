# THIS IS FOR UBUNTU

import nhk23
import time
import os
import used_testfiles.kbhit as kbhit

kb=kbhit.KBHit()

try:    
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    dynamixel_1=nhk23.Dynamixel("/dev/ttyUSB0",57600 ,1,2500,3800)
    dynamixel_1.enable_torque()

    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        
        if kb.getch() == chr(0x1b):
            break
        dynamixel_1.write_position(0)
        time.sleep(3)
        dynamixel_1.read_position()
        print("Press any key to continue! (or press ESC to quit!)")
        if kb.getch() == chr(0x1b):
            break

        dynamixel_1.write_position(1)
        time.sleep(3)
        dynamixel_1.read_position()
    
    print("プログラムを終了します")
    dynamixel_1.close_port()

except KeyboardInterrupt:
    print("プログラムを終了します")
    dynamixel_1.close_port()


