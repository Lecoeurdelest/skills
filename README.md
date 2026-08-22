# skill

A collection of Claude skills.

## Skills

| Skill | Description |
|---|---|
| [model-router](./model-router/) | Recommends the appropriate model and effort level at the end of each step using a scoring matrix (Claude / OpenAI / Gemini / open-weight) |
| [skill-limit-recovery](./skill-limit-recovery/) | Handles limit-related situations: context window, session limit, weekly quota, provider overload, and unsafe interruption |

## Install a skill

Each skill is a self-contained directory. Install one by copying its directory into `~/.claude/skills/`, for example:

```bash
cp -r model-router ~/.claude/skills/
cp -r skill-limit-recovery ~/.claude/skills/
```

Alternatively, use the `.skill` (ZIP) file if one is available.
