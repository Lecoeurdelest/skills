# Checkpoint Procedure

## Goal

Bring unfinished work to a recoverable and auditable state.

## Repository Capture

Run the applicable commands:

```bash
git status
git branch --show-current
git diff --stat
git diff > evidence/wip-token-limit.patch
```

On an isolated feature branch, a WIP commit may be used:

```bash
git add -A
git commit -m "WIP checkpoint: paused due to AI limit"
```

Do not create an unreviewed WIP commit directly on the main branch.

When a commit is unsuitable:

```bash
git stash push -u -m "ai-limit-checkpoint"
```

## Persist

Record:

- task ID,
- current phase,
- current state,
- branch,
- run ID,
- changed files,
- completed work,
- incomplete work,
- last successful command,
- failed command,
- tests passed,
- tests failed,
- tests not run,
- artifact locations,
- migration state,
- deployment state,
- known risks,
- exact next action.

## Rules

- Do not mark unverified work as complete.
- Do not overwrite prior evidence.
- Do not fabricate missing test output.
- Do not begin new scope while checkpointing.
