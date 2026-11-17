#!/usr/bin/env python3
"""Reproducible cellular-planning simulator for Mobile Computing Assignment 1."""
from __future__ import annotations
import csv, math, random, statistics, json
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
SEED = 4306
AREA_KM2 = 12.0
CHANNELS = 336
BUSY_ERLANG_PER_SUB = 0.025
GOS = 0.02
R_KM = 0.5
SUBSCRIBERS = [1000, 10000, 20000, 100000]
CLUSTERS = [3, 4, 7, 12]
PATH_LOSS = [2.5, 3.0, 4.0]
SAMPLES = 12000


def erlang_b(channels: int, offered: float) -> float:
    b = 1.0
    for m in range(1, channels + 1):
        b = offered * b / (m + offered * b)
    return b


def capacity_at_gos(channels: int, target: float = GOS) -> float:
    lo, hi = 0.0, max(1.0, channels * 3.0)
    for _ in range(80):
        mid = (lo + hi) / 2
        if erlang_b(channels, mid) <= target:
            lo = mid
        else:
            hi = mid
    return lo


def hex_area(radius: float) -> float:
    return 3 * math.sqrt(3) * radius * radius / 2


def generate_hex_grid(rings: int = 3, radius: float = R_KM, count: int = 19):
    """Generate axial hex-cell coordinates, ordered from the centre outward."""
    cells = []
    for q in range(-rings, rings + 1):
        for r in range(-rings, rings + 1):
            if max(abs(q), abs(r), abs(q + r)) <= rings:
                x = math.sqrt(3) * radius * (q + r / 2)
                y = 1.5 * radius * r
                ring = max(abs(q), abs(r), abs(q + r))
                cells.append({'q': q, 'r': r, 'x_km': x, 'y_km': y, 'ring': ring})
    cells.sort(key=lambda c: (c['ring'], c['r'], c['q']))
    return cells[:count]


def assign_channel_groups(cells, cluster_size: int, radius: float):
    """DSATUR-style backtracking coloring; same-group sites stay at least D apart."""
    reuse_distance = radius * math.sqrt(3 * cluster_size)
    n = len(cells)
    neighbours = [set() for _ in cells]
    for i in range(n):
        for j in range(i):
            dx = cells[i]['x_km'] - cells[j]['x_km']
            dy = cells[i]['y_km'] - cells[j]['y_km']
            if math.hypot(dx, dy) < reuse_distance - 1e-9:
                neighbours[i].add(j)
                neighbours[j].add(i)
    colors = [-1] * n

    def solve(done=0):
        if done == n:
            return True
        uncolored = [i for i, color in enumerate(colors) if color < 0]
        vertex = max(uncolored, key=lambda i: (
            len({colors[j] for j in neighbours[i] if colors[j] >= 0}),
            len(neighbours[i])))
        forbidden = {colors[j] for j in neighbours[vertex] if colors[j] >= 0}
        for color in range(cluster_size):
            if color not in forbidden:
                colors[vertex] = color
                if solve(done + 1):
                    return True
                colors[vertex] = -1
        return False

    if not solve():
        raise ValueError(f'Could not color {n} cells with N={cluster_size} under D={reuse_distance:.3f} km')
    return colors


def sir_samples(n_cluster: int, exponent: float, sectored: bool, seed: int) -> list[float]:
    rng = random.Random(seed)
    reuse = math.sqrt(3 * n_cluster)
    # First-tier co-channel sites lie at reuse distance; angular and radial
    # perturbations approximate user position and non-ideal site geometry.
    # The textbook equidistant edge-user sanity check is calculated separately:
    # SIR = (sqrt(3N))**n / 6.
    interferers = 2 if sectored else 6
    values = []
    for _ in range(SAMPLES):
        r_user = math.sqrt(rng.random()) * R_KM
        serving = max(0.025, r_user)
        total = 0.0
        for j in range(interferers):
            angle = 2 * math.pi * j / interferers + rng.uniform(-0.12, 0.12)
            d = reuse * R_KM + rng.uniform(-0.18, 0.18) * R_KM
            di = math.sqrt(max(0.01, d*d + r_user*r_user - 2*d*r_user*math.cos(angle)))
            shadow_db = rng.gauss(0, 4.0)
            total += (serving / di) ** exponent * 10 ** (shadow_db / 10)
        values.append(10 * math.log10(1 / max(total, 1e-15)))
    return values


def pct(values, p):
    s = sorted(values)
    return s[min(len(s)-1, int((len(s)-1)*p))]


def write_csv(path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    random.seed(SEED)
    cell_area = hex_area(R_KM)
    sites = math.ceil(AREA_KM2 / cell_area)
    sir_rows, capacity_rows, traffic_rows = [], [], []
    grid_cells = generate_hex_grid(rings=3, radius=R_KM, count=sites)
    channel_map_rows = []
    for cluster_size in CLUSTERS:
        groups = assign_channel_groups(grid_cells, cluster_size, R_KM)
        channels_per_cell = CHANNELS // cluster_size
        for cell, group in zip(grid_cells, groups):
            channel_map_rows.append({**cell, 'cluster_N': cluster_size, 'channel_group': group,
                                     'first_channel_index': group * channels_per_cell,
                                     'last_channel_index': (group + 1) * channels_per_cell - 1})

    strategies = [
        ('Fixed reuse', 7, 1.0, 'Fixed cluster reuse; six first-tier interferers'),
        ('120-degree sectoring', 7, 1/3, 'N=7 baseline; idealized two dominant interferers'),
        ('Dynamic borrowing', 4, 1.0, 'Effective N=4; borrowing subject to interference guard'),
        ('Hierarchical microcells N=3', 3, 1.0, 'N=3 local layer; smaller radius increases site count'),
        ('Hierarchical microcells N=7', 7, 1.0, 'N=7 local layer; conservative reuse with smaller radius'),
    ]
    for strategy, n0, factor, note in strategies:
        for n in CLUSTERS:
            for exponent in PATH_LOSS:
                for sectored in ([False, True] if strategy == '120-degree sectoring' else [False]):
                    vals = sir_samples(n, exponent, sectored, SEED + n*100 + int(exponent*10) + int(sectored))
                    sir_rows.append({
                        'strategy': strategy, 'cluster_N': n, 'path_loss_n': exponent,
                        'sectoring': sectored, 'samples': SAMPLES,
                        'sir_mean_db': round(statistics.mean(vals), 3),
                        'sir_p05_db': round(pct(vals, .05), 3),
                        'outage_below_12db': round(sum(v < 12 for v in vals)/len(vals), 5),
                    })
        effective_n = n0
        channels_cell = max(1, CHANNELS // effective_n)
        erlangs_cell = capacity_at_gos(channels_cell)
        effective_radius = R_KM / 2 if strategy.startswith('Hierarchical microcells') else R_KM
        nsites = sites * 4 if strategy.startswith('Hierarchical microcells') else sites
        total_erlangs = erlangs_cell * nsites
        for subs in SUBSCRIBERS:
            offered_total = subs * BUSY_ERLANG_PER_SUB
            offered_cell = offered_total / nsites
            blocking = erlang_b(channels_cell, offered_cell)
            traffic_rows.append({
                'strategy': strategy, 'subscribers': subs, 'sites': nsites,
                'channels_per_cell': channels_cell, 'offered_erlangs_total': round(offered_total, 3),
                'offered_erlangs_per_cell': round(offered_cell, 3),
                'blocking_probability': round(blocking, 6),
                'capacity_erlangs_at_2pct_per_cell': round(erlangs_cell, 3),
                'system_capacity_erlangs_at_2pct': round(total_erlangs, 3),
                'subscriber_capacity_at_2pct': math.floor(total_erlangs / BUSY_ERLANG_PER_SUB),
            })
        capacity_rows.append({
            'strategy': strategy, 'effective_cluster_N': effective_n,
            'channels_per_cell': channels_cell, 'cell_radius_km': effective_radius,
            'sites_for_12km2': nsites, 'erlangs_per_cell_at_2pct': round(erlangs_cell, 3),
            'system_erlangs_at_2pct': round(total_erlangs, 3),
            'subscriber_equivalent_at_2pct': math.floor(total_erlangs / BUSY_ERLANG_PER_SUB),
            'planning_cost_index': round(nsites + 0.15*nsites + (2.0 if strategy.startswith('Hierarchical microcells') else 0), 2),
            'assumption': note,
        })

    write_csv(OUT/'channel_map.csv', channel_map_rows, list(channel_map_rows[0]))
    write_csv(OUT/'sir_results.csv', sir_rows, list(sir_rows[0]))
    write_csv(OUT/'capacity_summary.csv', capacity_rows, list(capacity_rows[0]))
    write_csv(OUT/'traffic_results.csv', traffic_rows, list(traffic_rows[0]))

    event_erlangs = 25000 * 0.05
    base_event_rows = []
    for name, n, radius in [('Fixed reuse N=7',7,R_KM), ('Sectorized N=7',7,R_KM), ('Temporary microcells N=3',3,R_KM/2)]:
        count = math.ceil(1.0 / hex_area(radius))
        ch = CHANNELS // n
        per = event_erlangs / count
        b = erlang_b(ch, per)
        base_event_rows.append({'event_strategy':name,'event_erlangs_total':event_erlangs,'zone_sites':count,
                                'channels_per_site':ch,'offered_erlangs_per_site':round(per,3),
                                'blocking_probability':round(b,6),
                                'capacity_erlangs_at_2pct':round(capacity_at_gos(ch)*count,3)})
    write_csv(OUT/'event_surge.csv', base_event_rows, list(base_event_rows[0]))

    fig, ax = plt.subplots(figsize=(8,5))
    for n in CLUSTERS:
        row = [r for r in sir_rows if r['strategy']=='Fixed reuse' and r['cluster_N']==n and r['path_loss_n']==4.0][0]
        ax.scatter(n, row['sir_mean_db'], label=f'N={n}')
        ax.annotate(f"{row['sir_mean_db']:.1f} dB", (n,row['sir_mean_db']), xytext=(4,5), textcoords='offset points')
    ax.axhline(12, linestyle='--', label='12 dB planning threshold')
    ax.set(xlabel='Cluster size N', ylabel='Mean SIR (dB)', title='Reuse cluster size vs mean SIR (n=4)')
    ax.grid(True, alpha=.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT/'sir_vs_cluster.svg', format='svg')
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8,5))
    for name in ['Fixed reuse','120-degree sectoring','Dynamic borrowing','Hierarchical microcells N=3','Hierarchical microcells N=7']:
        rows = [r for r in traffic_rows if r['strategy']==name]
        ax.plot([r['subscribers'] for r in rows],[max(r['blocking_probability'],1e-6) for r in rows],marker='o',label=name)
    ax.axhline(.02,linestyle='--',label='2% GoS target')
    ax.set_yscale('log')
    ax.set(xlabel='Subscribers',ylabel='Erlang-B blocking probability',title='Busy-hour blocking vs subscriber growth')
    ax.grid(True,which='both',alpha=.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT/'blocking_vs_growth.svg',format='svg')
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8,5))
    for n in CLUSTERS:
        vals = [r['sir_mean_db'] for r in sir_rows if r['strategy']=='Fixed reuse' and r['cluster_N']==n]
        ax.plot(PATH_LOSS, vals, marker='o', label=f'N={n}')
    ax.set(xlabel='Path-loss exponent n',ylabel='Mean SIR (dB)',title='Propagation sensitivity')
    ax.grid(True,alpha=.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT/'sir_pathloss_sensitivity.svg',format='svg')
    plt.close(fig)

    print(json.dumps({'cell_area_km2':cell_area,'sites_baseline':sites,'event_erlangs':event_erlangs,
                      'sanity_N7_n4_sir_db':10*math.log10((math.sqrt(3*7)**4)/6),
                      'capacity':capacity_rows,'event':base_event_rows},indent=2))


if __name__ == '__main__':
    main()
