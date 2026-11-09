import numpy as np
import pandas as pd

TRIALS = 5000
SHIFT_MINUTES = 360
UPDATE_INTERVAL = 6
QUEUE_CAPACITY = 12
SEED = 20261109

def simulate(availability):
    rng = np.random.default_rng(SEED + int(availability * 100))
    generation_times = np.arange(0, SHIFT_MINUTES, UPDATE_INTERVAL)
    immediate_delivered = immediate_lost = 0
    queued_delivered = queued_lost = queued_pending = queued_delayed = 0
    queued_delays = []

    for _ in range(TRIALS):
        link_up = rng.random(SHIFT_MINUTES) < availability
        immediate_delivered += int(link_up[generation_times].sum())
        immediate_lost += int((~link_up[generation_times]).sum())

        queue = []
        lost = delayed = 0
        delivered = 0
        for minute in range(SHIFT_MINUTES):
            if minute % UPDATE_INTERVAL == 0:
                if len(queue) < QUEUE_CAPACITY:
                    queue.append(minute)
                else:
                    lost += 1
            if link_up[minute] and queue:
                created = queue.pop(0)
                delivered += 1
                if minute > created:
                    delayed += 1
                queued_delays.append(minute - created)

        queued_delivered += delivered
        queued_lost += lost
        queued_pending += len(queue)
        queued_delayed += delayed

    return {
        "availability_percent": int(availability * 100),
        "immediate_delivered_per_60": immediate_delivered / TRIALS,
        "immediate_delayed_per_60": 0.0,
        "immediate_lost_per_60": immediate_lost / TRIALS,
        "immediate_mean_delay_min": 0.0,
        "store_forward_delivered_per_60": queued_delivered / TRIALS,
        "store_forward_delayed_deliveries_per_60": queued_delayed / TRIALS,
        "store_forward_lost_per_60": queued_lost / TRIALS,
        "store_forward_pending_at_end_per_60": queued_pending / TRIALS,
        "store_forward_mean_delay_min": float(np.mean(queued_delays)) if queued_delays else 0.0,
    }

if __name__ == "__main__":
    results = pd.DataFrame([simulate(p) for p in (0.90, 0.60, 0.30)])
    results.to_csv("data/simulation_results.csv", index=False, float_format="%.3f")
    print(results.to_string(index=False))
