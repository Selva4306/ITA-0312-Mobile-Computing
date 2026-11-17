# Q5 – Scaling and sensitivity (3 marks)

- Per-cell channels are approximately S/N; per-cell circuit capacity generally falls as N rises.
- Ideal SIR scales as N^(n/2).
- Cell count scales as 1/R²; halving R creates about four times as many cells.
- Total offered traffic is 25 E at 1,000 subscribers; 250 E at 10,000; 500 E at 20,000; and 2,500 E at 100,000.
- Baseline N=7, R=0.50 km supports about 29,177 subscriber-equivalents. It fails at 100,000. One uniform split gives 76 cells and approximately four times the capacity (~116,700 subscriber-equivalents) in the ideal model.
- A smaller path-loss exponent (2.5) means distant interference decays less rapidly, making reuse harder. At n=4 ideal SIR is higher, but dense-area shadowing and blockage still require field validation.

A practical split trigger is a forecast cell load approaching its Erlang-B capacity or a 5th-percentile SIR below threshold. Split hotspots first rather than densifying every cell.

