#include <Arduino.h>
#include "rs_classes.h"
#include "v1_classes.h"

void setup(){
  Serial.begin(115200);
  rs_encoder_setup();
}
void loop(){
  serial_receive();
  rs_output();
}