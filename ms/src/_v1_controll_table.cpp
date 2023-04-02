#include <Arduino.h>

byte _PINNUM_ENCODER_A[6] = {22, 23, 24, 25, 26, 27};
byte _PINNUM_ENCODER_B[6] = {0, 1, 5, 4, 3, 2};
byte _PINNUM_OUTPUT_DIR[6] = {28, 29, 30, 31, 32, 33};
byte _PINNUM_OUTPUT_PWM[6]{4, 5, 6, 7, 8, 9};
int _RESOLUTION[6] = {512, 512, 512, 512, 2048, 2048};
byte __common_max_pwm = 240;
byte _MAX_PWM[6] = {240, 240, 240, 240, 240, 240};
float __common_gain_position_pid[3] = {0.001, 0.000, 0.0};
float _GAIN_POSITION_PID[6][3] = {
    {__common_gain_position_pid[0], __common_gain_position_pid[1], __common_gain_position_pid[2]},
    {__common_gain_position_pid[0], __common_gain_position_pid[1], __common_gain_position_pid[2]},
    {__common_gain_position_pid[0], __common_gain_position_pid[1], __common_gain_position_pid[2]},
    {__common_gain_position_pid[0], __common_gain_position_pid[1], __common_gain_position_pid[2]},
    {__common_gain_position_pid[0], __common_gain_position_pid[1], __common_gain_position_pid[2]},
    {__common_gain_position_pid[0], __common_gain_position_pid[1], __common_gain_position_pid[2]},
};
float __common_gain_speed_ffpid[4] = {0.10 / 1058, 0.0, 0.00002, 0.000};
float _GAIN_SPEED_FFPID[6][4] = {
    {__common_gain_speed_ffpid[0], __common_gain_speed_ffpid[1], __common_gain_speed_ffpid[2], __common_gain_speed_ffpid[3]}, 
    {__common_gain_speed_ffpid[0], __common_gain_speed_ffpid[1], __common_gain_speed_ffpid[2], __common_gain_speed_ffpid[3]}, 
    {__common_gain_speed_ffpid[0], __common_gain_speed_ffpid[1], __common_gain_speed_ffpid[2], __common_gain_speed_ffpid[3]}, 
    {__common_gain_speed_ffpid[0], __common_gain_speed_ffpid[1], __common_gain_speed_ffpid[2], __common_gain_speed_ffpid[3]}, 
    {__common_gain_speed_ffpid[0], __common_gain_speed_ffpid[1], __common_gain_speed_ffpid[2], __common_gain_speed_ffpid[3]}, 
    {__common_gain_speed_ffpid[0], __common_gain_speed_ffpid[1], __common_gain_speed_ffpid[2], __common_gain_speed_ffpid[3]}
};
long __common_integral_position_error_limit = 100000000;
long _INTEGRAL_POSITION_ERROR_LIMIT[6] = {
    __common_integral_position_error_limit, __common_integral_position_error_limit, __common_integral_position_error_limit, __common_integral_position_error_limit, __common_integral_position_error_limit, __common_integral_position_error_limit};
float __common_integral_speed_error_limit = 100000000;
float _INTEGRAL_VELOCITY_ERROR_LIMIT[6] = {
    __common_integral_speed_error_limit, __common_integral_speed_error_limit, __common_integral_speed_error_limit, __common_integral_speed_error_limit, __common_integral_speed_error_limit, __common_integral_speed_error_limit};
byte _MODE[6] = {0};
byte _DIRECTION_CONFIG[6] = {0};
byte _FORWARD_LEVEL[6] = {0};
byte _DT_MS=20;

volatile long _current_position[6] = {0};
float _current_velocity[6] = {0};
long _goal_position[6] = {0};
float _goal_velocity[6] = {0};
int _output_pwm[6] = {0};
int _previous_position_error[6] = {0};
float _previous_velocity_error[6] = {0};
long _integral_position_error[6] = {0};
float _integral_velocity_error[6] = {0};