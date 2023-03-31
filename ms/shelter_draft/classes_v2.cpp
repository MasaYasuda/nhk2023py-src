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

void __serial_sumcheck();
void __serial_receive_radicon(int num, float value);
void __serial_receive_pid_position(int num, int value);
void __serial_receive_pid_speed(int num, float value);
void __serial_receive_mode(int num, int);
void __serial_receive_dir_config();
void __serial_receive_forward_lev();
void Pininterrupt();
void Timerinterrupt();

void calc_radicon();
void calc_pid_position();
void calc_pid_speed();
void output_all();
