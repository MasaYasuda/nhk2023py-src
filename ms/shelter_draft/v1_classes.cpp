#include <Arduino.h>
#include <TimerOne.h>
#include <Wire.h>
#include "classes.h"

extern float storage[300];

void serial_receive()
{
  if (Serial.available() >= 6)
  {

    byte buf[6] = {0};      // バッファ用意
    int sumcheck = 0;       // チェックサム用変数用意
    buf[0] = Serial.read(); // 0バイト目読みとり
    sumcheck += buf[0];
    if (buf[0] == 0xFF)
    { // 開始バイトの場合
      for (int i = 1; i < 6; i++)
      {
        buf[i] = Serial.read();
        check += buf[i];
      }
      byte checksum = Serial.read(); // read checksum
      sumcheck &= 0xFF;              // calc check sum

      if (checksum == sumcheck)
      { // if checksum is correct
        int addr = buf[1];
        float value = 0;
        byte tmp_buf[4] = { 0 } for (int i = 0; i < 4; i++)
        {
          tmp_buf[i] = buf[i + 2];
        }
        memcpy(&value, tmp_buf, sizeof(value));
        if ()
      }
    }
  }
}

void serial_receive()
void __write_int_data()
void __write_long_data()
void __write_float_data()
void __write_byte_data()
void __write_bool_data()

void encoder_setup(){
  attachInterrupt(EncoderB[0], __pinInterrupt0R, RISING);
  attachInterrupt(EncoderB[1], __pinInterrupt1R, RISING);
  attachInterrupt(EncoderB[2], __pinInterrupt2R, RISING);
  attachInterrupt(EncoderB[3], __pinInterrupt3R, RISING);
  attachInterrupt(EncoderB[4], __pinInterrupt4R, RISING);
  attachInterrupt(EncoderB[5], __pinInterrupt5R, RISING);

  attachInterrupt(EncoderB[0], __pinInterrupt0F, FALLING);
  attachInterrupt(EncoderB[1], __pinInterrupt1F, FALLING);
  attachInterrupt(EncoderB[2], __pinInterrupt2F, FALLING);
  attachInterrupt(EncoderB[3], __pinInterrupt3F, FALLING);
  attachInterrupt(EncoderB[4], __pinInterrupt4F, FALLING);
  attachInterrupt(EncoderB[5], __pinInterrupt5F, FALLING);
}
void __pinInterrupt0R(){if(digitalRead(EncoderA[0])==1){count[0]++;}else{count[0]--;}}
void __pinInterrupt1R(){if(digitalRead(EncoderA[1])==1){count[1]++;}else{count[1]--;}}
void __pinInterrupt2R(){if(digitalRead(EncoderA[2])==1){count[2]++;}else{count[2]--;}}
void __pinInterrupt3R(){if(digitalRead(EncoderA[3])==1){count[3]++;}else{count[3]--;}}
void __pinInterrupt4R(){if(digitalRead(EncoderA[4])==1){count[4]++;}else{count[4]--;}}
void __pinInterrupt5R(){if(digitalRead(EncoderA[5])==1){count[5]++;}else{count[5]--;}}

void __pinInterrupt0F(){if(digitalRead(EncoderA[0])==0){count[0]++;}else{count[0]--;}}
void __pinInterrupt1F(){if(digitalRead(EncoderA[1])==0){count[1]++;}else{count[1]--;}}
void __pinInterrupt2F(){if(digitalRead(EncoderA[2])==0){count[2]++;}else{count[2]--;}}
void __pinInterrupt3F(){if(digitalRead(EncoderA[3])==0){count[3]++;}else{count[3]--;}}
void __pinInterrupt4F(){if(digitalRead(EncoderA[4])==0){count[4]++;}else{count[4]--;}}
void __pinInterrupt5F(){if(digitalRead(EncoderA[5])==0){count[5]++;}else{count[5]--;}}

void timer_setup(){
  Timer1.initialize(_DT_MS*1000); // 20msごとに割込み
  Timer1.attachInterrupt(__timer_calc);
}
void __timer_calc(){
  __calc_speed();
  __calc_ffpid_speed();
}
void __calc_speed(){
  for(int i=0;i<6;i++){
        long dif=count[i]-count_past[i];
        speed_now[i]=float(dif*1000*60/resolution[i]/dt_ms); //rpm
        count_past[i]=count[i];
    }
}
void __calc_pid_position()
void __calc_ffpid_speed()

void ____pinInterruptXX()
void output()
void switch_input()

