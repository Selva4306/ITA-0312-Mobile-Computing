# A4 – Tractability: local, cloud and hybrid

| Problem | Solution | Efficiently verified? | Resource class | Reason |
|---|---|---|---|---|
| Tiny on-device image classification | Label plus confidence for each image | Yes, bounded model/input; test vectors and latency | On-device feasible | Small fixed model, avoids network round-trip |
| Cloud speech recognition | Transcript with timestamps/confidence | Partly; service/model output is probabilistic | Network-bound | Audio upload, server inference and response latency |
| Nearby peer-to-peer sharing | Authenticated, integrity-checked transfer | Yes for protocol invariants and hashes | Hybrid required | Local radio discovery plus CPU/energy/security costs |
| End-to-end encrypted messaging | Confidential, authenticated message delivery | Crypto properties testable; proof requires formal analysis | Security-critical | Key management and protocol correctness dominate |
| Multiplayer state synchronisation | Bounded-latency consistent-enough game state | Simulation/load tests; global guarantees hard | Network-bound | Jitter, loss and concurrent state updates |
| Offline vector-map rendering | Correct visible tiles at target frame rate | Yes for tile correctness; performance profile needed | Battery-critical | Decode, memory cache and rendering consume resources |

**Why “runs slowly” is inadequate:** it omits workload size, input distribution, latency target, throughput, tail latency, energy, memory, thermal throttling, network quality and correctness. A slow operation may be acceptable for a background batch but unacceptable for a 60-fps UI.

**Local vs cloud:** local execution avoids network dependence and limits data exposure but is bounded by device CPU, memory and battery. Cloud offloading can scale compute centrally but adds latency, connectivity dependence, bandwidth cost and a larger privacy/security boundary. Hybrid placement must state what data leaves the device and what happens offline.
