import numpy as np
import math

def HighToTheta(High,
                Half_Highmax,
                tanmax):
    """
    param
    -----
    High:int
    Half_Highmax:int
    tanmax:float

    return
    ------
    theta:float
    """

    #print(High.shape)
    High=Half_Highmax-High
    High2=np.zeros(High.shape,float)
    HS=High.shape[0]
    #print(High2.shape)
    for i in range(1,HS):
        #print(i)
        #print(High[i])
        High2[i]=math.atan2(High[i]*tanmax,Half_Highmax)
        print(math.degrees(High2[i]))
    return High2


"""
HHM=720/2
H=600
tanmax=0.674

theta=HighToTheta(H,HHM,tanmax)

print(math.degrees(theta))
print(math.degrees(math.atan(tanmax)))
"""