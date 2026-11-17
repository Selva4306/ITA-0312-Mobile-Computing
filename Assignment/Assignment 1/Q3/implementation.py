# Task-specific implementation for Q3
import math
def erlang_b(c,a):
    b=1.0
    for m in range(1,c+1): b=a*b/(m+a*b)
    return b
def capacity(c,target=.02):
    lo,hi=0.0,c*3.0
    for _ in range(80):
        mid=(lo+hi)/2
        if erlang_b(c,mid)<=target: lo=mid
        else: hi=mid
    return lo
area=3*math.sqrt(3)*.5*.5/2
sites=math.ceil(12/area)
for n in (3,4,7,12):
    q=math.sqrt(3*n); c=336//n
    print(f"N={n}, Q={q:.3f}, D={.5*q:.3f} km, channels/cell={c}, sites={sites}, Erlangs/cell@2%={capacity(c):.3f}")
print("N=7,n=4 ideal SIR:",10*math.log10((3*7)**2/6),"dB")
