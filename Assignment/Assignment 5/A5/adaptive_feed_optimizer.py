from itertools import product
import csv

# Cost balances frame-time violations, energy and memory pressure.
def cost(q,cache,prefetch,device):
    frame=max(5,device["base_ms"] + q*2.4 + prefetch*0.7 - cache*0.9)
    energy= device["base_energy"] + q*1.8 + cache*0.8 + prefetch*0.5
    memory=cache*18 + prefetch*7
    drops=max(0,frame-16)
    return round(drops*8 + energy + max(0,memory-device["memory_mb"])*0.15,2),round(frame,2),round(energy,2),memory

def exact(device):
    options=[]
    for q,c,p in product([1,2,3],[1,2,3],[0,1,2]):
        v=cost(q,c,p,device)
        options.append((v[0],q,c,p,*v[1:]))
    return min(options)

def adaptive(device):
    q,c,p=2,2,1
    history=[]
    for step in range(8):
        before=cost(q,c,p,device)
        candidates=[(q,c,p),(max(1,q-1),c,p),(q,min(3,c+1),p),(q,c,max(0,p-1))]
        scored=[(cost(*x,device)[0],x) for x in candidates]
        best=min(scored,key=lambda x:x[0])[1]
        history.append([step,q,c,p,*before])
        if best==(q,c,p): break
        q,c,p=best
    v=cost(q,c,p,device)
    return (v[0],q,c,p,v[1],v[2],v[3]),history

def main():
    devices=[
      {"name":"Low-end","base_ms":14,"base_energy":3,"memory_mb":80},
      {"name":"Mid-range","base_ms":10,"base_energy":4,"memory_mb":120},
      {"name":"Flagship","base_ms":7,"base_energy":5,"memory_mb":180},
    ]
    rows=[]
    traces=[]
    for d in devices:
        e=exact(d); a,h=adaptive(d)
        rows.append([d["name"],*e,*a,"MATCH" if e[0]==a[0] else "DIFFERENT"])
        for x in h: traces.append([d["name"],*x])
    with open("a5_optimizer_comparison.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["device","exact_cost","exact_quality","exact_cache","exact_prefetch","exact_frame_ms","exact_energy","exact_memory_mb","adaptive_cost","adaptive_quality","adaptive_cache","adaptive_prefetch","adaptive_frame_ms","adaptive_energy","adaptive_memory_mb","result"]); w.writerows(rows)
    with open("a5_adaptive_trace.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["device","step","quality","cache","prefetch","cost","frame_ms","energy","memory_mb"]); w.writerows(traces)
    for r in rows: print(r[0],"exact=",r[1],"adaptive=",r[8],r[-1])

if __name__=="__main__": main()
