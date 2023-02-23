#include <Arduino.h>

void setup(){
    Serial.begin(115200);
    pinMode(30,OUTPUT);
    digitalWrite(30,LOW);
}
void loop(){
    digitalWrite(30,HIGH);
    analogWrite(6,0);
    Serial.println("POWER:0");
    delay(2000);
    analogWrite(6,100);
    Serial.println("POWER:25");
    delay(2000);
    analogWrite(6,200);
    Serial.println("POWER:50");
    delay(2000);
    analogWrite(6,100);
    Serial.println("POWER:25");
    delay(2000);
}