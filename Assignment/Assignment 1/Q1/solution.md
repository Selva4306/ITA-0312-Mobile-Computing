# Q1 – Alternative frequency-planning strategies (5 marks)

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

