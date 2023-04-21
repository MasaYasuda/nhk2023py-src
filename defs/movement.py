import numpy as np

def phase(phase_X,border_phase,PID,L_I,R_I,L_D,R_D):

    if(abs(phase_X)>border_phase):
        L_move=PID[0]*phase_X-PID[2]*(L_D)#+PID[1]*L_I
        R_move=PID[0]*phase_X-PID[2]*(R_D)#+PID[1]*R_I
    elif(phase_X>0):
        PID*=[1,1,1]#微調整の細かさ
        L_move=PID[0]*phase_X+PID[1]*L_I-PID[2]*(L_D)
        R_move=0.0
    else:        
        PID*=[1,1,1]#微調整の細かさ
        R_move=PID[0]*phase_X+PID[1]*R_I-PID[2]*(R_D)
        L_move=0.0

    return L_move,R_move


        