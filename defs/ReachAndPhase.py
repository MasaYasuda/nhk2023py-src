import numpy as np        
from defs import phase
import math

def RAP_def(pole_top,Y,h,w):
    Y_max=0.674
    X_max=(Y_max*w)/h

    
    theta_Y=phase.HighToTheta(pole_top[1].astype(int),int(h/2),Y_max)
    theta_X=phase.HighToTheta(pole_top[0].astype(int),int(w/2),X_max)

    Reach=Y/(math.cos(theta_X)*math.tan(theta_Y))

    return theta_X,Reach