# CORRECT

import nhk23

spin=1

motor=nhk23.Motor("roller") # make instance
motor.roller_setup(100,10,2.77)

output = motor.calc_roller_output(1)
print(motor.roller_speed)
print(output)
