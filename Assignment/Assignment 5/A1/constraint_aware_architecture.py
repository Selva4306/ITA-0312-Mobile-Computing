from dataclasses import dataclass, field
from collections import deque
import csv

@dataclass
class Work:
    wid: str
    kind: str
    priority: int
    sensitive: bool = False
    critical: bool = False
    status: str = "PENDING"

@dataclass
class Runtime:
    battery: int = 80
    network: bool = True
    doze: bool = False
    permission: bool = True
    logged_in: bool = True
    queue: deque = field(default_factory=deque)
    uploaded: list = field(default_factory=list)
    notifications: list = field(default_factory=list)
    trace: list = field(default_factory=list)

def feasible(w, s):
    if not s.logged_in:
        return "CANCEL_LOGOUT"
    if w.sensitive and not s.permission:
        return "REJECT_PERMISSION"
    if w.sensitive and not s.logged_in:
        return "REJECT_PRIVACY"
    if s.battery < 15 or s.doze:
        return "DEFER_POWER"
    if w.kind == "UPLOAD" and not s.network:
        return "DEFER_NETWORK"
    return "RUN"

def run():
    s=Runtime()
    events=[
        ("E1","SENSOR",{"battery":78}),
        ("E2","UPLOAD",{"network":True}),
        ("E3","DOZE",{"doze":True}),
        ("E4","CRITICAL",{"doze":False}),
        ("E5","LOGOUT",{"logged_in":False}),
    ]
    work=[Work("W1","COLLECT",1),Work("W2","UPLOAD",2,True),Work("W3","UPLOAD",1,True),Work("W4","ALERT",10,False,True)]
    for e,kind,change in events:
        for k,v in change.items(): setattr(s,k,v)
        if kind=="SENSOR":
            s.queue.append(work[0])
        elif kind=="UPLOAD":
            s.queue.append(work[1])
        elif kind=="DOZE":
            s.queue.append(work[2])
        elif kind=="CRITICAL":
            s.queue.append(work[3])
        elif kind=="LOGOUT":
            for w in list(s.queue):
                if w.sensitive: w.status="CANCELLED"
            s.queue=deque(w for w in s.queue if w.status=="PENDING")
        while s.queue:
            w=s.queue.popleft()
            decision=feasible(w,s)
            if decision=="RUN":
                w.status="SUCCESS"
                if w.kind=="UPLOAD": s.uploaded.append(w.wid)
                if w.critical: s.notifications.append(w.wid)
            elif decision.startswith("CANCEL") or decision.startswith("REJECT"):
                w.status=decision
            else:
                w.status=decision
                s.queue.append(w)
                break
            s.trace.append([e,w.wid,w.kind,decision,s.battery,s.network,s.doze,s.permission,s.logged_in])
        if kind=="LOGOUT":
            s.trace.append([e,"ALL","SESSION","CANCEL_PENDING",s.battery,s.network,s.doze,s.permission,s.logged_in])
    with open("a1_execution_trace.csv","w",newline="") as f:
        out=csv.writer(f); out.writerow(["event","work_id","type","decision","battery","network","doze","permission","logged_in"]); out.writerows(s.trace)
    print("Uploaded:",s.uploaded,"Notifications:",s.notifications)
    print("Trace rows:",len(s.trace),"Remaining backlog:",[w.wid for w in s.queue])

if __name__=="__main__": run()
