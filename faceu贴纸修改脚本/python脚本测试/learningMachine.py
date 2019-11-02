import math


def l(u,v):
    return math.pow(u*math.exp(v) - 2*v*math.exp(-u), 2)

def ud(u,v):
    return 2*(u*math.exp(v) - 2*v*math.exp(-u))*(math.exp(v) + 2*v*math.exp(-u))

def vd(u,v):
    return 2*(u*math.exp(v) - 2*v*math.exp(-u))*(u*math.exp(v) - 2*math.exp(-u))

v = 1.0
u = 1.0
rate = 0.1
count = 0
while l(u,v) > math.pow(10,-14):
    temp = u
    u = u - rate*ud(u,v)
    v = v - rate*vd(temp,v)
    count += 1
    print(count)
print("----------------")
print(count)
print(u, "   ",v)
print(l(u,v))