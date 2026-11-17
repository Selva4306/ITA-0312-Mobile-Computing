# Task-specific implementation for Q4
import csv
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"sir_results.csv"
if p.exists():
    rows=list(csv.DictReader(p.open()))
    for row in rows:
        if row["strategy"]=="Fixed reuse" and row["path_loss_n"]=="4.0":
            print("N",row["cluster_N"],"mean SIR",row["sir_mean_db"],"dB; 5th percentile",row["sir_p05_db"],"dB; outage",row["outage_below_12db"])
else:
    print("Use the shared ../sir_results.csv dataset for simulated edge/average comparisons.")
print("Best case: near serving site; average: representative mid-cell; worst: cell edge/corner near co-channel interferer.")
