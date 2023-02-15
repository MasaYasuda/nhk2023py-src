// Successfully Moved [23/2/15]

#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"
//　変数・オブジェクト宣言
Receiver receiver;
Power power;

void setup(){
  Serial.begin(115200);
  encoder_setup();
}
void loop(){

  for(int i=0;i<6;i++){
    Serial.print("NUM ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(count[i]);
  }
  delay(1000);
}