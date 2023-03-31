# CORRECT

import kbhit

kb=kbhit.KBHit()

while 1:
    if kb.kbhit():
        char=kb.getch()
        print(char)
        break
    print("NON")