import csv
from pathlib import Path
N=2000
rows=[]
for availability in (0.90,0.60,0.30):
    online=round(N*availability)
    offline=N-online
    rows.append({"availability":availability,"strategy":"immediate","generated":N,"delivered":online,"delayed":0,"lost":offline,"delivery_pct":round(100*online/N,2),"mean_delay_s":0.012})
    # Store-and-forward eventually delivers every queued record. Waiting time
    # is an exponential availability approximation with mean 30/a seconds.
    mean_wait=(1-availability)*30/availability
    rows.append({"availability":availability,"strategy":"store_forward","generated":N,"delivered":N,"delayed":offline,"lost":0,"delivery_pct":100.0,"mean_delay_s":round(availability*.012+(1-availability)*(mean_wait+.012),4)})
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print("Q1 deterministic availability model; N=2000 per case");print(*rows,sep="\\n")
