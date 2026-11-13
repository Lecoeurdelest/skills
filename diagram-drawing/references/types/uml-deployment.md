# UML deployment diagram

Spec type `uml-deployment` · UML structure diagram · frame heading `dep`

Shows where software runs: which artifacts are deployed on which nodes, and how the nodes communicate. Choose it for infrastructure and runtime topology. Choose a component diagram for the logical parts and their interfaces.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| DEP-01 | A node is a three-dimensional box. A device is a node with «device»; an execution environment is a node with «executionEnvironment». Nodes may be nested, an execution environment usually inside a device. | standard | script |
| DEP-02 | An artifact is a class rectangle with «artifact» or one of the standard artifact stereotypes («file», «document», «source», «library», «executable», «script»). A document icon in its top-right corner is optional. | standard | script |
| DEP-03 | A deployment is shown in one of three ways: the artifact drawn inside its target, a dashed line with an open arrowhead labelled «deploy» from the artifact to the target, or a text list of artifacts inside the target. | standard | script |
| DEP-04 | Artifacts are deployed, components are not. A component reaches a node through the artifact that manifests it: a dashed line with an open arrowhead labelled «manifest» from the artifact to the component. | standard | script |
| DEP-05 | A communication path is a plain association, a solid line, between two deployment targets. Label it with the medium or the protocol when that helps. | standard | script |
| DEP-06 | A dependency between artifacts is a dashed line with an open arrowhead from client to supplier. | standard | script |
| DEP-07 | An instance-level diagram names instances `name : Type`; the underline may be omitted. | standard | you |
| DEP-08 | Every artifact shown is deployed somewhere: inside a target or tied to one by «deploy». | convention | you |
| UML-01 | Keywords and stereotypes are written in guillemets before or above the element name: «interface», «component», «device». | standard | you |
| UML-02 | A note is a rectangle with a bent corner, tied to its element by a dashed line without arrowheads. It holds a remark or a constraint, never a step of the behavior. | standard | script |
| UML-03 | A constraint is text in curly braces: {ordered}, {xor}, {t..t+3}. | standard | script |
| UML-04 | The diagram frame is optional. When drawn it is a rectangle with a heading in a compartment at its top-left: the diagram kind, then the name. Short kinds: act, class, cmp, dep, sd, pkg, stm, uc. | standard | you |
| UML-05 | Only the elements and relationships listed in the type file appear in the diagram. A symbol borrowed from another diagram type makes the diagram wrong. | convention | script |
| UML-06 | One neutral fill. UML gives color no meaning, so a UML diagram has no legend. | convention | you |

Rows with a `UML-` id are the rules every UML diagram shares. Each UML type file repeats them, with the same wording, so that the file stands alone.

## Layout

- One row per tier, top to bottom: clients, entry points, services, data.
- A node that holds artifacts or other nodes is a node with `"container": true`; its contents carry `"parent"`.
- Communication paths are short straight lines between neighbouring nodes.

## Notation and rules

```json
{
  "id": "uml-deployment",
  "name": "UML deployment diagram",
  "prefix": "DEP",
  "legend": false,
  "rule_kinds": "UML-05",
  "nodes": {
    "node":                  {"shapes": ["cube"], "label": "\\S", "hint": "a name", "rule": "DEP-01", "draw": "three-dimensional box"},
    "device":                {"shapes": ["cube"], "label": "«device»", "hint": "«device» Name", "rule": "DEP-01", "draw": "three-dimensional box with «device»"},
    "execution-environment": {"shapes": ["cube"], "label": "«executionEnvironment»", "hint": "«executionEnvironment» Name", "rule": "DEP-01", "draw": "three-dimensional box with «executionEnvironment»"},
    "artifact":              {"shapes": ["rect"], "label": "«(artifact|file|document|source|library|executable|script)»", "hint": "«artifact» name", "rule": "DEP-02", "draw": "class rectangle with the keyword"},
    "component":             {"shapes": ["component", "rect"], "not_inside": ["node", "device", "execution-environment"], "rule": "DEP-04", "draw": "shown only as what an artifact manifests, never placed on a node"},
    "deployment-spec":       {"shapes": ["rect"], "label": "«deployment spec»", "hint": "«deployment spec» name", "draw": "class rectangle with the keyword and its properties"},
    "note":                  {"shapes": ["note"], "rule": "UML-02", "draw": "rectangle with a bent top-right corner"},
    "frame":                 {"shapes": ["frame"], "draw": "diagram frame: rectangle with the heading in a top-left compartment; mark it \"container\": true"}
  },
  "edges": {
    "communication-path": {"line": "solid", "head": "none", "from": ["node", "device", "execution-environment"], "to": ["node", "device", "execution-environment"], "rule": "DEP-05", "draw": "association between two deployment targets"},
    "deployment":         {"line": "dashed", "head": "open", "label": "«deploy»", "hint": "«deploy»", "from": ["artifact"], "to": ["node", "device", "execution-environment"], "rule": "DEP-03", "draw": "from the artifact to its target"},
    "manifestation":      {"line": "dashed", "head": "open", "label": "«manifest»", "hint": "«manifest»", "from": ["artifact"], "rule": "DEP-04", "draw": "from the artifact to the element it implements"},
    "dependency":         {"line": "dashed", "head": "open", "rule": "DEP-06", "draw": "from client to supplier"},
    "composition":        {"line": "solid", "tail": "diamond", "head": "none", "draw": "an artifact that contains another, or a node made of nodes"},
    "note-link":          {"line": "dashed", "head": "none", "touches": ["note"], "rule": "UML-02", "draw": "ties a note to the element it describes"}
  },
  "texts": {
    "constraint": {"label": "^\\{.+\\}$", "hint": "{text in curly braces}", "rule": "UML-03"},
    "heading":    {"draw": "the heading of a frame, placed in its top-left corner"}
  },
  "checks": []
}
```

## Sources

- uml-diagrams.org, deployment diagrams reference (artifact and its stereotypes, dependency, manifestation, node, device, execution environment, communication path, the forms of deployment, frame heading): https://www.uml-diagrams.org/deployment-diagrams-reference.html
- uml-diagrams.org, deployment diagrams overview (artifacts, not components, are deployed in UML 2): https://www.uml-diagrams.org/deployment-diagrams.html
- Not confirmed on those pages: the «deployment spec» keyword (the page was cut off there). It comes from the UML specification as remembered.
- DEP-08 is a rule of this skill.
- Rules shared by all UML diagrams (ids `UML-`): constraint and note notation from the class diagrams reference, https://www.uml-diagrams.org/class-reference.html; frame headings from the reference page of each diagram. UML-05 and UML-06 are rules of this skill, not of UML.
