import csv

records=[
 {"id":"R1","priority":10,"size_kb":12,"sensitive":True,"encrypted":True,"conflict":False},
 {"id":"R2","priority":2,"size_kb":900,"sensitive":False,"encrypted":True,"conflict":False},
 {"id":"R3","priority":8,"size_kb":35,"sensitive":True,"encrypted":False,"conflict":False},
 {"id":"R4","priority":5,"size_kb":60,"sensitive":False,"encrypted":True,"conflict":True},
 {"id":"R5","priority":1,"size_kb":8,"sensitive":False,"encrypted":True,"conflict":False},
]

def sync(records, network= "GOOD", battery=55, eventual=False):
    rows=[]
    for r in records:
        if r["sensitive"] and not r["encrypted"]:
            action="REJECT_UNENCRYPTED"
        elif r["conflict"]:
            action="RESOLVE_CONFLICT"
        elif network!="GOOD" and r["size_kb"]>50:
            action="DEFER_NETWORK"
        elif battery<20 and r["priority"]<8:
            action="DEFER_BATTERY"
        elif eventual and network!="GOOD":
            action="QUEUE_EVENTUAL"
        else:
            action="UPLOAD"
        rows.append([r["id"],r["priority"],r["size_kb"],r["sensitive"],r["encrypted"],r["conflict"],action])
    return rows

def main():
    rows=sync(records)
    with open("a2_sync_decisions.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["record","priority","size_kb","sensitive","encrypted","conflict","decision"]); w.writerows(rows)
    for row in rows: print(row[0],row[-1])
    print("Offline-first alternative:",[(r["id"],a[-1]) for r,a in zip(records,sync(records,"POOR",12,True))])

if __name__=="__main__": main()
