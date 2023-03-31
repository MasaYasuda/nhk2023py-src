import serial
import time
ser=serial.Serial("/dev/ArduinoMega1", 115200)

while True:
  bun=ser.readline()
  print(bun)
  time.sleep(0.01)