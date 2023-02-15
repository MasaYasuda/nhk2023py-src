import serial
 
 
ser = serial.Serial("COM11", 9600)
print(ser.name)
 
ser.write(b'I am Miura')
 
ser.close()
