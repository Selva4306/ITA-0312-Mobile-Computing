from dataclasses import dataclass
from collections import deque
import csv

@dataclass
class Task:
    task_id: str
    domain: str
    priority: int
    ready: bool = True
    attempts: int = 0
    status: str = "PENDING"

def schedule_or_execute(tasks, available=True, battery=70, permission=True):
    queue=deque(sorted(tasks,key=lambda t:t.priority,reverse=True))
    log=[]
    while queue:
        t=queue.popleft()
        t.attempts+=1
        if not permission and t.domain in ("SENSOR","SYNC"):
            t.status="CANCELLED_PERMISSION"
        elif battery<15:
            t.status="DEFER_LOW_BATTERY"
        elif not available and t.domain in ("SYNC","PUSH"):
            t.status="DEFER_OFFLINE"
        elif not t.ready:
            t.status="DEFER_NOT_READY"
        else:
            t.status="EXECUTED"
        log.append([t.task_id,t.domain,t.priority,t.attempts,t.status])
    return log

def main():
    tasks=[Task("S1","SENSOR",4),Task("D1","SYNC",3),Task("P1","PUSH",5)]
    rows=schedule_or_execute(tasks)
    with open("a3_framework_run.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["task_id","domain","priority","attempts","result"]); w.writerows(rows)
    for row in rows: print(row)

if __name__=="__main__": main()
