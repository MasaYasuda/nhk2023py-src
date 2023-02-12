#include <Arduino.h>

void setup(){
  Serial.begin(11520);
}
float order_rpm[4]={0};
const int pinPWM[4]={2,3,4,5};
int output_value[4]={0,0,0,0};

void loop(){
  if (Serial.read() == 0xFF)
    {
      int data1 = int(Serial.read());
      printf("%d",data1);
      order_rpm[data1] = Serial.parseFloat();
      if(order_rpm[data1]>1){order_rpm[data1]=1;}
      else if(order_rpm[data1]<1){order_rpm[data1]=-1;}
      output_value[data1]=int(order_rpm[data1]*255);
      analogWrite(pinPWM[data1],order_rpm[data1]);

    }

  printf("[");
  for (int i=0;i<4;i++){
    printf("%f",order_rpm[i]);
    if(i==3){
      break;
    }
    printf(",");
  }
  printf("]");
}