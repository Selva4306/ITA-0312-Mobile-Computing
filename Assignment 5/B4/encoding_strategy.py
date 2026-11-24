"""Practical resolution/bitrate/upload heuristic vs exhaustive baseline."""
import csv
from itertools import product
from pathlib import Path
OUT=Path(__file__).parent
DEVICES=[
 {"device":"Low-end","cpu":2,"battery":22,"network":1,"capacity":3000},
 {"device":"Mid-range","cpu":5,"battery":58,"network":2,"capacity":4500},
 {"device":"Flagship","cpu":9,"battery":86,"network":3,"capacity":5000},
 {"device":"Low-battery WiFi","cpu":7,"battery":12,"network":3,"capacity":4000},
]
RES=[480,720,1080]; BIT=[500,1200,2500]
def estimate(d,r,b):
    encode=(r/480)**2* b/500 / max(d["cpu"],1)*18
    upload=(b*8/1000)/max(d["network"],0.5)*2
    energy=encode*0.035+upload*0.02
    return encode+upload,energy
def choose(d):
    # Heuristic: low battery caps 480p/500 kbps; weak network caps 720p/1200; otherwise choose quality by CPU.
    if d["battery"]<20: return 480,500,"battery saver"
    if d["network"]<2: return 480,500,"weak-network saver"
    if d["cpu"]<4: return 480,500,"CPU saver"
    if d["cpu"]<7: return 720,1200,"balanced"
    return 1080,2500,"high-capability"
def main():
    rows=[]
    for d in DEVICES:
        r,b,rule=choose(d);t,e=estimate(d,r,b)
        rows.append({"device":d["device"],"resolution":r,"bitrate_kbps":b,"upload_timing":"when network validated; defer below 20% battery","rule":rule,"estimated_seconds":round(t,2),"energy_units":round(e,2),"battery_percent":d["battery"],"estimated_battery_impact_pct":round(e/max(d["capacity"],1)*100,4)})
    with (OUT/"device_allocations.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    # Exhaustive challenge on a flagship profile: compare all settings under the same scalar objective.
    d=DEVICES[2]; candidates=[]
    for r,b in product(RES,BIT):
        t,e=estimate(d,r,b); quality_penalty={480:8,720:3,1080:0}[r]
        candidates.append((round(e+quality_penalty,3),r,b,round(t,2),round(e,3)))
    best=min(candidates)
    print("Heuristic allocations:")
    for x in rows: print(x)
    print("Flagship exhaustive best (energy + quality penalty):",best)
    print("Heuristic may be suboptimal because fixed CPU/network tiers ignore clip duration, thermal state and marginal quality benefit.")
if __name__=="__main__":main()
