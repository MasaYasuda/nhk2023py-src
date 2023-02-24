#include <Arduino.h>


  

void setup()
{
  Serial.begin(115200);

  int pin_dir[6];
  int pin_pwm[6];
  // DIR_LEVEL : Cytron=0 , Polulu=1
  int PIN_DIR[6] = {28, 29, 30, 31, 32, 33};
  memcpy(pin_dir, PIN_DIR, 12);
  int PIN_PWM[6] = {4, 5, 6, 7, 8, 9};
  memcpy(pin_pwm, PIN_PWM, 12);

  for (int i = 0; i < 6; i++)
  {
    Serial.print("#");
    Serial.println(pin_dir[i]);
    
    pinMode(pin_dir[i], OUTPUT);
    digitalWrite(pin_dir[i], HIGH);
    analogWrite(pin_pwm[i], 0);
  }
}
void loop()
{
  delay(50);
}
