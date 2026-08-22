---
name: ai-limit-recovery
description: >
  Routes AI context, session, quota, provider, and interruption failures to
  the smallest applicable recovery playbook.
version: 2.0.0
language: en
---

# AI Limit Recovery Router

## Purpose

Keep unfinished AI-assisted work recoverable when the active model or session
becomes unavailable.

Do not load every playbook. Detect the active case, then read only the files
listed for that case.

## Core Rules

1. Never keep the only copy of task state inside the conversation.
2. Never claim unfinished or unverified work is complete.
3. Stop starting new high-risk work when interruption is likely.
4. Preserve repository state, evidence, tests, decisions, and the exact next action.
5. A new session must validate actual state before continuing.
6. Never fabricate missing work, logs, tests, evidence, or previous-session context.

## Routing

### Case A — Context window is becoming unreliable

Signals:

- Earlier decisions are forgotten.
- Requirements are contradicted.
- The conversation is too large.
- Old context must be repeatedly pasted.

Load:

- `cases/context-window.md`
- `common/checkpoint.md`
- `common/handoff.md`

### Case B — Session usage limit reached

Signals:

- The model is unavailable until a usage window resets.
- The task must pause for several hours.

Load:

- `cases/session-limit.md`
- `common/checkpoint.md`
- `common/handoff.md`

### Case C — Weekly quota exhausted

Signals:

- The preferred model is unavailable for an extended period.
- Usage will not reset within the current session window.

Load:

- `cases/weekly-quota.md`
- `common/checkpoint.md`
- `common/handoff.md`
- `common/model-fallback.md`

### Case D — Provider rate limit or overload

Signals:

- HTTP 429.
- Provider overload or capacity error.
- Temporary request rejection.

Load:

- `cases/provider-overload.md`

If retries fail and the task must pause, also load:

- `common/checkpoint.md`
- `common/handoff.md`

### Case E — Previous session stopped without a valid checkpoint

Signals:

- No reliable `HANDOFF.md`.
- Unknown uncommitted changes.
- Missing test or artifact state.
- The previous AI stopped unexpectedly.

Load:

- `cases/unsafe-interruption.md`
- `common/resume-validation.md`

## Standard States

Use only the states needed for the active case:

```text
RUNNING
TOKEN_WARNING
CHECKPOINTING
PAUSED_RESUMABLE
PAUSED_UNSAFE
RESUMING
VALIDATING
BLOCKED_AI_SESSION_LIMIT
BLOCKED_WEEKLY_QUOTA
BLOCKED_PROVIDER_CAPACITY
COMPLETED
```

`COMPLETED` is allowed only when all acceptance criteria are verified.
