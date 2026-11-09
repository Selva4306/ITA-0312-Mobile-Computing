import heapq
import numpy as np
import pandas as pd

FDMA_CHANNELS = 79
TDMA_SLOTS = 70
SIMULATION_MINUTES = 60
REPLICATIONS = 300
SEED = 20261109

SCENARIOS = {
    "Continuous voice": {"offered_erlangs": 75.0, "voice_fraction": 1.0,
                         "voice_duty": 1.0, "data_duty": 0.10, "synchronised": False},
    "Bursty data (10% duty)": {"offered_erlangs": 75.0, "voice_fraction": 0.0,
                               "voice_duty": 1.0, "data_duty": 0.10, "synchronised": False},
    "Synchronized mixed (70/30)": {"offered_erlangs": 75.0, "voice_fraction": 0.70,
                                   "voice_duty": 1.0, "data_duty": 0.10, "synchronised": True},
}

def simulate_one(capacity, cfg, rng):
    offered = cfg["offered_erlangs"]
    vf = cfg["voice_fraction"]
    nv = rng.poisson(offered * vf * SIMULATION_MINUTES / 4.0)
    nd = rng.poisson(offered * (1.0 - vf) * SIMULATION_MINUTES / 0.5)
    events = []
    for _ in range(nv):
        t = rng.uniform(0, SIMULATION_MINUTES)
        if cfg["synchronised"]:
            t = rng.choice([0.0, 15.0, 30.0, 45.0]) + rng.uniform(0, 1.0)
        events.append((t, rng.exponential(4.0), 1.0))
    for _ in range(nd):
        t = rng.uniform(0, SIMULATION_MINUTES)
        if cfg["synchronised"]:
            t = rng.choice([0.0, 15.0, 30.0, 45.0]) + rng.uniform(0, 1.0)
        events.append((t, rng.exponential(0.5), 0.10))
    events.sort(key=lambda x: x[0])

    departures = []
    accepted = blocked = 0
    reserved_minutes = payload_minutes = 0.0
    for arrival, duration, duty in events:
        while departures and departures[0] <= arrival:
            heapq.heappop(departures)
        if len(departures) >= capacity:
            blocked += 1
            continue
        accepted += 1
        heapq.heappush(departures, arrival + duration)
        occupied = min(duration, SIMULATION_MINUTES - arrival)
        reserved_minutes += occupied
        payload_minutes += occupied * duty

    capacity_minutes = capacity * SIMULATION_MINUTES
    return {
        "arrivals": len(events), "accepted": accepted, "blocked": blocked,
        "blocking_percent": 100 * blocked / len(events) if events else 0,
        "reserved_utilisation_percent": 100 * reserved_minutes / capacity_minutes,
        "payload_utilisation_percent": 100 * payload_minutes / capacity_minutes,
        "reserved_idle_waste_percent": 100 * (reserved_minutes-payload_minutes) / capacity_minutes,
        "unoccupied_capacity_percent": 100 * (1-reserved_minutes/capacity_minutes),
    }

def run():
    rng = np.random.default_rng(SEED)
    rows = []
    for scenario, cfg in SCENARIOS.items():
        for scheme, capacity in (("FDMA", FDMA_CHANNELS), ("TDMA", TDMA_SLOTS)):
            trials = [simulate_one(capacity, cfg, rng) for _ in range(REPLICATIONS)]
            rows.append({
                "scenario": scenario, "scheme": scheme,
                "usable_channels_or_slots": capacity,
                "mean_arrivals_per_hour": np.mean([x["arrivals"] for x in trials]),
                "mean_accepted_per_hour": np.mean([x["accepted"] for x in trials]),
                "blocking_percent": np.mean([x["blocking_percent"] for x in trials]),
                "reserved_utilisation_percent": np.mean([x["reserved_utilisation_percent"] for x in trials]),
                "payload_utilisation_percent": np.mean([x["payload_utilisation_percent"] for x in trials]),
                "reserved_idle_waste_percent": np.mean([x["reserved_idle_waste_percent"] for x in trials]),
                "unoccupied_capacity_percent": np.mean([x["unoccupied_capacity_percent"] for x in trials]),
            })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    result = run()
    result.to_csv("data/simulation_results.csv", index=False, float_format="%.3f")
    print(result.round(2).to_string(index=False))
