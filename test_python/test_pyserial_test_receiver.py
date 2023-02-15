import struct
import serial

ser = serial.Serial("COM3", 9600)
while True:
    try:
      data = ser.read(6)
      if data[0] == b'\xff':
          num1 = data[1]
          num2 = struct.unpack('f', data[2:6])[0]
          print(num1, num2)
    except:
      ser.close()