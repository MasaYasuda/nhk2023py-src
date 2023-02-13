import serial
import struct
import time
ser=serial.Serial("COM4", 115200)
value=float(0.0)
while True:
    
    
    data = [0xFF, value]
    packet = struct.pack('>Bf', *data)
    ser.write(packet)
    print(data)
    print(str(packet))

    value=value+1.0
    if value>3:
        value=0.0
    time.sleep(1.5)