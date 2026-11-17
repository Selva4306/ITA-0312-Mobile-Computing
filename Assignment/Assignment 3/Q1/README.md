# Q1 – Wireless Network Architecture and Mobility Analysis

Compares immediate-send with store-and-forward under 90%, 60% and 30% link availability. Uses 2,000 updates per case and fixed random seed 4306; records delivered, delayed, lost and mean delay.

Run `python implementation.py` to regenerate `output.csv`. The store-and-forward model assumes queued records are eventually delivered and uses an exponential reconnection-wait approximation (rate availability/30 per second); it is a reproducible simplified model, not a measured radio trace.
