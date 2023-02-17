import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
    
while 1:
    if getch() == chr(0x1b):
        break

    print("PIKAPIKA") 