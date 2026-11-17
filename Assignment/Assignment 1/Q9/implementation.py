# Task-specific implementation for Q9
import csv
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name in ("channel_map.csv","sir_results.csv","capacity_summary.csv","traffic_results.csv","event_surge.csv"):
 p=root/name
 if p.exists():
  with p.open(newline="") as f: rows=list(csv.DictReader(f))
  print(f"{name}: {len(rows)} data rows")
 else: print(f"{name}: missing; run ../simulator.py")
