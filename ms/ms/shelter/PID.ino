#include <Arduino.h>

/*

float Kp=1;
float Ki=0;
float Kd=0;
float pastdev[6]={0};
float integral[6]={0};

int pwmpower[6]={0};

*/

void pidCalc(){
  for(int i;i<6;i++){
    float dev=order_rpm[i]-now_rpm[i];

    float P=Kp*dev;

    integral[i]+=dev;
    float I=Ki*integral[i];

    float D=Kd*(dev-pastdev[i])/dt_ms;
    pastdev[i]=dev;
    int pwmpower_raw=(int)(P+I-D);
    pwmpower[i]=constrain(pwmpower_raw,-220,220);
  }
}