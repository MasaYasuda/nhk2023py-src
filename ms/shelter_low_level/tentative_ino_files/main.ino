#include <Arduino.h>

// global変数宣言------------------
// 全般
int dt_ms = 20;
// Encoder
const int EncoderA[6] = {22, 23, 24, 25, 26, 27};
const int EncoderB[6] = {2, 3, 18, 19, 20, 21}; // ArduinoMegaMotrSlaveは物理的なピン配置上B相割込みとなっている
long ECNT[6] = {0};
long pastECNT[6] = {0}; // Speed_calcで使用
// OutPut
const int pinDIR[6] = {28, 29, 30, 31, 32, 33};
const int pinPWM[6] = {4, 5, 6, 7, 8, 9};
// PID
float Kp = 1;
float Ki = 0;
float Kd = 0;
float pastdev[6] = {0};
float integral[6] = {0};
int pwmpower[6] = {0};
// Serial
float order_rpm[6] = {0};
// Timer_calc
float now_rpm[6] = {0};

// 以上------------------------------------

void setup()
{
  Serial.begin(115200);
  encoderSetup();
  timerSetup();
}

void loop()
{
  if (Serial.available() >= 6)
  {
    orderRead();
  }
  mdOutput();
}