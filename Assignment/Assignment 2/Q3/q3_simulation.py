import csv
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
DATA, FIG = ROOT / "data", ROOT / "figures"
DATA.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
SEED, BITS, EB_N0_DB = 20261109, 20000, 5.0
LENGTHS = [8, 16, 64]

def walsh(n):
    h = np.array([[1.0]])
    while len(h) < n:
        h = np.block([[h, h], [h, -h]])
    return h

def run_case(length, users, condition, rng):
    codes = rng.choice([-1.0, 1.0], (users, length)) if condition == "random_codes" else walsh(length)[:users].copy()
    if condition == "near_far":
        order = [2, 3] + [i for i in range(length) if i not in (2, 3)]
        codes = walsh(length)[order[:users]].copy()
    bits = rng.choice([-1.0, 1.0], (users, BITS))
    amps = np.ones(users)
    effective = codes.copy()
    if condition == "near_far":
        amps[0] = np.sqrt(10.0)
        effective[0] = np.roll(codes[0], 1)  # one-chip timing offset
    signal = (amps[:, None, None] * bits[:, :, None] * effective[:, None, :]).sum(axis=0)
    n0 = 10 ** (EB_N0_DB / 10)
    noise = rng.normal(0.0, np.sqrt(length / (2.0 * n0)), signal.shape)
    rx = signal + noise
    decisions = np.array([np.sign(rx @ codes[u] / length) for u in range(users)])
    err = decisions != bits
    measured = err[1:] if condition == "near_far" else err
    ber = float(measured.mean())
    worst = float(err[1:].mean(axis=1).max()) if condition == "near_far" else ber
    correlations = [abs(float(np.dot(effective[i], effective[j]) / length))
                    for i in range(users) for j in range(i + 1, users)]
    return ber, worst, int(measured.sum()), int(measured.size), correlations

def main():
    rng = np.random.default_rng(SEED)
    results, corrs, supports = [], [], []
    for length in LENGTHS:
        counts = sorted(set([2, 4, 8, min(16, length), min(32, length), length]))
        for cond in ["walsh_sync", "random_codes", "near_far"]:
            for users in counts:
                ber, worst, errors, total, cs = run_case(length, users, cond, rng)
                pg = 10 * np.log10(length)
                results.append(dict(condition=cond, code_length_chips=length, simultaneous_users=users,
                    bits_per_measured_user=BITS, measured_users=(users-1 if cond=="near_far" else users),
                    total_measured_bits=total, bit_errors=errors, ber="{:.8f}".format(ber),
                    worst_weak_user_ber="{:.8f}".format(worst), processing_gain_linear=length,
                    processing_gain_db="{:.3f}".format(pg), eb_n0_db=EB_N0_DB))
                corrs.append(dict(condition=cond, code_length_chips=length, simultaneous_users=users,
                    pair_count=len(cs), mean_absolute_correlation="{:.6f}".format(np.mean(cs) if cs else 0),
                    maximum_absolute_correlation="{:.6f}".format(max(cs) if cs else 0),
                    zero_correlation_fraction="{:.6f}".format(np.mean(np.array(cs)<1e-12) if cs else 1)))
                if worst <= 1e-2:
                    supports.append(dict(condition=cond, code_length_chips=length,
                        tested_users_at_ber_le_1e_2=users, ber_at_that_load="{:.8f}".format(worst)))
    # Keep the largest tested passing load for each condition and code length.
    best = {}
    for r in supports:
        key = (r["condition"], r["code_length_chips"])
        if key not in best or r["tested_users_at_ber_le_1e_2"] > best[key]["tested_users_at_ber_le_1e_2"]:
            best[key] = r
    for name, rows in [("simulation_results.csv", results), ("correlation_values.csv", corrs),
                       ("supported_users.csv", list(best.values()))]:
        with (DATA / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
    conditions = [
        ["walsh_sync","Walsh-Hadamard","All users chip-synchronous","Equal received power","Ideal orthogonal baseline"],
        ["random_codes","Random bipolar spreading sequences","All users chip-synchronous","Equal received power","Non-zero cross-correlation and multiple-access interference"],
        ["near_far","Walsh-Hadamard","Strong user delayed by one chip","Strong user has 10x power; others equal","Near-far leakage when timing destroys orthogonality"]]
    with (DATA / "test_conditions.csv").open("w", newline="") as f:
        w=csv.writer(f); w.writerow(["condition","code_family","timing","power_setting","purpose"]); w.writerows(conditions)
    # Simple SVG BER plot, using worst weak-user BER so the near-far effect is visible.
    colors={"walsh_sync":"#2563eb","random_codes":"#dc2626","near_far":"#16a34a"}
    labels={"walsh_sync":"Walsh synchronous","random_codes":"Random codes","near_far":"Walsh + 10x near-far"}
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="390" viewBox="0 0 1080 390">',
         '<rect width="100%" height="100%" fill="white"/>',
         '<text x="540" y="28" text-anchor="middle" font-family="Arial" font-size="19">DS-CDMA BER vs users (Eb/N0 = 5 dB)</text>']
    for panel, length in enumerate(LENGTHS):
        x0=65+panel*345; pw=290; ph=245; y0=325
        svg += ['<text x="{}" y="62" text-anchor="middle" font-family="Arial" font-size="15">{}-chip codes</text>'.format(x0+pw/2,length),
                '<path d="M{} 80 V{} H{}" fill="none" stroke="#333"/>'.format(x0,y0,x0+pw)]
        for t,v in enumerate([1,.1,.01,.001]):
            yy=80+t*ph/3
            svg += ['<path d="M{} {:.1f} H{}" stroke="#ddd"/>'.format(x0,yy,x0+pw),
                    '<text x="{}" y="{:.1f}" text-anchor="end" font-family="Arial" font-size="10">{}</text>'.format(x0-8,yy+4,v)]
        for cond in labels:
            sub=[r for r in results if r["code_length_chips"]==length and r["condition"]==cond]
            pts=[]
            for r in sub:
                xx=x0+(r["simultaneous_users"]-1)/max(1,length-1)*pw
                yy=80+(0-np.log10(max(float(r["worst_weak_user_ber"]),.0001)))/3*ph
                pts.append("{:.1f},{:.1f}".format(xx,yy))
            svg.append('<polyline points="{}" fill="none" stroke="{}" stroke-width="2.4"/>'.format(" ".join(pts),colors[cond]))
        svg.append('<text x="{}" y="352" text-anchor="middle" font-family="Arial" font-size="12">Users</text>'.format(x0+pw/2))
    for i,cond in enumerate(labels):
        x=350+i*160
        svg += ['<line x1="{}" y1="378" x2="{}" y2="378" stroke="{}" stroke-width="3"/>'.format(x,x+20,colors[cond]),
                '<text x="{}" y="382" font-family="Arial" font-size="11">{}</text>'.format(x+25,labels[cond])]
    svg.append('</svg>'); (FIG/"ber_vs_users.svg").write_text("\n".join(svg))
    sub=[r for r in corrs if r["code_length_chips"]==16 and r["simultaneous_users"]==8]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="330" viewBox="0 0 720 330">',
         '<rect width="100%" height="100%" fill="white"/>',
         '<text x="360" y="28" text-anchor="middle" font-family="Arial" font-size="17">Maximum cross-correlation (16 chips, 8 users)</text>']
    for i,r in enumerate(sub):
        x=105+i*205; v=float(r["maximum_absolute_correlation"]); h=v*190
        svg += ['<rect x="{}" y="{}" width="90" height="{}" fill="{}"/>'.format(x,250-h,h,colors[r["condition"]]),
                '<text x="{}" y="{}" text-anchor="middle" font-family="Arial" font-size="13">{:.3f}</text>'.format(x+45,242-h,v),
                '<text x="{}" y="275" text-anchor="middle" font-family="Arial" font-size="12">{}</text>'.format(x+45,labels[r["condition"]])]
    svg.append('</svg>'); (FIG/"correlation_comparison.svg").write_text("\n".join(svg))
    print("Created reproducible DS-CDMA results in", ROOT)

if __name__ == "__main__":
    main()
