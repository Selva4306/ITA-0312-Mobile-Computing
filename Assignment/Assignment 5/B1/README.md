# B1 – Instrumented background pipeline

Run `python background_pipeline.py`. The simulator records enqueued, deferred, cancelled/rejected, successful, peak-worker and residual-backlog counts in `comparison.csv`; each decision and its battery/network snapshot is in `decision_log.csv`.

FIFO is arrival order. Priority is descending priority with stable arrival order for ties. Both strategies apply identical feasibility checks, so priority changes selection order, not security policy. The dataset includes good connectivity, weak connectivity, low battery/Doze, an unencrypted payload and permission revocation.

**Validation:** good network + sufficient battery uploads; weak network and Doze/low battery defer; permission revocation cancels; plaintext is rejected before transmission. This is a deterministic simulation of Android policy, not a physical-device benchmark. Android implementation mapping: WorkManager for deferrable uploads, explicit worker intents/unique work, encrypted local storage, TLS, and cancellation on logout/permission changes.
