#include <Arduino.h>
#include "rs_classes.h"
#include "_v1_controll_table.h"
/**
 * @brief フラグ
 *
 */
byte __EMG = 0;

/* EMG=0 > 時計反時計回転共に許可　EMG=1 > 時計回転のみ許可　EMG>2 反時計回転のみ許可*/
void __emg1() { __EMG = 1; }
void __emg2() { __EMG = 2; }

void rs_encoder_setup()
{
  attachInterrupt(_PINNUM_ENCODER_B[0], __emg1, CHANGE);
  attachInterrupt(_PINNUM_ENCODER_B[1], __emg2, CHANGE);
}

void rs_output()
{
  if (_MODE[0] != 0)
  {
    int pwm = int(_output_pwm[0]);
    if (pwm >= 0) // 正回転の場合
    {
      if (__EMG != 2)// かつ正回転禁止"でない"場合
      {
        digitalWrite(_PINNUM_OUTPUT_DIR[0], _FORWARD_LEVEL[0]);
        analogWrite(_PINNUM_OUTPUT_PWM[0], pwm);
        __EMG = 0;
      }
    }
    else
    {
      if (__EMG != 1)
      {
        digitalWrite(_PINNUM_OUTPUT_DIR[0], 1 - _FORWARD_LEVEL[0]);
        analogWrite(_PINNUM_OUTPUT_PWM[0], (-1) * pwm);
        __EMG = 0;
      }
    }
  }
}