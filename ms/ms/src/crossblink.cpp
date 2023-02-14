#include <Arduino.h>
#include <Wire.h>

const int motorCount = 6;
float motorSpeeds[motorCount];
int pinPWM[4] = {2, 3, 4, 5};

typedef union {
  float val;
  byte binary[4];
} uf;

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
        byte bytes[4];
        Serial.readBytes(bytes, 4);
        speed = *((float*)bytes); 

        motorSpeeds[motorNumber] = speed;
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
