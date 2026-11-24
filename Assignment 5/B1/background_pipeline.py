"""Deterministic simulation of constraint-aware background upload scheduling."""
import csv
from pathlib import Path

OUT = Path(__file__).parent
ITEMS = [
    {"id":"S1","priority":2,"size":4,"sensitive":1,"encrypted":1,"network":3,"battery":70,"doze":0,"permission":1},
    {"id":"S2","priority":1,"size":40,"sensitive":1,"encrypted":1,"network":1,"battery":65,"doze":0,"permission":1},
    {"id":"S3","priority":3,"size":8,"sensitive":0,"encrypted":1,"network":3,"battery":18,"doze":1,"permission":1},
    {"id":"S4","priority":5,"size":2,"sensitive":1,"encrypted":1,"network":0,"battery":55,"doze":0,"permission":1},
    {"id":"S5","priority":4,"size":12,"sensitive":1,"encrypted":0,"network":3,"battery":80,"doze":0,"permission":1},
    {"id":"S6","priority":5,"size":3,"sensitive":1,"encrypted":1,"network":3,"battery":60,"doze":0,"permission":0},
    {"id":"S7","priority":2,"size":6,"sensitive":0,"encrypted":1,"network":3,"battery":75,"doze":0,"permission":1},
]
def run(order):
    queue = sorted(ITEMS, key=(lambda x: -x["priority"]) if order=="priority" else (lambda x: ITEMS.index(x)))
    rows=[]; active=0; peak=0; ok=deferred=cancelled=0
    for x in queue:
        reason=""; status=""
        if not x["permission"]:
            status="cancelled"; reason="permission revoked"
            cancelled += 1
        elif not x["encrypted"]:
            status="rejected"; reason="payload not encrypted"
            cancelled += 1
        elif x["network"] < 2:
            status="deferred"; reason="network unavailable/weak"
            deferred += 1
        elif x["battery"] < 25 or x["doze"]:
            status="deferred"; reason="battery reserve/Doze"
            deferred += 1
        else:
            active += 1; peak=max(peak,active)
            status="success"; reason="encrypted upload acknowledged"
            ok += 1; active -= 1
        rows.append({"strategy":order,"id":x["id"],"priority":x["priority"],"status":status,"reason":reason,"network":x["network"],"battery":x["battery"]})
    return rows,{"strategy":order,"enqueued":len(ITEMS),"deferred":deferred,"cancelled_or_rejected":cancelled,"successful":ok,"peak_workers":peak,"residual_backlog":deferred}
def main():
    rows=[]; summary=[]
    for s in ("FIFO","priority"):
        r,m=run(s); rows += r; summary.append(m)
    with (OUT/"decision_log.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    with (OUT/"comparison.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)
    for x in summary: print(x)
    print("Tests: good-network upload=success; weak network/Doze/low battery=deferred; revoked permission=cancelled; plaintext=security rejection.")
if __name__=="__main__": main()
