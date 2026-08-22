# Weekly Quota Recovery

## Trigger

Use this playbook when the preferred model is unavailable for an extended
period because its weekly usage quota is exhausted.

## Required Actions

1. Set state to `CHECKPOINTING`.
2. Apply `../common/checkpoint.md`.
3. Apply `../common/handoff.md`.
4. Classify the remaining work by risk.
5. Apply `../common/model-fallback.md`.

## Decision

### Approved equivalent model exists

Transfer the complete handoff package and require independent validation.

### Only a weaker model exists

Allow only low-risk or read-only work.

### No approved model exists

Set state to:

```text
BLOCKED_WEEKLY_QUOTA
```

or:

```text
BLOCKED_PROVIDER_CAPACITY
```

Do not use an unsuitable model merely to keep the task moving.
