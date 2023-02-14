#include <Arduino.h>
#include <Wire.h>

const int motorCount = 6;
float motorSpeeds[motorCount];
int pinPWM[4] = {2, 3, 4, 5};
float bytesToFloat(byte *buffer) {
  float value;
  memcpy(&value, buffer, sizeof(value));
  return value;
}

void setup()
{
  Serial.begin(115200);
  for (int i = 0; i < motorCount; i++)
  {
    motorSpeeds[i] = 0;
  }
}

void loop()
{
  if (Serial.available() >= 6) {
    Serial.println("RECEIVED");
    byte header = Serial.read();
    if (header == 0xFF) {
      byte motorNumber = Serial.read();
      Serial.println(motorNumber);
      if (motorNumber >= 0 && motorNumber < motorCount) {
        float speed = 0;
        byte value0=Serial.read();
        byte value1=Serial.read();
        byte value2=Serial.read();
        byte value3=Serial.read();
        byte buffer[4]={value0,value1,value2,value3};
        float value=bytesToFloat(buffer);
        //speed = Serial.read() | (Serial.read() << 8) | (Serial.read() << 16) | (Serial.read() << 24);
        //speed=(float)(value3|((0x0000|value2)<<8) | ((0x000000 | value1 ) << 16)|((0x00000000|value0)<<24));
        Serial.println(value0);
        Serial.println(value1);
        Serial.println(value2);
        Serial.println(value3);
        //Serial.println(speed);
        Serial.println(value);

        //motorSpeeds[motorNumber] = speed;
        motorSpeeds[motorNumber] = value;
        Serial.print("Motor: ");
        Serial.print(motorNumber);
        Serial.print(", Speed: ");
        Serial.println(motorSpeeds[motorNumber]);

        int count=(int)(speed);
        for(int i=0;i<count;i++){
            digitalWrite(13,HIGH);
            delay(200);
            digitalWrite(13,HIGH);
            delay(200);
        }
        while (Serial.available())Serial.read();
      }
    }
  }
}
