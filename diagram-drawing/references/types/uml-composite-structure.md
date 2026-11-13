# UML composite structure diagram

Spec type `uml-composite-structure` · UML structure diagram

Shows the inside of one classifier (its parts, ports and the connectors between them), or a collaboration of roles. Choose it to explain how one class or component is assembled. Choose a component diagram for the wiring between several components.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| CST-01 | The structured classifier is a rectangle with its name at the top; its internal structure is drawn inside it. | standard | script |
| CST-02 | A part, owned by composition, is a solid-outline box nested in the classifier. | standard | script |
| CST-03 | A property the classifier refers to without owning it is a dashed-outline box nested in the classifier. | standard | script |
| CST-04 | The multiplicity of a part or property goes in the top-right corner of its box. | standard | script |
| CST-05 | A port is a small square with its name beside it; a type follows after a colon and a multiplicity in square brackets. Provided and required interfaces hang on the port as a lollipop and a socket. | standard | script |
| CST-06 | A connector is a line that joins parts or ports, attached directly to them. | standard | script |
| CST-07 | A collaboration is a dashed ellipse holding its name; its roles and connectors may be shown in a compartment inside the ellipse. | standard | script |
| CST-08 | A collaboration use is a dashed ellipse labelled `useName : CollaborationType`. Each role binding is a dashed line from the ellipse to the element playing the role, labelled with the role name at that end. | standard | script |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- The classifier is a node with `"container": true`; parts and properties carry `"parent"`. Ports sit on its border.
- Leave 40 px between parts so connectors have room.

## Notation and rules

```json
{
  "id": "uml-composite-structure",
  "name": "UML composite structure diagram",
  "prefix": "CST",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "classifier":         {"shapes": ["rect"], "rule": "CST-01", "draw": "the structured classifier; \"container\": true"},
    "part":               {"shapes": ["rect"], "inside": ["classifier", "collaboration"], "rule": "CST-02", "draw": "solid box inside the classifier, labelled name : Type"},
    "property":           {"shapes": ["dashed-rect"], "inside": ["classifier"], "rule": "CST-03", "draw": "dashed box inside the classifier"},
    "port":               {"shapes": ["port"], "rule": "CST-05", "draw": "small square, name beside it"},
    "provided-interface": {"shapes": ["lollipop"], "rule": "CST-05", "draw": "ball on a stick"},
    "required-interface": {"shapes": ["socket"], "rule": "CST-05", "draw": "half-circle on a stick"},
    "collaboration":      {"shapes": ["dashed-ellipse"], "label": "\\S", "hint": "a name", "rule": "CST-07", "draw": "dashed ellipse"},
    "collaboration-use":  {"shapes": ["dashed-ellipse"], "label": ":", "hint": "useName : CollaborationType", "rule": "CST-08", "draw": "dashed ellipse"},
    "note":               {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":              {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "connector":      {"line": "solid", "head": "none", "from": ["part", "property", "port"], "to": ["part", "property", "port"], "rule": "CST-06", "draw": "joins parts or ports"},
    "interface-link": {"line": "solid", "head": "none", "touches": ["provided-interface", "required-interface"], "rule": "CST-05", "draw": "attaches a ball or socket to its port"},
    "role-binding":   {"line": "dashed", "head": ["none", "open"], "from": ["collaboration-use"], "rule": "CST-08", "draw": "from the collaboration use to the element playing the role; label = role name"},
    "note-link":      {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "multiplicity": {"label": "^(\\d+|\\*)(\\.\\.(\\d+|\\*))?$", "hint": "1, 0..1, *, 1..3", "rule": "CST-04"},
    "constraint":   {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":      {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": []
}
```

## Sources

- uml-diagrams.org, composite structures reference (structured classifier, part, non-composite property, multiplicity position, port, collaboration, collaboration use, role binding): https://www.uml-diagrams.org/composite-structure-diagrams-reference.html
- uml-diagrams.org, port (connector joined directly to ports): https://www.uml-diagrams.org/port.html
- Not confirmed on those pages: the line style of a connector. Solid, as for an association, comes from the UML specification as remembered.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
