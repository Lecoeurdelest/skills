# UML sequence diagram

Spec type `uml-sequence` · UML interaction diagram · frame heading `sd`

Shows the messages a set of participants exchange, in time order. Choose it when the order of calls and replies is the point. Choose a communication diagram when who talks to whom matters more than the order, and an activity diagram when the subject is a procedure, not a conversation.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| SEQ-01 | A lifeline is a head with a vertical line below it; the line may be dashed. The head is a rectangle reading `name : Type` (either part may be left out) or, for an actor, a stick figure. | standard | script |
| SEQ-02 | Every participant has its own lifeline, and time runs downward along it. | standard | script |
| SEQ-03 | An execution specification is a thin grey or white rectangle on the lifeline for as long as the participant is busy. Nested executions overlap, offset sideways. | standard | script |
| SEQ-04 | Synchronous call: solid line, filled arrowhead. Asynchronous message: solid line, open arrowhead. | standard | script |
| SEQ-05 | Reply: dashed line, open arrowhead, drawn back to the caller below the call it answers. | standard | script |
| SEQ-06 | Create message: dashed line, open arrowhead, ending on the head of the lifeline it creates. That head sits at the height of the message, lower than the other heads. | standard | script |
| SEQ-07 | Destruction: an X at the bottom of the lifeline, and nothing happens on that lifeline below it. UML has no arrow of its own for delete; label the message «destroy» when you need to name it. | standard | script |
| SEQ-08 | A message line runs horizontally or downward from sender to receiver, never upward. A self-message leaves its lifeline and returns to it lower down. | standard | script |
| SEQ-09 | A found message starts at a small black circle; a lost message ends at one. | standard | script |
| SEQ-10 | A combined fragment is a frame whose top-left tag holds its operator: alt, opt, loop, break, par, strict, seq, critical, ignore, consider, assert or neg. Operands are separated by dashed horizontal lines, and each guard stands in square brackets at the top of its operand. | standard | script |
| SEQ-11 | An interaction use is a frame tagged `ref` that names the interaction it stands for. | standard | script |
| SEQ-12 | A state invariant is a constraint in curly braces on the lifeline, or a state symbol on it. | standard | script |
| SEQ-13 | A synchronous call ends at an execution bar of the receiver. UML lets executions be left out; this skill always draws them. | convention | script |
| SEQ-14 | Work a participant does alone is a self-message. A person or outside system that takes part is a lifeline with its own messages. Neither is a note. | convention | you |
| SEQ-15 | A message label sits centred above its arrow, between the two lifelines the arrow joins. | convention | script |
| SEQ-16 | The frame around the whole diagram, when drawn, is headed `sd` and the interaction name. | standard | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Heads in one row at the top, in the order they first speak, the initiator on the left. Heads may sit 16 px apart.
- One message per row; rows 30 px apart or more. Sequence diagrams grow tall, so set `view_height` and split the diagram when it does not fit.
- A participant that talks to everyone is marked `"hub": true`.

## Modeling in the spec

- Head: a node of kind `lifeline` or `actor`. Line of life: a `guide` with `of` set to the head's id.
- Execution: a node of kind `execution` with `of`, `"on_guide": true` and `"standalone": true`, 8 px wide, centred on the guide.
- Message: an edge with `"anchor": "guide"`; its two points lie on the two lifelines at one `y` and stop at the edge of the execution bar. A create message ends on the border of the created head instead.
- Self-message: an edge from a head to itself with four points (out, down, back); its label sits to the right of the loop.
- Labels: `label_box` centred over the arrow, `"label_mask": true`, drawn with an opaque background so lifelines pass behind the text.
- Combined fragment: a node of kind `fragment` with `"container": true` and no lines, a text with role `operator` in its top-left corner, one text with role `guard` per operand, and a `guide` without `of` for each operand separator.
- Found or lost message: the far end is a node of kind `endpoint`.

## Notation and rules

```json
{
  "id": "uml-sequence",
  "name": "UML sequence diagram",
  "prefix": "SEQ",
  "legend": false,
  "rule_kinds": "UML-05",
  "generic": {"SEQ-15": "E12"},
  "nodes": {
    "lifeline":        {"shapes": ["rect"], "uniform": true, "rule": "SEQ-01", "draw": "head: rectangle reading name : Type"},
    "actor":           {"shapes": ["actor"], "rule": "SEQ-01", "draw": "head: stick figure with the name below"},
    "execution":       {"shapes": ["rect"], "text": false, "rule": "SEQ-03", "draw": "thin grey or white rectangle on the lifeline"},
    "fragment":        {"shapes": ["frame"], "rule": "SEQ-10", "draw": "frame with the operator in a top-left tag"},
    "interaction-use": {"shapes": ["frame"], "rule": "SEQ-11", "draw": "frame tagged ref, holding the name of the interaction; \"on_guide\": true"},
    "destruction":     {"shapes": ["x"], "text": false, "rule": "SEQ-07", "draw": "X at the bottom of a lifeline; \"of\" its head, \"on_guide\": true"},
    "state-invariant": {"shapes": ["text", "rounded"], "rule": "SEQ-12", "draw": "{constraint} on the lifeline, or a state symbol; \"on_guide\": true"},
    "endpoint":        {"shapes": ["dot"], "text": false, "rule": "SEQ-09", "draw": "small black circle: the unknown end of a found or lost message"},
    "note":            {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":           {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "sync":      {"line": "solid", "head": "filled", "to": ["lifeline", "actor"], "from": ["lifeline", "actor"], "rule": "SEQ-04", "draw": "synchronous call"},
    "async":     {"line": "solid", "head": "open", "to": ["lifeline", "actor"], "from": ["lifeline", "actor"], "rule": "SEQ-04", "draw": "asynchronous message or signal"},
    "reply":     {"line": "dashed", "head": "open", "to": ["lifeline", "actor"], "from": ["lifeline", "actor"], "rule": "SEQ-05", "draw": "reply to a synchronous call"},
    "create":    {"line": "dashed", "head": "open", "to": ["lifeline"], "from": ["lifeline", "actor"], "rule": "SEQ-06", "draw": "ends on the head of the created lifeline"},
    "delete":    {"line": "solid", "head": ["filled", "open"], "to": ["lifeline"], "from": ["lifeline", "actor"], "rule": "SEQ-07", "draw": "the receiver's lifeline ends in a destruction X just below"},
    "found":     {"line": "solid", "head": ["filled", "open"], "from": ["endpoint"], "to": ["lifeline", "actor"], "rule": "SEQ-09", "draw": "sender unknown"},
    "lost":      {"line": "solid", "head": ["filled", "open"], "from": ["lifeline", "actor"], "to": ["endpoint"], "rule": "SEQ-09", "draw": "receiver unknown"},
    "note-link": {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "operator":   {"label": "^(alt|opt|loop|break|par|strict|seq|critical|ignore|consider|assert|neg|ref)\\b", "hint": "an interaction operator such as alt, opt, loop, par, or ref", "rule": "SEQ-10"},
    "guard":      {"label": "^\\[.+\\]$", "hint": "[condition]", "rule": "SEQ-10"},
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": [
    {"check": "has_guide", "kinds": ["lifeline", "actor"], "rule": "SEQ-02"},
    {"check": "text_in", "kinds": ["fragment", "interaction-use"], "role": "operator", "min": 1, "max": 1, "rule": "SEQ-10"},
    {"check": "sequence", "rules": {"execution": "SEQ-03", "downward": "SEQ-08", "activation": "SEQ-13", "reply": "SEQ-05", "destruction": "SEQ-07"}}
  ]
}
```

## Sources

- uml-diagrams.org, sequence diagrams reference (lifeline, execution, message kinds, create, delete, found and lost messages, destruction, state invariant, operators): https://www.uml-diagrams.org/sequence-diagrams-reference.html
- uml-diagrams.org, sequence diagrams overview: https://www.uml-diagrams.org/sequence-diagrams.html
- Not confirmed on those pages: the dashed line between operands and the place of a guard at the top of its operand (SEQ-10). Both come from the UML specification as remembered.
- SEQ-13, SEQ-14 and SEQ-15 are rules of this skill, not of UML.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
