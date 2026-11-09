import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

methods = ["SDMA", "TDMA", "FDMA", "CDMA", "OFDMA"]
cases = {
    "cellular_voice": {
        "weights": [20, 30, 20, 15, 15],
        "criteria": ["capacity", "reliability", "fairness", "scalability", "simplicity"],
        "ratings": [[4,3,3,3,2], [3,5,5,4,4], [2,5,4,3,5], [4,4,4,4,2], [5,4,4,5,3]]
    },
    "tactical_link": {
        "weights": [10,25,10,15,10,30],
        "criteria": ["capacity", "reliability", "fairness", "scalability", "simplicity", "jam_resistance"],
        "ratings": [[3,3,3,3,2,4], [2,3,3,4,4,2], [2,2,3,3,5,1], [3,4,3,4,2,5], [5,2,3,4,3,2]]
    },
    "stadium_downlink": {
        "weights": [35,15,15,20,15],
        "criteria": ["capacity", "reliability", "fairness", "scalability", "simplicity"],
        "ratings": [[4,3,3,4,2], [3,4,4,4,4], [2,4,4,3,5], [3,3,3,4,2], [5,4,4,5,3]]
    },
    "sensor_network": {
        "weights": [15,20,15,30,20],
        "criteria": ["capacity", "reliability", "fairness", "scalability", "simplicity"],
        "ratings": [[3,3,3,2,2], [3,4,4,4,5], [2,4,3,3,5], [3,4,3,4,2], [4,4,4,4,2]]
    }
}

scores = []
sensitivity = []
for case, data in cases.items():
    weights = data["weights"]
    base = []
    for method, rating in zip(methods, data["ratings"]):
        score = sum(w * r for w, r in zip(weights, rating)) / sum(weights)
        base.append(score)
        scores.append([case, method, round(score, 3)])
    winner = methods[base.index(max(base))]
    sensitivity.append([case, "base", winner])
    for i, criterion in enumerate(data["criteria"]):
        for change in [0.8, 1.2]:
            changed = weights[:]
            changed[i] *= change
            values = [sum(w*r for w, r in zip(changed, rating)) / sum(changed)
                      for rating in data["ratings"]]
            new_winner = methods[values.index(max(values))]
            sensitivity.append([case, criterion + (" -20%" if change < 1 else " +20%"),
                                new_winner])

with (DATA / "weighted_scores.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["deployment", "technique", "weighted_score_out_of_5"])
    w.writerows(scores)

with (DATA / "sensitivity.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["deployment", "weight_test", "winning_technique"])
    w.writerows(sensitivity)

print("Weighted scores and one-at-a-time +/-20% sensitivity results saved.")
for case in cases:
    rows = [r for r in scores if r[0] == case]
    print(case, sorted(rows, key=lambda x: -x[2]))
