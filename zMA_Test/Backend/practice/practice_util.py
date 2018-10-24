def showstat(status):
    mastered = 0
    reviewing = 0
    learning = 0
    for s in status.items():
        if s[1]=='green' :
            mastered += 1
        elif s[1]=='yellow' :
            reviewing += 1
        elif s[1]=='red':
            learning += 1
    return  mastered,reviewing,learning