# UML activity diagram

Spec type `uml-activity` · UML behavior diagram · frame heading `act`

Shows a flow of actions with decisions, parallel branches and, when needed, who performs each action. Choose it for a business process or an algorithm with concurrency. Choose a flowchart for a simple procedure, and a state machine diagram when the subject is the life of one object.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| ACT-01 | An action is a round-cornered rectangle with its name inside. | standard | script |
| ACT-02 | Initial node: a small solid circle. An activity may have several, and a flow may also start elsewhere (for example at an accept event action), so an initial node is usual but not mandatory. | standard | script |
| ACT-03 | Activity final: a solid circle inside a hollow circle; it stops every flow. Flow final: a circle with an X; it ends only its own flow. Use flow final where other flows must go on. | standard | script |
| ACT-04 | Activity edges, control flow and object flow alike, are solid lines with an open arrowhead. | standard | script |
| ACT-05 | Decision and merge are diamonds, and the diamond carries no text. What a decision tests is written in the guards on its exits; to name it, attach a note with «decisionInput». A merge has two or more flows in and exactly one out; it never synchronizes concurrent flows. | standard | script |
| ACT-06 | Guards stand in square brackets on the flows leaving a decision, and at most one of them is [else]. This skill also requires at least two exits and a guard on each. | convention | script |
| ACT-07 | Fork and join are line segments (bars), never diamonds. Fork: one flow in, two or more out. Join: two or more in, one out. | standard | script |
| ACT-08 | Alternative branches that later reach a join are merged first, because a join waits for every flow that enters it. | standard | you |
| ACT-09 | A partition is a swimlane: two parallel lines, horizontal or vertical, with the partition name in a box at one end. Nodes between the lines belong to it. | standard | script |
| ACT-10 | Send signal action: a convex pentagon. Accept event action: a concave pentagon. Accept time event (wait): an hourglass. | standard | script |
| ACT-11 | A pin is a small rectangle attached to its action. A data store is an object node with «datastore». | standard | script |
| ACT-12 | An edge connector is a small circle holding a label, and each label appears on exactly two connectors. | standard | script |
| ACT-13 | Nothing enters an initial node and nothing leaves a final node. | standard | script |
| ACT-14 | The activity itself, when shown, is a round-cornered rectangle with its name at the top-left, or a frame headed `act`. | standard | script |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- The main flow runs top to bottom or left to right. Fork and join bars lie across the flow.
- Swimlanes run along the flow; an action sits in the lane of whoever performs it (`"parent"` set to the lane, the lane `"container": true`).
- A fork or join bar is about 6 px thick and long enough for its flows to arrive 12 px apart.

## Notation and rules

```json
{
  "id": "uml-activity",
  "name": "UML activity diagram",
  "prefix": "ACT",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "action":            {"shapes": ["rounded"], "uniform": true, "rule": "ACT-01", "draw": "round-cornered rectangle"},
    "initial":           {"shapes": ["dot"], "text": false, "rule": "ACT-02", "draw": "small solid circle"},
    "activity-final":    {"shapes": ["bullseye"], "text": false, "rule": "ACT-03", "draw": "solid circle inside a hollow circle"},
    "flow-final":        {"shapes": ["circle-x"], "text": false, "rule": "ACT-03", "draw": "circle with an X"},
    "decision":          {"shapes": ["diamond"], "text": false, "rule": "ACT-05", "draw": "empty diamond; the condition goes in the guards, or in a note with «decisionInput»"},
    "merge":             {"shapes": ["diamond"], "text": false, "rule": "ACT-05", "draw": "diamond"},
    "fork":              {"shapes": ["bar"], "text": false, "rule": "ACT-07", "draw": "bar"},
    "join":              {"shapes": ["bar"], "text": false, "rule": "ACT-07", "draw": "bar"},
    "send-signal":       {"shapes": ["signal-send"], "rule": "ACT-10", "draw": "convex pentagon"},
    "accept-event":      {"shapes": ["signal-accept"], "rule": "ACT-10", "draw": "concave pentagon"},
    "accept-time-event": {"shapes": ["hourglass"], "rule": "ACT-10", "draw": "hourglass; its text goes beside it"},
    "object":            {"shapes": ["rect"], "rule": "ACT-11", "draw": "object node; a data store adds «datastore»"},
    "pin":               {"shapes": ["port"], "rule": "ACT-11", "draw": "small rectangle attached to its action"},
    "connector":         {"shapes": ["circle"], "label": "\\S", "hint": "a label", "rule": "ACT-12", "draw": "small circle holding a label"},
    "partition":         {"shapes": ["lane"], "rule": "ACT-09", "draw": "swimlane; \"container\": true"},
    "activity":          {"shapes": ["rounded", "frame"], "rule": "ACT-14", "draw": "the whole activity; \"container\": true"},
    "note":              {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":             {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "flow":      {"line": "solid", "head": "open", "rule": "ACT-04", "draw": "control flow or object flow"},
    "note-link": {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": [
    {"check": "degree", "kinds": ["initial"], "dir": "in", "max": 0, "rule": "ACT-13"},
    {"check": "degree", "kinds": ["activity-final", "flow-final"], "dir": "out", "max": 0, "rule": "ACT-13"},
    {"check": "degree", "kinds": ["merge"], "dir": "in", "min": 2, "rule": "ACT-05"},
    {"check": "degree", "kinds": ["merge"], "dir": "out", "min": 1, "max": 1, "rule": "ACT-05"},
    {"check": "degree", "kinds": ["decision"], "dir": "out", "min": 2, "rule": "ACT-06"},
    {"check": "edge_labels", "kinds": ["decision"], "pattern": "^\\[.+\\]$", "hint": "[guard]", "at_most_one": "^\\[else\\]$", "one_hint": "[else]", "rule": "ACT-06"},
    {"check": "degree", "kinds": ["fork"], "dir": "in", "min": 1, "max": 1, "rule": "ACT-07"},
    {"check": "degree", "kinds": ["fork"], "dir": "out", "min": 2, "rule": "ACT-07"},
    {"check": "degree", "kinds": ["join"], "dir": "in", "min": 2, "rule": "ACT-07"},
    {"check": "degree", "kinds": ["join"], "dir": "out", "min": 1, "max": 1, "rule": "ACT-07"},
    {"check": "paired_labels", "kinds": ["connector"], "rule": "ACT-12"}
  ]
}
```

A combined merge and decision, or join and fork, drawn as one symbol is allowed by UML; model it as two nodes here so the rules above can be checked.

## Sources

- uml-diagrams.org, activity diagrams reference (activity, partition, action, signal and time event actions, pins, data store, edges, guards, connectors): https://www.uml-diagrams.org/activity-diagrams-reference.html
- uml-diagrams.org, activity diagram controls (initial, flow final, activity final, decision, merge, fork, join): https://www.uml-diagrams.org/activity-diagrams-controls.html
- Not confirmed on those pages: the plain rectangle as the shape of an object node, and ACT-13. Both come from the UML specification as remembered, not from a page read for this file.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
