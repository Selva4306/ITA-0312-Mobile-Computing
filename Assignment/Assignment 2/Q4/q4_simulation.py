import csv, math, cmath
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"; DATA.mkdir(exist_ok=True)
USERS, SUBCARRIERS, REALISATIONS, SNR=8,64,1000,10.0
MIN_RATE=8.0
SEED=44064

class LCG:
    def __init__(self,seed): self.s=seed & 0xffffffff
    def random(self):
        self.s=(1664525*self.s+1013904223)&0xffffffff
        return (self.s+1)/4294967297.0

def main():
    rng=LCG(SEED)
    schemes=["fixed_contiguous","interleaved_round_robin","channel_aware_best_subcarrier","minimum_rate_aware"]
    totals={s:0.0 for s in schemes}; fair={s:0.0 for s in schemes}
    user_totals={s:[0.0]*USERS for s in schemes}
    for _ in range(REALISATIONS):
        gains=[[-math.log(rng.random()) for _ in range(USERS)] for _ in range(SUBCARRIERS)]
        allocations={s:[[] for _ in range(USERS)] for s in schemes[:3]}
        for k in range(SUBCARRIERS):
            allocations["fixed_contiguous"][k//8].append(k)
            allocations["interleaved_round_robin"][k%USERS].append(k)
            u=max(range(USERS),key=lambda j:gains[k][j])
            allocations["channel_aware_best_subcarrier"][u].append(k)
        mine=[[] for _ in range(USERS)]
        for u in range(USERS):
            for k in range(u,SUBCARRIERS,16): mine[u].append(k)
        used={k for group in mine for k in group}
        remaining=[k for k in range(SUBCARRIERS) if k not in used]
        def rates_now():
            return [sum(math.log2(1+SNR*gains[k][u]) for k in mine[u]) for u in range(USERS)]
        while min(rates_now())<MIN_RATE and remaining:
            rates=rates_now(); u=min(range(USERS),key=lambda j:rates[j])
            k=max(remaining,key=lambda j:gains[j][u]); mine[u].append(k); remaining.remove(k)
        for k in remaining:
            u=max(range(USERS),key=lambda j:gains[k][j]); mine[u].append(k)
        allocations["minimum_rate_aware"]=mine
        for s,groups in allocations.items():
            rates=[sum(math.log2(1+SNR*gains[k][u]) for k in groups[u]) for u in range(USERS)]
            total=sum(rates); totals[s]+=total
            fair[s]+=total*total/(USERS*sum(x*x for x in rates))
            for u,x in enumerate(rates): user_totals[s][u]+=x
    summary=[]; per_user=[]
    for s in schemes:
        avg=totals[s]/REALISATIONS
        summary.append({"scheme":s,"mean_sum_throughput_bps_hz":f"{avg:.4f}",
            "jains_fairness":f"{fair[s]/REALISATIONS:.4f}",
            "minimum_mean_user_rate":f"{min(user_totals[s])/REALISATIONS:.4f}",
            "maximum_mean_user_rate":f"{max(user_totals[s])/REALISATIONS:.4f}"})
        for u,x in enumerate(user_totals[s],1):
            per_user.append({"scheme":s,"user":u,"mean_throughput_bps_hz":f"{x/REALISATIONS:.4f}"})
    for name,rows in [("simulation_results.csv",summary),("per_user_throughput.csv",per_user)]:
        with (DATA/name).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    with (DATA/"orthogonality.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["subcarrier_pair","normalised_inner_product"])
        for a,b in [(0,1),(0,2),(1,2)]:
            dot=sum(cmath.exp(2j*math.pi*(a-b)*n/SUBCARRIERS) for n in range(SUBCARRIERS))/SUBCARRIERS
            w.writerow([f"{a}-{b}",f"{abs(dot):.12f}"])
    print("Completed",REALISATIONS,"realisations; target rate",MIN_RATE,"bps/Hz.")
    for row in summary: print(row)
if __name__=="__main__": main()
