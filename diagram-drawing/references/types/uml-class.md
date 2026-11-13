# UML class diagram

Spec type `uml-class` · UML structure diagram · frame heading `class`

Shows types (classes, interfaces, enumerations) with their features and the static relationships between them. Choose it for a domain model or a design. Choose an object diagram to show concrete instances at one moment.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| CLS-01 | A class is a solid rectangle with the name compartment on top. Attributes and operations follow in their own compartments, separated by horizontal lines; an empty compartment may be left out. | standard | script |
| CLS-02 | Members read `visibility name : Type`, where visibility is + public, - private, # protected or ~ package. Operations add a parameter list: `+ total(rate : Decimal) : Money`. | standard | you |
| CLS-03 | An interface is a class rectangle with «interface» before the name, or a ball (provided) or socket (required) attached to its classifier by a solid line. An enumeration carries «enumeration» and lists its literals one per line. A primitive type carries «primitive». | standard | script |
| CLS-04 | Association: a solid line. An open arrowhead marks a navigable end, a small x a non-navigable end, and no adornment leaves navigability unspecified. | standard | script |
| CLS-05 | Aggregation: a hollow diamond at the aggregate (whole) end. Composition: a filled diamond at the composite end. | standard | script |
| CLS-06 | A part belongs to at most one composite at a time, so the multiplicity at the composite end is 1 or 0..1. | standard | you |
| CLS-07 | Generalization: a solid line with a hollow triangle pointing at the more general classifier. | standard | script |
| CLS-08 | Interface realization: a dashed line with a hollow triangle pointing at the interface. Dependency: a dashed line with an open arrowhead from client to supplier. | standard | script |
| CLS-09 | A multiplicity is written `1`, `0..1`, `*`, `0..*`, `1..*` or `m..n`, next to the end it describes. Every association end that matters has one. | standard | script |
| CLS-10 | An association with more than two ends is a diamond with one solid line to each classifier. | standard | script |
| CLS-11 | An abstract classifier has its name in italics or is marked {abstract}; static members are underlined. | standard | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- The general classifier sits above the specific ones; a whole sits left of or above its parts.
- Associated classes sit side by side so the line runs horizontally and the end labels sit above it, clear of the class text.
- At most three classes per row.

## Modeling in the spec

- A class is one node of shape `compartments`. Its `lines` are the name, then `---`, the attributes, `---`, the operations. A line that is exactly `---` is a compartment separator.
- A multiplicity or role name is a text with role `multiplicity` or `role`, placed 6 px or more from the line, near the end it belongs to.
- For aggregation and composition the edge runs from the whole to the part, so the diamond is the `tail`.
- An association class and a qualifier are not modelled by the spec; draw them by hand and check them yourself.

## Notation and rules

```json
{
  "id": "uml-class",
  "name": "UML class diagram",
  "prefix": "CLS",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "class":              {"shapes": ["compartments", "rect"], "label": "\\S", "hint": "a name", "max_lines": 12, "rule": "CLS-01", "draw": "rectangle with name, attribute and operation compartments"},
    "interface":          {"shapes": ["compartments", "rect"], "label": "«interface»", "hint": "«interface» Name", "max_lines": 12, "rule": "CLS-03", "draw": "class rectangle with «interface»"},
    "provided-interface": {"shapes": ["lollipop"], "rule": "CLS-03", "draw": "ball on a stick, the interface name beside it"},
    "required-interface": {"shapes": ["socket"], "rule": "CLS-03", "draw": "half-circle on a stick, the interface name beside it"},
    "enumeration":        {"shapes": ["compartments", "rect"], "label": "«enumeration»", "hint": "«enumeration» Name", "max_lines": 12, "rule": "CLS-03", "draw": "class rectangle listing the literals"},
    "datatype":           {"shapes": ["compartments", "rect"], "label": "«(dataType|primitive)»", "hint": "«dataType» Name or «primitive» Name", "max_lines": 12, "rule": "CLS-03", "draw": "class rectangle with the keyword"},
    "association-node":   {"shapes": ["diamond"], "rule": "CLS-10", "draw": "diamond joining the ends of an n-ary association"},
    "note":               {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":              {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "association":    {"line": "solid", "head": ["none", "open", "x"], "tail": ["none", "open", "x"], "rule": "CLS-04", "draw": "open arrowhead = navigable end, x = not navigable"},
    "aggregation":    {"line": "solid", "tail": "hollow-diamond", "head": ["none", "open"], "rule": "CLS-05", "draw": "from the whole (diamond) to the part"},
    "composition":    {"line": "solid", "tail": "diamond", "head": ["none", "open"], "rule": "CLS-05", "draw": "from the composite (filled diamond) to the part"},
    "generalization": {"line": "solid", "head": "hollow", "rule": "CLS-07", "draw": "from the specific classifier to the general one"},
    "realization":    {"line": "dashed", "head": "hollow", "to": ["interface"], "rule": "CLS-08", "draw": "from the implementing classifier to the interface"},
    "dependency":     {"line": "dashed", "head": "open", "rule": "CLS-08", "draw": "from client to supplier; a keyword such as «use» may label it"},
    "interface-link": {"line": "solid", "head": "none", "touches": ["provided-interface", "required-interface"], "rule": "CLS-03", "draw": "attaches a ball or socket to its classifier"},
    "note-link":      {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "multiplicity": {"label": "^(\\d+|\\*)(\\.\\.(\\d+|\\*))?(\\s*\\{.+\\})?$", "hint": "1, 0..1, *, 0..*, 1..* or m..n", "rule": "CLS-09"},
    "role":         {"draw": "association end name, optionally with a visibility sign"},
    "constraint":   {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":      {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": [
    {"check": "degree", "kinds": ["association-node"], "dir": "out", "min": 3, "edge_kinds": ["association"], "rule": "CLS-10"}
  ]
}
```

For an n-ary association, draw each of its lines as an `association` edge from the diamond to a classifier.

## Sources

- uml-diagrams.org, class diagrams reference (class, interface, enumeration, primitive type, operations, multiplicity, constraints, n-ary association, aggregation, composition): https://www.uml-diagrams.org/class-reference.html
- uml-diagrams.org, association (navigability notation, end ownership): https://www.uml-diagrams.org/association.html
- uml-diagrams.org, generalization: https://www.uml-diagrams.org/generalization.html
- uml-diagrams.org, component diagrams reference (realization as a dashed line with a hollow triangle) and deployment diagrams reference (dependency as a dashed line with an open arrowhead from client to supplier).
- Not confirmed on those pages: CLS-11 and the «dataType» keyword. Both come from the UML specification as remembered.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
