import msvcrt

while 1:
    if msvcrt.kbhit():
        print("FIN")     
        break
    print("NOW HIT")


