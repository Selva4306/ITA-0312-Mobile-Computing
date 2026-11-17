# Task-specific implementation for Q11
decision={"macro_cluster_N":7,"macro_radius_km":.5,"sectoring":"3 x 120-degree sectors at high-load sites","borrowing":"guarded dynamic borrowing for transient imbalance","microcells":"split overloaded hotspots; use N=3 or N=4 only after SIR validation","gos_target":.02}
for k,v in decision.items(): print(f"{k}: {v}")
print("Use traffic heatmaps for selective rather than blanket densification.")
