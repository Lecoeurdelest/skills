# Session Usage Limit Recovery

## Trigger

Use this playbook when the active model is unavailable until the current usage
window resets.

## Required Actions

1. Stop implementation immediately after reaching a safe boundary.
2. Set state to `CHECKPOINTING`.
3. Apply `../common/checkpoint.md`.
4. Apply `../common/handoff.md`.
5. Set state to `BLOCKED_AI_SESSION_LIMIT`.
6. Do not restart the task in an unprepared session.
7. Preserve the branch, patch or WIP commit, logs, tests, and artifacts.

## Resume

After the usage window resets:

1. Start a new session.
2. Read the specification and `HANDOFF.md`.
3. Apply `../common/resume-validation.md`.
4. Continue only when the checkpoint is `VALID` or the mismatch has been resolved.
