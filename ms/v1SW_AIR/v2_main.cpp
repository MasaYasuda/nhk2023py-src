
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
  for(byte i=0;i<6;i++){
    check_sw(i);
  }
  /*
  Serial.print(_output_pwm[0]);
  Serial.print(" ");
  Serial.println(_output_pwm[1]);
  
  Serial.print(_goal_velocity[0]);
  Serial.print(" ");
  Serial.println(_goal_velocity[1]);
  */
  output();
  delay(5);
}