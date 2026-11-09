# Assignment 2 – Q1: Mobile Communication or Mobile Computing?

This folder contains an original analysis and reproducible simulation for the field-service technology audit.

## Files
- [Q1_Report.md](Q1_Report.md) – complete written answer, classification, simulation methodology, results and conclusion
- [q1.py](q1.py) – reproducible Monte Carlo simulation
- [data/simulation_results.csv](data/simulation_results.csv) – averaged simulation results
- [figures/simulation_comparison.svg](figures/simulation_comparison.svg) – delivery and delay chart
- [requirements.txt](requirements.txt) – Python dependencies

## Run the simulation
Install dependencies and run from this folder:

```bash
pip install -r requirements.txt
python q1.py
```

The script recreates `data/simulation_results.csv`. It uses a fixed random seed for reproducibility.

## Model assumptions
A six-hour shift has 60 updates, one generated every six minutes. Link state is independently sampled once per minute using the stated availability probability. The immediate strategy attempts transmission only at update creation and drops a failed update. The store-and-forward strategy uses a FIFO queue of capacity 12; a link-up minute sends one queued update. Overflow drops the newest update. The simulation stops at shift end; remaining queued updates are reported as pending, not lost. Results are averages over 5,000 trials, so fractional counts are expected values per 60 generated updates.

A formatted DOCX and PDF version are also available as separate attachments in the ChatGPT conversation.

## Q2 – Sharing the Channel: FDMA vs TDMA

Q2's simulation files are stored separately in the `Q2/` folder.

- [Q2 simulation source](Q2/q2_simulation.py)
- [Traffic scenario definitions](Q2/data/traffic_scenarios.csv)
- [Simulation results](Q2/data/simulation_results.csv)
- [FDMA vs TDMA comparison chart](Q2/figures/fdma_tdma_comparison.svg)

### Run Q2 simulation

From the `Assignment/Assignment 2` folder:

```bash
pip install -r requirements.txt
cd Q2
python q2_simulation.py
```

The simulation compares 79 estimated usable FDMA channels with 70 estimated usable TDMA slots. It models a 60-minute period, 300 replications per traffic condition, Poisson arrivals and exponential holding times. The three conditions are continuous voice, bursty data with 10% payload duty cycle, and a 70/30 voice-data mix with synchronised arrival bursts (the edge case). Results report blocking, reserved-channel utilisation, payload utilisation, reserved-but-idle capacity and unoccupied capacity. The fixed random seed makes the results reproducible.
