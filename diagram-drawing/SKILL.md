---
name: diagram-drawing
description: Use before drawing or editing any diagram in any tool or language - a flowchart or one of the 14 UML diagram types (class, object, package, component, composite structure, deployment, profile, use case, activity, state machine, sequence, communication, timing, interaction overview). Gives per-type notation criteria, layout rules and a lint gate that stops wrong symbols, clipped text and messy arrows.
---

# Diagram drawing

Use this skill for every diagram, whatever tool draws it (draw.io, an inline SVG or HTML widget, Mermaid, FigJam, a whiteboard, anything connected later) and whatever language the labels are in. It draws 15 diagram types: the 14 diagram types of UML 2.5 and the flowchart. Charts of numeric data are out of scope; use a data visualization skill for those.

## Why this skill exists

A diagram goes wrong in two ways. The notation is wrong: a reply drawn as a solid arrow, a fork drawn as a diamond, a flowchart box where the type has no such symbol. Or the geometry is wrong: clipped labels, arrows through boxes and text. Both happen because you usually cannot see the diagram after you draw it, and both have the same fix: describe the diagram as a layout spec with explicit kinds and geometry, let a script check it against the rules of its type, repair it until it passes, and only then hand it to the drawing tool unchanged.

On notation, geometry, sizing and arrow routing this skill overrides a tool's own guidance (for example a tool that says "do not add waypoints"). The tool's guidance still governs its syntax, colors and theme.

## Diagram types

| Family | Spec types |
|---|---|
| UML structure | `uml-class`, `uml-object`, `uml-package`, `uml-component`, `uml-composite-structure`, `uml-deployment`, `uml-profile` |
| UML behavior | `uml-use-case`, `uml-activity`, `uml-state-machine` |
| UML interaction | `uml-sequence`, `uml-communication`, `uml-timing`, `uml-interaction-overview` |
| Not UML | `flow` (flowchart) |

Every diagram is exactly one of these types. When the user names a type, draw that type; do not swap it for one that is easier to lay out. When no type is named, choose the one whose purpose matches the request (each type file says when to choose it) and say which you chose. If the content fits none of them, say so and offer the nearest type.

Each type has its own file, `references/types/<spec type>.md`, with the criteria for that type: what each element looks like, how elements may be connected, and what the structure must satisfy. Every criterion has an id (`SEQ-05`, `FLOW-09`), a basis (`standard` or `convention`) and a check (`script` or `you`). Every type file stands alone: read only the file for your type. The few rules all UML diagrams share (ids `UML-01` to `UML-06`) are repeated in each UML file.

## Workflow

1. **Type and inventory.** Fix the diagram type and read its type file. List every element the user named and give each one a `kind` from that file; if something has no kind there, it does not belong in this diagram type. Pick one main flow direction (`LR` or `TB`) where the type has one. Write labels in the language of the user's request; keep technical terms and identifiers as they are.
2. **Choose the tool** (see below).
3. **Write the layout spec** as JSON, with `type`, kinds and labels first, without final sizes.
4. **Size from measurement.** Run the lint with `--sizes` to get the minimum box size for each label.
5. **Place and route** using the layout notes in the type file and the layout recipe below.
6. **Lint.** Run the script. Fix every `FAIL`, then run it again. Allow at most three rounds; if it still fails, simplify (shorter labels, fewer boxes, split into two diagrams) instead of shrinking fonts or loosening thresholds.
7. **Check what the script cannot.** Go through the criteria marked `you` in the type file and fix what fails.
8. **Emit** the diagram from the spec exactly: positions from the spec, and for every node and edge the shape, line and arrowheads that `--styles` prints. Do not adjust coordinates or styles by hand after the lint.
9. **Look at it when you can.** If the tool returns an image or the environment can rasterize the result, view it before sending. The lint is necessary, not sufficient.
10. **Report** in one line, in the user's language: the diagram type, how many checks passed, and which criteria you checked by eye or could not check for this tool.

Do not send a diagram with a known `FAIL` silently. If the user insists on something that fails a check, send it and name the failing check or criterion id.

## Choosing the tool

1. A tool the user names wins.
2. Otherwise use an explicit-coordinate tool (draw.io XML, SVG, a whiteboard with coordinates) and draw from the linted spec. This is the only path on which both the notation and the geometry are checked, so it is the default for all 15 types.
3. A diagram that needs interaction (click to highlight, step through) goes to an HTML widget.
4. An auto-layout grammar (Mermaid and similar) is for when the user asks for it or nothing else is available. It picks the symbols and the layout itself, so neither can be linted; say so in the report.

## Layout spec

Coordinates are absolute pixels, origin top-left. One spec per diagram.

| Level | Fields |
|---|---|
| top | `title`, `type` (required: a spec type from the table above), `direction` (`"LR"` or `"TB"`), `view_width` (px the diagram is displayed at: 800 by default, 680 for a 680-wide inline SVG), `view_height` (set it when the tool also limits height, 800 for draw.io inline), `canvas` `{w,h}`, `font_size` (default 14), `requested` (labels the user asked for, as they appear in the diagram), `thresholds` (overrides), `nodes`, `edges`, `texts`, `guides` |
| node | `id`, `kind` (required: an element of the type), `x`, `y`, `w`, `h`, `lines` (one string per rendered line, you break the lines; `---` starts a new compartment), `shape` (only to pick a non-default shape the kind allows), `of` (the participant an execution bar or destruction belongs to), `font_size`, `bold_first` (default true), `fill`, `text_color`, `fill_dark`, `text_dark`, `container`, `header_h`, `parent`, `hub`, `standalone`, `on_guide` |
| edge | `id`, `kind` (required: a relationship of the type), `from`, `to`, `points` (every corner of the route; first point on the source border, last on the target border), `label` (a string, or a list with one string per line), `label_box` `[x,y,w,h]`, `label_font_size`, `label_mask`, `line`, `head`, `tail` (only to pick a non-default value the kind allows), `back`, `anchor` (`"guide"` when the ends sit on lifelines instead of box borders) |
| text | `id`, `role` (`"title"`, `"legend"`, `"note"`, or a role of the type such as `"guard"`, `"operator"`, `"multiplicity"`, `"message"`), `x`, `y`, `w`, `h`, `lines`, `font_size` |
| guide | `id`, `of` (the node it belongs to), `points` (a lifeline, a timeline or a separator as a polyline) |

The kind decides how a thing is drawn. A reply is dashed with an open arrowhead because its kind is `reply`, so you never set that yourself; `--styles` prints the resolved shape, line and arrowheads for every node and edge.

Keep `canvas.w` at or below `view_width`, and `canvas.h` at or below `view_height` when it is set, so nothing is scaled down. If the content does not fit, split the diagram.

## Layout recipe

- **Grid first.** Give each box a column and a row so that boxes joined by an arrow sit in neighbouring cells. Most messy arrows are a placement problem, so move boxes before bending arrows.
- **Gutters.** Leave 40 to 60 px between columns and between rows. Arrows travel only in gutters, never under a box.
- **Sizes.** Column width is the widest box in the column; row height is the tallest box in the row. Use at least 120x50 for a box that holds text.
- **Routes.** Aligned neighbours get a straight arrow. Otherwise use an L or Z route with at most two bends. Put the last segment at least 20 px long so the arrowhead is visible.
- **Sharing a side.** Arrows that leave or enter the same side of a box use different anchor points at least 12 px apart.
- **Back edges.** At most two arrows may run against the main direction. Route them through the outer gutter and mark them `"back": true`.
- **Busy boxes.** A box with more than four arrows needs a hub or bus box (`"hub": true`) or a split diagram.
- **Edge labels.** Use the labels the type requires (guards, keywords such as «include», message names) and no others. Keep each to three words and place it in clear gutter space, with `label_box` when it should not sit on the middle of the line.
- **Labels in boxes.** A short title plus an optional subtitle, at most three lines (class-like boxes may hold more). Longer explanation belongs in the reply text.
- **Color.** UML diagrams use one neutral fill and no legend. A flowchart may use up to four fills by role, with a legend.

## Checks the script runs

Notation, from the type file:

| Id | Rule |
|---|---|
| N0 | `type` names a known diagram type |
| N1 | Every node has a `kind` that the type defines |
| N2 | Each node has a shape its kind allows, a label of the required form, and sits where its kind must or must not sit; texts with a role have the required form |
| N3 | Every edge has a `kind` that the type defines |
| N4 | Each edge has the line and arrowheads of its kind, the required keyword or label, and joins kinds it may join |
| N5 | The structural rules of the type hold (for example one start, guards on every decision exit, a reply after its call) |

N1 to N5 messages cite the criterion they enforce, for example `SEQ-05`; look it up in the type file.

Geometry and style, for every type:

| Id | Rule (default threshold) |
|---|---|
| T1 | Text fits inside 80% of the box width and height (less in diamonds, ellipses and other tapered shapes) |
| T2 | At most 3 lines per box, or the limit of its kind |
| T3 | Every font is at least 12 px after scaling to `view_width` and `view_height` |
| T4 | Warns when characters had to be measured by estimate |
| G1 | No overlapping boxes or text blocks; boxes at least 30 px apart |
| G2 | Everything at least 20 px inside the canvas |
| G3 | Boxes of a kind the type marks as uniform share one size |
| G4 | At most 15 boxes |
| G5 | Children sit inside their container with a 10 px margin |
| E1 | Every arrow has existing ends and an explicit route |
| E2 | Route starts and ends on the borders of its boxes (or on their lifelines) |
| E3 | No arrow through, or within 6 px of, another box |
| E4 | No arrow over a text block, container title or another arrow's label |
| E5 | No arrow crossings |
| E6 | No arrows on top of each other or closer than 12 px in parallel |
| E7 | At most 2 bends per arrow |
| E8 | Route at most 1.5 times the straight distance (back edges exempt) |
| E9 | At most 2 back edges |
| E10 | At most 4 arrows per box (hubs exempt) |
| E11 | Last segment at least 20 px |
| E12 | A label sits within 8 px of its own arrow and overlaps nothing; a sequence message label is centered over its arrow and stays between its two lifelines |
| E13 | No lifeline (guide) through a text block, an unmasked arrow label, or a box that is not on that lifeline |
| S1 | No unconnected box unless marked `standalone` |
| S2 | Every `requested` element appears |
| S4 | A title exists |
| S5 | A legend exists when fill colors differ, for types that use a legend (line styles need none: the kind fixes them) |
| S6 | At most 4 fill colors |
| S7 | Text to fill contrast at least 4.5:1 (dark pair too when given) |
| X1 | Ids are present and unique |

The script cannot judge four things, so check them yourself: the criteria marked `you` in the type file, labels in the user's language, arrow directions and order matching what the user described, and the rendered image when you can view it.

Change a threshold through `thresholds` only when the user asks for it, and say so in the reply.

## Running the script

The script ships with this skill as `scripts/diagram_lint.py`:

```bash
python3 "<this skill's base directory>/scripts/diagram_lint.py" spec.json --sizes    # minimum box sizes
python3 "<this skill's base directory>/scripts/diagram_lint.py" spec.json            # lint
python3 "<this skill's base directory>/scripts/diagram_lint.py" spec.json --styles   # shape, line and arrowheads to draw
python3 "<this skill's base directory>/scripts/diagram_lint.py" --types              # list the diagram types
```

Install Pillow (`pip install pillow`) if it is missing; without it the script falls back to conservative width estimates. Text is measured with the widest font available locally, which lands within about 8% of common UI fonts; the 80% fit rule absorbs that difference.

If no code can be run at all, go through every criterion of the type file by hand and apply the geometry table with these estimates: 0.62 em per Latin or Vietnamese character, 1.08 em per CJK character, 1.3 em per line. Tell the user the checks were done by hand.

## Emitting from the spec

`references/shapes.md` says what each shape, line and arrowhead word looks like and how to draw it. A shape the tool has no stencil for is built from rectangles, ellipses and lines; never substitute a plain box for it.

**draw.io XML.** Use the spec's `x`, `y`, `w`, `h` and font size for every vertex, with `whiteSpace=wrap;html=1` and the lines joined by `<br>` exactly as in `lines`. Children of a container use coordinates relative to the container. Draw each arrow with no `edgeStyle`, the interior route points as waypoints (`<Array as="points">`), `exitX/exitY/entryX/entryY` computed from the first and last point as a fraction of the box, and the line and arrowheads from `--styles`. Do not request automatic routing or layout, because they move what the lint approved. Draw an edge label as its own text cell at the linted `label_box`.

**Lifelines in draw.io.** Lifelines, timelines and the messages between them are edges with free end points (`sourcePoint` and `targetPoint`, no source or target cell). Draw lifelines first, then frames, then execution bars and notes, so they cover the lifeline behind them. Each label is its own text cell at the linted `label_box`, drawn last and with an opaque label background.

**Inline SVG.** Set `view_width` and `canvas.w` to the SVG's display width. One `<text>` or `<tspan>` per entry in `lines`; each arrow is a `<path>` through the route points with `fill="none"` and a marker for its arrowhead.

**HTML widget (browser layout).** Let the browser size the boxes (CSS grid, boxes grow with their text) and compute arrow coordinates at runtime from the boxes' real positions. Because the final geometry is not known in advance, keep the design inside what cannot go wrong: every arrow joins two boxes that are neighbours in the same row or column, gutters are at least 40 px, and there are no labels on arrows. Still lint a nominal spec for the notation and structure checks.

**Auto-layout grammars (Mermaid and similar).** Nothing can be linted. Use the grammar's own diagram keyword for the type, check the criteria of the type file against what the grammar will draw, and limit the input: at most 12 boxes, labels within 160 px measured by `--sizes`, line breaks placed by you, at most one back edge. Tell the user that the checks could not be run.

**A tool not listed here.** Classify it as explicit-coordinate, browser-layout or auto-layout and follow that family's rule.

## Click to highlight

When the user wants to click an arrow and see what it connects, build an HTML widget:

- Each arrow is an SVG group with a visible line and a transparent hit line at least 20 px wide.
- Clicking an arrow highlights the arrow and its two end boxes and dims everything else. Clicking a box highlights the box, its arrows and their other ends. Clicking again clears the selection.
- Show what the selected arrow carries in a detail line below the diagram instead of a label on the arrow.
- Make boxes and arrows reachable by keyboard (focusable, Enter or Space selects).

## When the user reports a defect

Reproduce it in the spec and name the criterion or check that should have caught it. If none covers it, say that this is a gap, then close it: add the criterion to the type file as `references/types/README.md` describes, so the same defect cannot pass again.

## Extending this skill

Criteria live in the type files, not in this file and not in the script. `references/types/README.md` explains the file format, the rule vocabulary, and the steps to add a criterion or a whole diagram type. After any change to a type file, run:

```bash
python3 "<this skill's base directory>/scripts/diagram_lint.py" --check-types
```
