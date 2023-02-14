#include <Arduino.h>
#include <Wire.h>

const int motorCount = 6;
float motorSpeeds[motorCount];
int pinPWM[4] = {2, 3, 4, 5};

typedef union {
  float val;
  byte binary[4];
} uf;

typedef union {
    byte b[4];
    float f;
  } FloatByteUnion;

  float bytesToFloat(byte *buffer) {
    FloatByteUnion value;
    for (int i = 0; i < 4; i++) {
      value.b[i] = buffer[i];
    }
    return value.f;
  }

void setup()
{
  Serial.begin(115200);
  byte buffer[4]={0b00000000,0b00000000,0b10000000,0b00111111};
  float value=bytesToFloat(buffer);
  Serial.println(value);
}

void loop()
{
}
