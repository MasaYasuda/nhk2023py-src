#include <Arduino.h>

void setup() {
    pinMode( 13, OUTPUT );
    Serial.begin(115200);
}
void loop() {
    digitalWrite( 13, HIGH );
    delay(100);
    digitalWrite( 13, LOW );
    delay(300);
    Serial.println("Hello World!");
}