# Task-specific implementation for Q1
import math
CHANNELS=336
for n in (3,4,7,12):
    print(f"N={n}: channels/cell={CHANNELS//n}, reuse ratio Q={math.sqrt(3*n):.3f}")
print("Strategies: fixed reuse, 120-degree sectoring, guarded borrowing, macro-micro splitting.")
print("Selection rule: retain only candidates meeting the SIR threshold; compare capacity and planning cost.")
