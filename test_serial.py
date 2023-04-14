import serial
import time

try:
    
    ser = serial.Serial()
    ser.port = "/dev/ArduinoMega2"     #デバイスマネージャでArduinoのポート確認
    ser.baudrate = 115200 #Arduinoと合わせる
    ser.setDTR(False)     #DTRを常にLOWにしReset阻止
    ser.open()            #COMポートを開く
    
    while 1:
        ser.write(int(1))
        time.sleep(2) 
        ser.write(int(0))
        time.sleep(2) 

    ser.close()           #COMポートを閉じる

except KeyboardInterrupt:
    print("プログラムを終了します")
    ser.close()