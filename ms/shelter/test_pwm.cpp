#include <Arduino.h>

void setup(){
    Serial.begin(115200);
    pinMode(28,OUTPUT);
    digitalWrite(28,LOW);
}
void loop(){
    digitalWrite(28,HIGH);
    analogWrite(4,0);
    Serial.println("POWER:0");
    delay(2000);
    analogWrite(4,100);
    Serial.println("POWER:25");
    delay(2000);
    analogWrite(4,200);
    Serial.println("POWER:50");
    delay(2000);
    analogWrite(4,100);
    Serial.println("POWER:25");
    delay(2000);
}