# Assignment 1 – CO1: Hexagonal Cellular Network Planning

This folder contains the design report, reproducible Python simulator, generated CSV datasets and figures for the 12 km² university-township cellular planning assignment.

## Files

- `report.md` – answers Tasks 1–12, derivations, pseudocode, design decision and stadium challenge.
- `simulator.py` – fixed-seed Monte-Carlo SIR, Erlang-B capacity, subscriber-growth and event-surge model.
- `sir_results.csv` – mean / 5th-percentile SIR and outage results for N=3,4,7,12 and n=2.5,3,4.
- `capacity_summary.csv` – strategy-level channels, sites and 2% GoS capacity.
- `traffic_results.csv` – blocking and offered traffic for 1k, 10k, 20k and 100k subscribers.
- `event_surge.csv` – stadium surge scenarios.
- `sir_vs_cluster.svg`, `blocking_vs_growth.svg`, `sir_pathloss_sensitivity.svg` – generated plots.

## Run

Python 3.10+ is recommended. Install dependencies:

```bash
python -m pip install matplotlib
python simulator.py
```

The simulator uses fixed seed `4306` and 12,000 samples per SIR case. Running it regenerates the CSV files and plots in the same directory. The code uses only the Python standard library plus Matplotlib.

## Key assumptions

- Township area: 12 km²; available duplex traffic channels: 336.
- Busy-hour traffic: 0.025 Erlang/subscriber; target blocking: 2%.
- Assumed macro cell radius: 0.5 km (sensitivity should be repeated after a site survey).
- Path-loss exponents: 2.5, 3.0 and 4.0; lognormal shadowing standard deviation: 4 dB.
- Sectoring is idealised as two dominant first-tier interferers; real antenna patterns require field validation.
- Planning cost index is relative effort only, not a currency estimate.

## Validation

The textbook equal-distance check for N=7, n=4 and six first-tier interferers is `10 log10((3N)^(n/2)/6) = 18.663 dB`, matching the assignment's approximately 18.7 dB sanity target. The Monte-Carlo results intentionally differ because they sample user locations and shadowing.

## Important interpretation

The results are engineering estimates, not a licensed-frequency plan. Before deployment, replace the assumed radius, traffic distribution, propagation and antenna parameters with surveyed values and validate backhaul, control-channel and regulatory constraints.
