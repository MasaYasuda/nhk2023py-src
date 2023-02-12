#include <Arduino.h>
  
/*

const int EncoderA[6] ={22,23,24,25,26,27};
const int EncoderB[6] ={2,3,18,19,20,21}; //ArduinoMegaMotrSlaveは物理的なピン配置上B相割込みとなっている
long ECNT[6]={0};
long pastECNT[6]={0};//Speed_calcで使用

*/


void pinInterrupt0R(){if(digitalRead(EncoderA[0])==1){ECNT[0]++;}else{ECNT[0]--;}}
void pinInterrupt1R(){if(digitalRead(EncoderA[1])==1){ECNT[1]++;}else{ECNT[1]--;}}
void pinInterrupt2R(){if(digitalRead(EncoderA[2])==1){ECNT[2]++;}else{ECNT[2]--;}}
void pinInterrupt3R(){if(digitalRead(EncoderA[3])==1){ECNT[3]++;}else{ECNT[3]--;}}
void pinInterrupt4R(){if(digitalRead(EncoderA[4])==1){ECNT[4]++;}else{ECNT[4]--;}}
void pinInterrupt5R(){if(digitalRead(EncoderA[5])==1){ECNT[5]++;}else{ECNT[5]--;}}

void pinInterrupt0F(){if(digitalRead(EncoderA[0])==0){ECNT[0]++;}else{ECNT[0]--;}}
void pinInterrupt1F(){if(digitalRead(EncoderA[1])==0){ECNT[1]++;}else{ECNT[1]--;}}
void pinInterrupt2F(){if(digitalRead(EncoderA[2])==0){ECNT[2]++;}else{ECNT[2]--;}}
void pinInterrupt3F(){if(digitalRead(EncoderA[3])==0){ECNT[3]++;}else{ECNT[3]--;}}
void pinInterrupt4F(){if(digitalRead(EncoderA[4])==0){ECNT[4]++;}else{ECNT[4]--;}}
void pinInterrupt5F(){if(digitalRead(EncoderA[5])==0){ECNT[5]++;}else{ECNT[5]--;}}

void encoderSetup(){
  attachInterrupt(EncoderB[0], pinInterrupt0R, RISING);
  attachInterrupt(EncoderB[1], pinInterrupt1R, RISING);
  attachInterrupt(EncoderB[2], pinInterrupt2R, RISING);
  attachInterrupt(EncoderB[3], pinInterrupt3R, RISING);
  attachInterrupt(EncoderB[4], pinInterrupt4R, RISING);
  attachInterrupt(EncoderB[5], pinInterrupt5R, RISING);

  attachInterrupt(EncoderB[0], pinInterrupt0F, FALLING);
  attachInterrupt(EncoderB[1], pinInterrupt1F, FALLING);
  attachInterrupt(EncoderB[2], pinInterrupt2F, FALLING);
  attachInterrupt(EncoderB[3], pinInterrupt3F, FALLING);
  attachInterrupt(EncoderB[4], pinInterrupt4F, FALLING);
  attachInterrupt(EncoderB[5], pinInterrupt5F, FALLING);
}