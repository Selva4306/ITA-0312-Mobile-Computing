# Assignment 5 – Mobile Computing

This folder contains the complete response to Part A (A1–A5) and Part B (B1–B4).

## Structure
- `A1`–`A5`: architectural models, analysis, language-independent pseudocode and traces.
- `B1`: constraint-aware background-work simulation, FIFO vs priority scheduling, tests and measurements.
- `B2`: equal-size easy and adversarial workloads with prediction and measured outcomes.
- `B3`: exhaustive and adaptive feed optimisation, counter-example and scalability measurements.
- `B4`: encoding/upload heuristic, sample device profiles and engineering decision note.

## Run the implementations
Python 3.10+ is sufficient; no third-party packages are required.

```bash
python B1/background_pipeline.py
python B2/adversarial_workloads.py
python B3/feed_optimisation.py
python B4/encoding_strategy.py
```

Each script writes/refreshes its CSV result files in its own question folder. The committed CSV and text outputs are reproducible reference runs. The SVG chart in B3 is a vector graph.

## Measurement note
This assignment uses deterministic simulations so that battery, network, Doze, permission, worker concurrency, frame time, and energy estimates can be tested repeatably on a desktop. These are modelled values, not measurements from a physical Android handset. An Android production implementation would replace the simulated state provider with Android APIs and instrument WorkManager/foreground-service events.

## Security assumptions
Sensitive records are encrypted before enqueue/upload; transport is authenticated TLS; logs contain identifiers and counters rather than health payloads. Logout invalidates credentials and cancels account-scoped pending work.
