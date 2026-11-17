# Task-specific implementation for Q2
params={"area_km2":12.0,"duplex_traffic_channels":336,"erlang_per_subscriber":0.025,"gos_target":0.02,"macro_radius_km":0.5,"shadowing_sigma_db":4.0,"subscribers":[1000,10000,20000,100000]}
for key,value in params.items(): print(f"{key}: {value}")
