#include <Arduino.h>
#include <Wire.h>
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
  float strength=order_speed[5];
  analogWrite(4,int(240*strength));
}