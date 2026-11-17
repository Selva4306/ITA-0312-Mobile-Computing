import csv
from pathlib import Path
nodes=30; speed=15; gateway_spacing=400; registration_rtt=157
handoffs=speed*60/gateway_spacing; registrations=handoffs+2; signalling=registrations*152/60; gap=50+20+registration_rtt
rows=[("gateway_handoffs_per_minute",round(handoffs,2),"per_min"),("registrations_including_refresh_per_minute",round(registrations,2),"per_min"),("mobile_ip_signalling_per_node",round(signalling,2),"B/s"),("mobile_ip_signalling_30_nodes",round(signalling*nodes,2),"B/s"),("gateway_handoff_interruption",gap,"ms"),("mesh_route_repair",100,"ms"),("tunnel_overhead_200B",10,"percent"),("tunnel_overhead_1000B",2,"percent")]
with Path(__file__).with_name("output.csv").open("w",newline="") as f:
 w=csv.writer(f);w.writerow(["metric","value","unit"]);w.writerows(rows)
print(*rows,sep="\\n")
