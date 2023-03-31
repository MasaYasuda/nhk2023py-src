import nhk23

move=[-1/1.41421353,1/1.41421353,1/1.41421353,-1/1.41421353]
rot=[1,1,1,1]
motor=nhk23.Motor("omni")

print(motor.calc_omni_output_for_radicon(move,rot))