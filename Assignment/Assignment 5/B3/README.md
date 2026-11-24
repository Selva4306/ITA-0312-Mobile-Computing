# B3 – Exact and approximate feed optimisation

Run `python feed_optimisation.py`. Exact search enumerates 3 quality × 3 cache × 3 prefetch settings (27 configurations per item replay) and selects minimum modelled cost. The adaptive method begins at high quality and reduces quality/prefetch under frame-time pressure. CSVs include at least three test cases, a counterexample candidate, and operation counts as feed size grows.

The cost model is deliberately explicit and deterministic: frame-time estimate, energy estimate, and a fourfold penalty for frame time above 16 ms. It is a teaching model, not a claim about Android GPU performance. The adaptive method is feasible-oriented and has no global optimality guarantee; a greedy change can ignore a lower-cost combination elsewhere in the search space.
