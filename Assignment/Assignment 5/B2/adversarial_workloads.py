"""Equal-size workload experiment: easy vs constraint-adversarial."""
import csv
from pathlib import Path
OUT=Path(__file__).parent
EASY=[(3,3,80,1),(3,3,75,1),(2,3,70,1),(2,3,65,1),(1,3,60,1),(1,3,55,1),(2,3,50,1),(1,3,45,1)]
HARD=[(3,0,80,1),(3,1,18,1),(2,0,70,1),(2,3,20,1),(1,1,60,1),(1,0,55,1),(2,1,22,1),(1,3,19,0)]
def evaluate(name, data):
    rows=[]; success=defer=cancel=0; attempts=0
    for i,(priority,net,battery,permission) in enumerate(data,1):
        attempts+=1
        if not permission: status="cancelled"; cancel+=1; why="permission revoked"
        elif net<2: status="deferred"; defer+=1; why="network below threshold"
        elif battery<25: status="deferred"; defer+=1; why="battery below reserve"
        else: status="delivered"; success+=1; why="constraints satisfied"
        rows.append({"workload":name,"record":f"R{i}","priority":priority,"network":net,"battery":battery,"permission":permission,"status":status,"reason":why})
    return rows,{"workload":name,"records":len(data),"processed":attempts,"deferrals":defer,"cancellations":cancel,"deliveries":success}
def main():
    a,ma=evaluate("A_easy",EASY); b,mb=evaluate("B_adversarial",HARD); rows=a+b; summary=[ma,mb]
    for name,data in (("workload_trace.csv",rows),("summary.csv",summary)):
        with (OUT/name).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
    print("Prediction: B requires more deferred/rejected handling because most records violate network, battery or permission constraints.")
    for x in summary: print(x)
if __name__=="__main__": main()
