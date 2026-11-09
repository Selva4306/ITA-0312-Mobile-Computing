import csv, math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"; FIG=ROOT/"figures"; DATA.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)
NS=[2,4,8,16]; THRESHOLD_DB=10.0
def af_power(n,deg):
    x=math.pi*math.sin(math.radians(deg))
    den=n*math.sin(x/2)
    if abs(den)<1e-12: return 1.0
    return (math.sin(n*x/2)/den)**2
def db(x): return 10*math.log10(max(x,1e-15))
def main():
    rows=[]; sir_rows=[]; pattern=[]
    for n in NS:
        vals=[(a,af_power(n,a)) for a in [i/10 for i in range(-900,901)]]
        hpbw=2*next(a for a,p in vals if a>=0 and p<=0.5)
        first_null=math.degrees(math.asin(min(1.0,2/n))) if n>2 else 90.0
        sidelobes=[p for a,p in vals if abs(a)>=first_null+0.1]
        sll=db(max(sidelobes)) if sidelobes else float("-inf")
        minsep=None
        for sep in range(5,61):
            sir=-db(af_power(n,sep))
            if sir>=THRESHOLD_DB: minsep=sep; break
        rows.append({"elements":n,"spacing_wavelengths":0.5,"hpbw_degrees":f"{hpbw:.2f}",
            "first_null_degrees":f"{first_null:.2f}","max_sidelobe_level_dB":f"{sll:.2f}",
            "sir_threshold_dB":THRESHOLD_DB,"minimum_separation_degrees":minsep if minsep else "not_met_5_to_60"})
        for sep in range(5,61,5):
            leak=af_power(n,sep)
            sir_rows.append({"elements":n,"separation_degrees":sep,"interference_gain_linear":f"{leak:.8f}",
                "interference_gain_dB":f"{db(leak):.3f}","equal_power_sir_dB":f"{-db(leak):.3f}"})
        for angle in range(-90,91,5):
            power=af_power(n,angle)
            pattern.append({"elements":n,"angle_degrees":angle,"normalised_power":f"{power:.8f}","pattern_dB":f"{db(power):.3f}"})
    for name,data in [("array_metrics.csv",rows),("sir_vs_separation.csv",sir_rows),("array_pattern.csv",pattern)]:
        with (DATA/name).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
    with (DATA/"design_parameters.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["parameter","value"]);w.writerows([["array","uniform linear array"],["element spacing","lambda/2"],["steering direction","0 degrees broadside"],["SIR threshold","10 dB"],["equal transmit powers","assumed"],["sector comparator","ideal 120 degree sector"],["pattern formula","|sin(N psi/2)/(N sin(psi/2))|; psi=pi(sin(theta)-sin(theta0))"]])
    print("Computed array patterns and SIR for N=2,4,8,16.")
    for r in rows: print(r)
if __name__=="__main__": main()
