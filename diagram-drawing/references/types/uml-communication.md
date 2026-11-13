# UML communication diagram

Spec type `uml-communication` · UML interaction diagram · frame heading `sd`

Shows the same kind of interaction as a sequence diagram, laid out by who talks to whom; numbers on the messages give the order. Choose it when the structure of the collaboration matters more than the timeline. It was called a collaboration diagram in UML 1.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| COM-01 | A lifeline is a rectangle only: the head, with no line of life below it. It reads `name : Type`; either part may be left out. | standard | script |
| COM-02 | Lifelines that exchange messages are joined by a plain line. | standard | script |
| COM-03 | A message is shown on that line as its label with a small arrow above the line pointing at the receiver. The label is the sequence expression, a colon and the message name: `1: order()`, `1.1: check()`. | standard | script |
| COM-04 | The sequence expression is a list of terms separated by dots. The integer of a term gives the order inside the call one level up, so 1.1 and 1.2 happen within 1. | standard | you |
| COM-05 | A letter after the integer names a concurrent thread: 2a and 2b run concurrently. | standard | you |
| COM-06 | A guard in square brackets makes a message conditional: `1.2 [x > y]: draw()`. | standard | you |
| COM-07 | An asterisk marks iteration, with an optional clause in square brackets: `3 *[i=1..n]: search()`. An asterisk followed by two vertical bars means the iterations run concurrently. | standard | you |
| COM-08 | The diagram has no time axis, no execution bars and no combined fragments. | standard | script |
| COM-09 | The frame, when drawn, is headed `sd`; communication diagrams have no heading of their own. | standard | you |
| COM-10 | Each sequence number is used once. | convention | script |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Put the lifeline that starts the interaction on the left or at the top, and the ones it talks to around it, so no link crosses a box.
- Leave 60 px or more between linked lifelines: the message labels need the room.

## Modeling in the spec

- A link is an edge of kind `link` without a label.
- Each message is a text with role `message`, placed 6 px or more beside its link, with a field `"toward"` naming the receiving lifeline. When emitting, draw a small arrow next to the text pointing at that lifeline.

## Notation and rules

```json
{
  "id": "uml-communication",
  "name": "UML communication diagram",
  "prefix": "COM",
  "legend": false,
  "rule_kinds": "COM-08",
  "nodes": {
    "lifeline": {"shapes": ["rect"], "uniform": true, "rule": "COM-01", "draw": "rectangle reading name : Type, no line below it"},
    "actor":    {"shapes": ["actor"], "rule": "COM-01", "draw": "stick figure with the name below"},
    "note":     {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":    {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "link":      {"line": "solid", "head": "none", "rule": "COM-02", "draw": "plain line between two lifelines that exchange messages"},
    "note-link": {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "message":    {"label": "^\\d+[a-z]*(\\.\\d+[a-z]*)*\\s*(\\*(\\|\\|)?)?\\s*(\\[[^\\]]*\\])?\\s*:\\s*\\S", "hint": "1: name(), 1.1: name(), 2a: name(), 1.2 [guard]: name(), 3 *[i=1..n]: name()", "rule": "COM-03"},
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": [
    {"check": "unique_texts", "role": "message", "key": "^[^:\\[*]*", "rule": "COM-10"}
  ]
}
```

## Sources

- uml-diagrams.org, communication diagrams overview (message drawn as a line with the sequence expression and an arrow above it, sequence expression syntax, frame): https://www.uml-diagrams.org/communication-diagrams.html
- uml-diagrams.org, communication diagrams reference (lifeline without a tail, sequential and concurrent messages, guard, iteration): https://www.uml-diagrams.org/communication-diagrams-reference.html
- COM-10 is a rule of this skill.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
