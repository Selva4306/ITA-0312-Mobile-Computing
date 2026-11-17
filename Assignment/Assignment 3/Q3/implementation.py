import csv
from pathlib import Path
edges=[("S","A"),("S","B"),("A","C"),("B","C"),("C","D"),("D","E")]
g={}
for a,b in edges:g.setdefault(a,[]).append(b);g.setdefault(b,[]).append(a)
def shortest(s,d):
 q=[(s,[s])]
 while q:
  u,p=q.pop(0)
  if u==d:return p
  for v in g.get(u,[]):
   if v not in p:q.append((v,p+[v]))
 return []
rows=[]
for s,d in [("S","E"),("A","D"),("B","E"),("S","C")]:
 p=shortest(s,d);h=len(p)-1
 rows.append({"source":s,"destination":d,"mesh_path":"-".join(p),"mesh_hops":h,"mesh_delay_ms":h*12,"cellular_air_hops":1,"cellular_core_assumed_ms":20,"cellular_total_model_ms":32})
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(*rows,sep="\\n")
