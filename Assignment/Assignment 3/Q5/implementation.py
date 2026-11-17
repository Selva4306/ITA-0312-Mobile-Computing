import csv
from pathlib import Path
# DSDV-style shortest-hop table convergence with destination sequence numbers.
def converge(nodes,edges,seq):
    routes={u:{u:(u,0,seq[u])} for u in nodes}
    changed=True
    while changed:
        changed=False
        for u,v in edges:
            for src,dst in ((u,v),(v,u)):
                for dest,(nxt,hop,sn) in list(routes[dst].items()):
                    cand=(dst,hop+1,sn)
                    old=routes[src].get(dest)
                    if old is None or sn>old[2] or (sn==old[2] and cand[1]<old[1]):
                        routes[src][dest]=cand;changed=True
    return routes
nodes=list("ABCDE"); edges=[("A","B"),("A","C"),("B","D"),("C","D"),("D","E")]
seq={"A":100,"B":202,"C":304,"D":406,"E":508}
before=converge(nodes,edges,seq)
# Link D-E fails; E reattaches to C and advertises a newer even sequence.
new_edges=[e for e in edges if set(e)!={"D","E"}]+[("C","E")]
seq["E"]=510
after=converge(nodes,new_edges,seq)
trace=[]
for label,table in (("before",before),("after",after)):
    for dest,(nxt,hop,sn) in sorted(table["A"].items()):
        trace.append({"phase":label,"source":"A","destination":dest,"next_hop":nxt,"hop_count":hop,"sequence_number":sn})
with Path(__file__).with_name("route_trace.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=trace[0].keys());w.writeheader();w.writerows(trace)
rows=[]
for n in (10,20,40,60,80):
    rows.append({"nodes":n,"update_interval_s":5,"header_B":24,"entry_B":12,"dsdv_full_dump_Bps":round(n*(24+12*n)/5,2),"complexity":"O(N^2)"})
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print("A to E before:",before["A"]["E"],"; after:",after["A"]["E"])
print("Wrote route_trace.csv and output.csv")
