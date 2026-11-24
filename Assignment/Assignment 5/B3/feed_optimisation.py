"""Exhaustive vs adaptive feed configuration experiment."""
import csv
from itertools import product
from pathlib import Path
OUT=Path(__file__).parent
# quality levels 1..3, cache sizes 1..3, prefetch windows 0..2
def cost(q,c,p,load):
    frame=max(7, 9 + load*2 + q*2 - c*1.5 - p*1.0)
    energy=2.0*q + 0.8*c + 0.6*p
    drops=max(0,frame-16)*4
    return round(drops+energy,2),round(frame,2),round(energy,2)
def exact(load):
    candidates=[]
    for q,c,p in product(range(1,4),range(1,4),range(0,3)):
        v=cost(q,c,p,load); candidates.append((v[0],q,c,p,v[1],v[2]))
    return min(candidates)
def adaptive(load):
    q,c,p=3,2,2; changes=0
    while True:
        cur=cost(q,c,p,load)
        if cur[1]>16 and (q>1 or c<3 or p>0):
            if q>1: q-=1
            elif p>0: p-=1
            else: c+=1
            changes+=1
        else: break
        if changes>10: break
    v=cost(q,c,p,load)
    return (v[0],q,c,p,v[1],v[2],changes)
def main():
    cases=[("light",1),("medium",3),("heavy",5),("counterexample",2)]
    rows=[]
    for name,load in cases:
        e=exact(load); a=adaptive(load)
        rows.append({"case":name,"load":load,"exact_cost":e[0],"approx_cost":a[0],"match":int(e[0]==a[0]),"exact_q":e[1],"exact_cache":e[2],"exact_prefetch":e[3],"adaptive_q":a[1],"adaptive_cache":a[2],"adaptive_prefetch":a[3],"adaptive_changes":a[6]})
    with (OUT/"cost_comparison.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    sizes=[]
    for n in (3,6,12,24):
        count=0
        for _ in range(n):
            for q,c,p in product(range(1,4),range(1,4),range(0,3)):
                cost(q,c,p,3);count+=1
        sizes.append({"feed_items":n,"quality_levels":3,"cache_levels":3,"prefetch_levels":3,"exact_config_evaluations":count,"adaptive_decision_steps":n*3})
    with (OUT/"scalability.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=sizes[0].keys());w.writeheader();w.writerows(sizes)
    for r in rows: print(r)
    print("Scalability:",sizes)
if __name__=="__main__":main()
