import nhk23
import time
import os
try:    
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    dynamixel_1=nhk23.Dynamixel("COM3",115200,1,2500,3800)
    dynamixel_1.enable_torque()

    while True:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break
        dynamixel_1.write_position(0)
        time.sleep(0.01)
        
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break
        dynamixel_1.write_position(1)
        time.sleep(0.01)
    
    print("プログラムを終了します")
    dynamixel_1.close_port()

except KeyboardInterrupt:
    print("プログラムを終了します")
    dynamixel_1.close_port()


