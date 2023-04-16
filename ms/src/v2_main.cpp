
#include <Arduino.h>
#include <v2_classes.h>
#include <_v2_controll_table.h>

void setup(){
  Serial.begin(115200);
  timer_setup();
  Serial.print("BEGIN\n");
}
void loop(){
  serial_receive();

  /*
  Serial.print(_output_pwm[0]);
  Serial.print(" ");
  Serial.println(_output_pwm[1]);
  
  Serial.print(_goal_velocity[0]);
  Serial.print(" ");
  Serial.println(_goal_velocity[1]);
  */
  check_sw(0);
  output();
  delay(10);
}