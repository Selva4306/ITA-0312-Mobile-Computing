# A2 – Safe incremental data replication

## A2.1 Diagnosis
The naïve loop attempts every record regardless of priority, size, network, battery, encryption or account state. It wastes radio wakeups and retries after network failure, may transmit sensitive plaintext, ignores duplicate/conflicting versions, and cannot distinguish permanent rejection from temporary unavailability.

## A2.2 Incremental algorithm
```text
SYNC(local, remote, state):
  for each record r selected by priority then age:
    if loggedOut or permissionRevoked: CANCEL_REMAINING(); stop
    if not encrypted(r) or not authenticatedTLS: QUARANTINE(r); continue
    if battery < reserve or networkQuality < required(r):
       DEFER(r); continue
    remoteVersion := FETCH_VERSION_IF_CHEAP(r)
    if remoteVersion conflicts with r.version:
       if mergeIsSafe(r): RESOLVE_WITH_VERSIONED_MERGE(r)
       else: MARK_CONFLICT_FOR_USER(r); continue
    if recordExpiredOrUserDeleted(r): DISCARD_WITH_AUDIT(r); continue
    if upload(r) acknowledged: MARK_SYNCED(r)
    else: DEFER_WITH_EXPONENTIAL_BACKOFF(r)
```
The sync set is built one record at a time. No payload is transmitted before the security and feasibility checks.

## A2.3 Five-record pruning trace
| ID | Priority | Size | Sensitivity | State | Decision |
|---|---:|---:|---|---|---|
| R1 | Critical | 4 KB | High | encrypted | Upload on validated Wi-Fi |
| R2 | High | 80 KB | Medium | encrypted | Defer: weak metered network |
| R3 | Low | 2 MB | Low | encrypted | Defer: battery below reserve |
| R4 | Medium | 12 KB | High | plaintext | Reject/quarantine immediately |
| R5 | High | 20 KB | Medium | encrypted | Upload after constraints recover |

**Early termination:** R4's plaintext branch is rejected before network transfer. Further upload attempts cannot make it safe; only encryption and validation can change its eligibility. R2/R3 are deferred, not discarded, because their failures are environmental and temporary.

## A2.4 Offline-first challenge
A permanent discard rule based solely on temporary network absence is invalid under offline-first eventual consistency. The violated assumption is that an unavailable remote endpoint means the record is no longer useful. Offline-first requires durable local retention, version metadata, conflict resolution and retry after reconnection. Security violations (plaintext, invalid authority) remain rejection conditions.
