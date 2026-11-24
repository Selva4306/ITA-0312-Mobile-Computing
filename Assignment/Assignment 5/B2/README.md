# B2 – Adversarial workloads

Both workloads contain eight records and use the same thresholds: network quality >= 2, battery >= 25%, and permission granted. Workload A places most records in feasible conditions. Workload B deliberately clusters weak/offline network, low battery and a revoked permission.

Run `python adversarial_workloads.py`. It produces `workload_trace.csv` and `summary.csv`. The prediction is that B will cause more deferrals/cancellations despite identical input size. The structural cause is constraint density and distribution, not record count.
