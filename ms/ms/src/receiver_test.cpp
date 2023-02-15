#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"
//　変数・オブジェクト宣言

Receiver receiver;
Power power;
void setup(){
  Serial.begin(115200);
  pinMode(13,OUTPUT);
}
void loop(){
  receiver.read_order();//->order_speed[6]
  int count=(int)(order_speed[5]);
  for(int i=0;i<count;i++){
      digitalWrite(13,HIGH);
      delay(200);
      digitalWrite(13,LOW);
      delay(200);
  }
}