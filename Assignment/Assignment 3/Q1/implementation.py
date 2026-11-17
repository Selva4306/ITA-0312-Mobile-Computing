import csv, random
from pathlib import Path
SEED=4306
N=2000
rng=random.Random(SEED)
rows=[]
for availability in (0.90,0.60,0.30):
    for strategy in ("immediate","store_forward"):
        delivered=delayed=lost=0; delays=[]
        for _ in range(N):
            online=rng.random()<availability
            if strategy=="immediate":
                if online: delivered+=1; delays.append(0.012)
                else: lost+=1
            elif online:
                delivered+=1; delays.append(0.012)
            else:
                delayed+=1; delivered+=1
                delays.append(rng.expovariate(availability/30.0)+0.012)
        rows.append({"availability":availability,"strategy":strategy,"generated":N,"delivered":delivered,"delayed":delayed,"lost":lost,"delivery_pct":round(100*delivered/N,2),"mean_delay_s":round(sum(delays)/len(delays),4) if delays else ""})
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print("Q1 complete; fixed seed",SEED);print(*rows,sep="\n")
