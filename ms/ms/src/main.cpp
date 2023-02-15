#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"
float i=0.0;
//　変数・オブジェクト宣言
Power power;
void setup(){
  Serial.begin(115200);
}
void loop(){

  power_rate[2]=i;
  power.output(power_rate);
  int *pwm=power.getOutput_pwm();
  Serial.println(pwm[2]);
  delay(100);
  i+=i+0.01;
  if(i>1){i=0;}
}