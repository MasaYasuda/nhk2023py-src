////Successfully Moved [23/2/15]

#include <Arduino.h>
#include <TimerOne.h>
#include <Wire.h>
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
  float orsp[6]={10.0};
  memcpy(order_speed,orsp,6);
  Serial.print("Speed ");
  Serial.print(0);
  Serial.print(": ");
  Serial.println(speed_now[0]);
  
  Serial.print("pid ");
  Serial.print(0);
  Serial.print(": ");
  Serial.println(power_rate[0]);

  delay(1000);
}

