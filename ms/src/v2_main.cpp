
#include <Arduino.h>
#include <v2_classes.h>
#include <_v2_controll_table.h>

void setup(){
  Serial.begin(115200);
  timer_setup();
  Serial.print("BEGIN\n");
  encoder_setup(2);
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
  Serial.print(_output_pwm[2]);
  Serial.print("->");
  Serial.print(_current_velocity[2]);
  Serial.print("::");
  Serial.print(_output_pwm[1]);
  Serial.print("->");
  Serial.println(_current_velocity[1]);
  delay(1);
}