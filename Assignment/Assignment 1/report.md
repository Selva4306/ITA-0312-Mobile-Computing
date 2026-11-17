# Assignment 1 – CO1: Hexagonal Cellular Network Planning

**Scenario:** 12 km² university township. **Inputs:** 336 duplex traffic channels after control overhead; 0.025 Erlang/subscriber; target GoS ≤2%; subscribers 1,000 → 10,000 → 20,000 → 100,000+; stadium event 25,000 people × 0.05 Erlang in 1 km² for four hours.

> **Assumptions:** The brief does not specify cell radius, shadowing spread, traffic distribution or cost rates. This analysis assumes macro radius R=0.50 km, lognormal shadowing σ=4 dB and uses a relative planning-cost index (not currency). These must be replaced by survey data before deployment.

## Executive recommendation

Use a hierarchical macro/micro network with conservative N=7 reuse, 120° sectoring at interference-limited macro sites and guarded dynamic channel borrowing for short local peaks. The 19-cell macro layout supports about 29,177 subscriber-equivalents at 2% blocking. At 100,000 subscribers, introduce a microcell layer in overloaded areas. A uniform first split gives 76 cells (R≈0.25 km) and about 2,917.8 Erlangs of idealised capacity, or roughly 116,700 subscriber-equivalents.

For the four-hour stadium event, do not permanently densify the township. Use temporary small cells / cell-on-wheels and guarded borrowing. Seven temporary N=3 sites still produce approximately 38.2% blocking in the simplified model; at least 13 sites are required by the Erlang-B estimate to approach 2% GoS, with additional engineering margin and SIR/backhaul validation.

## Task 1 – Alternative frequency-planning strategies (5 marks)

### A. Fixed cluster reuse (iterative)

A cluster of N cells receives disjoint channel groups, repeated in non-adjacent clusters. Valid ideal hexagonal cluster sizes satisfy N=i²+ij+j²; tested values 3, 4, 7 and 12 are valid. Reuse distance D=R√(3N) and reuse ratio Q=D/R=√(3N).

The 336 channels are treated as duplex traffic circuits after control overhead. FDMA separates carriers by frequency; TDMA divides carriers into time slots; CDMA/OFDMA allocate code/subcarrier resources. They are not physically identical, so the model uses a circuit-equivalent abstraction.

Pseudocode:
```text
INPUT: S channels, candidate cluster sizes Nset, hexagonal grid G
best ← NONE
FOR each N IN Nset DO
    IF N = i² + i·j + j² for integer i,j THEN
        C ← FLOOR(S/N)
        Q ← SQRT(3N)
        estimate first-tier SIR for selected path-loss exponent
        IF SIR ≥ required_threshold THEN
            assign N disjoint channel groups
            repeat cluster pattern across G
            retain feasible candidate with best cost/capacity
        END IF
    END IF
END FOR
RETURN best channel map
```
**Principle:** spatial reuse. **Preprocessing/cost:** traffic heatmap, hex-grid/site coordinates, terrain/building and propagation survey, channel inventory. The operator bears survey and planning cost. Large N improves SIR but reduces channels per cell.

### B. 120° sectorised reuse

Divide each site into three directional sectors and use directional antennas to reduce dominant co-channel interference. The idealised model uses two dominant interferers rather than six; side lobes, reflections and sector overlap make real performance less ideal.

```text
FOR each cell
    divide azimuth into three 120-degree sectors
    assign antenna, azimuth, tilt and power
    map each user to the strongest usable serving sector
    calculate SIR including side-lobe leakage
    IF SIR < threshold THEN adjust tilt, azimuth or reuse plan
END FOR
```
**Principle:** spatial filtering. **Preprocessing/cost:** antenna patterns, azimuth/tilt survey, sector traffic forecasts and drive tests. It improves interference and directional capacity but adds radio/antenna and optimisation cost.

### C. Guarded dynamic channel borrowing

A congested cell borrows an idle neighbour channel only when an interference guard is satisfied. It returns the channel when the call ends, the donor needs it or the guard fails.

```text
WHEN call arrives in cell c
    IF local channel idle THEN allocate it
    ELSE
        candidates ← idle neighbour channels satisfying reuse/SIR guard
        IF candidates exist THEN
            choose candidate with greatest predicted SIR margin
            mark channel BORROWED(c, donor, expiry)
            allocate channel
        ELSE block call
        END IF
    END IF
WHEN call ends OR guard fails OR donor load rises
    release borrowed channel and update both cell tables
END
```
**Principle:** trunking efficiency and load balancing. **Preprocessing/cost:** channel occupancy, neighbour list, interference matrix and coordination signalling. It improves local busy-hour use but adds control complexity.

### D. Hierarchical macro–micro layer (recursive)

Keep macro cells for broad coverage and add microcells in hotspots. A split changes R→R/2; hexagonal cell area falls by four, so four child cells cover approximately one parent cell.

```text
PROCEDURE SPLIT(cell)
    IF demand ≤ capacity OR radius ≤ minimum_radius THEN RETURN
    create four child cells of radius cell.radius/2
    assign a reuse-feasible channel plan and lower transmit power
    FOR each child DO estimate demand/capacity; SPLIT(child) END FOR
END
```
**Principle:** spatial reuse by cell splitting. **Preprocessing/cost:** fine-grained traffic map, site acquisition, power, permits, backhaul and handoff survey. Capacity grows, but so do sites, handoffs and operating cost.

## Task 2 – Governing design parameters (2 marks)

| Strategy | Governing parameter | Reason / growth response |
|---|---|---|
| Fixed reuse | Cluster N and reuse ratio Q | N controls channels/cell (S/N) and co-channel spacing (√3NR). Higher demand favours smaller N or more cells, constrained by SIR. |
| Sectoring | Sector width/count and effective interferer count | Directional isolation changes interference; add sectors where demand is directional, avoiding overlap. |
| Dynamic borrowing | Borrowable pool and interference guard | Determines whether spare channels can be reused safely; borrowing contention rises with demand. |
| Macro–micro | Radius R and split depth k | Sites scale approximately as 1/R²; smaller cells enable more spatial reuse and more handoffs. |

## Task 3 – Capacity and interference derivation (6 marks)

### Geometry and sites

For a regular hexagon with centre-to-vertex radius R, side length is R and area A_cell=(3√3/2)R². At R=0.50 km, A_cell=0.649519 km². Therefore ceil(12/0.649519)=19 idealised macro cells cover 12 km². Boundary clipping and terrain may increase the real count.

### Cluster and reuse

N=i²+ij+j², D=R√(3N), Q=D/R=√(3N). For N=7, Q=√21=4.5826 and D=2.291 km at R=0.50 km.

### Channels and Erlang-B

Channels per cell C=floor(S/N). For N=7, C=48. Offered traffic per cell for U uniformly distributed subscribers is A=U×0.025/19 Erlangs.

Erlang-B recursion:
B(0,A)=1
B(m,A)=A·B(m−1,A)/(m+A·B(m−1,A)).

Solving B(48,A)≤0.02 gives about 38.392 Erlangs/cell. System capacity is 19×38.392=729.448 Erlangs, equivalent to approximately 29,178 subscribers at 0.025 Erlang each.

### SIR

For i₀ equal-distance first-tier interferers at D, serving distance R and path-loss exponent n:
SIR≈(D/R)^n/i₀=(3N)^(n/2)/i₀.

For N=7, n=4 and six interferers: SIR=21²/6=73.5; 10log10(73.5)=18.663 dB, matching the brief's approximately 18.7 dB check. Ideal 120° sectoring with two dominant interferers gives 10log10(21²/2)=23.43 dB, a theoretical 4.77 dB gain. Real antenna patterns reduce this ideal gain.

### Cost–capacity

Cost=c_survey·N_sites+c_site·N_sites+c_coordination·N_sectors+c_backhaul·N_micro.
The simulator uses a relative effort index 1.15×N_sites plus a small micro-layer setup weight; it is not a currency estimate.

C_system(N,R)=N_sites(R)×ErlangB_inverse(floor(S/N),0.02).
The design objective is minimum cost subject to blocking ≤2%, SIR ≥ threshold, coverage and backhaul constraints—not maximum capacity alone.

## Task 4 – Best, average and worst cases (4 marks)

- **Best SIR:** user close to serving base station; desired power is high and co-channel sites are relatively distant.
- **Average SIR:** representative mid-cell location with typical shadowing and no dominant obstruction.
- **Worst SIR:** cell edge/corner near a boundary shared with a co-channel cell; serving distance is large and an interferer may be relatively close. Sector boundaries may also cause overlap/null issues.
- **Best blocking:** off-peak, when offered Erlangs are low.
- **Average blocking:** normal busy hour.
- **Worst blocking:** event surge or concentrated hotspot; blocking rises sharply when offered traffic approaches/exceeds circuit capacity.

For fixed D/R>1, ideal SIR increases with (D/R)^n; larger n attenuates distant interferers more strongly. In dense areas, however, shadowing, building penetration and coverage holes can dominate. Lognormal shadowing widens the SIR distribution, so the 5th percentile is more useful for edge reliability than the mean.

## Task 5 – Scaling and sensitivity (3 marks)

- Per-cell channels are approximately S/N; per-cell circuit capacity generally falls as N rises.
- Ideal SIR scales as N^(n/2).
- Cell count scales as 1/R²; halving R creates about four times as many cells.
- Total offered traffic is 25 E at 1,000 subscribers; 250 E at 10,000; 500 E at 20,000; and 2,500 E at 100,000.
- Baseline N=7, R=0.50 km supports about 29,177 subscriber-equivalents. It fails at 100,000. One uniform split gives 76 cells and approximately four times the capacity (~116,700 subscriber-equivalents) in the ideal model.
- A smaller path-loss exponent (2.5) means distant interference decays less rapidly, making reuse harder. At n=4 ideal SIR is higher, but dense-area shadowing and blockage still require field validation.

A practical split trigger is a forecast cell load approaching its Erlang-B capacity or a 5th-percentile SIR below threshold. Split hotspots first rather than densifying every cell.

## Task 6 – Recurrence for repeated splitting (3 marks)

Let C₀ be initial cell count, R₀ initial radius and k uniform split rounds. Each split creates four children:

- R_k=R₀/2^k
- C_k=4C_(k−1)=C₀·4^k
- With an unchanged feasible per-cell channel plan, ideal aggregate capacity T_k=4T_(k−1)=T₀·4^k
- Required transmit power for equal edge field: P_k=P₀/2^(nk)
- At fixed speed, handoff boundary opportunity scales approximately as H_k∝1/R_k=2^k/R₀
- Work/site cost per uniform round is proportional to the number of cells split (C₀·4^(k−1)).

For selective splitting, if fraction f of current cells is split each round:
C_k=C_(k−1)(1+3f)=C₀(1+3f)^k.
Capacity scales similarly only when split cells receive a complete interference-feasible channel plan. Base case: k=0, C₀=19, R₀=0.50 km.

## Task 7 – Solve and interpret recurrence (4 marks)

Uniform splitting meets demand D when T₀·4^k≥D, hence
k_min=ceil(log₄(D/T₀)) (zero if D≤T₀).

Selective splitting:
k_min=ceil(log(D/T₀)/log(1+3f)).

For baseline capacity ~29,177 subscribers and demand 100,000, D/T₀≈3.43; one uniform split round (4×) is sufficient in the ideal model. It increases sites from 19 to 76 and halves radius to 0.25 km. Cost/backhaul rise and handoff opportunities roughly double; lower transmit power can reduce interference. Selective splitting reduces cost when demand is concentrated.

## Task 8 – Implementation and tests (4 marks)

simulator.py generates axial hex-grid coordinates, assigns channel groups with an interference-distance graph-colouring check, computes hexagonal area/site estimates, applies Erlang-B recursion and inverse capacity search, and runs fixed-seed Monte-Carlo SIR for N={3,4,7,12} and n={2.5,3,4}, a sectorised two-interferer comparison, subscriber-growth blocking and the event surge. It uses seed 4306 and 12,000 SIR samples per case.

The textbook N=7,n=4,six-interferer sanity case is calculated separately as 18.663 dB. Monte-Carlo results differ because they sample user locations, vary interferer distances and include shadowing. The dynamic-borrowing capacity row is an effective-N=4 guarded-borrowing planning proxy, not a time-stepped donor-cell state simulation; its feasibility still requires a live interference guard.

## Task 9 – Experimental evidence (3 marks)

- channel_map.csv: generated axial cell coordinates and channel-group allocation for N=3,4,7,12.\n- sir_results.csv: mean SIR, 5th percentile and outage probability.
- capacity_summary.csv: channels/cell, sites, 2% Erlangs and relative planning-cost index.
- traffic_results.csv: offered traffic and blocking at 1k, 10k, 20k and 100k.
- event_surge.csv: stadium surge and temporary-site estimates.
- Figures: sir_vs_cluster.svg, blocking_vs_growth.svg, sir_pathloss_sensitivity.svg.

Channels, sites, Erlangs, blocking and outage are the primary evidence; execution time is not used as the sole performance measure.

## Task 10 – Theory vs simulation (4 marks)

The N=7,n=4 analytical check is 18.663 dB. Monte-Carlo results vary because user positions, interferer distances and shadowing vary. The analytical formula assumes six equal-distance interferers and representative edge geometry; it is not the SIR of every user. Erlang-B assumes Poisson arrivals, exponential holding times, an infinite-source population and no queueing. Real results differ due to handoff priority, retrials, non-uniform traffic, sector imbalance, borrowing and integer channel rounding.

## Task 11 – Final recommendation (4 marks)

Deploy a macro layer with N=7 and R≈0.50 km; add three 120° sectors at high-load/interference-limited sites and guarded borrowing for transient imbalance. At 100,000 subscribers, add a microcell layer in overloaded areas. The conservative uniform upper-bound is 76 sites at R≈0.25 km and N=7; traffic heatmaps should determine which sites actually need splitting. Use N=3 or N=4 locally only after validating SIR and neighbour interference. This balances capacity, interference, handoff load, site cost and maintainability.

## Task 12 – Stadium design challenge (8 marks)

### A. Impact

Event offered traffic is 25,000×0.05=1,250 Erlangs in 1 km². Uniform traffic and permanent-capacity assumptions no longer hold. The surge is predictable, lasts four hours and occurs about twice monthly.

### B. Original design

At R=0.50 km, the idealised 1 km² zone has two macro sites. N=7 gives 48 channels/site and 625 Erlangs/site. Erlang-B predicts about 92.3% blocking. Sectoring improves SIR but cannot create enough circuits; the macro layout cannot be reused unchanged.

### C. Adaptation

Deploy temporary stadium small cells / cell-on-wheels, local N=3 reuse, power control, directional antennas and guarded borrowing. Seven temporary R=0.25 km sites still predict about 38.2% blocking. A 112-channel N=3 site carries about 99.624 Erlangs at 2% GoS; ceil(1250/99.624)=13 temporary sites are the simplified theoretical minimum. Add operational margin (e.g. 15–16 sites), validate SIR, and provide temporary backhaul. Remove/return temporary resources after the event.

### D. Defence

A permanent 13+ site stadium layer would be underused most of the month. Temporary deployment aligns cost with the predictable eight event-hours/month while leaving township macro coverage intact. The decision depends on SIR, backhaul and interference validation. If temporary sites cannot be deployed, call admission/load controls or additional spectrum are needed; sectoring alone cannot provide 1,250 Erlangs.

## Assumptions and limitations

1. R=0.50 km, σ=4 dB shadowing, ideal geometry and cost weights are assumptions, not measured facts.
2. Erlang-B is a loss model without queueing; handoff/priority policies may change blocking.
3. Sectoring is idealised as two dominant interferers; measured antenna patterns are less ideal.
4. Monte-Carlo results are comparative engineering estimates, not a calibrated propagation prediction.
5. Dynamic borrowing is represented by an effective N=4 planning case, not a full call-arrival/channel-donor event simulation. The SIR Monte-Carlo sweep is a common geometry comparison; sectoring is the variant that changes the dominant-interferer count.\n6. Deployment requires drive tests, terrain/building data, antenna patterns, regulatory checks and backhaul validation.
