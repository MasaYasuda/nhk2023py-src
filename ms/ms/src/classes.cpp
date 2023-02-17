#include <Arduino.h>
#include <TimerOne.h>
#include <Wire.h>
#include "classes.h"

// global変数宣言　###############################

int mode[6]={0,0,0,0,0,0};
/* Mode= 0:Radio Controll  10:Position PID  20:Speed PID  30:Output disable  */
int direction_config[6]={0,0,0,0,0,0};
/* To know the config number, please refer to this "" */

const long dt_ms=20;
const int EncoderA[6] ={22,23,24,25,26,27};
const int EncoderB[6] ={0,1,5,4,3,2}; //ArduinoMegaMotrSlaveは物理的なピン配置上B相割込みとなっている

const float KP_SPEED=0.001;
const float KI_SPEED=0.000;
const float KD_SPPED=-0.0;
const float Kp_speed[6]={KP_SPEED,KP_SPEED,KP_SPEED,KP_SPEED,KP_SPEED,KP_SPEED};
const float Ki_speed[6]={KI_SPEED,KI_SPEED,KI_SPEED,KI_SPEED,KI_SPEED,KI_SPEED};
const float Kd_speed[6]={KD_SPPED,KD_SPPED,KD_SPPED,KD_SPPED,KD_SPPED,KD_SPPED};

const float KP_POSITION=0.001;
const float KI_POSITION=0.000;
const float KD_POSITION=-0.0;
const float Kp_position[6]={KP_POSITION,KP_POSITION,KP_POSITION,KP_POSITION,KP_POSITION,KP_POSITION};
const float Ki_position[6]={KI_POSITION,KI_POSITION,KI_POSITION,KI_POSITION,KI_POSITION,KI_POSITION};
const float Kd_position[6]={KD_POSITION,KD_POSITION,KD_POSITION,KD_POSITION,KD_POSITION,KD_POSITION};


long count_past[6]={0};

float integral_position[6]={0};
float dev_position_past[6]={0};

float dev_speed_past[6]={0};
float integral_speed[6]={0};


//extern global変数
volatile long count[6]={0};
float speed_now[6]={0};
float order_speed[6]={0};
int order_count[6]={0};
float power_rate[6]={0};
float power_rate_past[6]={0};


// 関数宣言 ###############################
// Function For pinInterrupt
void pinInterrupt0R(){if(digitalRead(EncoderA[0])==1){count[0]++;}else{count[0]--;}}
void pinInterrupt1R(){if(digitalRead(EncoderA[1])==1){count[1]++;}else{count[1]--;}}
void pinInterrupt2R(){if(digitalRead(EncoderA[2])==1){count[2]++;}else{count[2]--;}}
void pinInterrupt3R(){if(digitalRead(EncoderA[3])==1){count[3]++;}else{count[3]--;}}
void pinInterrupt4R(){if(digitalRead(EncoderA[4])==1){count[4]++;}else{count[4]--;}}
void pinInterrupt5R(){if(digitalRead(EncoderA[5])==1){count[5]++;}else{count[5]--;}}

void pinInterrupt0F(){if(digitalRead(EncoderA[0])==0){count[0]++;}else{count[0]--;}}
void pinInterrupt1F(){if(digitalRead(EncoderA[1])==0){count[1]++;}else{count[1]--;}}
void pinInterrupt2F(){if(digitalRead(EncoderA[2])==0){count[2]++;}else{count[2]--;}}
void pinInterrupt3F(){if(digitalRead(EncoderA[3])==0){count[3]++;}else{count[3]--;}}
void pinInterrupt4F(){if(digitalRead(EncoderA[4])==0){count[4]++;}else{count[4]--;}}
void pinInterrupt5F(){if(digitalRead(EncoderA[5])==0){count[5]++;}else{count[5]--;}}

void encoder_setup(){
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

//Function Fot Timer Interrupt
void timer_setup(){
  Timer1.initialize(dt_ms*1000); // 20msごとに割込み
  Timer1.attachInterrupt(timer_calc);
}
void calc_speed(){
    for(int i=0;i<6;i++){
        long dif=count[i]-count_past[i];
        speed_now[i]=float(dif*1000*60/1024/dt_ms); //rpm
        count_past[i]=count[i];
    }
}

void calc_pid_position_type(){
    for(int i=0;i<6;i++){
        if(mode[i]==10){
        float dev_position=float(order_count[i]-count[i]);
        float P=Kp_position[i]*dev_position;
        integral_position[i]+=dev_position;
        float I=Ki_position[i]*integral_position[i];
        float D=Kd_position[i]*(dev_position-dev_position_past[i])/dt_ms;
        dev_poition_past[i]=dev_position;
        float power_rate_raw=(float)(P+I-D);
        power_rate[i]=constrain(power_rate_raw+power_rate_past[i],-1,1);

        power_rate_past[i]=power_rate[i];
        
        }
    }
}

void calc_pid_speed_type(){
    for(int i=0;i<6;i++){
        if(mode[i]==20){
        float dev_speed=order_speed[i]-speed_now[i];
        float P=Kp_speed[i]*dev_speed;
        integral_speed[i]+=dev_speed;
        float I=Ki_speed[i]*integral[i];
        float D=Kd_speed[i]*(dev_speed-dev_speed_past[i])/dt_ms;
        dev_speed_past[i]=dev_speed;
        float power_rate_raw=(float)(P+I-D);
        power_rate[i]=constrain(power_rate_raw+power_rate_past[i],-1,1);

        power_rate_past[i]=power_rate[i];

        }
    }
}

void timer_calc(){
    calc_speed();
    calc_pid_position_type();
    calc_pid_speed_type();
}

// クラスメソッド宣言 ###############################
//  コンストラクタ

void Receiver::read_order(){
    if (Serial.available() >= 6) {
        Serial.println("RECEIVED");
        byte header = Serial.read();
        if (header == 0xFF) {
            byte motorNumber = Serial.read();
            Serial.println(motorNumber);
            if (motorNumber >= 0 && motorNumber < 6) { //値受信
                uf order;
                for(int i=3;i>-1;i--){//little indian
                order.binary[i]=Serial.read(); 
                float config_check=1;

                if(direction_config[motorNumber]==2 ||direction_config[motorNumber]==3){
                    config_check=-1;
                }

                if(mode[motorNumber]==0){ //ラジコンモード
                    power_rate[motorNumber]=config_check*constrain(order.val,-1,1);
                    Serial.print("Motor: ");
                    Serial.print(motorNumber);
                    Serial.print(", Power: ");
                    Serial.println(power_rate[motorNumber]);

                }else if (mode[motorNumber]==10){//ポジションPIDモード

                    order_count[motorNumber] = config_check*(int(order.val)+count[i]);
                    Serial.print("Motor: ");
                    Serial.print(motorNumber);
                    Serial.print(", Count: ");
                    Serial.println(order_count[motorNumber]);
                    
                }else if (mode[motorNumber]==20){// スピードPIDモード
                    order_speed[motorNumber] = config_check*order.val;
                    Serial.print("Motor: ");
                    Serial.print(motorNumber);
                    Serial.print(", Speed: ");
                    Serial.println(order_speed[motorNumber]);
                }

            }else if(motorNumber>99 && motorNumber<106){
                uf order;
                for(int i=3;i>-1;i--){//little indian
                order.binary[i]=Serial.read(); 
                }
                mode[motorNumber-100] = int(order.val);
                Serial.print("DefineMotor: ");
                Serial.print(motorNumber);
                Serial.print(", Mode: ");
                Serial.println(,mode[motorNumber-100]);
            }else if(motorNumber>199 && motorNumber<206){
                uf order;
                for(int i=3;i>-1;i--){//little indian
                order.binary[i]=Serial.read(); 
                }
                direction_config[motorNumber-200] = int(order.val);
                Serial.print("Direction config num : ");
                Serial.print(motorNumber);
                Serial.print(", config: ");
                Serial.println(,direction_config[motorNumber-200]);
            }
        }
    }
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

void Power::output(float *power_rate)
{
    for (int i = 0; i < 6; i++)
    {
        float config_check=1;
        if(direction_config[motorNumber]==1 ||direction_config[motorNumber]==2){
            config_check=-1;
        }

        output_pwm[i]=int(config_check*max_pwm*(power_rate[i]));
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
