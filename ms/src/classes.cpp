#include <Arduino.h>
#include <TimerOne.h>
#include <Wire.h>
#include "classes.h"

// global変数宣言　###############################

const long dt_ms=20;
const int EncoderA[6] ={22,23,24,25,26,27};
const int EncoderB[6] ={0,1,5,4,3,2}; //ArduinoMegaMotrSlaveは物理的なピン配置上B相割込みとなっている
const int resolution[6]={512,512,512,512,2048,2048};

const float KF_SPEED=0.10/1058;
const float KP_SPEED=0.0000;
const float KI_SPEED=0.00002;
const float KD_SPPED=0.0000;
const float INTEGRAL_LIMIT_SPEED=100000000;

const float Kf_speed[6]={KF_SPEED,KF_SPEED,KF_SPEED,KF_SPEED,KF_SPEED,KF_SPEED};
const float Kp_speed[6]={KP_SPEED,KP_SPEED,KP_SPEED,KP_SPEED,KP_SPEED,KP_SPEED};
const float Ki_speed[6]={KI_SPEED,KI_SPEED,KI_SPEED,KI_SPEED,KI_SPEED,KI_SPEED};
const float Kd_speed[6]={KD_SPPED,KD_SPPED,KD_SPPED,KD_SPPED,KD_SPPED,KD_SPPED};
const float Integtal_limit_speed[6]={INTEGRAL_LIMIT_SPEED,INTEGRAL_LIMIT_SPEED,INTEGRAL_LIMIT_SPEED,INTEGRAL_LIMIT_SPEED,INTEGRAL_LIMIT_SPEED,INTEGRAL_LIMIT_SPEED};

const float KP_POSITION=0.001;
const float KI_POSITION=0.000;
const float KD_POSITION=0.0;
const float Kp_position[6]={KP_POSITION,KP_POSITION,KP_POSITION,KP_POSITION,KP_POSITION,KP_POSITION};
const float Ki_position[6]={KI_POSITION,KI_POSITION,KI_POSITION,KI_POSITION,KI_POSITION,KI_POSITION};
const float Kd_position[6]={KD_POSITION,KD_POSITION,KD_POSITION,KD_POSITION,KD_POSITION,KD_POSITION};


int mode[6]={0};
/* Mode= 0:Radio Controll  10:Position PID  20:Speed PID  30:Output disable  */
int direction_config[6]={0};
/* To know the config number, please refer to this "" */
int forward_dir_level[6] = {0,0,0,0,0,0};
/* Cytron: 0  /  Polulu G2: 1  */

volatile long count_past[6]={0};

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
        speed_now[i]=float(dif*1000*60/resolution[i]/dt_ms); //rpm
        count_past[i]=count[i];
    }
}
void calc_speed_delay(int num){
    unsigned long tmp_ms=0;
    for(int i=0;i<num;i++){
        tmp_ms=millis();
        count_past[i]=count[i];
        while(dt_ms>millis()-tmp_ms){}
        long dif=count[i]-count_past[i];
        speed_now[i]=float(dif*1000*60/resolution[i]/dt_ms); //rpm
    }
}

void calc_pid_position_type(){
    for(int i=0;i<6;i++){
        if(mode[i]==10){
        float dev_position=float(order_count[i]-count[i]);
        float P=Kp_position[i]*dev_position;
        integral_position[i]+=dev_position;
        integral_position[i]  = constrain(integral_position[i], -1,1);
        float I=Ki_position[i]*integral_position[i];
        float D=Kd_position[i]*(dev_position-dev_position_past[i])/dt_ms;
        dev_position_past[i]=dev_position;
        float power_rate_raw=float(P+I-D);
        power_rate[i]=constrain(power_rate_raw,-1,1);

        
        }
    }
}

void calc_pid_speed_type(){
    for(int i=0;i<6;i++){
        if(mode[i]==20){
            float dev_speed=order_speed[i]-speed_now[i];
            float P=Kp_speed[i]*dev_speed;
            integral_speed[i]+=dev_speed;
            integral_speed[i]  = constrain(integral_speed[i], -Integtal_limit_speed[i],Integtal_limit_speed[i]); 
            float I=Ki_speed[i]*integral_speed[i];
            float D=Kd_speed[i]*(dev_speed-dev_speed_past[i])/dt_ms;
            dev_speed_past[i]=dev_speed;
            float power_rate_raw=float(P+I+D);
            power_rate[i]=constrain(power_rate_raw,-1,1);
                
            //Serial.print("Speed Calclated:");
            //Serial.println(i);
        }
    }
}

void calc_ff_pid_speed_type(){
    for(int i=0;i<6;i++){
        if(mode[i]==20){
            float F= Kf_speed[i]*order_speed[i];
            float dev_speed=order_speed[i]-speed_now[i];
            float P=Kp_speed[i]*dev_speed;
            integral_speed[i]+=dev_speed;
            integral_speed[i]  = constrain(integral_speed[i], -Integtal_limit_speed[i],Integtal_limit_speed[i]); 
            float I=Ki_speed[i]*integral_speed[i];
            float D=Kd_speed[i]*(dev_speed-dev_speed_past[i])/dt_ms;
            dev_speed_past[i]=dev_speed;
            float power_rate_raw=constrain(float(P+I+D),-1,1);
            power_rate[i]=constrain(F+power_rate_raw,-1,1);
            /*
            Serial.print("FF & PID Speed Calclated:");
            Serial.println(i);
            */
            
             
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
        //Serial.println("RECEIVED");
        byte header = Serial.read();
        if (header == 0xFF) {
            byte motorNumber = Serial.read();
            //Serial.println(motorNumber);
            if (motorNumber >= 0 && motorNumber < 6) { //値受信

                uf order;
                for(int i=3;i>-1;i--){//little indian
                    order.binary[i]=Serial.read(); 
                }

                float config_check=1;
                if(direction_config[motorNumber]==2 ||direction_config[motorNumber]==3){
                    config_check=-1;
                }

                if(mode[motorNumber]==0){ //ラジコンモード
                    power_rate[motorNumber]=config_check*constrain(order.val,-1,1);
                    //Serial.print("Motor: ");
                    //Serial.print(motorNumber);
                    //Serial.print(", Power: ");
                    //Serial.println(power_rate[motorNumber]);

                }else if (mode[motorNumber]==10){//ポジションPIDモード

                    order_count[motorNumber] = config_check*(int(order.val)+count[motorNumber]);
                    //Serial.print("Motor: ");
                    //Serial.print(motorNumber);
                    //Serial.print(", Count: ");
                    //Serial.println(order_count[motorNumber]);
                    
                }else if (mode[motorNumber]==20){// スピードPIDモード
                    order_speed[motorNumber] = config_check*order.val;
                    //Serial.print("Motor: ");
                    //Serial.print(motorNumber);
                    //Serial.print(", Speed: ");
                    //Serial.println(order_speed[motorNumber]);
                }
            }

                
            /*
            config系

            -モータの制御モード（ラジコン、位置型PID、速度型PID）
            -出力回転方向とエンコーダーカウント正方向のつじつま合わせ
            -MD別　正方向出力のDIRの定義

            */ 
        
            else if(motorNumber>99 && motorNumber<106){
                uf order;
                for(int i=3;i>-1;i--){//little indian
                order.binary[i]=Serial.read(); 
                }
                mode[motorNumber-100] = int(order.val);
                //Serial.print("DefineMotor: ");
                //Serial.print(motorNumber);
                //Serial.print(", Mode: ");
                //Serial.println(mode[motorNumber-100]);

            }else if(motorNumber>199 && motorNumber<206){
                uf order;
                for(int i=3;i>-1;i--){//little indian
                order.binary[i]=Serial.read(); 
                }
                direction_config[motorNumber-200] = int(order.val);
                //Serial.print("Direction config num : ");
                //Serial.print(motorNumber);
                //Serial.print(", config: ");
                //Serial.println(direction_config[motorNumber-200]);
                
            }else if(motorNumber>209 && motorNumber<216){
                uf order;
                for(int i=3;i>-1;i--){//little indian
                order.binary[i]=Serial.read(); 
                }
                forward_dir_level[motorNumber-210] = int(order.val);
                //Serial.print("Direction config num : ");
                //Serial.print(motorNumber);
                //Serial.print(", forward_dir_level: ");
                //Serial.println(forward_dir_level[motorNumber-210]);
            }
        }
    }
}

Power::Power()
{
    // DIR_LEVEL : Cytron=0 , Polulu=1
    int PIN_DIR[6]={28, 29, 30, 31, 32, 33};
    memcpy(pin_dir,PIN_DIR,12);
    int PIN_PWM[6]={4, 5, 6, 7, 8, 9};
    memcpy(pin_pwm,PIN_PWM,12);
    
    output_dir[6] = {0};
    output_pwm[6] = {0};
    max_pwm = 240;
    for (int i = 0; i < 6; i++)
    {
        pinMode(pin_dir[i], OUTPUT);
        digitalWrite(pin_dir[i], LOW);
        analogWrite(pin_pwm[i], 0);
    }
}

void Power::output(float *power_rate)
{
    for (int i = 0; i < 6 ; i++)
    {   
        float config_check=1;
        if(direction_config[i]==1 ||direction_config[i]==2){
            config_check=-1;
        }

        output_pwm[i]=int(config_check*max_pwm*(power_rate[i]));
        if (output_pwm[i] >= 0)
        {
            digitalWrite(pin_dir[i], forward_dir_level[i]);
            analogWrite(pin_pwm[i], output_pwm[i]);
        }
        else
        {
            int dir = 1 - forward_dir_level[i];
            digitalWrite(pin_dir[i], dir);
            analogWrite(pin_pwm[i], (-1) * output_pwm[i]);
        }
    }
}