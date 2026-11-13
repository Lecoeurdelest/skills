# UML timing diagram

Spec type `uml-timing` · UML interaction diagram · frame heading `sd`

Shows how the state or condition of participants changes along a time axis. Choose it when durations and deadlines are the point (protocol timeouts, hardware signals). Choose a sequence diagram when only the order matters.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| TIM-01 | Each lifeline is a horizontal band labelled with the name of the classifier or instance it stands for, placed inside the frame or in a swimlane. | standard | script |
| TIM-02 | Time runs along one linear axis shared by every lifeline; this skill draws it left to right with tick labels below the bands. | standard | you |
| TIM-03 | A state or condition timeline shows the participant moving between named states or conditions: the line stays level while one holds and steps to another level when it changes. Each level is named at the left edge of the band. | standard | script |
| TIM-04 | A duration constraint or a time constraint is an interval in curly braces, tied to the stretch or the instant it constrains: {1..6 min}, {t..t+3}. | standard | script |
| TIM-05 | Destruction: an X at the end of a timeline, and nothing follows on that lifeline. | standard | script |
| TIM-06 | A message between lifelines is an arrow from the sender's timeline to the receiver's, at the time it is sent. | standard | script |
| TIM-07 | A change caused by an event lines up vertically with that event. | convention | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Bands stacked top to bottom, each 80 px or taller, all with the same left and right edge.
- State names in a column at the left of each band; the timeline starts to the right of that column.

## Modeling in the spec

- A band is a node of kind `lifeline` with `"container": true`; its `lines` hold the participant name.
- The timeline is a `guide` with `of` set to the band, drawn as a stepped polyline inside it.
- State names are texts with role `state`; tick labels are texts with role `tick`; constraints are texts with role `constraint`.
- A message is an edge of kind `message` with `"anchor": "guide"` from one band's timeline to another's.

## Notation and rules

```json
{
  "id": "uml-timing",
  "name": "UML timing diagram",
  "prefix": "TIM",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "lifeline":    {"shapes": ["band"], "rule": "TIM-01", "draw": "horizontal band named after the participant; \"container\": true"},
    "destruction": {"shapes": ["x"], "text": false, "rule": "TIM-05", "draw": "X at the end of a timeline; \"on_guide\": true"},
    "note":        {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":       {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "message":   {"line": "solid", "head": ["open", "filled"], "from": ["lifeline"], "to": ["lifeline"], "rule": "TIM-06", "draw": "from the sender's timeline to the receiver's"},
    "note-link": {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "state":      {"draw": "name of a state or condition level, at the left edge of the band"},
    "tick":       {"draw": "label on the time axis"},
    "constraint": {"label": "^\\{.+\\}$", "hint": "{interval}", "rule": "TIM-04"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": [
    {"check": "has_guide", "kinds": ["lifeline"], "rule": "TIM-03"}
  ]
}
```

## Sources

- uml-diagrams.org, timing diagrams overview and reference (lifeline, state or condition timeline, duration constraint, time constraint, destruction occurrence): https://www.uml-diagrams.org/timing-diagrams.html and https://www.uml-diagrams.org/timing-diagrams-reference.html
- Not confirmed on those pages, which name these elements in a figure caption without describing them: how a message and the timing ruler are drawn, and the general value lifeline (a band that states the value and crosses over where it changes). TIM-02 and TIM-06 follow the UML specification as remembered; the general value lifeline is left out of this file until it is checked.
- TIM-07 is a rule of this skill.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
