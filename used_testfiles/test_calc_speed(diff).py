import math

class DiffDrive:
  """差動二輪制御用モーター回転量計算

  Parameters
  ----------
  __DIAMETER :float
  __DISTANCE : float
  __MAX_MOVE :  float
  __MAX_ROT : float
  __GEAR_RATIO :int
    最終的なタイヤの回転量と観測エンコーダーの回転量の比

  """
  def __init__(self,diameter=0.0,distance=0.0,max_move=0.0,max_rot=0.0,gear_ratio=0.0):
    """差動二輪制御用モーター回転量計算

    Parameters
    ----------
    diameter : float, optional
        直径[mm], by default 0.0
    distance : float, optional
        対角線長[mm], by default 0.0
    max_move : float, optional
        最大移動速度[m/s], by default 0.0
    max_rot : float, optional
        最大旋回速度[rpm], by default 0.0
    gear_ratio : float, optional
        最終的な出力回転量と観測エンコーダーの回転量の比
        =エンコーダーの観測回転量/出力1回転
        , by default 0.0
    """
    
    self.__DIAMETER =diameter
    self.__DISTANCE=distance
    self.__MAX_MOVE=max_move
    self.__MAX_ROT=max_rot
    self.__GEAR_RATIO=gear_ratio
    
  def calc_speed_radicon(self,move,rot):
    """ラジコン制御用各エンコーダーの目標観測回転量の算出

    Parameters
    ----------
    move : float
        -1~1で示される前後移動の強さ
    rot : float
        -1~1で示される回転運動の強さ
        
    Returns 
    ----------
    R_speed :
      -1~1で示される右車輪の回転量の大きさ 
    L_speed :
      -1~1で示される左車輪の回転量の大きさ
      
    """
    R_speed = move - rot
    L_speed = move + rot

    # 大きすぎる値（1以上）のとき圧縮する
    R_abs = abs(R_speed)  # 絶対値を求める
    L_abs = abs(L_speed)  # 絶対値を求める

    if R_abs > 1 or L_abs > 1:
        if R_abs >= L_abs:
            R_speed = R_speed / R_abs  # 圧縮
            L_speed = L_speed / R_abs  # 圧縮
        elif R_abs < L_abs:
            R_speed = R_speed / L_abs
            L_speed = L_speed / L_abs
            
    return R_speed,L_speed
    
  def calc_speed(self,move,rot):
    """フィードバック制御用各エンコーダーの目標観測回転量の算出
    配列は右前、左前、左後、右後 の順

    Parameters
    ----------
    move : float
        -1~1で示される前後移動の強さ
    rot : float
        -1~1で示される回転運動の強さ
        
    Returns
    -------
    R_speed :
      右車輪エンコーダーの目標観測回転量 [rpm]
    L_speed :
      左車輪エンコーダーの目標観測回転量 [rpm]
    """
  
    mv=self.__MAX_MOVE * move * 2 * 30000 / self.__DIAMETER /math.pi # N[rpm]=30*v[m/s]/(r[mm]*pi)
    rt=self.__MAX_ROT * rot *self.__DISTANCE/ self.__DIAMETER # v[m/s]=ω*r=ω'*r'
    R_speed=(mv+rt)*self.__GEAR_RATIO
    L_speed=(mv-rt)*self.__GEAR_RATIO
    return R_speed,L_speed
  
diff=DiffDrive(127,254,0.5,30,24)
print(diff.calc_speed(-1,1))