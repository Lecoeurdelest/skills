# Diagram Drawing Skill

Layout rules and a lint gate for box-and-arrow diagrams, for any drawing tool
and any label language. The agent describes the diagram as a layout spec
(JSON), measures it with `scripts/diagram_lint.py`, fixes every failure, and
only then hands the geometry to the drawing tool.

## Structure

```text
diagram-drawing/
├── SKILL.md
├── README.md
├── scripts/
│   └── diagram_lint.py
└── tests/
    ├── pass-pdca.json
    ├── fail-text-and-routes.json
    └── fail-structure.json
```

## Requirements

Python 3.8+. Pillow is optional but recommended (`pip install pillow`): with it
text is measured using local fonts, without it the script falls back to
conservative estimates.

## Try the lint

```bash
python3 scripts/diagram_lint.py tests/pass-pdca.json              # PASS, exit 0
python3 scripts/diagram_lint.py tests/fail-text-and-routes.json   # FAIL, exit 1
python3 scripts/diagram_lint.py tests/fail-structure.json         # FAIL, exit 1
python3 scripts/diagram_lint.py tests/pass-pdca.json --sizes      # minimum box sizes
```

The two `fail-*` specs carry planted defects (clipped text, arrows through
boxes and over text, overlapping arrows, missing legend, low contrast,
unanchored routes, too many arrows on one box) and exist to show that each
check fires.

## Status

The lint has been exercised on the three specs in `tests/`. The emit rules for
individual drawing tools in `SKILL.md` have not yet been validated against
rendered output.
