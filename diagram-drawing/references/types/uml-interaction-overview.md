# UML interaction overview diagram

Spec type `uml-interaction-overview` · UML interaction diagram · frame heading `sd`

Shows the control flow between whole interactions: an activity diagram whose nodes are sequence diagrams or references to them. Choose it to tie several sequence diagrams into one scenario with branches.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| IOV-01 | Every node that does work is an interaction: an inline interaction (a frame headed `sd` holding a small interaction diagram) or an interaction use (a frame tagged `ref` naming another interaction). Plain actions do not appear. | standard | script |
| IOV-02 | The control nodes are those of the activity diagram, with the same shapes: initial, flow final, activity final, decision, merge, fork and join. | standard | script |
| IOV-03 | Flows are solid lines with an open arrowhead. Flows leaving a decision carry guards in square brackets; this skill requires at least two exits and a guard on each. | standard | script |
| IOV-04 | Lifelines and messages appear only inside an inline interaction, never at the overview level. | standard | you |
| IOV-05 | Branching and joining are properly nested: whatever a decision or fork opens is closed by its merge or join before the enclosing one closes. | standard | you |
| IOV-06 | The whole diagram sits in a frame headed `sd` (or `interaction`) and its name. | standard | you |
| IOV-07 | A merge has two or more flows in and one out; a fork has one in and two or more out; a join has two or more in and one out. Nothing enters an initial node or leaves a final node. | standard | script |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Lay it out like an activity diagram: main flow top to bottom, branches side by side.
- An inline interaction is a node with `"container": true` holding its own small diagram; keep it to a few lifelines, or use a `ref` and draw the interaction separately.

## Notation and rules

```json
{
  "id": "uml-interaction-overview",
  "name": "UML interaction overview diagram",
  "prefix": "IOV",
  "legend": false,
  "rule_kinds": "IOV-01",
  "nodes": {
    "interaction":     {"shapes": ["frame"], "rule": "IOV-01", "draw": "frame headed sd, holding an inline interaction; \"container\": true"},
    "interaction-use": {"shapes": ["frame"], "rule": "IOV-01", "draw": "frame tagged ref, holding the name of the interaction"},
    "initial":         {"shapes": ["dot"], "text": false, "rule": "IOV-02", "draw": "small solid circle"},
    "activity-final":  {"shapes": ["bullseye"], "text": false, "rule": "IOV-02", "draw": "solid circle inside a hollow circle"},
    "flow-final":      {"shapes": ["circle-x"], "text": false, "rule": "IOV-02", "draw": "circle with an X"},
    "decision":        {"shapes": ["diamond"], "text": false, "rule": "IOV-02", "draw": "empty diamond; the condition goes in the guards"},
    "merge":           {"shapes": ["diamond"], "text": false, "rule": "IOV-02", "draw": "diamond"},
    "fork":            {"shapes": ["bar"], "text": false, "rule": "IOV-02", "draw": "bar"},
    "join":            {"shapes": ["bar"], "text": false, "rule": "IOV-02", "draw": "bar"},
    "note":            {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":           {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "flow":      {"line": "solid", "head": "open", "rule": "IOV-03", "draw": "control flow"},
    "note-link": {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "heading":    {"label": "^(sd|ref|interaction)\\b", "hint": "sd Name or ref", "rule": "IOV-01"},
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"}
  },
  "checks": [
    {"check": "text_in", "kinds": ["interaction", "interaction-use"], "role": "heading", "min": 1, "max": 1, "rule": "IOV-01"},
    {"check": "degree", "kinds": ["initial"], "dir": "in", "max": 0, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["activity-final", "flow-final"], "dir": "out", "max": 0, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["merge"], "dir": "in", "min": 2, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["merge"], "dir": "out", "min": 1, "max": 1, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["fork"], "dir": "in", "min": 1, "max": 1, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["fork"], "dir": "out", "min": 2, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["join"], "dir": "in", "min": 2, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["join"], "dir": "out", "min": 1, "max": 1, "rule": "IOV-07"},
    {"check": "degree", "kinds": ["decision"], "dir": "out", "min": 2, "rule": "IOV-03"},
    {"check": "edge_labels", "kinds": ["decision"], "pattern": "^\\[.+\\]$", "hint": "[guard]", "at_most_one": "^\\[else\\]$", "one_hint": "[else]", "rule": "IOV-03"}
  ]
}
```

The inherited `frame` and `heading` cover the outer frame of IOV-06. The lifelines and messages inside an inline interaction are not checked by these rules; lint that interaction as its own `uml-sequence` spec.

## Sources

- uml-diagrams.org, interaction overview diagrams (allowed activity elements, no actions, proper nesting): https://www.uml-diagrams.org/interaction-overview-diagrams.html
- uml-diagrams.org, interaction overview diagrams reference (frame, inline interaction): https://www.uml-diagrams.org/interaction-overview-diagrams-reference.html
- uml-diagrams.org, activity diagram controls, for the shapes and flow counts of the control nodes: https://www.uml-diagrams.org/activity-diagrams-controls.html
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
