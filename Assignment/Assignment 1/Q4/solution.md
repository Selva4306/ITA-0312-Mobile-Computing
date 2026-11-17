# Q4 – Best, average and worst cases (4 marks)

- **Best SIR:** user close to serving base station; desired power is high and co-channel sites are relatively distant.
- **Average SIR:** representative mid-cell location with typical shadowing and no dominant obstruction.
- **Worst SIR:** cell edge/corner near a boundary shared with a co-channel cell; serving distance is large and an interferer may be relatively close. Sector boundaries may also cause overlap/null issues.
- **Best blocking:** off-peak, when offered Erlangs are low.
- **Average blocking:** normal busy hour.
- **Worst blocking:** event surge or concentrated hotspot; blocking rises sharply when offered traffic approaches/exceeds circuit capacity.

For fixed D/R>1, ideal SIR increases with (D/R)^n; larger n attenuates distant interferers more strongly. In dense areas, however, shadowing, building penetration and coverage holes can dominate. Lognormal shadowing widens the SIR distribution, so the 5th percentile is more useful for edge reliability than the mean.

