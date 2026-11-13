# Diagram types

One file per diagram type. Each file holds the criteria for that type and, in a JSON block, the rules the lint script reads. The script and you read the same file, so the two cannot drift apart.

## Index

| Spec type | File | Ids | Use it for |
|---|---|---|---|
| `uml-class` | `uml-class.md` | CLS | types, their features and static relationships |
| `uml-object` | `uml-object.md` | OBJ | instances and links at one moment |
| `uml-package` | `uml-package.md` | PKG | grouping of model elements and dependencies between groups |
| `uml-component` | `uml-component.md` | CMP | replaceable parts and the interfaces that wire them |
| `uml-composite-structure` | `uml-composite-structure.md` | CST | the inside of one classifier, or a collaboration |
| `uml-deployment` | `uml-deployment.md` | DEP | where artifacts run and how nodes communicate |
| `uml-profile` | `uml-profile.md` | PRF | stereotypes that extend UML |
| `uml-use-case` | `uml-use-case.md` | UC | what a system offers to its actors |
| `uml-activity` | `uml-activity.md` | ACT | a flow of actions with decisions and parallel work |
| `uml-state-machine` | `uml-state-machine.md` | STM | the states of one object and its transitions |
| `uml-sequence` | `uml-sequence.md` | SEQ | messages between participants in time order |
| `uml-communication` | `uml-communication.md` | COM | the same messages, laid out by who talks to whom |
| `uml-timing` | `uml-timing.md` | TIM | state changes along a time axis |
| `uml-interaction-overview` | `uml-interaction-overview.md` | IOV | control flow between whole interactions |
| `flow` | `flow.md` | FLOW | a step-by-step procedure (flowchart, not UML) |

Every file stands alone; there is no shared file. The rules all UML diagrams share have the ids `UML-01` to `UML-06` and are repeated, word for word, in each `uml-*` file. `--check-types` fails when a row with the same id reads differently in two files, so change such a row in every file that has it.

## Parts of a type file

1. **Header.** The spec type, the family, the frame heading, and when to choose this type over its neighbours.
2. **Criteria.** A table with four columns. `Id` is the prefix and a number, never reused. `Criterion` is one rule in plain words. `Basis` is `standard` when the notation standard says so, `convention` when it is common practice or a rule of this skill. `Check` is `script` when a rule in the JSON block enforces it, `you` when only a reader can judge it.
3. **Layout** and, where the type needs it, **Modeling in the spec**.
4. **Notation and rules.** The JSON block described below.
5. **Sources.** The pages the criteria were checked against, and a plain list of anything that was not confirmed there.

## The rules block

```text
id, name, prefix      spec type, the name used in messages, the id prefix
legend                true when differing fills or line kinds need a legend
rule_kinds            criterion cited when a spec uses a kind the type does not have
generic               {criterion id: generic check id} for criteria a generic check enforces, such as E12
nodes                 {kind: {...}}   every element the type may contain
edges                 {kind: {...}}   every relationship
texts                 {role: {...}}   free text with a meaning, such as a guard
checks                [ {...} ]       structural rules
```

Keys of a node kind: `shapes` (allowed shapes, the first is the default), `draw` (what it looks like, for you), `rule` (criterion id), `label` (pattern the text must match), `label_by_shape` (pattern per shape), `hint` (the pattern in plain words), `text: false` (the symbol carries no text), `inside` and `not_inside` (kinds it must or must not sit in), `uniform` (all nodes of this kind share one size), `max_lines`.

Keys of an edge kind: `line` (`solid` or `dashed`), `head` and `tail` (one value or a list; the first is the default), `draw`, `rule`, `label` and `hint`, `from` and `to` (allowed kinds at each end), `between` (allowed unordered pairs; a one-item pair means both ends are that kind), `rule_between`, `touches` (at least one end is one of these kinds).

Keys of a text role: `label`, `hint`, `rule`, `draw`.

The shape, line and arrowhead words are listed in `../shapes.md`.

Structural checks, each with `rule` and usually `kinds`:

| `check` | Meaning | Other keys |
|---|---|---|
| `count` | how many nodes of these kinds exist | `min`, `max`, `per: "parent"`, `where: "no_in"` or `"no_out"`, `what` |
| `degree` | how many edges enter or leave each such node | `dir`, `min`, `max`, `edge_kinds` |
| `not_both` | such a node has edges in or out, not both | |
| `edge_labels` | every edge leaving (or entering) such a node has a label matching a pattern | `pattern`, `hint`, `dir`, `at_most_one`, `one_hint` |
| `operand_guards` | when such a node holds text, every edge leaving it has a label matching a pattern (the rest of a comparison) | `pattern`, `hint` |
| `reachable` | every node can be reached from a node of these kinds that nothing enters | `skip_kinds`, `what` |
| `reaches` | every node can reach a node of these kinds that nothing leaves | `skip_kinds`, `what` |
| `paired_labels` | each label on such nodes appears on exactly two of them | `exact: false` for two or more |
| `text_in` | each such node holds texts of a role | `role`, `min`, `max` |
| `unique_texts` | no two texts of a role share a key | `role`, `key` |
| `has_guide` | each such node has a guide (its lifeline or timeline) | |
| `sequence` | execution bars, message direction, replies and destruction of a sequence diagram | `rules` |

## Changing or adding criteria

1. Check the rule against the standard or a reference that quotes it, and note the page under Sources. If you cannot confirm it, say so there.
2. Add a row to the criteria table with the next free id. Never renumber: lint messages and earlier reviews cite these ids.
3. If the script can check it, express it in the rules block and set Check to `script`. If the vocabulary above cannot express it, set Check to `you`; add a new check to `scripts/diagram_lint.py` only when several types need it.
4. Run `python3 scripts/diagram_lint.py --check-types`. It fails when the block does not parse, uses an unknown word or kind, cites an id that has no row, or when a row marked `script` has no rule.
5. Add or extend a spec in `tests/`: one that passes, and one that breaks the new rule and is reported with its id.

The same symbol can mean different things in different types, so state it in each type that has it. The diamond is the usual trap: a flowchart decision holds its question (FLOW-09), a UML activity decision is empty (ACT-05), and a UML choice is empty or holds only the left operand its guards share (STM-05, STM-14).

## Adding a diagram type

1. Copy the type file closest to the new one and rename it to the new spec type, for example `bpmn.md` or `er.md`. The file name is the `type` a spec uses. A new UML-based type keeps the `UML-` rows and their `note`, `frame`, `note-link`, `constraint` and `heading` entries; any other type drops them.
2. Pick a new id prefix and rewrite the header, criteria, layout and sources.
3. List every element under `nodes` and every relationship under `edges`. If the type needs a symbol that `../shapes.md` lacks, add it there and to `SHAPES` in the script.
4. Add the type to the index above and to the table in `SKILL.md`.
5. Follow steps 4 and 5 of the previous list.
