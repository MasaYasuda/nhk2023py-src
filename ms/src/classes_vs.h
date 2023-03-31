#ifndef _CLASSES_V2_H_
#define _CLASSES_V2_H_


#include <Arduino.h>
#include <TimerOne.h>
#include <Wire.h>
#include "classes.h"


extern float storage[300];

void serial_receive();
void __serial_sumcheck();
void __serial_receive_radicon(int num , float value);
void __serial_receive_pid_position(int num , int value);
void __serial_receive_pid_speed(int num , float value);
void __serial_receive_mode(int num , int );
void __serial_receive_dir_config();
void __serial_receive_forward_lev();
void Pininterrupt();
void Timerinterrupt();

void calc_radicon();
void calc_pid_position();
void calc_pid_speed();
void output_all();










