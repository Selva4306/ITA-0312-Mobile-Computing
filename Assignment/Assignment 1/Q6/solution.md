# Q6 – Recurrence for repeated splitting (3 marks)

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

