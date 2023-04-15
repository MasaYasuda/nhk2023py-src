/**
 * @file v1_classes.cpp
 * @brief ArduinoMegaMotorSlave用の関数群です。
 * @date 23/4/2 <br>
 * ほぼ完成
 * @par TEST<br>
 * wawawa
 * @author Masanaga Yasuda
*/

#include <Arduino.h>
#include <TimerOne.h>
#include "_v1_controll_table.h"
#include "v1_classes.h"

void __clear_table(byte addr){
  _current_position[addr]=0;
  _current_velocity[addr]=0;
  _goal_position[addr]=0;
  _goal_velocity[addr]=0;
  _output_pwm[addr]=0;
  _previous_position_error[addr]=0;
  _previous_velocity_error[addr]=0;
  _integral_position_error[addr]=0;
  _integral_velocity_error[addr]=0;
}

void serial_receive()
{
  if (Serial.available() >= 6)
  {

    byte buf[7] = {0};      // バッファ用意
    byte tmp_sum = 0;       // チェックサム用変数用意
    buf[0] = Serial.read(); // 0バイト目読みとり
    tmp_sum += buf[0];
    if (buf[0] == 0xFF)
    { // 開始バイトの場合
      //Serial.println("RECEIVED");
      for (byte i = 1; i < 6; i++)
      {
        buf[i] = Serial.read();
        tmp_sum += buf[i];
      }
      buf[6] = Serial.read(); // read checksum
      tmp_sum &= 0xFF;              // calc check sum

      if (buf[6]==tmp_sum)
      { // if checksum is correct
        Serial.println("CORRECT CHECKSUM");
        byte addr = buf[1];  
        byte tmp_buf[4] = {0};  
        float value = 0;    
         for (int i = 0; i < 4; i++)
        {
          tmp_buf[i] = buf[i + 2];
        }
        memcpy(&value, tmp_buf, sizeof(value));
        //Serial.println(addr);
        //Serial.println(value);
        if (addr>=0 && addr <6 ){
          //Serial.println("VALUE INPUT");
          int config_check=1;
          if(_DIRECTION_CONFIG[addr]==2 ||_DIRECTION_CONFIG[addr]==3){
              config_check=-1;
          }
          if(_MODE[addr]==100){// ラジコンモード
            _output_pwm[addr]=int(config_check*value*_MAX_PWM[addr]);
            Serial.println(_output_pwm[addr]);
          }else if(_MODE[addr]==20){// 速度型PIDモード
            _goal_velocity[addr]=float(config_check*value);
          }else if(_MODE[addr]==10){// 位置型PIDモード
            _goal_position[addr]=long(config_check*value);
            Serial.println("POSITION MODE");
          }
        }else if(addr>=200 && addr <206){//write _MODE
          //Serial.print("MODE:");
          //Serial.println(value);
          __clear_table(addr-200);
          _MODE[addr-200]=byte(value);
          if (_MODE[addr-200]==10 || _MODE[addr-200]==20){
            encoder_setup(addr-200);
          }
        }else if(addr>=210 && addr <216){//write _DIRECTION_CONFIG
          _DIRECTION_CONFIG[addr-210]=byte(value);
        }else if(addr>=220 && addr <226){//write _FORWARD_LEVEL
          _FORWARD_LEVEL[addr-220]=byte(value);
        }
      }
    }
  }
}



void __pinInterrupt0R(){if(digitalRead(_PINNUM_ENCODER_A[0])==1){_current_position[0]++;}else{_current_position[0]--;}}
void __pinInterrupt1R(){if(digitalRead(_PINNUM_ENCODER_A[1])==1){_current_position[1]++;}else{_current_position[1]--;}}
void __pinInterrupt2R(){if(digitalRead(_PINNUM_ENCODER_A[2])==1){_current_position[2]++;}else{_current_position[2]--;}}
void __pinInterrupt3R(){if(digitalRead(_PINNUM_ENCODER_A[3])==1){_current_position[3]++;}else{_current_position[3]--;}}
void __pinInterrupt4R(){if(digitalRead(_PINNUM_ENCODER_A[4])==1){_current_position[4]++;}else{_current_position[4]--;}}
void __pinInterrupt5R(){if(digitalRead(_PINNUM_ENCODER_A[5])==1){_current_position[5]++;}else{_current_position[5]--;}}

void __pinInterrupt0F(){if(digitalRead(_PINNUM_ENCODER_A[0])==0){_current_position[0]++;}else{_current_position[0]--;}}
void __pinInterrupt1F(){if(digitalRead(_PINNUM_ENCODER_A[1])==0){_current_position[1]++;}else{_current_position[1]--;}}
void __pinInterrupt2F(){if(digitalRead(_PINNUM_ENCODER_A[2])==0){_current_position[2]++;}else{_current_position[2]--;}}
void __pinInterrupt3F(){if(digitalRead(_PINNUM_ENCODER_A[3])==0){_current_position[3]++;}else{_current_position[3]--;}}
void __pinInterrupt4F(){if(digitalRead(_PINNUM_ENCODER_A[4])==0){_current_position[4]++;}else{_current_position[4]--;}}
void __pinInterrupt5F(){if(digitalRead(_PINNUM_ENCODER_A[5])==0){_current_position[5]++;}else{_current_position[5]--;}}


void encoder_setup(byte num){
  switch (num)
  {
  case 0:
    attachInterrupt(_PINNUM_ENCODER_B[0], __pinInterrupt0R, RISING);
    attachInterrupt(_PINNUM_ENCODER_B[0], __pinInterrupt0F, FALLING);
    break;
  case 1:
    attachInterrupt(_PINNUM_ENCODER_B[1], __pinInterrupt1R, RISING);
    attachInterrupt(_PINNUM_ENCODER_B[1], __pinInterrupt1F, FALLING);
    break;
  case 2:
    attachInterrupt(_PINNUM_ENCODER_B[2], __pinInterrupt2R, RISING);
    attachInterrupt(_PINNUM_ENCODER_B[2], __pinInterrupt2F, FALLING);
    break;
  case 3:
    attachInterrupt(_PINNUM_ENCODER_B[3], __pinInterrupt3R, RISING);
    attachInterrupt(_PINNUM_ENCODER_B[3], __pinInterrupt3F, FALLING);
    break;
  case 4:
    attachInterrupt(_PINNUM_ENCODER_B[4], __pinInterrupt4R, RISING);
    attachInterrupt(_PINNUM_ENCODER_B[4], __pinInterrupt4F, FALLING);
    break;
  case 5:
    attachInterrupt(_PINNUM_ENCODER_B[5], __pinInterrupt5R, RISING);
    attachInterrupt(_PINNUM_ENCODER_B[5], __pinInterrupt5F, FALLING);
    break;
  default:
    break;
  }
}

void __calc_speed(){
  for(int i=0;i<6;i++){
        long error=_current_position[i]-_integral_position_error[i];
        _current_velocity[i]=float(error*1000*60/_RESOLUTION[i]/_DT_MS); //rpm
        _integral_position_error[i]+=error;
    }
}

void __calc_pid_position(){
  for(int i=0;i<6;i++){
    if(_MODE[i]==10){
    long error=_goal_position[i]-_current_position[i];
    float P=_GAIN_POSITION_PID[i][0]*float(error);
    _integral_position_error[i]+=error;
    _integral_position_error[i]  = constrain(_integral_position_error[i], -_INTEGRAL_POSITION_ERROR_LIMIT[i],_INTEGRAL_POSITION_ERROR_LIMIT[i]);
    float I=_GAIN_POSITION_PID[i][1]*float(_integral_position_error[i]);
    float D=_GAIN_POSITION_PID[i][2]*float((error-_previous_position_error[i]))/_DT_MS;
    _previous_position_error[i]=error;
    _output_pwm[i]=int(constrain(P+I+D,-_MAX_PWM[i],_MAX_PWM[i]));
    }
  }
}

void __calc_ffpid_speed(){
  for(int i=0;i<6;i++){
    if(_MODE[i]==20){
      float F= _GAIN_SPEED_FFPID[i][0]*_goal_velocity[i];
      float error=_goal_velocity[i]-_current_velocity[i];
      float P=_GAIN_SPEED_FFPID[i][1]*error;
      _integral_velocity_error[i]+=error;
      _integral_velocity_error[i]  = constrain(_integral_velocity_error[i], -_INTEGRAL_VELOCITY_ERROR_LIMIT[i],_INTEGRAL_VELOCITY_ERROR_LIMIT[i]); 
      float I=_GAIN_SPEED_FFPID[i][2]*_integral_velocity_error[i];
      float D=_GAIN_SPEED_FFPID[i][3]*(error-_previous_velocity_error[i])/_DT_MS;
      _previous_velocity_error[i]=error;
      _output_pwm[i]=int(constrain(F+P+I+D,-_MAX_PWM[i],_MAX_PWM[i]));
    }
  }
}

void __timer_calc(){
  __calc_speed();
  __calc_pid_position();
  __calc_ffpid_speed();
}

void timer_setup(){
  Timer1.initialize(_DT_MS*1000); // 20msごとに割込み
  Timer1.attachInterrupt(__timer_calc);
}

void output(){
  for (int i = 0; i < 6 ; i++){   
    if(_MODE[i]!=0){
      int config_check=1;
      if(_DIRECTION_CONFIG[i]==1 ||_DIRECTION_CONFIG[i]==2){
          config_check=-1;
      }

      int pwm=int(config_check*_output_pwm[i]);
      if (pwm >= 0)
      {
          digitalWrite(_PINNUM_OUTPUT_DIR[i], _FORWARD_LEVEL[i]);
          analogWrite(_PINNUM_OUTPUT_PWM[i], pwm);
      }
      else
      {
          digitalWrite(_PINNUM_OUTPUT_DIR[i], 1 - _FORWARD_LEVEL[i]);
          analogWrite(_PINNUM_OUTPUT_PWM[i], (-1) * pwm);
      }
    }
    else {
      digitalWrite(_PINNUM_OUTPUT_DIR[i],LOW);
      analogWrite(_PINNUM_OUTPUT_PWM[i],0);
    }
  }
}

