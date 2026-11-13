# skill

A collection of Claude skills.

## Skills

| Skill | Description |
|---|---|
| [diagram-drawing](./diagram-drawing/) | Notation criteria per diagram type (the 14 UML types and the flowchart) and a lint gate for any tool or language; checks symbols, text fit and arrow routes before drawing |
| [model-router](./model-router/) | Routes each step to a model and effort level; complex steps also offer coordinator-led or direct execution with per-agent model checks |
| [skill-limit-recovery](./skill-limit-recovery/) | Handles limit-related situations: context window, session limit, weekly quota, provider overload, and unsafe interruption |

## Install a skill

Each skill is a self-contained directory. Install one by copying its directory into `~/.claude/skills/`, for example:

```bash
cp -r diagram-drawing ~/.claude/skills/
cp -r model-router ~/.claude/skills/
cp -r skill-limit-recovery ~/.claude/skills/
```

Alternatively, use the `.skill` (ZIP) file if one is available.
