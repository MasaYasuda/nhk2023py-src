import nhk23
import pygame
import time
import os

try:
    #########

    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print("コントローラのボタンを押してください")
    
    #########
    
    transmitter = nhk23.Transmitter("/dev/ttyACM0", 115200)
    mode_array=[0,0,100,100,100,100]
    direction_config_array =[0,0,0,0,0,0] #回転が逆だったら3にする
    forward_direction_array=[1,1,0,0,0,0]

    transmitter.write_config_all(mode_array,direction_config_array,forward_direction_array)
    
    emit_order=0
    while True:
        transmitter.reset_input_buffer()
        
        ## Get Inputs
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYHATMOTION: # 発射用ローラー 
                if (j.get_hat(0))[1]==1:
                    emit_order=emit_order+0.2
                    time.sleep(0.1)
                elif (j.get_hat(0))[1]==-1:
                    emit_order=emit_order-0.2
                    time.sleep(0.1)
                print()
            elif event.type == pygame.JOYBUTTONDOWN: # 引き込みローラー
                if j.get_button(0):
                    print("四角ボタンが押されました")
                    time.sleep(0.1)

        emit_order=max(0,min(emit_order,1))
        print(str(emit_order))

        transmitter.write_single_auto(0,emit_order*1)
        time.sleep(0.1)
        transmitter.write_single_auto(1,emit_order*1)
        time.sleep(0.1)

        # 引き込み用ローラー
        print()

        
except KeyboardInterrupt:
    print("プログラムを終了します")
    init_array=[0,0,0,0,0,0]
    transmitter.write_all_auto([0,1,2,3,4,5],init_array)
    j.quit()
    transmitter.close()
    

