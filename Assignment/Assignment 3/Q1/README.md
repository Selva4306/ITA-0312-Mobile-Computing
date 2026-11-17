# Q1 – Wireless Network Architecture and Mobility Analysis

Compares immediate-send with store-and-forward under 90%, 60% and 30% link availability. Uses 2,000 updates per case and fixed seed 4306; records delivery, delay, loss and mean delay.

Run `python implementation.py` to regenerate `output.csv`. The queue reconnection delay is an exponential approximation (mean 30/availability seconds), not a measured radio trace.
