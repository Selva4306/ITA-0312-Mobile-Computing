import csv
from pathlib import Path
rows=[(2,.98,95.2,34.0),(8,1.67,95.6,37.9),(20,3.32,94.4,43.0)]
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.writer(f);w.writerow(["active_flows","aodv_overhead_kBps","delivery_pct","mean_delay_ms","control_behaviour"])
 for flows,over,delivery,delay in rows:w.writerow([flows,over,delivery,delay,"RREQ/RREP on demand; RERR on break; 1 Hz hello"])
print("Q6 AODV comparison output written")
