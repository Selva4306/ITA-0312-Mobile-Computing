import csv

cases=[
 ["On-device image classification (tiny model)","Predicted label within target accuracy","Unit tests plus labelled validation set","On-device feasible","Small model; bounded compute and no network round-trip."],
 ["Cloud-based speech recognition","Transcript meeting word-error target","Reference audio corpus and API tests","Network-bound","Upload and response latency dominate; connectivity and privacy matter."],
 ["Peer-to-peer file sharing among nearby devices","Verified file delivered to intended peer","Chunk hashes, transfer tests and peer-discovery tests","Hybrid required","Discovery is local, transfer is network-dependent and intermittent."],
 ["End-to-end encrypted messaging","Authenticated plaintext available only to endpoints","Cryptographic test vectors and protocol verification","Security-critical","Key handling, authentication and metadata exposure dominate."],
 ["Real-time multiplayer game state synchronisation","Clients converge within latency and consistency bounds","Deterministic replay, latency simulation and state invariants","Hybrid required","Local prediction plus server/peer reconciliation balances latency and authority."],
 ["Large-scale offline map rendering with vector tiles","Correct visible map within frame and memory budgets","Tile coverage, rendering benchmarks and visual checks","Battery-critical","Large decode/render workloads stress CPU, memory and battery; cache strategically."]
]
def main():
    with open("a4_tractability_matrix.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["problem","solution","efficient_verification","resource_class","reason"]); w.writerows(cases)
    for x in cases: print(x[0],"=>",x[3])
    print("Performance is multidimensional: latency, throughput, energy, memory, network cost, privacy and responsiveness.")
    print("Local/cloud choice changes data exposure, offline behaviour, server scalability and round-trip latency.")

if __name__=="__main__": main()
