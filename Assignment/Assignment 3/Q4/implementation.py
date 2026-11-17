import csv
from pathlib import Path
rows=[("normal_mobile_ip_downlink",82,"ms",150,"yes"),("route_optimised_downlink",40,"ms",150,"yes"),("handoff_interruption",160,"ms",200,"yes"),("frames_lost_per_handoff_at_50pps",8,"frames","","buffer"),("handoff_loss_at_2_per_minute_50pps",0.533,"percent",1.0,"yes"),("ip_in_ip_overhead_200B",10,"percent","","review"),("ip_in_ip_overhead_1000B",2,"percent","","yes")]
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.writer(f);w.writerow(["metric","value","unit","target","pass"]);w.writerows(rows)
for r in rows:print(r)
