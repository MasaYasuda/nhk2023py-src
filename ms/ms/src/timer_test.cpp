//

#include <Arduino.h>
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

  for(int i=0;i<6;i++){
    Serial.print("Speed ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(speed_now[i]);
  }
  delay(1000);
}