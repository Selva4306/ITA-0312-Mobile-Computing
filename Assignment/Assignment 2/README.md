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

## Q3 – CDMA: Orthogonality, Spreading and the Near-Far Problem

Q3's reproducible direct-sequence CDMA simulation and evidence are stored in `Q3/`.

- [Q3 simulation source](Q3/q3_simulation.py)
- [Test condition definitions](Q3/data/test_conditions.csv)
- [BER simulation results](Q3/data/simulation_results.csv)
- [Pairwise code-correlation summary](Q3/data/correlation_values.csv)
- [Users meeting the BER target](Q3/data/supported_users.csv)
- [BER vs users chart](Q3/figures/ber_vs_users.svg)
- [Correlation comparison chart](Q3/figures/correlation_comparison.svg)

### Run Q3 simulation

From the `Assignment/Assignment 2` folder:

```bash
pip install -r requirements.txt
cd Q3
python q3_simulation.py
```

The simulation uses 20,000 bits per measured user, a fixed seed, and Eb/N0 of 5 dB. It tests 8-, 16- and 64-chip spreading codes under synchronous Walsh orthogonality, random non-orthogonal codes, and a near-far case with a 10-times-power interferer delayed by one chip. The one-chip offset is intentional: unequal power alone does not destroy perfectly synchronous Walsh orthogonality, but timing error creates cross-correlation that lets the strong user interfere with weaker users. Processing gain is N, or 10 log10(N) dB.

## Q4 – OFDMA: Subcarrier Allocation and Fairness

Q4 compares three allocation methods and a minimum-rate-aware option for 8 users sharing 64 subcarriers.

- [Simulation source](Q4/q4_simulation.py)
- [Summary results](Q4/data/simulation_results.csv)
- [Per-user throughput](Q4/data/per_user_throughput.csv)
- [Numerical orthogonality check](Q4/data/orthogonality.csv)

Run from this folder:

```bash
cd Q4
python q4_simulation.py
```

The simulation uses 1,000 fixed-seed fading realisations and SNR = 10 (linear). It reports sum spectral efficiency and Jain's fairness. The minimum-rate-aware method targets 8 bps/Hz per user: each user first receives four separated subcarriers, then the weakest-rate user receives the best remaining subcarrier until the target is reached; leftover subcarriers go to the strongest channel. Numerical inner products for subcarriers 0, 1 and 2 are zero to the shown precision.

Subcarrier spacing and useful symbol duration obey Δf = 1/Tu. For example, 15 kHz spacing gives Tu = 66.67 μs. A cyclic prefix copies the symbol tail to the front so multipath delay does not destroy orthogonality, provided the delay spread fits inside the prefix.

## Q5 – SDMA: Directional Antennas and ULA Beamforming

Q5 evaluates a half-wavelength-spaced uniform linear array steered to broadside, using an equal-power SIR threshold of 10 dB.

- [Simulation source](Q5/q5_simulation.py)
- [Array metrics and minimum separation](Q5/data/array_metrics.csv)
- [SIR by angular separation](Q5/data/sir_vs_separation.csv)
- [Normalised array patterns](Q5/data/array_pattern.csv)
- [Design assumptions](Q5/data/design_parameters.csv)

Run from this folder:

```bash
cd Q5
python q5_simulation.py
```

The normalised array factor is AF(θ) = |sin(Nψ/2)/(N sin(ψ/2))|, where ψ = π(sin θ − sin θ0) for d = λ/2. The 10 dB SIR threshold is first met at approximately 53°, 23°, 11° and 6° for N = 2, 4, 8 and 16 respectively. Larger arrays narrow the main lobe and improve angular separation, while the peak sidelobe remains around −11 to −13 dB for N ≥ 4.

An ideal omni antenna has no angular discrimination. An ideal 120° sector rejects users outside its sector but cannot separate users within the same sector. At a toll plaza, vehicles are mostly aligned in one direction, so angular separation is limited; SDMA alone is not reliable. Use scheduled time/frequency resources or additional spatial/channel discrimination instead.
