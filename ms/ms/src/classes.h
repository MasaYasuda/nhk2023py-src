#ifndef _CLASSES_H_
#define _CLASSES_H_

#include <Arduino.h>

// 構造体宣言
typedef union
{
  float val;
  byte binary[4];
} uf;

// クラス宣言
class Power
{
public:
  //  コンストラクタ
  Power();
  void output();
  int *getOutput_dir();
  int *getOutput_pwm();

private:
  int pin_dir[6];
  int pin_pwm[6];
  int output_dir[6];
  int output_dir[6];
};

class TimerPID
{
public:
  TimerPID();
  void calc_speed(int count[6]);
  void calc_pid(float order_speed[6]);
  float *getPower_rate();

private:
  int count_past[6];
  int resolution;
  float speed_past[6];
  float Kp;
  float Ki;
  float Kd;
  int dev_past[6];
  int integtal[6];
  float power_rate[6];
};

class Encoder
{
public:
  Encoder();
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
