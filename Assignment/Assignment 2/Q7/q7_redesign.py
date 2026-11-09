import csv
import random
import math

CAPACITY = 79
MINUTES = 60
TRIALS = 300
SEED = 20261110
OFFERED_ERLANGS = 75.0
MEAN_SESSION = 0.5
DUTY = 0.10


def poisson(lam, rng):
    limit = math.exp(-lam)
    product = 1.0
    count = 0
    while product > limit:
        count += 1
        product *= rng.random()
    return count - 1


def make_sessions(rng):
    arrivals = []
    rate = OFFERED_ERLANGS / MEAN_SESSION
    for minute in range(MINUTES):
        count = poisson(rate, rng)
        for _ in range(count):
            start = minute + rng.random()
            duration = rng.expovariate(1 / MEAN_SESSION)
            arrivals.append((start, duration))
    return sorted(arrivals)


def original(sessions):
    departures = []
    blocked = accepted = 0
    reserved = 0.0
    for start, duration in sessions:
        while departures and departures[0] <= start:
            departures.sort()
            departures.pop(0)
        if len(departures) >= CAPACITY:
            blocked += 1
        else:
            accepted += 1
            end = min(start + duration, MINUTES)
            reserved += max(0.0, end - start)
            departures.append(start + duration)
            departures.sort()
    return blocked, accepted, reserved


def redesigned(sessions, rng):
    slots_per_minute = 10
    total_slots = MINUTES * slots_per_minute
    changes = [0] * (total_slots + 1)
    for start, duration in sessions:
        end = min(start + duration, MINUTES)
        first = min(total_slots, int(start * slots_per_minute))
        last = min(total_slots, int(end * slots_per_minute))
        if first < last:
            changes[first] += 1
            changes[last] -= 1
    active_sessions = attempted = served = used_channel_minutes = 0
    for slot in range(total_slots):
        active_sessions += changes[slot]
        bursts = sum(1 for _ in range(active_sessions) if rng.random() < DUTY)
        attempted += bursts
        served += min(bursts, CAPACITY)
        used_channel_minutes += min(bursts, CAPACITY)
    return attempted, served, used_channel_minutes


def run():
    rng = random.Random(SEED)
    rows = []
    for _ in range(TRIALS):
        sessions = make_sessions(rng)
        old_blocked, old_accepted, reserved = original(sessions)
        attempts, served, used = redesigned(sessions, rng)
        rows.append((old_blocked, old_accepted, reserved, attempts, served, used, len(sessions)))

    total = [sum(row[i] for row in rows) / TRIALS for i in range(7)]
    old_blocked, old_accepted, reserved, attempts, served, used, arrivals = total
    original_blocking = 100 * old_blocked / arrivals
    original_reserved = 100 * reserved / (CAPACITY * MINUTES)
    original_payload = 100 * (reserved * DUTY) / (CAPACITY * MINUTES)
    original_waste = original_reserved - original_payload
    new_burst_blocking = 100 * (attempts - served) / attempts if attempts else 0
    new_channel_use = 100 * used / (CAPACITY * MINUTES * 10)
    new_payload = new_channel_use
    result = [
        ["Original dedicated FDMA", arrivals, old_accepted, original_blocking,
         "", original_reserved, "", original_payload, original_waste,
         "One channel held for full session"],
        ["Redesigned on-demand FDMA", arrivals, "", "",
         new_burst_blocking, "", new_channel_use, new_payload, 0.0,
         "Channel allocated only during active burst"],
    ]
    with open("data/comparison.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["strategy", "sessions_offered_per_hour", "sessions_accepted_per_hour",
                         "session_blocking_percent", "burst_blocking_percent",
                         "reserved_channel_utilisation_percent", "active_channel_utilisation_percent",
                         "payload_capacity_utilisation_percent", "reserved_idle_waste_percent", "allocation_rule"])
        writer.writerows([[r[0], f"{r[1]:.2f}", r[2] if r[2] == "" else f"{r[2]:.2f}",
                           r[3] if r[3] == "" else f"{r[3]:.3f}",
                           r[4] if r[4] == "" else f"{r[4]:.3f}",
                           r[5] if r[5] == "" else f"{r[5]:.3f}",
                           r[6] if r[6] == "" else f"{r[6]:.3f}",
                           f"{r[7]:.3f}", f"{r[8]:.3f}", r[9]] for r in result])
    print("Original: session blocking %.3f%%, reserved utilisation %.3f%%, idle waste %.3f%%" %
          (original_blocking, original_reserved, original_waste))
    print("Redesigned: burst blocking %.3f%%, active utilisation %.3f%%" %
          (new_burst_blocking, new_channel_use))


if __name__ == "__main__":
    run()
