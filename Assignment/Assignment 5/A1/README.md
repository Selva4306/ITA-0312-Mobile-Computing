# A1 – Constraint-aware Intent and background-work architecture

## A1.1 Problem model
**Inputs:** timestamped sensor events, network state/type/quality, battery level, Doze state, runtime permissions, user preferences, authentication state and pending work queue.

**Outputs:** acknowledged encrypted records, local critical-event notifications, audit counters and a residual backlog when delivery is unsafe or unavailable.

**Decisions:** whether to enqueue; select WorkManager (deferrable/retryable upload) or a short-lived foreground service (user-visible, immediate critical operation); explicit vs implicit vs ordered intent; execute, defer, cancel or reject.

**Constraints:** minimum battery reserve, Doze/background limits, permission still granted, authenticated session, encryption at rest and in transit, validated destination, network availability and bounded worker concurrency.

**Goal:** every eligible record is eventually acknowledged without exposing plaintext or violating platform/user constraints; critical alerts are delivered locally without waiting for cloud connectivity.

## A1.2 Runtime state
Maintain queue entries `(id, createdAt, priority, encryptedPayloadRef, retryCount, status, accountEpoch)`; current network/battery/Doze/permission snapshot; authentication epoch; active worker IDs; last acknowledged sequence; notification deduplication keys; cancellation token. Persist queue and acknowledgements transactionally so process death cannot silently lose work.

## A1.3 Feasibility / pruning
- Reject if permission is absent, account epoch is stale, payload is not encrypted, destination is not allow-listed, or authentication is invalid.
- Defer upload if network is absent/unvalidated, quality is below threshold, device is in Doze without an eligible expedited path, or battery is below reserve.
- Cancel account-scoped work on logout/revocation; retain only encrypted local records if policy permits.
- Never prune a critical local notification merely because upload is infeasible.

## A1.4 Architectural pseudocode
```text
SCHEDULE(state):
  snapshot := READ_ATOMIC_CONSTRAINT_SNAPSHOT()
  item := SELECT_HIGHEST_ELIGIBLE_PRIORITY(state.queue)
  if item = NONE: return IDLE
  if not PERMISSION_GRANTED(snapshot) or not SESSION_VALID(item.accountEpoch):
      CANCEL(item); AUDIT("rejected: authority"); return REJECTED
  if not ENCRYPTED(item.payloadRef) or not ALLOWED_DESTINATION(item.destination):
      QUARANTINE(item); AUDIT("rejected: security"); return REJECTED
  if item.kind = CRITICAL_ALERT:
      intent := EXPLICIT_ORDERED_INTENT(AlertReceiver, item.id)
      if APP_VISIBLE_OR_ALERT_EXEMPT(snapshot):
          DISPATCH(intent); MARK_NOTIFIED(item); return NOTIFIED
      else:
          POST_LOCAL_NOTIFICATION(item); MARK_NOTIFIED(item); return NOTIFIED
  if not NETWORK_VALIDATED(snapshot) or snapshot.battery < BATTERY_RESERVE
     or (snapshot.doze and not DOZE_ELIGIBLE(item)):
      SET_STATE(item, DEFERRED); ENQUEUE_UNIQUE_WORK(item, constraints); return DEFERRED
  intent := EXPLICIT_INTENT(UploadWorker, opaqueWorkId=item.id)
  if ACTIVE_WORKERS >= MAX_WORKERS: return DEFERRED
  START_OR_ENQUEUE(intent)
  result := AWAIT_BOUNDED_RESULT()
  if result = ACK:
      TRANSACTIONALLY_MARK_ACKED(item); DELETE_LOCAL_PAYLOAD_AFTER_POLICY_CHECK()
      return SUCCESS
  if result = RETRYABLE:
      INCREMENT_RETRY(item); SET_STATE(item, DEFERRED); SCHEDULE_BACKOFF(item)
      return DEFERRED
  CANCEL_ACTIVE_OPERATION(); RESTORE_QUEUE_STATE(item); return FAILURE
```

## A1.5 Five-event trace
| Event | State/decision | Action |
|---|---|---|
| Sensor reading S1 | Permission/session valid; encrypt and queue | Choose upload candidate |
| Network becomes validated | Battery 72%, not Doze | Constraint check passes; enqueue worker |
| Device enters Doze | Non-expedited upload not eligible | Defer; retain encrypted item |
| Critical threshold event | Local alert independent of cloud | Ordered explicit alert intent; notify user |
| User logs out | Account epoch changes | Cancel unique account work, invalidate token, keep/delete encrypted backlog per consent policy |

**Trace summary:** choose S1 → check battery/network/security → defer during Doze → notify critical event locally → cancel account work on logout. No plaintext is broadcast or written to logs.
