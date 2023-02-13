#include <Arduino.h>
#include <Wire.h>

const int motorCount = 6;
float motorSpeeds[motorCount];
int pinPWM[4] = {2, 3, 4, 5};
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
      if (motorNumber >= 0 && motorNumber < motorCount) {
        
        float speed = 0;
        speed = Serial.read() | (Serial.read() << 8) | (Serial.read() << 16) | (Serial.read() << 24);
        motorSpeeds[motorNumber] = speed;
        Serial.print("Motor: ");
        Serial.print(motorNumber);
        Serial.print(", Speed: ");
        Serial.println(motorSpeeds[motorNumber]);
        
        int output_value = 240 * (motorSpeeds[motorNumber]);
        analogWrite(pinPWM[motorNumber], output_value);
        
        
        
      }
    }
  }
}
