import math
T0=29177
for demand in (100000,200000,300000):
    k=max(0,math.ceil(math.log(demand/T0,4)))
    print(f"demand={demand}: uniform split rounds={k}, sites={19*4**k}, radius={.5/2**k:.3f} km")
def selective_rounds(demand,capacity,f):
    return 0 if demand<=capacity else math.ceil(math.log(demand/capacity)/math.log(1+3*f))
print("100k demand, selective split f=0.5:",selective_rounds(100000,T0,.5),"rounds")
