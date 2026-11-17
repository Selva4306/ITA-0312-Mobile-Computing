# Task-specific implementation for Q6
C0=19
R0=.5
T0=29177
for k in range(4):
    print(f"round={k}: cells={C0*4**k}, radius={R0/2**k:.4f} km, ideal capacity={T0*4**k:.0f} subscribers")
print("Selective split: C_k=C_0(1+3f)^k for split fraction f.")
