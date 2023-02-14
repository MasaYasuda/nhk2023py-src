#include <Arduino.h>
#include <TimerOne.h>
#include "classes.h"

//  コンストラクタ
Power::Power()
{
    // DIR_LEVEL : Cytron=0 , Polulu=1
    const int pin_dir[6] = {28, 29, 30, 31, 32, 33};
    const int pin_pwm[6] = {4, 5, 6, 7, 8, 9};
    int output_dir[6] = {0};
    int output_pwm[6] = {0};
    const int max_pwm = 240;
    int forward_dir_level = 0;
    for (int i = 0; i < 4; i++)
    {
        pinMode(pin_dir[i], OUTPUT);
        digitalWrite(pin_dir[i], LOW);
        analogWrite(pin_pwm[i], 0);
    }
}
void Power::output(float pid_rate[6])
{
    for (int i = 0; i < 6; i++)
    {
        output_pwm[i] = max_pwm * pid_rate[i];
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
int *Power::getOutput_dir()
{
    return output_dir;
}
int *Power::getOutput_pwm()
{
    return output_pwm;
}

TimerPID::TimerPID(int RESOLUTION,float KP,float KI ,float KD)
{
    int count_past[6]={0};
    int resolution=RESOLUTION;
    float speed_now[6]={0};
    float Kp=KP;
    float Ki=KI;
    float Kd=KD;
    int dev_past[6]={0};
    int integtal[6]={0};
    float power_rate[6]={0};

    Timer1.initialize(20000); // 20msごとに割込み
    Timer1.attachInterrupt(timerCalc);
}
float *TimerPID::getPower_rate(){
    return power_rate;
}
void TimerPID::calc_speed(int count[6]){
    for(int i=0;i<6;i++){
        int dif=count[i]-count_past[i];
        speed_now[i]=dif*1000*60/resolution/20 //rpm
    }
}
void TimerPID::calc_pid(float order_speed[6]){

}


int count_past[6];
int resolution;
float speed_past[6];
float Kp;
float Ki;
float Kd;
int dev_past[6];
int integtal[6];
float power_rate[6];

class Encoder
{
public:
    Encoder::Encoder()
    {
    }
    int *getCount();
    void pinInterrupt0R();
    void pinInterrupt1R();
    void pinInterrupt2R();
    void pinInterrupt3R();
    void pinInterrupt4R();
    void pinInterrupt5R();

    void pinInterrupt0F();
    void pinInterrupt1F();
    void pinInterrupt2F();
    void pinInterrupt3F();
    void pinInterrupt4F();
    void pinInterrupt5F();

private:
    int count[6];
};

class Receiver : public Serial
{
public:
    Receiver(int baudrate);
    float *getOrder_speed();
    void read_order();

private
    uf order_speed[6];
}
#endif //_CLASSES_H_
