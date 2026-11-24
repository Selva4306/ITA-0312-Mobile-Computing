# B4 – Multimedia framework engineering decision

Run `python encoding_strategy.py`. The rule selects resolution/bitrate tiers from CPU, battery and network state; upload is deferred when battery is below 20% or connectivity is not validated. Output includes chosen parameters, estimated encode+upload time, modelled energy and estimated battery impact for four device profiles.

## Challenge
The tier heuristic does not consider clip duration, thermal throttling, codec hardware acceleration, or content complexity. A fixed tier can therefore be suboptimal compared with enumerating the nine resolution/bitrate pairs for a small known workload.

## Decision note
- Exhaustive search is unattractive for thousands of concurrent devices because per-request search multiplies parameter combinations, device profiles and changing network states.
- The heuristic guarantees only that it follows its stated thresholds; it does not guarantee global minimum energy or best perceptual quality.
- It makes a small constant number of decisions and can avoid encoding/uploading at unsafe battery/network conditions.
- Exact search is appropriate offline for calibration or a tiny bounded parameter set. Cloud assistance can estimate profiles, but should not require uploading private raw video just to choose settings.
- Monitor encode latency, upload completion/tail latency, retry rate, battery drain, thermal throttling, resolution distribution, failure rates and user-visible quality before rollout.
