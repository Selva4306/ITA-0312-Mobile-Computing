# Q12 – Stadium design challenge (8 marks)

### A. Impact

Event offered traffic is 25,000×0.05=1,250 Erlangs in 1 km². Uniform traffic and permanent-capacity assumptions no longer hold. The surge is predictable, lasts four hours and occurs about twice monthly.

### B. Original design

At R=0.50 km, the idealised 1 km² zone has two macro sites. N=7 gives 48 channels/site and 625 Erlangs/site. Erlang-B predicts about 92.3% blocking. Sectoring improves SIR but cannot create enough circuits; the macro layout cannot be reused unchanged.

### C. Adaptation

Deploy temporary stadium small cells / cell-on-wheels, local N=3 reuse, power control, directional antennas and guarded borrowing. Seven temporary R=0.25 km sites still predict about 38.2% blocking. A 112-channel N=3 site carries about 99.624 Erlangs at 2% GoS; ceil(1250/99.624)=13 temporary sites are the simplified theoretical minimum. Add operational margin (e.g. 15–16 sites), validate SIR, and provide temporary backhaul. Remove/return temporary resources after the event.

### D. Defence

A permanent 13+ site stadium layer would be underused most of the month. Temporary deployment aligns cost with the predictable eight event-hours/month while leaving township macro coverage intact. The decision depends on SIR, backhaul and interference validation. If temporary sites cannot be deployed, call admission/load controls or additional spectrum are needed; sectoring alone cannot provide 1,250 Erlangs.

