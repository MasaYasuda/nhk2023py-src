import pygame
import time
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print("コントローラのボタンを押してください")
try:
    while True:
        pygame.event.get() #戻り値を変数に格納しなくともJoystickメソッドを使う前に実行する必要。
        if j.get_button(0):
            print("四角ボタンが押されました")
            time.sleep(0.1)
        else:
            print("四角ボタンは押されていません")

except KeyboardInterrupt:
    print("プログラムを終了します")
    j.quit()