#ifndef _V1_CLASSES_H_
#define _V1_CLASSES_H_

void serial_receive();
void encoder_setup();
void __pinInterrupt0R();
void __pinInterrupt1R();
void __pinInterrupt2R();
void __pinInterrupt3R();
void __pinInterrupt4R();
void __pinInterrupt5R();
void __pinInterrupt0F();
void __pinInterrupt1F();
void __pinInterrupt2F();
void __pinInterrupt3F();
void __pinInterrupt4F();
void __pinInterrupt5F();

void timer_setup();
void __timer_calc();
void __calc_speed();
void __calc_pid_position();
void __calc_ffpid_speed();

void output();
void __clear_table(byte addr);

#endif // _V1_CLASSES_H_









