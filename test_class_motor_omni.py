# CORRECT

import nhk23


move=[0,1,0,-1]
rot=[1,1,1,1]


motor=nhk23.Motor("omni") # make instance
motor.omni_setup(127,306,1,30,200,[14,14,14,14])

output = motor.calc_omni_output(move,rot)  # move,rot is "Vector.move","Vector.rot"

print(motor.omni_speed)
print(output)

"""
move=[0.0, 1.0, 0.0, -1.0]
rot=[0, 0, 0, 0]


move=[0.7071067811865475, 0.7071067811865475, -0.7071067811865475, -0.7071067811865475]
rot=[0, 0, 0, 0]


"""

