# emit_speed [m/s] = 3.14*100/(60000*2.77) * rpm_mow
# 逆に, rpm[rpm] = 60000*2.77/(3.14*100)* emit_speed
print("emit_speed:"+str(3.14*100/(60000*2.77) * 0))
print("rpm:"+str(60000*2.77/(3.14*100) *1 ))

# move_speed [m/s] = 3.14*127/(60000*14) * rpm_now
# 逆に, rpm_now = 60000*14/(3.14*127) * move_speed [m/s] 
print("move_speed:"+str(3.14*127/(60000*14) * 1746))
print("rpm_now:"+str(60000*14/(3.14*127) *1 ))


