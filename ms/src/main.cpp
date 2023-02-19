#include <Arduino.h>
#include <Wire.h>
#include <TimerOne.h>
#include "classes.h"
// 関数

//　変数・オブジェクト宣言


Receiver receiver;
Power power;



void setup(){
  Serial.begin(115200);
  encoder_setup();
  /*
  
  timer_setup();
  */
}
void loop(){
  receiver.read_order();//->order_speed[6]
  power.output(power_rate);
  calc_speed_delay(2);
  calc_pid_speed_type();

  /*
  power.output(power_rate);
  Serial.print("OUTPUT:");
  Serial.println(power_rate[0]);

  Serial.print("Speed now:");
  Serial.println(speed_now[0]);
  delay(100);
  
  Serial.print("Speed [0]:");
  Serial.print(speed_now[0]);
  Serial.print("  Speed [1]:");
  Serial.prinln(speed_now[0]);

  Serial.print("COUNT:");
  Serial.println(count[0]);
  */

  
  delay(1);
}