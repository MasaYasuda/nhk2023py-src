# nhk2023py-src

this is the codes for Robots made by Grobo in NHK2023

forward_level
 polulu:1 , cytron 0

-----------RABBIT---------
定義：前＝射出方向

差動二輪
 [R,L]
 速度型FFPID
 エンコーダー分解度=512
 MAX_PWM=240
 FFPIDゲイン=0,0,0.01,0
 integral_speed_error_limit = 100000
 direction_config=[2,0]
 設定:DiffDrive(127,254,0.4,30,28)　一応もっと出せるはず
 上設定推奨最大値:move=1 , rot=1

射出ローラー
 [上、下]
 速度型FFPID
 エンコーダー分解度＝256
 MAX_PWM=240
 FFPIDゲイン=?,?,?,?
 integral_speed_error_limit = 100000?
 direction_config=[?,?]  多分[3,0]
 設定:SingleDrive(100,10,2.77)

昇降モーター
 [single]
 ラジコン
 MAX_PWM=240
 direction_config=[?]
 モーター正転＝
 上限界検出スイッチ＝A
 下限界検出スイッチ＝B
 推奨速度：
 
引き込みラッピニ
 [single]
 ラジコン
 MAX_PWM=240
 direction_config=[0]
 戻し限界検出スイッチ＝A
 引き込み限界検出スイッチ＝B
 推奨速度：正回転(=戻し)=0.3
           負回転(=引き込み)=0.5

Dynamixelハンド
  ID1(右手):2500~3800(開) kakunou=2138  kai =3803 chokkaku=3193   hoji=2922
  ID2(左手):500(開)~1870  kakunou=2115  kai = 324 chokkaku=959  hoji=1252

----------ELEPHANT----------
定義：前＝射出方向

4輪メカナム
[R,L]
 速度型FFPID
 エンコーダー分解度=512
 MAX_PWM=240
 FFPIDゲイン=0,0,0.01,0
 integral_speed_error_limit = 100000
 direction_config=[2,0]
 設定:DiffDrive(127,254,0.4,30,28)　一応もっと出せるはず
 上設定推奨最大値:move=1 , rot=1

 [右前,左前,左後,右後]
 速度型FFPID
 エンコーダー分解度=360?
 MAX_PWM=240
 FFPIDゲイン=0,0,0.01,0
 integral_speed_error_limit = 100000
 direction_config=[?,?,?,?]

射出ローラー
 [上、下]
 速度型FFPID
 エンコーダー分解度＝256
 MAX_PWM=240
 FFPIDゲイン=?,?,?,?
 integral_speed_error_limit = 100000?
 direction_config=[?,?]  多分[3,0]
 設定:SingleDrive(100,10,2.77)

引き込みエアシリ
　[1段目,2段目]


昇降モーター
 [R,L]
 [上、下]
 速度型FFPID
 エンコーダー分解度＝256
 MAX_PWM=240
 FFPIDゲイン=?,?,?,?
 direction_config=[?,?]  

Dynamixelハンド
  右手　Dynamixel MAX開き 1350~2048 前ならえ
　左手　Dynamixel 前ならえ　1900~2600 MAX開き