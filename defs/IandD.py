def IANdD(L_power,R_power,L_log,R_log,L_I,R_I):
    L_D=L_power-L_log
    R_D=R_power-R_log
    L_I+=L_D
    R_I+=R_D
    return L_I,R_I,L_D,R_D
