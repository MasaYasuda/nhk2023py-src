import struct
import serial
ser=serial.Serial("/dev/ttyACM0",115200)



def write_single(motor_num):
    # 1Byte目は固定値0xFF
    # 2Byte目は1Byteデータ（数値）
    # 3~6Byte目はfloat型数値
    data = [0xFF,motor_num.to_bytes(1,"big"),500.0]
    print(data)
    print(len(data))
    packet = struct.pack('>Bcf', *data)
    ser.write(packet)
    print(packet)
    print(len(packet))
    return data

write_single(3)