# Assignment 2 – Mobile Computing (Q1–Q7)

All assignment work is organised into separate question folders. The Assignment 2 directory contains only the seven question folders and this common README.

## Question folders
- [Q1 – Mobile Communication or Mobile Computing](Q1/)
- [Q2 – FDMA vs TDMA](Q2/)
- [Q3 – CDMA](Q3/)
- [Q4 – OFDMA](Q4/)
- [Q5 – SDMA](Q5/)
- [Q6 – Multiple-Access Selection](Q6/)
- [Q7 – Diagnose, Redesign and Validate](Q7/)

## Q1 – Mobile Communication or Mobile Computing
- [Q1 answer](Q1/Q1_Report.md)
- [Simulation source](Q1/q1.py)
- [Simulation results](Q1/data/simulation_results.csv)
- [Delivery and delay chart](Q1/figures/simulation_comparison.svg)
- [Python dependencies](Q1/requirements.txt)

Run from the Assignment 2 folder:

```bash
pip install -r Q1/requirements.txt
cd Q1
python q1.py
```

## Q1 model assumptions
A six-hour shift has 60 updates, one generated every six minutes. Link state is independently sampled once per minute using the stated availability probability. The immediate strategy attempts transmission only at update creation and drops a failed update. The store-and-forward strategy uses a FIFO queue of capacity 12; a link-up minute sends one queued update. Overflow drops the newest update. The simulation stops at shift end; remaining queued updates are reported as pending, not lost. Results are averages over 5,000 trials.

## Q2 – Sharing the Channel: FDMA vs TDMA

Q2's simulation files are stored separately in the `Q2/` folder.

- [Q2 simulation source](Q2/q2_simulation.py)
- [Traffic scenario definitions](Q2/data/traffic_scenarios.csv)
- [Simulation results](Q2/data/simulation_results.csv)
- [FDMA vs TDMA comparison chart](Q2/figures/fdma_tdma_comparison.svg)

### Run Q2 simulation

From the `Assignment/Assignment 2` folder:

```bash
pip install -r Q1/requirements.txt
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
pip install -r Q1/requirements.txt
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

## Q6 – Choosing Multiple-Access Techniques for Real Deployments

Q6 uses a weighted 1–5 decision matrix for five access methods across four deployments. Weights are deployment-specific and total 100% per case. A small Python script calculates weighted scores and tests each criterion at -20% and +20%, one at a time.

- [Decision matrix and weights](Q6/data/ratings_and_weights.csv)
- [Weighted scores](Q6/data/weighted_scores.csv)
- [Sensitivity results](Q6/data/sensitivity.csv)
- [Calculation script](Q6/q6_decision.py)

Run with:

```bash
cd Q6
python q6_decision.py
```

Recommended choices:
- Cellular voice: TDMA primary, FDMA+TDMA hybrid (classic dedicated carrier/slot organisation).
- Tactical link: CDMA with direct-sequence spreading or frequency hopping and power control; anti-jam performance depends on processing gain and waveform implementation.
- Stadium downlink: OFDMA primary, with SDMA beamforming as a spatial reuse layer.
- 5,000 low-rate sensors: scheduled TDMA primary, with FDMA channel groups if needed; short packets, aggregation and sleep scheduling reduce overhead.

Sensitivity check: no winning technique changes when any single criterion weight is adjusted by ±20% while the other weights remain fixed. These are reasoned qualitative ratings, not measured field performance.


## Q7 – Diagnose, Redesign and Validate: On-Demand FDMA Allocation

Q7 selects the bursty-data FDMA limitation found in Q2. The original dedicated design held one channel for an entire data session even though the payload was active for only 10% of the session. Q2 measured 79.95% reserved-but-idle capacity for this case.

- [Redesign simulation](Q7/q7_redesign.py)
- [Original vs redesigned results](Q7/data/comparison.csv)
- [Simulation parameters](Q7/data/design_parameters.csv)

### Diagnosis and objective

With 79 usable FDMA channels and 75 Erlangs of offered bursty-data traffic, the original design reserved a channel from session admission until session completion. The channel remained unavailable to other users during the 90% inactive portion. The limiting characteristic is session-level exclusive reservation, not the 25 kHz channel width itself.

Objective: keep the same 79-channel pool and offered traffic, allocate a channel only while a data burst is active, reduce reserved-but-idle capacity from about 80% to 0%, and keep burst blocking below 1%.

### Revised strategy

Split the data session into short 6-second scheduling intervals. At each interval, identify sessions that are still alive, determine which have data ready, and allocate free FDMA channels only to those active bursts. Release each channel at the end of the interval; inactive sessions retain their session state but do not hold radio capacity.

Pseudocode:

```text
For each 6-second interval:
    Find sessions that have not ended
    For each live session:
        If a data burst is ready:
            Add it to the request queue
    Assign up to 79 free channels to queued bursts
    Transmit assigned bursts
    Release all assigned channels
    Keep unfinished sessions for the next interval
```

The prototype uses 300 replications, the same 60-minute period, 79 channels, 75 Erlangs, 0.5-minute mean session duration and 10% activity. The original and redesigned cases use the same generated session arrivals in each replication. The redesigned model samples burst activity in 6-second intervals.

### Prediction and validation

Prediction: channel holding waste should fall sharply because inactive sessions no longer reserve channels. The number of data bursts blocked should remain low because average active demand is much smaller than 79 channels.

The simulation measured 79.933% reserved-idle waste and 5.591% session blocking in the original model. The redesigned model measured 0.000% reserved-idle waste and 0.000% burst blocking; active channel use was 9.408%. The original and redesigned blocking figures refer to different units (session admission versus individual burst requests), so they should not be interpreted as a direct like-for-like blocking comparison. The comparable capacity result is the drop in reserved-idle waste; useful payload capacity use rose from 8.881% to 9.408%.

### Final evaluation and trade-offs

The prediction was supported: the redesign removes long-lived reservations and eliminates reserved-idle waste in this prototype. It adds a scheduler, session-state tracking, request/grant signalling and up to 6 seconds of scheduling granularity. The simulation does not charge control-message overhead or model queueing delay, so a real deployment must measure those costs. Dedicated allocation may still be preferable for continuous voice or delay-sensitive traffic, where a stable channel avoids repeated requests and scheduling delay.

Run from the assignment folder:

```bash
cd Q7
python q7_redesign.py
```
