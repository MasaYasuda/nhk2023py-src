#include <Arduino.h>
#include <Wire.h>
#include <TimerOne.h>
#include "classes.h"
//　変数・オブジェクト宣言
Receiver receiver;
Power power;

void setup(){
  Serial.begin(115200);
  encoder_setup();
  timer_setup();
}
void loop(){
  receiver.read_order();//->order_speed[6]
  power.output(power_rate);
  Serial.println(power_rate[0]);
  delay(100);
}