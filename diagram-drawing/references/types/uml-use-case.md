# UML use case diagram

Spec type `uml-use-case` · UML behavior diagram · frame heading `uc`

Shows what a system (the subject) offers to the actors around it. Choose it to agree on scope and on who uses what. It shows no order of steps: use an activity or sequence diagram for that.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| UC-01 | An actor is a stick figure with its name above or below it, or a class rectangle with «actor». Every actor has a name. | standard | script |
| UC-02 | A use case is an ellipse with its name inside (the name may also go below the ellipse). Every use case has a name. | standard | script |
| UC-03 | The subject is a rectangle with its name in an upper corner. The use cases that apply to it sit inside; actors stand outside. | standard | script |
| UC-04 | An actor and a use case that communicate are joined by an association: a solid line, without arrowheads unless navigability matters. | standard | script |
| UC-05 | Include: dashed line, open arrowhead from the including (base) use case to the included one, labelled «include». The included behavior is required. | standard | script |
| UC-06 | Extend: dashed line, open arrowhead from the extending use case to the extended (base) one, labelled «extend». The extension is optional; its condition and extension point go in a note tied to the arrow. | standard | script |
| UC-07 | Generalization between two actors or between two use cases: solid line, hollow triangle at the general one. | standard | script |
| UC-08 | Two use cases of the same subject are never joined by a plain association. Relate them with include, extend or generalization. | standard | script |
| UC-09 | A use case names a result of value to an actor, not an internal step of the system. | standard | you |
| UC-10 | Extension points, when shown, are listed in a compartment of the use case headed `extension points`. | standard | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- Primary actors stand left of the subject, at the height of their use cases. Supporting actors (other systems) stand on the right.
- Use cases form one column inside the subject. Included and extending use cases go in a second column beside the ones that use them.
- Mark the subject `"container": true` and give each use case `"parent"` set to its id.

## Notation and rules

```json
{
  "id": "uml-use-case",
  "name": "UML use case diagram",
  "prefix": "UC",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "actor":    {"shapes": ["actor", "rect"], "label": "\\S", "label_by_shape": {"rect": "«actor»"}, "hint": "a name (with «actor» when drawn as a rectangle)", "not_inside": ["subject"], "rule": "UC-01", "draw": "stick figure with the name below or above"},
    "use-case": {"shapes": ["ellipse", "rect"], "label": "\\S", "hint": "a name", "uniform": true, "rule": "UC-02", "draw": "ellipse with the name inside"},
    "subject":  {"shapes": ["rect"], "rule": "UC-03", "draw": "rectangle with the subject name in an upper corner; \"container\": true"},
    "note":     {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":    {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "association":    {"line": "solid", "head": ["none", "open"], "tail": ["none", "open"], "between": [["actor", "use-case"]], "rule": "UC-04", "rule_between": "UC-08", "draw": "actor communicates with use case"},
    "include":        {"line": "dashed", "head": "open", "label": "«include»", "hint": "«include»", "from": ["use-case"], "to": ["use-case"], "rule": "UC-05", "draw": "from the including (base) use case to the included one"},
    "extend":         {"line": "dashed", "head": "open", "label": "«extend»", "hint": "«extend»", "from": ["use-case"], "to": ["use-case"], "rule": "UC-06", "draw": "from the extending use case to the extended (base) one"},
    "generalization": {"line": "solid", "head": "hollow", "between": [["actor"], ["use-case"]], "rule": "UC-07", "draw": "from the specific actor or use case to the general one"},
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

- uml-diagrams.org, use case diagrams reference (subject, actor, use case, association, include, extend, generalization, extension points): https://www.uml-diagrams.org/use-case-reference.html
- uml-diagrams.org, UML use case (two use cases of one subject cannot be associated): https://www.uml-diagrams.org/use-case.html
- uml-diagrams.org, use case include: https://www.uml-diagrams.org/use-case-include.html
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
