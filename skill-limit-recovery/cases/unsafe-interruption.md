# Unsafe Interruption Recovery

## Trigger

Use this playbook when the previous session ended without a trusted checkpoint.

Examples:

- no `HANDOFF.md`,
- unknown uncommitted changes,
- incomplete migration state,
- missing test evidence,
- uncertain deployment state,
- partial generated artifacts.

## Mandatory State

```text
PAUSED_UNSAFE
```

## Prohibited Action

Do not continue implementation immediately.

## Recovery Procedure

1. Inspect Git status, branch, commits, diff, and stash state.
2. Inspect logs, artifacts, database state, and deployment state.
3. Identify the last verified successful operation.
4. Separate verified work from inferred work.
5. Do not recreate missing evidence.
6. Apply `../common/resume-validation.md`.
7. Create a new trusted `HANDOFF.md`.
8. Continue only after the state is validated.

If reconstruction is incomplete, remain `PAUSED_UNSAFE`.
