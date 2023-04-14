#include <Arduino.h>

void setup(){
    Serial.begin(115200);
}
void loop(){
    if(Serial.available()>=1){
        int tmp=int(Serial.read());
        Serial.print(tmp);
        delay(0.005);
    }
}