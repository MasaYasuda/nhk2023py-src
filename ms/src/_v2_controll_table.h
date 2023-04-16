#ifndef __V2_CONTROLL_TABLE_H_
#define __V2_CONTROLL_TABLE_H_

/**
 * これは接触スイッチとAir操作も併用したコントロールテーブルです（試験的）
*/


extern byte _PINNUM_ENCODER_A[6];
extern byte _PINNUM_ENCODER_B[6];
extern byte _PINNUM_INPUT_A[6];
extern byte _PINNUM_INPUT_B[6];

extern byte _PINNUM_OUTPUT_DIR[6];
extern byte _PINNUM_OUTPUT_PWM[6];
extern int _RESOLUTION[6];
extern byte __common_max_pwm;
extern byte _MAX_PWM[6];
extern float __common_gain_position_pid[3];
extern float _GAIN_POSITION_PID[6][3];
extern float __common_gain_speed_ffpid[4];
extern float _GAIN_SPEED_FFPID[6][4];
extern long __common_integral_position_error_limit;
extern long _INTEGRAL_POSITION_ERROR_LIMIT[6];
extern float _INTEGRAL_VELOCITY_ERROR_LIMIT[6] ;
extern byte _MODE[6];
extern byte _DIRECTION_CONFIG[6];
extern byte _FORWARD_LEVEL[6];
extern byte _DT_MS;

extern volatile long _current_position[6];
extern float _current_velocity[6];

extern long _goal_position[6];
extern float _goal_velocity[6];
extern int _output_pwm[6];
extern byte _output_air[12];
extern int _previous_position_error[6];
extern float _previous_velocity_error[6];
extern long _integral_position_error[6];
extern float _integral_velocity_error[6];

extern byte _sw_index[6];

#endif // __V2_CONTROLL_TABLE_H_