# A3 – Common background-work design pattern

| Design component | Sensor collection | Data sync | Push notification |
|---|---|---|---|
| State | Sensor permission, sampling interval, last sample | Encrypted queue, versions, retry count | Token, delivery ID, dedupe state |
| Decision variable | Sample now or wait | Upload/defer/resolve | Deliver now/retry |
| Candidate choices | Scheduled worker, foreground service | WorkManager worker | FCM callback, local notification |
| Feasibility | Permission, battery, sampling policy | Network, battery, encryption, session | Valid token, channel permission |
| Goal | Persist valid reading | Remote acknowledgement | Exactly-once user-visible effect (deduplicated) |
| Prune/defer | Doze or revoked permission | Weak network/low battery | Invalid token or rate limit |
| Undo/cancel | Stop sensor and close resource | Cancel request; restore pending state | Cancel duplicate notification / invalidate token |

## A3.1 Common pattern
All three are asynchronous state machines. Each selects a candidate operation, checks preconditions, executes under resource/security constraints, records a durable result, and retries, defers or cancels when conditions change. Their differences are in payload and completion semantics, not the scheduling pattern.

## A3.2 Generic framework
```text
SCHEDULE_OR_EXECUTE(state):
  refresh state.constraints atomically
  task := select(state.pending, priority, deadline)
  if task = NONE: return IDLE
  if task.authority invalid: cancel(task); audit(); return REJECT
  if task.security invariant false: quarantine(task); return REJECT
  if not feasible(task, state.constraints):
      persist(DEFERRED, task); registerConstraintTrigger(task); return DEFER
  checkpoint := saveRecoverableState(task)
  acquireBoundedResources(task)
  result := execute(task)
  if result successful: commitResultAndRelease(task); return DONE
  rollbackTo(checkpoint); releaseAllResources(task)
  if result retryable: scheduleBackoff(task); return DEFER
  cancel(task); return FAILED
```

## A3.3 Undo/cancellation
Cancellation must release sensors, sockets, locks and worker slots and restore queue status. For data sync, if a network request is cancelled after bytes are sent but before acknowledgement, the client must not mark the record complete. It retains the record and uses an idempotency key on retry; otherwise it can silently lose data or create duplicates.
