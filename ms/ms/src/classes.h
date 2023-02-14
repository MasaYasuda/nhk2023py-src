#ifndef _CLASSES_H_
#define _CLASSES_H_


// 構造体宣言
typedef union
{
  float val;
  byte binary[4];
} uf;

// クラス宣言
class Receiver
{
public:
  Receiver(int baudrate);
  float *getOrder_speed(){return order_speed;};
  void read_order();

private:
  float order_speed[6];
};

class Encoder
{
public:
  Encoder();
  int *getCount(){return count;};
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
  int EncoderA[6];
  int EncoderB[6];
  int count[6];
};


class TimerPID
{
public:
  TimerPID(int RESOLUTION,float KP,float KI ,float KD);
  void calc_speed(int *count);
  void calc_pid(float *order_speed);
  void timer_calc_auto(Encoder e, Receiver r);
  float *getPower_rate(){return power_rate;};

private:
  int dt_ms;
  int count_past[6];
  int resolution;
  float Kp;
  float Ki;
  float Kd;
  int dev_past[6];
  int integral[6];
  float speed_now[6];
  float power_rate[6];
};
class Power
{
public:
  //  コンストラクタ
  Power();
  void output(TimerPID t);
  int *getOutput_dir(){return output_dir;};
  int *getOutput_pwm(){return output_pwm;};

private:
  int pin_dir[6];
  int pin_pwm[6];
  int output_dir[6];
  int output_pwm[6];
  int max_pwm;
  int forward_dir_level;
};


#endif //_CLASSES_H_
