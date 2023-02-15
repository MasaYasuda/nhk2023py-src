#include <Arduino.h>

/*

float order_rpm[6]={0};

*/

/*
プロトコルの想定
ーーー
1バイト目＝0xFF（all 1）
2バイト目＝モーター番号 （0~5）
3～６バイト目＝回転速度（rpm）
ーーー
*/

void orderRead()
{
  if (Serial.read() == 0xFF)
  {
    int data1 = Serial.read();
    order_rpm[data1] = Serial.parseFloat();
  }
}
//
