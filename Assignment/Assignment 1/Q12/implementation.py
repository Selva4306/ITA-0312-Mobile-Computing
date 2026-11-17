# Task-specific implementation for Q12
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
traffic=25000*.05
for name,n,r in [("Macro N=7",7,.5),("Temporary N=3",3,.25)]:
 sites=math.ceil(1/(3*math.sqrt(3)*r*r/2)); ch=336//n; per=traffic/sites
 print(f"{name}: sites={sites}, channels/site={ch}, load/site={per:.1f} E, blocking={erlang_b(ch,per):.1%}")
print(f"N=3 capacity/site at 2%={capacity(112):.3f} E; minimum sites={math.ceil(traffic/capacity(112))}; plan 15-16 with margin.")
