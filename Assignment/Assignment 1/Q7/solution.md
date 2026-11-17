# Q7 – Solve and interpret recurrence (4 marks)

Uniform splitting meets demand D when T₀·4^k≥D, hence
k_min=ceil(log₄(D/T₀)) (zero if D≤T₀).

Selective splitting:
k_min=ceil(log(D/T₀)/log(1+3f)).

For baseline capacity ~29,177 subscribers and demand 100,000, D/T₀≈3.43; one uniform split round (4×) is sufficient in the ideal model. It increases sites from 19 to 76 and halves radius to 0.25 km. Cost/backhaul rise and handoff opportunities roughly double; lower transmit power can reduce interference. Selective splitting reduces cost when demand is concentrated.

