import csv
from collections import deque
from pathlib import Path
# AODV route discovery: flood one RREQ per node, record reverse paths,
# then return an RREP along the reverse path from destination to source.
graph={"S":["A","B"],"A":["S","C"],"B":["S","C"],"C":["A","B","Y"],"Y":["C","X","D"],"X":["B","Y"],"D":["Y"]}
def discover(source,destination):
    q=deque([source]); parent={source:None}; events=[]
    while q:
        u=q.popleft(); events.append({"node":u,"event":"RREQ_RECEIVE","decision":"destination" if u==destination else "rebroadcast"})
        if u==destination: break
        for v in graph[u]:
            if v not in parent: parent[v]=u; q.append(v)
    if destination not in parent:return [],events
    path=[];u=destination
    while u is not None:path.append(u);u=parent[u]
    path.reverse()
    for u in reversed(path):events.append({"node":u,"event":"RREP_RECEIVE","decision":"install_forward_route"})
    return path,events
path,events=discover("S","D")
with Path(__file__).with_name("route_trace.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["node","event","decision"]);w.writeheader();w.writerows(events)
# Flow-load observations transcribed from the assignment's model dataset.
rows=[(2,.98,95.2),(8,1.67,95.6),(20,3.32,94.4)]
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["active_flows","aodv_overhead_kBps","delivery_pct","control_behaviour"])
    for flow,over,delivery in rows:w.writerow([flow,over,delivery,"RREQ/RREP on demand; RERR on break; 1 Hz hello"])
print("Discovered route:", " -> ".join(path));print("Wrote route_trace.csv and output.csv")
