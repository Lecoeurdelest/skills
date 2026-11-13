# Diagram Drawing Skill

Notation criteria and a lint gate for 15 diagram types (the 14 UML 2.5 diagram
types and the flowchart), for any drawing tool and any label language. The
agent describes the diagram as a layout spec (JSON), checks it with
`scripts/diagram_lint.py` against the criteria of its diagram type and against
the geometry rules, fixes every failure, and only then hands it to the drawing
tool.

## Structure

```text
diagram-drawing/
├── SKILL.md                     workflow, spec format, generic checks, emit rules
├── README.md
├── references/
│   ├── shapes.md                shape, line and arrowhead vocabulary
│   └── types/
│       ├── README.md            index, file format, how to add criteria or a type
│       ├── uml-<type>.md        one self-contained file per UML diagram type (14 files)
│       └── flow.md              flowchart
└── scripts/
    └── diagram_lint.py
```

Each type file holds its criteria (id, wording, basis, who checks it) and a
JSON block with the rules the script enforces. The script reads that block, so
the criteria a person reads and the rules the script runs are one file.

## Requirements

Python 3.8+. Pillow is optional but recommended (`pip install pillow`): with it
text is measured using local fonts, without it the script falls back to
conservative estimates.

## Try it

```bash
python3 scripts/diagram_lint.py --types                              # the 15 diagram types
python3 scripts/diagram_lint.py --check-types                        # validate every type file
python3 scripts/diagram_lint.py spec.json                            # lint a layout spec
python3 scripts/diagram_lint.py spec.json --styles                   # what to draw for each kind
```

## Status

- Criteria were checked against the reference pages listed under "Sources" in
  each type file. Items that could not be confirmed there are named in the same
  section.
- The repository has no test specs. `--check-types` validates the type files only; the lint rules have not been run against a spec for every type.
- The emit rules for individual drawing tools in `SKILL.md` and
  `references/shapes.md` have not been validated against rendered output for
  every shape.
