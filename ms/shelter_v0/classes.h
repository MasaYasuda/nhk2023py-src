#ifndef _CLASSES_H_
#define _CLASSES_H_

// 構造体宣言　###############################
typedef union
{
  float val;
  byte binary[4];
} uf;

// global変数宣言　###############################
extern volatile long count[6];
extern float speed_now[6];
extern float order_speed[6];
extern float power_rate[6];
extern float power_rate_past[6];

// 関数宣言 ###############################
void timer_setup();
void calc_speed();
void calc_speed_delay(int num);
void calc_pid_position_type();
void calc_pid_speed_type();
void calc_ff_pid_speed_type();
void timer_calc();

void encoder_setup();
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



// クラス宣言 ###############################
class Receiver
{
public:
  void read_order();
private:
  int check_loss;
};


class Power
{
public:
  //  コンストラクタ
  Power();
  void output(float *power_rate);
  int *getOutput_dir(){return output_dir;};
  int *getOutput_pwm(){return output_pwm;};

private:
  int pin_dir[6];
  int pin_pwm[6];
  int output_dir[6];
  int output_pwm[6];
  int max_pwm;
};


#endif //_CLASSES_H_
