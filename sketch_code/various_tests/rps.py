# 0 rock, 1 paper, 2 scissors
# winner x = 0, y = 1
# draw = 2
def rps(x,y):
    if x == y:
        return 2
    if x == 0:
        if y == 1:
            return 1
        else:
            return 0
    if x == 1:
        if y == 0:
            return 0
        else: 
            return 1
    if y == 0:
        return 1
    else:
        return 0

print(rps(2,2))
    