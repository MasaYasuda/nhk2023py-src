#include <Arduino.h>

/*

const int pinDIR[6]={28,29,30,31,32,33};
const int pinPWM[6]={4,5,6,7,8,9};
*/

void mdOutput()
{
  for (int i = 0; i < 6; i++)
  {
    if (pwmpower[i] >= 0)
    {
      digitalWrite(pinDIR[i], LOW);
      analogWrite(pinPWM[i], pwmpower[i]);
    }
    else
    {
      digitalWrite(pinDIR[i], HIGH);
      analogWrite(pinPWM[i], abs(pwmpower[i]));
    }
  }
}