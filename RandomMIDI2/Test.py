from ObjectModel import *
a = LimitData()
for i in a.title:
    print(i)
    a[i] = 1
print(a.scale)
LimitData().scale
