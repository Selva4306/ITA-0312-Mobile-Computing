# Q8 – Implementation and tests (4 marks)

simulator.py generates axial hex-grid coordinates, assigns channel groups with an interference-distance graph-colouring check, computes hexagonal area/site estimates, applies Erlang-B recursion and inverse capacity search, and runs fixed-seed Monte-Carlo SIR for N={3,4,7,12} and n={2.5,3,4}, a sectorised two-interferer comparison, subscriber-growth blocking and the event surge. It uses seed 4306 and 12,000 SIR samples per case.

The textbook N=7,n=4,six-interferer sanity case is calculated separately as 18.663 dB. Monte-Carlo results differ because they sample user locations, vary interferer distances and include shadowing. The dynamic-borrowing capacity row is an effective-N=4 guarded-borrowing planning proxy, not a time-stepped donor-cell state simulation; its feasibility still requires a live interference guard.

