# Task-specific implementation for Q10
import math
analytical=10*math.log10((3*7)**2/6)
print(f"Analytical N=7,n=4,six-interferer SIR = {analytical:.3f} dB")
print("Compare with ../sir_results.csv Monte-Carlo mean and 5th percentile.")
print("Differences reflect sampled user positions, interferer distances and lognormal shadowing.")
print("Erlang-B assumes Poisson arrivals, exponential holding times, infinite source and no queueing.")
