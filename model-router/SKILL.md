---
name: model-router
description: Routes the next step of a task to an LLM and reasoning-effort level using a scoring matrix across Claude, OpenAI, Gemini, and open-weight models. For complex steps, also requires a choice between coordinator-led agents and direct execution and model-checks every proposed agent role. Use this at the end of EVERY step of ANY multi-step task—coding, research, data work, writing, or ops—even when the user never mentions models, cost, or effort. Also use whenever the user asks which model to use, how much effort to use, whether to switch models, whether a task is worth Opus, whether a cheaper model can handle it, how to reduce token costs, or asks to route, pick, downgrade, or upgrade a model for a task.
---

# Model Router

At the end of each step in a multi-step task, insert a small table recommending a model and effort level for the **next step**.

Why this exists: people default to running an entire task on one model—either one that is too powerful (wasting money on renaming a file) or too weak (having Haiku write a migration script). Cost and quality hinge on choosing the wrong model for **individual steps**, not for the task as a whole. This table forces a fresh choice at every step boundary.

## When to run

Use this for any task with at least two steps. Insert the table after reporting the result of the completed step and before starting the next one.

Do not insert it for casual conversation, a one-shot question, or the final step. When a long task has no next step, replace it with a one-line cost summary.

## Scoring: four signals, each scored 0–2

Score the **next step**, not the overall task. This is the most common mistake: a demanding task does not mean every step in it is demanding.

**A — Ambiguity.** 0: the specification is clear; just execute it. 1: some details require inference. 2: the problem must be defined before it can be solved.

**B — Reasoning depth.** 0: one lookup or transformation. 1: two to four dependent operations. 2: at least five operations, or a global invariant must be maintained throughout.

**C — Consequences of error.** 0: read-only; retry if wrong. 1: writes files or generates code and can be fixed. 2: irreversible—deployment, migration, data deletion, sending something externally, or producing a figure the user will cite to others.

**D — Context load.** 0: under approximately 5K tokens. 1: multiple sources that can each be processed independently. 2: multiple sources must be cross-checked, or a large codebase must be kept in mind.

Map the total score of 0–8 to a tier:

| Total | Tier | Name |
|---|---|---|
| 0–2 | 1 | Cheap/fast |
| 3–4 | 2 | Workhorse |
| 5–6 | 3 | Heavy |
| 7–8 | 4 | Frontier |

## Complex-task execution choice

Treat a next step with a score of 5–8 as complex. Before starting it, present
exactly two execution options and wait for the user to choose unless they have
already selected a mode for the current task:

1. **Coordinator-led agents.** Create one dedicated coordinator agent whose only
   responsibilities are decomposition, delegation, progress tracking, and final
   synthesis. It must not inspect implementation artifacts, edit files, execute
   the work, run tests, or perform the worker's validation. The coordinator must
   delegate inspection, execution, and validation to at least one separate worker
   agent.
2. **Direct execution.** Do not create a coordinator. The current agent performs
   the work directly using the model and effort selected for the complex step.

Before creating any agent in option 1, score that agent's assigned work separately
with A–D and select its model and effort from this router. Do not automatically
inherit the coordinator's or parent agent's configuration. Show the user the
role-specific model check in a compact table before spawning, and apply each
selection to the spawn configuration when the environment supports it:

```text
| Role | Responsibility | Model | Effort | Score |
|---|---|---|---|---|
| Coordinator | Decompose, delegate, track, synthesize | gpt-5.6-terra | medium | 4 (A1 B2 C0 D1) |
| Worker 1 | Inspect, implement, and validate | gpt-5.6-sol | high | 6 (A1 B2 C1 D2) |
```

Add a row for every worker. Check which models and effort levels the agent-spawn
environment actually supports before presenting the table. If the ideal selection
is unavailable, use the closest available model in the same tier and the closest
supported effort that does not weaken an irreversible-action override; label the
substitution explicitly. If the selected environment cannot create a dedicated
coordinator plus at least one separate worker, state that constraint and use option
2 only after the user approves it. Do not present these two options again for later
complex steps in the same task unless the chosen mode becomes unavailable or the
user asks to reconsider it.

## Selection table

| Tier | Anthropic | OpenAI | Google | Open-weight | Effort |
|---|---|---|---|---|---|
| 1 | Haiku 4.5 | gpt-5.6-luna | Gemini 3.5 Flash-Lite | DeepSeek V4 Flash | `low` / `minimal` |
| 2 | Sonnet 5 | gpt-5.6-terra | Gemini 3.7 Flash | GLM 5.2 | `medium` |
| 3 | Sonnet 5 or Opus 5 | gpt-5.6-sol | Gemini 3.7 Flash | DeepSeek V4 Pro | `high` |
| 4 | Opus 5 / Fable 5 | gpt-5.6-sol | Gemini 3.7 Flash | Kimi K3 | `xhigh` → `max` |

Choose a column by strength, not habit:

- **Agentic coding, multi-file repository edits, long-running sessions** → Anthropic
- **Multimodal work (image/video/audio), extremely long context at low cost** → Google
- **Layout and visual judgment, programmable tool orchestration** → OpenAI
- **Data that cannot leave the infrastructure, or extremely large bulk workloads** → open-weight

For complete pricing and effort scales, see `references/roster.md`. For detailed mappings by task type (research, writing, data analysis, debugging, and ops), see `references/matrix.md`.

## Override rules

Apply these after determining the tier. Overrides take precedence over the score.

1. **Irreversible** (C=2) → increase effort by one level and **do not** lower the tier to save money. Include a confirmation step before execution.
2. **Response required in under two seconds**, or speaking directly to an end user → lower the tier by one and use effort no higher than `low`.
3. **Bulk workload of at least 500 calls** → lower the tier by one, use `low` effort, and use a batch API (approximately 50% cheaper).
4. **Sensitive or on-premises data** → use only the open-weight column and keep the same tier.
5. **Mechanical step** (run a command, rename, format, or commit) → always Tier 1, regardless of how demanding the overall task is.
6. **Context over 200K tokens** → use only a model with a context window of at least 1M tokens, or split the context first.
7. **The previous attempt failed** → do not repeat the same configuration. Change exactly one axis: increase the tier by one **or** switch providers, but not both. If both change, it is impossible to know which change resolved the problem. After a second failure, stop and ask the user instead of escalating again.

## Format

For a non-complex next step, use exactly one table at the end of the step:

```
| Next step | Model | Effort | Score | Reason |
|---|---|---|---|---|
| Update API validation | Sonnet 5 | medium | 4 (A1 B1 C1 D1) | scoped code change with known behavior |

Fallback: tests expose cross-module behavior → Opus 5 / high.
```

For a complex next step, replace that single recommendation with an execution
choice block. Show exactly two options—coordinator-led agents and direct
execution—plus the proposed role-specific model-check table for option 1. Include
the direct model and effort in option 2:

```text
| Option | Mode | Configuration | Trade-off |
|---|---|---|---|
| 1 | Coordinator-led agents | One coordinator plus at least one separate worker; see role checks below | more oversight and delegation overhead |
| 2 | Direct execution | Current agent: Opus 5 / max; 7 (A2 B2 C2 D1) | less overhead and no independent delegation |
```

Then show the role-specific table from the complex-task rule and end with
`Choose option 1 or 2.`

Keep the "Reason" column to approximately 12 words at most—it is a note, not a paragraph. Include the "Fallback" line only when there is a genuine risk; omit it entirely when the next step is straightforward.

**If the configuration is unchanged from the previous step**, do not repeat the table. Write one line instead: `→ keep Sonnet 5 / medium.` Repeating the same table five times in a row creates noise, and readers will begin to ignore it even when it eventually changes.

## Examples

**Completed step:** read three configuration files and locate the timeout declarations.
**Next step:** make the timeout consistent in all three places.

| Next step | Model | Effort | Score | Reason |
|---|---|---|---|---|
| Update timeout in three files | Haiku 4.5 | low | 2 (A0 B1 C1 D0) | mechanical edit; exact locations are known |

---

**Completed step:** finished the schema for the ingestion pipeline.
**Next step:** choose a backfill strategy for 400M rows in production.

| Option | Mode | Configuration | Trade-off |
|---|---|---|---|
| 1 | Coordinator-led agents | One coordinator plus one separate worker; see role checks below | independent execution and validation; more overhead |
| 2 | Direct execution | Current agent: Opus 5 / max; 7 (A2 B2 C2 D1) | less overhead and no independent delegation |

| Role | Responsibility | Model | Effort | Score |
|---|---|---|---|---|
| Coordinator | Decompose, delegate, track, synthesize | Sonnet 5 | medium | 4 (A1 B2 C0 D1) |
| Worker 1 | Inspect constraints, design the strategy, and validate rollback | Opus 5 | max | 7 (A2 B2 C2 D1) |

Choose option 1 or 2.

---

**Completed step:** finalized the outline for a market report.
**Next step:** read 40 articles and extract revenue figures.

| Next step | Model | Effort | Score | Reason |
|---|---|---|---|---|
| Extract figures from 40 sources | Gemini 3.5 Flash-Lite | low | 3 (A0 B1 C1 D1) | repetitive extraction; each source is independent and cheap |

Fallback: route any source with nested tables separately to Sonnet 5 / medium.

Note the last example: a score of 3 maps to Tier 2, but the bulk rule lowers it to Tier 1. Overrides take precedence over the score—state that in the "Reason" column so readers do not assume the scoring is wrong.

## Maintain accuracy

Model names and prices change quickly. If a user mentions a model that is not in `references/roster.md`, or if the table may be outdated, search the web before making a recommendation instead of guessing from memory. Recommending a nonexistent model is worse than making no recommendation. The roster begins with its most recent update date.
