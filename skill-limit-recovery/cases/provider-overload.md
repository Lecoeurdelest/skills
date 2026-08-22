# Provider Overload and Rate-Limit Recovery

## Trigger

Use this playbook for temporary provider failures such as:

- HTTP 429,
- overload,
- capacity unavailable,
- retry-after responses,
- transient provider errors.

## Retry Policy

Default:

```text
maximum_attempts = 3
backoff = exponential
persist_state_before_retry = true
infinite_retry = false
```

For each attempt, record:

- attempt number,
- operation,
- error,
- provider response,
- retry condition,
- final result.

## Outcome

### Retry succeeds

Continue the active task.

### Retry limit is reached

1. Stop retrying.
2. Set state to `CHECKPOINTING`.
3. Apply `../common/checkpoint.md`.
4. Apply `../common/handoff.md`.
5. Set state to `PAUSED_RESUMABLE` or `BLOCKED_PROVIDER_CAPACITY`.
