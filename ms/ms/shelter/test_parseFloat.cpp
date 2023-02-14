#include <Arduino.h>

void setup(){
    Serial.begin(115200);
    pinMode( 13, OUTPUT );
}
void loop(){
    if (Serial.available() >= 5) {
        Serial.println("RECEIVED");
        byte header = Serial.read();
        if (header == 0xFF) {
            float value = 0;
            value = (float)(Serial.read() | (Serial.read() << 8) | (Serial.read() << 16) | (Serial.read() << 24));
            Serial.println(value);

            /*
            float value = Serial.parseFloat();  
            Serial.println(value); 
            while (Serial.available() > 0) {//受信バッファクリア
                char t = Serial.read();
            }
            */
            
            int count=(int)(value);
            for(int i=0;i<count;i++){
                digitalWrite(13,HIGH);
                delay(200);
                digitalWrite(13,HIGH);
                delay(200);
            }
        }
        
    }
    delay(10);
}