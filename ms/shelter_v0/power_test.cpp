// THIS PROGRAM IS SUCCESSFULLY MOVED [23/02/15]

#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"
//　変数・オブジェクト宣言
Receiver receiver;
Power power;

void setup(){
  Serial.begin(115200);
}
void loop(){
  for(int i=0;i<3;i++){
    power_rate[i]=1;
  }

  power.output(power_rate);
  int *pwm=power.getOutput_pwm();
  for(int i=0;i<6;i++){
    Serial.println(pwm[i]);
  }
  delay(10000);
}