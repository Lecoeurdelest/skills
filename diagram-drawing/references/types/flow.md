# Flowchart

Spec type `flow` · not UML · symbols of ANSI and ISO 5807:1985

Shows a procedure step by step: what is done, where it branches, where it ends. Choose it for a simple process or algorithm. Choose a UML activity diagram when the process has parallel work or responsibilities per role, and a state machine diagram when the subject is one object changing state.

## Criteria

| Id | Criterion | Basis | Check |
|---|---|---|---|
| FLOW-01 | Terminal (start, end): a stadium, oval or rounded rectangle holding "Start", "End" or a phrase that signals it. | standard | script |
| FLOW-02 | Process: a rectangle. Decision: a diamond. Input or output: a parallelogram. Predefined process (defined elsewhere): a rectangle with double vertical edges. | standard | script |
| FLOW-03 | Document: a rectangle with a wavy base. Data file or database: a cylinder. Manual input: a quadrilateral whose top slopes up from left to right. Manual operation: a trapezoid with the longer side on top. Preparation: an elongated hexagon. | standard | script |
| FLOW-04 | On-page connector: a small circle holding a letter; the same letter marks where the flow continues. Off-page connector: a home-plate pentagon holding a reference. | standard | script |
| FLOW-05 | Annotation: an open rectangle tied to its symbol by a dashed or solid line. | standard | script |
| FLOW-06 | Flowlines are solid. The standard asks for arrowheads only where the flow runs against top-to-bottom, left-to-right; this skill draws an arrowhead on every flowline. | convention | script |
| FLOW-07 | Exactly one start terminal, which nothing enters, and at least one end terminal, which nothing leaves. No terminal has flow both in and out. | convention | script |
| FLOW-08 | Every symbol can be reached from the start, and an end can be reached from every symbol. A loop returns to an earlier step; it never ends nowhere. | convention | script |
| FLOW-09 | A decision asks a question or tests a condition, written inside the diamond. It has at least two exits, each labelled with its outcome (Yes, No, or the value). | convention | script |
| FLOW-10 | Only a decision branches: every other symbol has at most one flowline leaving it. | convention | script |
| FLOW-11 | The standard direction of flow is top to bottom and left to right. This skill allows at most two flowlines against the main direction. | convention | script |
| FLOW-12 | Colors may mark roles, with a legend that says what each one means. | convention | script |

## Layout

- The main path runs down one column (`"direction": "TB"`) or along one row (`"LR"`). A branch moves to the neighbouring column or row at the height of its decision.
- A loop goes back through the outer gutter and is marked `"back": true`.
- Swimlanes (kind `lane`, `"container": true`) may group steps by who performs them. They are common practice, not part of the standard symbol set.

## Notation and rules

```json
{
  "id": "flow",
  "name": "flowchart",
  "prefix": "FLOW",
  "legend": true,
  "generic": {"FLOW-11": "E9", "FLOW-12": "S5"},
  "nodes": {
    "terminator":         {"shapes": ["pill", "ellipse", "rounded"], "label": "\\S", "hint": "Start, End or a phrase that signals it", "rule": "FLOW-01", "draw": "stadium, oval or rounded rectangle"},
    "process":            {"shapes": ["rect"], "uniform": true, "rule": "FLOW-02", "draw": "rectangle"},
    "decision":           {"shapes": ["diamond"], "label": "\\S", "hint": "the question or condition it tests", "rule": "FLOW-09", "draw": "diamond holding a question or condition"},
    "data":               {"shapes": ["parallelogram"], "rule": "FLOW-02", "draw": "parallelogram: input or output"},
    "predefined-process": {"shapes": ["subroutine"], "rule": "FLOW-02", "draw": "rectangle with double vertical edges"},
    "document":           {"shapes": ["document"], "rule": "FLOW-03", "draw": "rectangle with a wavy base"},
    "database":           {"shapes": ["cylinder"], "rule": "FLOW-03", "draw": "cylinder"},
    "manual-input":       {"shapes": ["manual-input"], "rule": "FLOW-03", "draw": "quadrilateral whose top slopes up to the right"},
    "manual-operation":   {"shapes": ["trapezoid"], "rule": "FLOW-03", "draw": "trapezoid, longer side on top"},
    "preparation":        {"shapes": ["hexagon"], "rule": "FLOW-03", "draw": "elongated hexagon"},
    "connector":          {"shapes": ["circle"], "label": "\\S", "hint": "a letter or number", "rule": "FLOW-04", "draw": "small circle with a letter"},
    "off-page-connector": {"shapes": ["pentagon"], "label": "\\S", "hint": "a page or section reference", "rule": "FLOW-04", "draw": "home-plate pentagon"},
    "annotation":         {"shapes": ["bracket"], "rule": "FLOW-05", "draw": "open rectangle (a bracket) beside its text"},
    "lane":               {"shapes": ["lane"], "draw": "swimlane; \"container\": true"}
  },
  "edges": {
    "flow":            {"line": "solid", "head": ["filled", "open"], "rule": "FLOW-06", "draw": "flowline with an arrowhead"},
    "annotation-link": {"line": ["dashed", "solid"], "head": "none", "touches": ["annotation"], "rule": "FLOW-05", "draw": "ties an annotation to its symbol"}
  },
  "texts": {},
  "checks": [
    {"check": "count", "kinds": ["terminator"], "where": "no_in", "min": 1, "max": 1, "what": "start terminal(s) with nothing entering", "rule": "FLOW-07"},
    {"check": "count", "kinds": ["terminator"], "where": "no_out", "min": 1, "what": "end terminal(s) with nothing leaving", "rule": "FLOW-07"},
    {"check": "not_both", "kinds": ["terminator"], "rule": "FLOW-07"},
    {"check": "reachable", "kinds": ["terminator"], "what": "start terminal", "skip_kinds": ["annotation"], "rule": "FLOW-08"},
    {"check": "reaches", "kinds": ["terminator"], "what": "end terminal", "skip_kinds": ["annotation", "off-page-connector"], "rule": "FLOW-08"},
    {"check": "degree", "kinds": ["decision"], "dir": "out", "min": 2, "edge_kinds": ["flow"], "rule": "FLOW-09"},
    {"check": "edge_labels", "kinds": ["decision"], "pattern": "\\S", "hint": "its outcome (Yes, No, or the value)", "rule": "FLOW-09"},
    {"check": "degree", "kinds": ["process", "data", "predefined-process", "document", "database", "manual-input", "manual-operation", "preparation"], "dir": "out", "max": 1, "edge_kinds": ["flow"], "rule": "FLOW-10"},
    {"check": "paired_labels", "kinds": ["connector"], "exact": false, "rule": "FLOW-04"}
  ]
}
```

On-page connectors break the flow on purpose, so the two reachability checks do not follow a jump from one connector to its partner. In a chart that uses connectors, check FLOW-08 across the jumps yourself.

## Sources

- Wikipedia, Flowchart, section "Common symbols" and "Other symbols" (history of the ANSI and ISO symbol sets, shape of each symbol, arrowheads only against the standard direction): https://en.wikipedia.org/wiki/Flowchart
- ISO 5807:1985 is the standard behind that table. Its text is sold by ISO and was not read for this file, so FLOW-01 to FLOW-05 rest on the secondary source above.
- FLOW-06 to FLOW-12 are common practice and rules of this skill, not requirements of the standard.
