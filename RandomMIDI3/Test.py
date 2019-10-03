from enum import Enum


class aaa(Enum):
    a = 0
    b = 1
    c = 2
    d = "c"


print(aaa[aaa.d.value].value)
