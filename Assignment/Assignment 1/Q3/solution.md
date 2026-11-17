# Q3 – Capacity and interference derivation (6 marks)

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

