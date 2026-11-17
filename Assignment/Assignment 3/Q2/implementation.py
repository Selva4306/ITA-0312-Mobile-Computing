import csv
from pathlib import Path
rows=[]
for name,mn_fa,fa_ha,proc in [("baseline",12,30,5),("regional_anchor",12,8,5),("route_optimised",12,30,5)]:
 rtt=2*mn_fa+2*fa_ha+proc
 path=(28+12) if name=="route_optimised" else ((28+8+12) if name=="regional_anchor" else (40+30+12))
 gap=50+20+rtt
 rows.append({"design":name,"registration_rtt_ms":rtt,"downlink_path_ms":path,"handoff_gap_ms":gap,"packets_lost_at_50pps":round(gap/1000*50,2),"ipip_overhead_pct_1000B":2.0,"ipip_overhead_pct_200B":10.0})
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print(*rows,sep="\\n")
