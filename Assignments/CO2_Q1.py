
import random
from collections import deque

TOTAL_UPDATES = 100
LINK_AVAILABILITY = [0.90, 0.60, 0.30]


def immediate_transmission(probability):
    delivered = 0
    lost = 0

    for _ in range(TOTAL_UPDATES):
        if random.random() < probability:
            delivered += 1
        else:
            lost += 1

    return delivered, 0, lost, 0


def store_and_forward(probability):
    queue = deque()
    delivered = 0
    delayed = 0
    delivery_delays = []

    # Generate and process updates
    for time in range(TOTAL_UPDATES):
        queue.append(time)

        if random.random() < probability and queue:
            created_time = queue.popleft()
            delay = time - created_time

            delivered += 1
            delivery_delays.append(delay)

            if delay > 0:
                delayed += 1

    # Send remaining queued updates when connection returns
    time = TOTAL_UPDATES

    while queue:
        if random.random() < probability:
            created_time = queue.popleft()
            delay = time - created_time

            delivered += 1
            delayed += 1
            delivery_delays.append(delay)

        time += 1

    mean_delay = sum(delivery_delays) / len(delivery_delays)

    return delivered, delayed, 0, mean_delay


print("MOBILE DATA SYNCHRONISATION SIMULATION")
print("-" * 65)

for probability in LINK_AVAILABILITY:

    print(f"\nLink Availability: {probability * 100:.0f}%")

    # Reproducible results
    random.seed(42)
    immediate = immediate_transmission(probability)

    random.seed(42)
    queued = store_and_forward(probability)

    print("\nImmediate Transmission:")
    print("Delivered:", immediate[0])
    print("Delayed:", immediate[1])
    print("Lost:", immediate[2])
    print("Mean Delay:", immediate[3])

    print("\nStore-and-Forward:")
    print("Delivered:", queued[0])
    print("Delayed:", queued[1])
    print("Lost:", queued[2])
    print("Mean Delay:", round(queued[3], 2))
