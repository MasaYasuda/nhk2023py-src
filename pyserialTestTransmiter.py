import serial
import struct

ser = serial.Serial('COM3', 9600)

while True:
  try:
    data = [0xFF, 100, 3.14159265]

    # 1Byte目は固定値0xFF
    # 2Byte目は1Byteデータ（数値）
    # 3~6Byte目はfloat型数値
    packet = struct.pack('>Bif', *data)
    ser.write(packet)
  except:
    ser.close()