# UML object diagram

Spec type `uml-object` · UML structure diagram

Shows concrete instances and the links between them at one moment. Choose it to illustrate a class diagram with an example, or to show a particular configuration. UML 2.5 no longer defines the object diagram as a diagram of its own; it is a class diagram drawn at instance level.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| OBJ-01 | The diagram holds instance specifications, their slots and links only. Classes do not appear in it. | standard | script |
| OBJ-02 | An instance uses the classifier rectangle. Its title is `name : Classifier`, underlined. The name or the classifier may be left out, the colon stays. The underline may be dropped only when the diagram obviously shows instances. | standard | script |
| OBJ-03 | A slot reads `feature = value`, one per line, below the title. | standard | you |
| OBJ-04 | A link is an instance of an association and is drawn like one: a solid line between two instances. Its name may be underlined; end names and navigation arrows are allowed. | standard | script |
| OBJ-05 | An instance shows values, so it has no operations compartment. | convention | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Follow the layout of the class diagram the instances come from, so the two can be compared.
- Give the title its own line and separate the slots with `---`.

## Notation and rules

```json
{
  "id": "uml-object",
  "name": "UML object diagram",
  "prefix": "OBJ",
  "legend": false,
  "rule_kinds": "OBJ-01",
  "nodes": {
    "instance": {"shapes": ["compartments", "rect"], "label": ":", "hint": "name : Classifier (underlined)", "max_lines": 10, "rule": "OBJ-02", "draw": "classifier rectangle with an underlined title and slots below"},
    "note":     {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":    {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "link":      {"line": "solid", "head": ["none", "open"], "tail": ["none", "open"], "from": ["instance"], "to": ["instance"], "rule": "OBJ-04", "draw": "an instance of an association"},
    "note-link": {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "role":       {"draw": "end name of a link"},
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": []
}
```

## Sources

- uml-diagrams.org, UML 2.5 diagrams overview (the object diagram has no definition in UML 2.5; its elements are instance specification, slot and link): https://www.uml-diagrams.org/uml-25-diagrams.html
- uml-diagrams.org, UML core elements reference (instance name notation, slots, link): https://www.uml-diagrams.org/uml-core-reference.html
- OBJ-05 is a rule of this skill.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
