#include <Arduino.h>
#include "classes.h"

//　変数・オブジェクト宣言
Receiver receiver;
Power power;

void setup(){
  Serial.begin(115200);
  encoder_setup();
  timer_setup();
  /*
  
  
  */
}
void loop(){
  receiver.read_order();//->order_speed[6]
  power.output(power_rate);
  Serial.println("HelloWorld");
  delay(20);
}
  /*
  
  calc_speed_delay(4);
  calc_ff_pid_speed_type();

  power.output(power_rate);
  Serial.print("OUTPUT:");
  Serial.println(power_rate[0]);

  Serial.print("Speed [0]:");
  Serial.println(speed_now[0]);
  Serial.print("Speed [1]:");
  Serial.println(speed_now[1]);
  Serial.print("Speed [2]:");
  Serial.println(speed_now[2]);
  Serial.print("Speed [3]:");
  Serial.println(speed_now[3]);
  
  
  delay(100);
  

  Serial.print("OUTPUT [0]:");
  Serial.print(power_rate[0]);
  Serial.print("  OUTPUT [1]:");
  Serial.print(power_rate[1]);
  Serial.print("  OUTPUT [2]:");
  Serial.print(power_rate[2]);
  Serial.print("  OUTPUT [3]:");
  Serial.println(power_rate[3]);



  
  Serial.print("Speed [0]:");
  Serial.print(speed_now[0]);
  Serial.print("  Speed [1]:");
  Serial.print(speed_now[1]);
  Serial.print("  Speed [2]:");
  Serial.print(speed_now[2]);
  Serial.print("  Speed [3]:");
  Serial.println(speed_now[3]);
  
  Serial.print("OUTPUT [0]:");
  Serial.print(power_rate[0]);
  Serial.print("  OUTPUT [1]:");
  Serial.print(power_rate[1]);
  Serial.print("  OUTPUT [2]:");
  Serial.print(power_rate[2]);
  Serial.print("  OUTPUT [3]:");
  Serial.println(power_rate[3]);
  Serial.println("");
  */