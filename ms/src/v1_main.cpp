#include <Arduino.h>
#include <v1_classes.h>
#include <_v1_controll_table.h>

void setup(){
  Serial.begin(115200);
  //timer_setup();
  Serial.print("BEGIN\n");
}
void loop(){
  serial_receive();
  /*
  output();
  
  Serial.print(_output_pwm[0]);
  Serial.print(" ");
  Serial.println(_output_pwm[1]);
  */
  delay(10);
}