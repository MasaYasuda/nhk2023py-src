#include <Arduino.h>

void setup(){
    Serial.begin(115200);
    pinMode(31,OUTPUT);
    digitalWrite(31,LOW);
}
void loop(){
    digitalWrite(31,HIGH);
    analogWrite(7,0);
    Serial.println("POWER:0");
    delay(2000);
    analogWrite(7,100);
    Serial.println("POWER:25");
    delay(2000);
    analogWrite(7,200);
    Serial.println("POWER:50");
    delay(2000);
    analogWrite(7,100);
    Serial.println("POWER:25");
    delay(2000);
}