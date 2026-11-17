# Task-specific implementation for Q5
import math
base=29177
for users in (1000,10000,20000,100000):
    print(f"{users:>7} subscribers: {users*.025:.1f} offered Erlangs; baseline capacity pass={users<=base}")
print("Halving cell radius multiplies ideal site count and aggregate capacity by approximately four.")
