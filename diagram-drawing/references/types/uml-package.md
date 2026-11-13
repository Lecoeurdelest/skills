# UML package diagram

Spec type `uml-package` · UML structure diagram · frame heading `pkg`

Shows how model elements are grouped into packages and how the packages depend on each other. Choose it for the module or layer structure of a system.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| PKG-01 | A package is a rectangle with a small tab on the left of its top edge. | standard | script |
| PKG-02 | When members are drawn inside the package, its name goes on the tab; otherwise the name goes in the body. | standard | you |
| PKG-03 | Members drawn outside the package hang on solid lines that end in a circled plus at the package. | standard | script |
| PKG-04 | A member of a package has only public (+) or private (-) visibility. | standard | you |
| PKG-05 | Package import: a dashed line with an open arrowhead from the importing namespace to the imported package, labelled «import» when public and «access» when private. | standard | script |
| PKG-06 | Package merge: a dashed line with an open arrowhead from the receiving package to the merged package, labelled «merge». | standard | script |
| PKG-07 | Plain dependency: a dashed line with an open arrowhead from the package that depends to the package it needs. | standard | script |
| PKG-08 | A model is a package with a small triangle in the upper right corner of its body. | standard | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Put a package above or left of the packages that depend on it, so most arrows point one way.
- A package that shows its members is a node with `"container": true`; its members carry `"parent"`.

## Notation and rules

```json
{
  "id": "uml-package",
  "name": "UML package diagram",
  "prefix": "PKG",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "package": {"shapes": ["folder"], "label": "\\S", "hint": "a name", "rule": "PKG-01", "draw": "rectangle with a small tab at the top-left"},
    "class":   {"shapes": ["compartments", "rect"], "max_lines": 12, "draw": "a packageable element shown as a member"},
    "note":    {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":   {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "import":      {"line": "dashed", "head": "open", "label": "«(import|access)»", "hint": "«import» or «access»", "to": ["package"], "rule": "PKG-05", "draw": "from the importing namespace to the imported package"},
    "merge":       {"line": "dashed", "head": "open", "label": "«merge»", "hint": "«merge»", "from": ["package"], "to": ["package"], "rule": "PKG-06", "draw": "from the receiving package to the merged package"},
    "dependency":  {"line": "dashed", "head": "open", "rule": "PKG-07", "draw": "from the dependent package to the one it needs"},
    "containment": {"line": "solid", "tail": "circle-plus", "head": "none", "from": ["package"], "rule": "PKG-03", "draw": "from the package (circled plus) to a member drawn outside it"},
    "note-link":   {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": []
}
```

## Sources

- uml-diagrams.org, package diagrams reference (package, members inside and outside, visibility, element and package import, merge, model): https://www.uml-diagrams.org/package-diagrams-reference.html
- uml-diagrams.org, package diagrams notation: https://www.uml-diagrams.org/package-diagrams.html
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
