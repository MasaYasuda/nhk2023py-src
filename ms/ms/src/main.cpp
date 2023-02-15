#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"

//　変数・オブジェクト宣言
Receiver receiver(115200);
Power power;
void setup(){
  encoder_setup();
  timer_setup();
}
void loop(){
  receiver.read_order();
  power.output(power_rate);
}