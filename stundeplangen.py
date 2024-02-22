h=8
m=15
d=0
for d in range(10):
    x = str(h).zfill(2)
    y = str(h+1).zfill(2)
    print(x+":15-"+y+":00")
    h += 1

