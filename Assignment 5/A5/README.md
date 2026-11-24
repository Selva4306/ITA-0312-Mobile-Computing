# A5 – Approximate UI/graphics optimisation

## A5.1 Exact perspective
For a finite feed, enumerate every tuple (decode quality, cache capacity, prefetch distance), replay the workload, and calculate cost = weighted frame drops + energy + memory penalty. Choose the lowest-cost feasible tuple. The search grows as the product of the number of levels in each dimension; device profiles and feed sequences multiply evaluation cost. Exact replay also becomes stale as network/battery conditions change.

## A5.2 Adaptive heuristic
```text
ADAPT(metrics, params):
  repeat:
    metrics := MEASURE(frameTime, droppedFrames, battery, memory)
    if frameTime > 16ms or memoryPressure high:
       lower decode quality one level
       evict least-recently-used unpinned cache entries
       reduce prefetch distance
    else if frameTime < 13ms and battery > reserve and memoryPressure low:
       raise quality one level if budget allows
       increase prefetch by at most one item
    apply(params); wait for measurement window
  until parameters unchanged for 3 windows or budget exhausted
  return params, metrics
```
Selection criterion: first preserve the 16 ms frame-time target and memory/battery safety; improve quality only when measured headroom exists.

## A5.3 Trade-off
A feasible smooth configuration satisfies service constraints on observed windows. It does not prove globally minimum energy for a specified quality because the heuristic is local, workload-dependent and may settle at a local/non-optimal point. Exact optimality is traded for bounded, responsive decisions.
