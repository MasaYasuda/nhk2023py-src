/**
 * @brief ウサギの引き込み制御用マイコン用関数
 * @date 23/4/2
 * 仮完成
 * @author Masanaga Yasuda
 * @par 依存関係に注意<br>
 * 
*/

#include <Arduino.h>
#include "rs_classes.h"
#include "v1_classes.h"

void setup(){
  Serial.begin(115200);
  rs_encoder_setup();
}
void loop(){
  serial_receive();
  rs_output();
}