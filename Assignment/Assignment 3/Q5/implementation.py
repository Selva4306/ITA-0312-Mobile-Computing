import csv
from pathlib import Path
rows=[]
for n in (10,20,40,60,80):
 rate=n*(24+12*n)/5
 rows.append({"nodes":n,"update_interval_s":5,"header_B":24,"entry_B":12,"dsdv_full_dump_Bps":round(rate,2),"complexity":"O(N^2)"})
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(*rows,sep="\\n")
