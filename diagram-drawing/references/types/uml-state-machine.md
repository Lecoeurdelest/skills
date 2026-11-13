# UML state machine diagram

Spec type `uml-state-machine` · UML behavior diagram · frame heading `stm`

Shows the states one object can be in and the transitions between them. Choose it for a lifecycle (an order, a session, a device). Choose an activity diagram when the subject is a procedure carried out by several parties.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| STM-01 | A state is a rectangle with rounded corners and its name inside. Internal activities go in a second compartment, labelled `entry /`, `do /` and `exit /`. | standard | script |
| STM-02 | Initial pseudostate: a small solid circle, at most one per region. Exactly one transition leaves it, and that transition has no trigger and no guard; an effect after a slash is allowed. | standard | script |
| STM-03 | Final state: a circle around a small solid circle. Nothing leaves it. | standard | script |
| STM-04 | A transition is a solid arrow from source to target, labelled `trigger [guard] / effect`. Every part is optional, so a transition without a trigger (a completion transition) is valid. | standard | script |
| STM-05 | Choice: a diamond. The condition is not written inside it: each transition leaving it carries a guard in square brackets, and [else] is added so that one guard always holds. The diamond stays empty, or holds only the left operand that all its guards share, with the rest of each guard on its transition (`verdict` inside, `[= passed]` and `[else]` outside). This skill requires at least two exits. | standard | script |
| STM-06 | Junction: a small black circle that chains transitions into one path. | standard | script |
| STM-07 | Fork and join: short heavy bars. Transitions leaving a fork and transitions entering a join carry no trigger and no guard. | standard | script |
| STM-08 | Terminate: a cross. Entry point: a small circle on the border of the state machine or composite state. Exit point: a small circle with a cross on the border. Entry and exit points carry their name beside them. | standard | script |
| STM-09 | Shallow history: a small circle containing H. Deep history: a small circle containing H*. A composite state has at most one of each. | standard | script |
| STM-10 | A composite state draws its substates inside its own rounded rectangle. Each region may have its own initial pseudostate and final state. | standard | you |
| STM-11 | A state name says what holds while the object is there (Waiting, Paid), not what the object does. | convention | you |
| STM-12 | A protocol state machine is marked {protocol} near its name. Its states have no entry, exit or do activities, it has no history pseudostates, and its transitions read `[precondition] trigger / [postcondition]`. | standard | you |
| STM-13 | The frame, when drawn, is headed `stm` and the name of the state machine. | standard | you |
| STM-14 | When the diamond of a choice holds text, that text is the left operand its guards share, and every guard except [else] holds only the rest of the comparison: `[= passed]`, `[> 10]`. A whole question in the diamond with Yes and No exits is flowchart notation, not UML. | standard | script |
| STM-15 | When all guards of a choice test the same value, this skill writes that value in the diamond, so the reader sees what is being decided. The diamond stays empty only when the guards test different things. | convention | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- The main path runs left to right in one row. States that leave it (cancelled, failed) go in the row below, under the state they are reached from.
- Transitions are straight where the boxes allow it; place the states so that no transition passes through another state.
- A composite state is a node with `"container": true`; its substates carry `"parent"`.

## Notation and rules

```json
{
  "id": "uml-state-machine",
  "name": "UML state machine diagram",
  "prefix": "STM",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "state":           {"shapes": ["rounded"], "label": "\\S", "hint": "a name", "max_lines": 5, "rule": "STM-01", "draw": "rounded rectangle; a line \"---\" starts the internal activities compartment"},
    "composite-state": {"shapes": ["rounded"], "rule": "STM-01", "draw": "rounded rectangle holding its substates; \"container\": true"},
    "initial":         {"shapes": ["dot"], "text": false, "rule": "STM-02", "draw": "small solid circle"},
    "final":           {"shapes": ["bullseye"], "text": false, "rule": "STM-03", "draw": "circle around a small solid circle"},
    "choice":          {"shapes": ["diamond"], "rule": "STM-05", "draw": "diamond; empty, or holding only the left operand its guards share (STM-14, STM-15)"},
    "junction":        {"shapes": ["dot"], "text": false, "rule": "STM-06", "draw": "small black circle"},
    "fork":            {"shapes": ["bar"], "text": false, "rule": "STM-07", "draw": "short heavy bar"},
    "join":            {"shapes": ["bar"], "text": false, "rule": "STM-07", "draw": "short heavy bar"},
    "terminate":       {"shapes": ["x"], "text": false, "rule": "STM-08", "draw": "cross"},
    "entry-point":     {"shapes": ["circle"], "rule": "STM-08", "draw": "small circle on the border, name beside it"},
    "exit-point":      {"shapes": ["circle-x"], "rule": "STM-08", "draw": "small circle with a cross on the border, name beside it"},
    "shallow-history": {"shapes": ["circle"], "label": "^H$", "hint": "H", "rule": "STM-09", "draw": "small circle containing H"},
    "deep-history":    {"shapes": ["circle"], "label": "^H\\*$", "hint": "H*", "rule": "STM-09", "draw": "small circle containing H*"},
    "note":            {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":           {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "transition": {"line": "solid", "head": "open", "rule": "STM-04", "draw": "labelled trigger [guard] / effect, each part optional"},
    "note-link":  {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": [
    {"check": "count", "kinds": ["initial"], "per": "parent", "max": 1, "what": "initial pseudostate(s) in one region", "rule": "STM-02"},
    {"check": "degree", "kinds": ["initial"], "dir": "out", "min": 1, "max": 1, "rule": "STM-02"},
    {"check": "edge_labels", "kinds": ["initial"], "pattern": "^\\s*(/.*)?$", "hint": "nothing, or / effect (no trigger, no guard)", "rule": "STM-02"},
    {"check": "degree", "kinds": ["final", "terminate"], "dir": "out", "max": 0, "rule": "STM-03"},
    {"check": "degree", "kinds": ["choice"], "dir": "out", "min": 2, "rule": "STM-05"},
    {"check": "edge_labels", "kinds": ["choice"], "pattern": "\\[.+\\]", "hint": "[guard]", "at_most_one": "\\[else\\]", "one_hint": "[else]", "rule": "STM-05"},
    {"check": "operand_guards", "kinds": ["choice"], "pattern": "^\\[\\s*(else\\s*\\]|=|!=|≠|<|>|≤|≥|in\\b|is\\b|not\\b)", "hint": "[= value], [> 10] or [else]", "rule": "STM-14"},
    {"check": "edge_labels", "kinds": ["fork"], "pattern": "^\\s*(/.*)?$", "hint": "nothing (no trigger, no guard)", "rule": "STM-07"},
    {"check": "edge_labels", "kinds": ["join"], "dir": "in", "pattern": "^\\s*(/.*)?$", "hint": "nothing (no trigger, no guard)", "rule": "STM-07"},
    {"check": "count", "kinds": ["shallow-history"], "per": "parent", "max": 1, "what": "shallow history pseudostate(s) in one composite state", "rule": "STM-09"},
    {"check": "count", "kinds": ["deep-history"], "per": "parent", "max": 1, "what": "deep history pseudostate(s) in one composite state", "rule": "STM-09"}
  ]
}
```

## Sources

- uml-diagrams.org, state machine diagrams reference (simple and composite state, initial, terminate, entry and exit point, choice, fork, join, final state, protocol state machine): https://www.uml-diagrams.org/state-machine-diagrams-reference.html
- uml-diagrams.org, state machine diagrams overview (junction, shallow and deep history, transition syntax): https://www.uml-diagrams.org/state-machine-diagrams.html
- uml-diagrams.org, protocol state machine diagrams: https://www.uml-diagrams.org/protocol-state-machine-diagrams.html
- STM-15 is a rule of this skill; UML allows the empty diamond as well.
- Not confirmed on those pages: the open arrowhead of a transition (the pages say only "arrow"), and that nothing leaves a final state. Both come from the UML specification as remembered.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
