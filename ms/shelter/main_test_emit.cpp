#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"

//　変数・オブジェクト宣言
Receiver receiver;
Power power;

void setup(){
  Serial.begin(115200);
  
  encoder_setup();
  /*
  encoder_setup();
  timer_setup();
  */
}
void loop(){
  receiver.read_order();//->order_speed[6]
  power.output(power_rate);
  /*
  calc_speed_delay(2);
  calc_ff_pid_speed_type();
  
  */
  
  Serial.print(" OUTPUT[0]:");
  Serial.println(power_rate[0]);

  delay(10);
}

  /*
  
  calc_speed_delay(4);
  calc_ff_pid_speed_type();

  power.output(power_rate);
  Serial.print("OUTPUT:");
  Serial.println(power_rate[0]);

  Serial.print("Speed now:");
  Serial.println(speed_now[0]);
  delay(100);
  

  Serial.print("OUTPUT [0]:");
  Serial.print(power_rate[0]);
  Serial.print("  OUTPUT [1]:");
  Serial.print(power_rate[1]);
  Serial.print("  OUTPUT [2]:");
  Serial.print(power_rate[2]);
  Serial.print("  OUTPUT [3]:");
  Serial.println(power_rate[3]);

  */