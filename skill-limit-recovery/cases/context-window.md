# Context Window Recovery

## Trigger

Use this playbook when the conversation is too large or the agent is becoming
unreliable because earlier context is no longer retained accurately.

## Required Actions

1. Set state to `TOKEN_WARNING`.
2. Stop accepting new scope.
3. Finish or safely stop the smallest current work unit.
4. Do not begin a migration, deployment, destructive operation, or large refactor.
5. Apply `../common/checkpoint.md`.
6. Apply `../common/handoff.md`.
7. Set state to `PAUSED_RESUMABLE`.
8. Start a fresh session with the authoritative files and handoff.

## Resume Rule

A summary of the old conversation is not sufficient evidence.

The new session must validate:

- repository state,
- current branch,
- changed files,
- artifacts,
- tests,
- decisions,
- exact next action.

Use `../common/resume-validation.md` when resuming.
