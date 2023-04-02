#include <Arduino.h>
#include <v1_classes.h>

void setup(){
  Serial.begin(115200);
  timer_setup();
}
void loop(){
  serial_receive();
  output();
  delay(10);
}