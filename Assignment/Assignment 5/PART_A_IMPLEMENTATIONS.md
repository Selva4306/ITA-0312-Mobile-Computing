# Part A executable implementations (A1–A5)

The original Part A questions mainly ask for architecture, pseudocode and analysis. To make the work reproducible, each A-folder now also contains a runnable Python implementation or executable analysis generator, plus a sample CSV output.

## Run

Run each command from its matching question folder:

| Folder | Command | Output |
|---|---|---|
| A1 | `python constraint_aware_architecture.py` | `a1_execution_trace.csv` |
| A2 | `python incremental_sync.py` | `a2_sync_decisions.csv` |
| A3 | `python generic_background_framework.py` | `a3_framework_run.csv` |
| A4 | `python tractability_classifier.py` | `a4_tractability_matrix.csv` |
| A5 | `python adaptive_feed_optimizer.py` | `a5_optimizer_comparison.csv`, `a5_adaptive_trace.csv` |

Python 3.9+ is sufficient; the scripts use only the standard library.

## What each implementation demonstrates

- **A1:** Constraint-aware task selection, execution, deferral, permission checks, logout cancellation and a five-event trace.
- **A2:** Record-by-record Upload / Defer / Reject / Conflict-Resolve decisions using sensitivity, encryption, priority, size, battery and network conditions.
- **A3:** A shared scheduler applied to sensor collection, data synchronisation and push delivery, with explicit task outcomes.
- **A4:** An executable generator for the six-problem tractability/resource-classification matrix and verification notes.
- **A5:** Exhaustive search compared with a greedy adaptive feed configuration across low-end, mid-range and flagship device profiles; operation choices and costs are written to CSV.

## Scope and limitations

These are deterministic, simplified Python models for demonstrating the requested algorithms. They are not Android WorkManager deployments, real sensor uploads, production multimedia benchmarks or measurements from physical phones. The cost functions and device profiles are illustrative assumptions, stated in the source code. The scripts regenerate the sample outputs when run.
