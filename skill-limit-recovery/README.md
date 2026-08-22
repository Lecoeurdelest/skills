# Limit Recovery Skill

This skill uses progressive disclosure.

The agent first reads `SKILL.md`, detects the active failure type, and then
loads only the relevant case and common modules.

## Structure

```text
skill-limit-recovery/
├── SKILL.md
├── README.md
├── cases/
│   ├── context-window.md
│   ├── session-limit.md
│   ├── weekly-quota.md
│   ├── provider-overload.md
│   └── unsafe-interruption.md
└── common/
    ├── checkpoint.md
    ├── handoff.md
    ├── resume-validation.md
    └── model-fallback.md
```

## Recommended Invocation

```text
Read skills/skill-limit-recovery/SKILL.md.

Detect the active recovery case and load only the files referenced by that
route. Do not load unrelated case playbooks.
```

## Example: Session Limit

```text
Active case: SESSION_USAGE_LIMIT

Load:
- skills/skill-limit-recovery/cases/session-limit.md
- skills/skill-limit-recovery/common/checkpoint.md
- skills/skill-limit-recovery/common/handoff.md
```

## Example: New Session Recovery

```text
Load:
- skills/skill-limit-recovery/cases/unsafe-interruption.md
- skills/skill-limit-recovery/common/resume-validation.md

Do not modify code until resume validation is complete.
```
