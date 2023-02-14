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
      Serial.println(motorNumber);
      if (motorNumber >= 0 && motorNumber < motorCount) {
        float speed = 0;
        byte value0=Serial.read();
        byte value1=Serial.read();
        byte value2=Serial.read();
        byte value3=Serial.read();
        //speed = Serial.read() | (Serial.read() << 8) | (Serial.read() << 16) | (Serial.read() << 24);
        speed=float(value0|(value1<<8)|(value2<<16)|(value3<<24));
        Serial.println(value0);
        Serial.println(value0);
        Serial.println(value0);
        Serial.println(value0);
        Serial.println(speed);
        //motorSpeeds[motorNumber] = speed;
        Serial.print("Motor: ");
        Serial.print(motorNumber);
        Serial.print(", Speed: ");
        Serial.println(motorSpeeds[motorNumber]);
        /*
        if (abs(motorSpeeds[motorNumber]) > 1)
        {
          motorSpeeds[motorNumber] = 0;
        }
        int output_value = 240 * (motorSpeeds[motorNumber]);
        analogWrite(pinPWM[motorNumber], output_value);
        */
        int count=(int)(value);
        for(int i=0;i<count;i++){
            digitalWrite(13,HIGH);
            delay(200);
            digitalWrite(13,HIGH);
            delay(200);
        }
      }
    }
  }
}
