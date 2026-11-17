# Assignment 3 – Mobile Computing (CO3)

**Repository location:** this folder is at the same level as `Assignment 1` inside `Assignment/`.

This submission is organised question-wise. Every Q folder contains:
- `README.md` – what the implementation does and how to run it.
- `implementation.py` – runnable Python model/calculation.
- `output.csv` – committed output table.
- `dataset.csv` – input or comparison evidence used by the task.

| Folder | Task | Evidence / implementation |
|---|---|---|
| [Q1](Q1/) | Wireless architecture and mobility | Link-availability / store-and-forward model |
| [Q2](Q2/) | Mobile IP and mobility management | Registration, tunnel, route and interruption calculations |
| [Q3](Q3/) | Cellular vs ad hoc networks | Mesh shortest-path and hop-delay comparison |
| [Q4](Q4/) | Mobile IP application requirements | Ambulance/healthcare QoS and overhead budget |
| [Q5](Q5/) | Proactive routing (DSDV) | Periodic table-update overhead model and reported comparison dataset |
| [Q6](Q6/) | Reactive routing (AODV) | Flow-load comparison and route-control evidence |
| [Q7](Q7/) | Emergency network design challenge | Hybrid AODV mesh + Mobile IP gateway calculations |

## Run all implementations

From this directory:

```bash
python Q1/implementation.py
python Q2/implementation.py
python Q3/implementation.py
python Q4/implementation.py
python Q5/implementation.py
python Q6/implementation.py
python Q7/implementation.py
```

Each script writes its task's `output.csv` in the same folder. Python 3 standard library only; no third-party packages required.

## Evidence and assumptions

- Q1 is a fixed-seed Monte Carlo availability model with 2,000 updates per case. Store-and-forward assumes eventual reconnection and uses an exponential waiting-time approximation; this is not a real radio trace.
- Q2–Q4 are analytical/illustrative models using the explicit delays, packet sizes and QoS assumptions documented in the assignment answer. They are not live Mobile IP or cellular measurements.
- Q5–Q6 include the routing comparison observations already documented in the assignment answer. The committed scripts regenerate the analytical AODV/DSDV output tables; the datasets label report-derived observations rather than claiming a fresh emulator run.
- Q7 is a planning calculation for a hybrid emergency mesh, not a packet-level network emulator.

The assignment's design pseudocode, architecture diagrams, explanations and manual traces should be read alongside these implementations. Model values must be identified as assumptions during submission/viva; do not describe them as field measurements.
