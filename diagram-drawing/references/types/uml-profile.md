# UML profile diagram

Spec type `uml-profile` · UML structure diagram

Shows an extension of UML itself: stereotypes, the metaclasses they extend and their tag definitions. Choose it only when defining a profile. To use a stereotype in a model, draw the ordinary diagram and write the stereotype in guillemets.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| PRF-01 | A profile uses the package notation with «profile» before or above its name. | standard | script |
| PRF-02 | A metaclass is a class rectangle with «Metaclass» above its name (lower-case «metaclass» before UML 2.4). | standard | script |
| PRF-03 | A stereotype is a class rectangle with «stereotype» before or above its name. Its properties are its tag definitions. | standard | script |
| PRF-04 | Extension: a solid line with a filled triangular arrowhead from the stereotype to the metaclass it extends. Navigability arrows are not shown on it. | standard | script |
| PRF-05 | A required extension is marked {required} near the extension end; multiplicity 1 says the same. | standard | you |
| PRF-06 | A stereotype generalizes or specializes only another stereotype: a solid line with a hollow triangle at the general one. | standard | script |
| PRF-07 | Profile application: a dashed line with an open arrowhead from the applying package to the profile, labelled «apply». | standard | script |
| PRF-08 | A metaclass reference is an import labelled «reference». | standard | script |
| PRF-09 | Every stereotype extends at least one metaclass, directly or through a parent stereotype. | convention | you |
| PRF-10 | An applied stereotype is written with an upper-case first letter since UML 2.4 («Servlet»); lower case is still valid but obsolete. | standard | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Metaclasses in the top row, the stereotypes that extend them below, so extension arrows point up.
- The profile is a node with `"container": true` when its contents are drawn inside it.

## Notation and rules

```json
{
  "id": "uml-profile",
  "name": "UML profile diagram",
  "prefix": "PRF",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "profile":    {"shapes": ["folder"], "label": "«profile»", "hint": "«profile» Name", "rule": "PRF-01", "draw": "package symbol with «profile»"},
    "metaclass":  {"shapes": ["compartments", "rect"], "label": "«metaclass»", "hint": "«Metaclass» Name", "max_lines": 12, "rule": "PRF-02", "draw": "class rectangle with «Metaclass»"},
    "stereotype": {"shapes": ["compartments", "rect"], "label": "«stereotype»", "hint": "«stereotype» Name", "max_lines": 12, "rule": "PRF-03", "draw": "class rectangle with «stereotype»; tag definitions as attributes"},
    "package":    {"shapes": ["folder"], "draw": "a package the profile is applied to"},
    "class":      {"shapes": ["compartments", "rect"], "max_lines": 12, "draw": "a class, data type or enumeration the profile defines"},
    "note":       {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":      {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "extension":           {"line": "solid", "head": "filled", "from": ["stereotype"], "to": ["metaclass"], "rule": "PRF-04", "draw": "from the stereotype to the metaclass"},
    "generalization":      {"line": "solid", "head": "hollow", "from": ["stereotype"], "to": ["stereotype"], "rule": "PRF-06", "draw": "from the specific stereotype to the general one"},
    "profile-application": {"line": "dashed", "head": "open", "label": "«apply»", "hint": "«apply»", "to": ["profile"], "rule": "PRF-07", "draw": "from the applying package to the profile"},
    "reference":           {"line": "dashed", "head": "open", "label": "«reference»", "hint": "«reference»", "from": ["profile"], "rule": "PRF-08", "draw": "from the profile to the metaclass or package it imports"},
    "note-link":           {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": []
}
```

## Sources

- uml-diagrams.org, profile diagrams reference (profile, metaclass, stereotype, tag definitions, extension, required extension, generalization of stereotypes, reference, profile application, capitalization of applied stereotypes): https://www.uml-diagrams.org/profile-diagrams-reference.html
- Not confirmed on that page: the line style and arrowhead of the «reference» import. Dashed with an open arrowhead, as for any import, comes from the package diagrams reference.
- PRF-09 is a rule of this skill.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
