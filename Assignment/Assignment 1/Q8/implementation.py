# Task-specific implementation for Q8
from pathlib import Path
import runpy
parent=Path(__file__).resolve().parents[1]
sim=parent/"simulator.py"
if sim.exists():
    print("Running shared reproducible simulator.py ...")
    runpy.run_path(str(sim),run_name="__main__")
else: print("Missing ../simulator.py")
