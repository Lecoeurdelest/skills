# UML component diagram

Spec type `uml-component` · UML structure diagram · frame heading `cmp`

Shows the replaceable parts of a system and the interfaces through which they are wired together. Choose it for a service or module architecture where the contracts between parts matter. Choose a deployment diagram to show where things run.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| CMP-01 | A component is a classifier rectangle with «component». The component icon in its top-right corner may stand in for the keyword. | standard | script |
| CMP-02 | Provided interface: a ball on a stick (lollipop). Required interface: a half-circle on a stick (socket). Each is attached to its component or port by a solid line, with the interface name beside it. | standard | script |
| CMP-03 | A port is a small square on the boundary of its component, with its name beside it. | standard | script |
| CMP-04 | Assembly connector: a solid line between parts or between ports on parts. Between two simple ports it may be drawn as the ball fitted into the socket; that form is not used for ports with several interfaces or for parts without ports. | standard | script |
| CMP-05 | Delegation connector: a line from the port on the outer boundary to the inner part or port that handles the request. | standard | script |
| CMP-06 | Component realization: a dashed line with a hollow triangle from the realizing classifier to the component. The realizing classifiers may instead be nested inside the component. | standard | script |
| CMP-07 | Dependency and usage: a dashed line with an open arrowhead from client to supplier. | standard | script |
| CMP-08 | Large units carry the standard stereotypes such as «Subsystem» or «Service». | standard | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Place a provider and its consumer side by side so the ball and the socket face each other.
- A component that shows its insides is a node with `"container": true`; the parts carry `"parent"`. Ports sit on its border, centred on the line.

## Notation and rules

```json
{
  "id": "uml-component",
  "name": "UML component diagram",
  "prefix": "CMP",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "component":          {"shapes": ["component", "rect"], "label": "\\S", "label_by_shape": {"rect": "«.+»"}, "hint": "a name, with «component» or another keyword when no icon is drawn", "rule": "CMP-01", "draw": "rectangle with the component icon top-right, or with «component»"},
    "provided-interface": {"shapes": ["lollipop"], "rule": "CMP-02", "draw": "ball on a stick"},
    "required-interface": {"shapes": ["socket"], "rule": "CMP-02", "draw": "half-circle on a stick"},
    "interface":          {"shapes": ["compartments", "rect"], "label": "«interface»", "hint": "«interface» Name", "max_lines": 12, "draw": "interface shown with its operations"},
    "port":               {"shapes": ["port"], "rule": "CMP-03", "draw": "small square on the component boundary"},
    "class":              {"shapes": ["compartments", "rect"], "max_lines": 12, "draw": "a classifier that realizes a component"},
    "artifact":           {"shapes": ["rect"], "label": "«.+»", "hint": "«artifact» name", "draw": "class rectangle with «artifact»"},
    "note":               {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":              {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "interface-link": {"line": "solid", "head": "none", "touches": ["provided-interface", "required-interface"], "rule": "CMP-02", "draw": "attaches a ball or socket to its component or port"},
    "assembly":       {"line": "solid", "head": "none", "rule": "CMP-04", "draw": "between parts or ports; or the ball fitted into the socket"},
    "delegation":     {"line": "solid", "head": ["open", "none"], "touches": ["port"], "rule": "CMP-05", "draw": "from the outer port to the inner part or port"},
    "realization":    {"line": "dashed", "head": "hollow", "to": ["component"], "rule": "CMP-06", "draw": "from the realizing classifier to the component"},
    "dependency":     {"line": "dashed", "head": "open", "rule": "CMP-07", "draw": "from client to supplier; «use» for a usage"},
    "manifestation":  {"line": "dashed", "head": "open", "label": "«manifest»", "hint": "«manifest»", "from": ["artifact"], "rule": "CMP-07", "draw": "from the artifact to the component it implements"},
    "note-link":      {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": []
}
```

## Sources

- uml-diagrams.org, component diagrams reference (component, provided and required interface, realization, delegation and assembly connectors): https://www.uml-diagrams.org/component-diagrams-reference.html
- uml-diagrams.org, component (standard stereotypes): https://www.uml-diagrams.org/component.html
- uml-diagrams.org, port and connector: https://www.uml-diagrams.org/port.html and https://www.uml-diagrams.org/composite-structure-diagrams/connector.html
- Not confirmed on those pages: whether a delegation connector carries an arrowhead. The rule accepts both.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
