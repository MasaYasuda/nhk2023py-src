import math
class Vector:
  '''
  HOW TO USE Vector class
  
  vector=nhk23.Vector() # make instance
  move,rot = vector.calc_vector(x,y,rotation)  # calc.vector using  x,y,rotation
  
  ********
  move : [a1,a2,a3,a4] -1~1
  rot : [ROT,ROT,ROT,ROT] -1~1
  ********
  '''
  def __init__ (self):
    self.move =[0]
    self.rot =[0]
  
  def calc_move(self,x,y):
    r = math.sqrt(x**2 + y**2) 
    if abs(r)<0.2:
      r=0
    r = max(-1, min(r, 1))
    theta = math.atan2(y, x) # rad
    
    x = r * math.cos(theta)/math.sqrt(2)
    y = r * math.sin(theta)/math.sqrt(2)
    self.move = [x - y, x + y, -x + y, -x - y]
    return
  
  def calc_rot(self,rot):
    if abs(rot)<0.2:
      rot=0
    rot = max(-1, min(rot, 1))
    self.rot = [rot,rot,rot,rot]
    return
  
  def calc_vector(self,x,y,rot):
    self.calc_move(x,y)
    self.calc_rot(rot)
    return self.move , self.rot


vector=Vector()
move,rot = vector.calc_vector(0.8,0.8,0) 
print(move)
print(rot)

