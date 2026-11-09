import csv, math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"; DATA.mkdir(exist_ok=True)
USERS, SUBCARRIERS, REALISATIONS, SNR=8,64,1000,10.0
SEED=44064

class LCG:
    def __init__(self,seed): self.s=seed & 0xffffffff
    def random(self):
        self.s=(1664525*self.s+1013904223)&0xffffffff
        return (self.s+1)/4294967297.0

def main():
    rng=LCG(SEED)
    schemes=["fixed_contiguous","interleaved_round_robin","channel_aware_best_subcarrier"]
    totals={s:0.0 for s in schemes}; fair={s:0.0 for s in schemes}
    user_totals={s:[0.0]*USERS for s in schemes}
    for _ in range(REALISATIONS):
        gains=[[-math.log(rng.random()) for _ in range(USERS)] for _ in range(SUBCARRIERS)]
        for s in schemes:
            rates=[0.0]*USERS
            for k in range(SUBCARRIERS):
                if s=="fixed_contiguous": u=k//8
                elif s=="interleaved_round_robin": u=k%USERS
                else: u=max(range(USERS),key=lambda j:gains[k][j])
                rates[u]+=math.log2(1+SNR*gains[k][u])
            total=sum(rates); totals[s]+=total
            fair[s]+=total*total/(USERS*sum(x*x for x in rates))
            for u,x in enumerate(rates): user_totals[s][u]+=x
    summary=[]
    per_user=[]
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
    print("Completed",REALISATIONS,"channel realisations.")
if __name__=="__main__": main()
