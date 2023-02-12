#include <Arduino.h>
#include <TimerOne.h> 

/*

#include <TimerOne.h>

float now_rpm[6]={0};

*/

void speedCalc()
{
  for (int i = 0; i < 6; i++)
  {
    int dev = ECNT[i] - pastECNT[i];
    now_rpm[i] = dev / dt_ms * 60 * 1000;
    pastECNT[i] = ECNT[i];
  }
}

void timerSetup()
{
  Timer1.initialize(20000); // 20msごとに割込み
  Timer1.attachInterrupt(timerCalc);
}

void timerCalc()
{
  speedCalc();
  pidCalc();
}

//
