# Resume Validation

## Rule

Do not modify code or production state until validation is complete.

## Mandatory Checks

1. Read the authoritative specification.
2. Read `HANDOFF.md` if present.
3. Check current branch and Git status.
4. Review relevant commits, diff, patch, and stash.
5. Verify referenced files, logs, and artifacts.
6. Verify database, migration, and deployment state when applicable.
7. Re-run relevant tests.
8. Compare actual state with handoff claims.
9. Record every mismatch.
10. Approve one exact next action.

Recommended commands:

```bash
git status
git branch --show-current
git log --oneline -10
git diff
```

## Required Output

```text
RESUME VALIDATION

Checkpoint status: VALID / PARTIALLY_VALID / INVALID
Repository state: CLEAN / DIRTY / CONFLICTED
Current branch:
Last completed phase:
Artifacts verified:
Tests revalidated:
Differences from handoff:
Approved next action:
```

Use this statement when needed:

```text
Previous result reported, but not independently revalidated in this session.
```
