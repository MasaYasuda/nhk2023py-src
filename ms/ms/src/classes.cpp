#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"

//  コンストラクタ
Receiver::Receiver(int baudrate){
    Serial.begin(baudrate);
    order_speed[6]={0};    
}

void Receiver::read_order(){
    if (Serial.available() >= 6) {
    Serial.println("RECEIVED");
    byte header = Serial.read();
    if (header == 0xFF) {
      byte motorNumber = Serial.read();
      Serial.println(motorNumber);
      if (motorNumber >= 0 && motorNumber < 6) {
        uf speed;
        for(int i=0;i<4;i++){//little indian
          speed.binary[3-i]=Serial.read(); 
        }
        order_speed[motorNumber] = speed.val;
        Serial.print("Motor: ");
        Serial.print(motorNumber);
        Serial.print(", Speed: ");
        Serial.println(order_speed[motorNumber]);
        }
    }
  }
}


Encoder::Encoder(){
    //ArduinoMegaMotrSlaveは物理的なピン配置上B相割込みとなっていることに注意
    int encA[6]= {22,23,24,25,26,27};
    memcpy(EncoderA,encA,6);
    int encB[6]= {2,3,18,19,20,21};
    memcpy(EncoderB,encB,6);   
    count[6]={0};
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
void Encoder::pinInterrupt0R(){if(digitalRead(EncoderA[0])==1){count[0]++;}else{count[0]--;}}
void Encoder::pinInterrupt1R(){if(digitalRead(EncoderA[1])==1){count[1]++;}else{count[1]--;}}
void Encoder::pinInterrupt2R(){if(digitalRead(EncoderA[2])==1){count[2]++;}else{count[2]--;}}
void Encoder::pinInterrupt3R(){if(digitalRead(EncoderA[3])==1){count[3]++;}else{count[3]--;}}
void Encoder::pinInterrupt4R(){if(digitalRead(EncoderA[4])==1){count[4]++;}else{count[4]--;}}
void Encoder::pinInterrupt5R(){if(digitalRead(EncoderA[5])==1){count[5]++;}else{count[5]--;}}

void Encoder::pinInterrupt0F(){if(digitalRead(EncoderA[0])==0){count[0]++;}else{count[0]--;}}
void Encoder::pinInterrupt1F(){if(digitalRead(EncoderA[1])==0){count[1]++;}else{count[1]--;}}
void Encoder::pinInterrupt2F(){if(digitalRead(EncoderA[2])==0){count[2]++;}else{count[2]--;}}
void Encoder::pinInterrupt3F(){if(digitalRead(EncoderA[3])==0){count[3]++;}else{count[3]--;}}
void Encoder::pinInterrupt4F(){if(digitalRead(EncoderA[4])==0){count[4]++;}else{count[4]--;}}
void Encoder::pinInterrupt5F(){if(digitalRead(EncoderA[5])==0){count[5]++;}else{count[5]--;}}


TimerPID::TimerPID(int RESOLUTION,float KP,float KI ,float KD)
{
    dt_ms = 20;
    count_past[6]={0};
    resolution=RESOLUTION;
    speed_now[6]={0};
    Kp=KP;
    Ki=KI;
    Kd=KD;
    dev_past[6]={0};
    integral[6]={0};
    power_rate[6]={0};

    Timer1.initialize(dt_ms*1000); // 20msごとに割込み
    Timer1.attachInterrupt(timer_calc_auto);
}
void TimerPID::calc_speed(int *count){
    for(int i=0;i<6;i++){
        int dif=count[i]-count_past[i];
        speed_now[i]=dif*1000*60/resolution/20; //rpm
    }
}
void TimerPID::calc_pid(float *order_speed){
    for(int i=0;i<6;i++){
        float dev=order_speed[i]-speed_now[i];
        float P=Kp*dev;
        integral[i]+=dev;
        float I=Ki*integral[i];
        float D=Kd*(dev-dev_past[i])/dt_ms;
        dev_past[i]=dev;
        float power_rate_raw=(float)(P+I-D);
        power_rate[i]=constrain(power_rate_raw,-1,1);
    }
}
void TimerPID::timer_calc_auto(Encoder e,Receiver r){
    int *cnt = e.getCount();
    calc_speed(cnt);
    float *order_sp = r.getOrder_speed();
    calc_pid(order_sp);
}


Power::Power()
{
    // DIR_LEVEL : Cytron=0 , Polulu=1
    int PIN_DIR[6]={28, 29, 30, 31, 32, 33};
    memcpy(pin_dir,PIN_DIR,6);
    int PIN_PWM[6]={4, 5, 6, 7, 8, 9};
    memcpy(pin_pwm,PIN_PWM,6);
    output_dir[6] = {0};
    output_pwm[6] = {0};
    max_pwm = 240;
    forward_dir_level = 0;
    for (int i = 0; i < 6; i++)
    {
        pinMode(pin_dir[i], OUTPUT);
        digitalWrite(pin_dir[i], LOW);
        analogWrite(pin_pwm[i], 0);
    }
}
void Power::output(TimerPID t)
{
    float *pr= t.getPower_rate();
    for (int i = 0; i < 6; i++)
    {
        output[i]=(int)(max_pwm*(pr[i]));
        if (output_pwm[i] >= 0)
        {
            digitalWrite(pin_dir[i], forward_dir_level);
            analogWrite(pin_pwm[i], output_pwm[i]);
        }
        else
        {
            int dir = 1 - forward_dir_level;
            digitalWrite(pin_dir[i], dir);
            analogWrite(pin_pwm[i], (-1) * output_pwm[i]);
        }
    }
}
