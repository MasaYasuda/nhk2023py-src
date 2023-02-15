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
  receiver.read_order();//->order_speed[6]
  for(int i=0;i<6;i++){
    power_rate[i]=order_speed[i];
  }
  power.output(power_rate);
  int *pwm=power.getOutput_pwm();
  Serial.println(pwm[2]);
}