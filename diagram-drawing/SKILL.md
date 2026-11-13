---
name: diagram-drawing
description: Use before drawing or editing any diagram (flowchart, architecture, process, sequence, org chart, mind map, sơ đồ) in any tool or language. Gives layout rules and a lint gate that stops clipped text and messy arrows.
---

# Diagram drawing

Use this skill for every box-and-arrow diagram, whatever tool draws it (draw.io, an inline SVG or HTML widget, Mermaid, FigJam, a whiteboard, anything connected later) and whatever language the labels are in. Charts of numeric data are out of scope; use a data visualization skill for those.

## Why this skill exists

You usually cannot see the diagram after you draw it. Guessing text width from character counts fails, most of all for accented scripts such as Vietnamese and for CJK, and letting a tool route arrows by itself gives paths you cannot inspect. The result is clipped labels and arrows that run through boxes and text. The fix is to stop guessing: describe the diagram as a layout spec with explicit geometry, measure it with a script, repair it until it passes, and only then hand it to the drawing tool unchanged.

On geometry, sizing and arrow routing this skill overrides a tool's own guidance (for example a tool that says "do not add waypoints"). The tool's guidance still governs its syntax, colors and theme.

## Workflow

1. **Inventory.** List the boxes, the arrows and every element the user named. Pick the diagram type and one main flow direction (`LR` or `TB`). Write labels in the language of the user's request; keep technical terms and identifiers as they are.
2. **Choose the tool** (see below).
3. **Write the layout spec** as JSON, labels first, without final sizes.
4. **Size from measurement.** Run the lint with `--sizes` to get the minimum box size for each label, then give every box of the same `kind` the largest size in that kind.
5. **Place and route** using the layout recipe below.
6. **Lint.** Run the script. Fix every `FAIL`, then run it again. Allow at most three rounds; if it still fails, simplify (shorter labels, fewer boxes, split into two diagrams) instead of shrinking fonts or loosening thresholds.
7. **Emit** the diagram from the spec exactly. Do not adjust coordinates by hand after the lint.
8. **Look at it when you can.** If the tool returns an image or the environment can rasterize the result, view it before sending. The lint is necessary, not sufficient.
9. **Report** in one line, in the user's language: how many checks passed and which checks could not be run for this tool.

Do not send a diagram with a known `FAIL` silently. If the user insists on something that fails a check, send it and name the failing check.

## Choosing the tool

1. A tool the user names wins.
2. Sequence, Gantt, ER, class, state, timeline and mind map diagrams go to an auto-layout grammar (Mermaid or a tool that accepts it). Their layouts are formulaic and boxes size themselves to the text.
3. A diagram that needs interaction (click to highlight, step through) goes to an HTML widget.
4. Everything else (flowchart, process, architecture, org chart) goes to an explicit-coordinate tool (draw.io XML, SVG, a whiteboard with coordinates) drawn from the linted spec.

## Layout spec

Coordinates are absolute pixels, origin top-left. One spec per diagram.

| Level | Fields |
|---|---|
| top | `title`, `type` (`"flow"` turns on the start-point check), `direction` (`"LR"` or `"TB"`), `view_width` (px the diagram is displayed at: 800 by default, 680 for a 680-wide inline SVG), `canvas` `{w,h}`, `font_size` (default 14), `requested` (labels the user asked for, as they appear in the diagram), `thresholds` (overrides), `nodes`, `edges`, `texts` |
| node | `id`, `x`, `y`, `w`, `h`, `lines` (one string per rendered line, you break the lines), `kind`, `font_size`, `bold_first` (default true), `fill`, `text_color`, `fill_dark`, `text_dark`, `container`, `header_h`, `parent`, `start`, `hub`, `standalone` |
| edge | `id`, `from`, `to`, `points` (every corner of the route; first point on the source border, last on the target border), `label`, `label_box` `[x,y,w,h]`, `label_font_size`, `style` (`"solid"` or `"dashed"`), `back` |
| text | `id`, `role` (`"title"`, `"legend"`, `"note"`), `x`, `y`, `w`, `h`, `lines`, `font_size` |

Keep `canvas.w` at or below `view_width` so nothing is scaled down. If the content does not fit, split the diagram.

## Layout recipe

- **Grid first.** Give each box a column and a row so that boxes joined by an arrow sit in neighbouring cells. Most messy arrows are a placement problem, so move boxes before bending arrows.
- **Gutters.** Leave 40 to 60 px between columns and between rows. Arrows travel only in gutters, never under a box.
- **Sizes.** Column width is the widest box in the column; row height is the tallest box in the row. Use at least 120x50 for a box.
- **Routes.** Aligned neighbours get a straight arrow. Otherwise use an L or Z route with at most two bends. Put the last segment at least 20 px long so the arrowhead is visible.
- **Sharing a side.** Arrows that leave or enter the same side of a box use different anchor points at least 12 px apart.
- **Back edges.** At most two arrows may run against the main direction. Route them through the outer gutter and mark them `"back": true`. For a loop, prefer a short note ("repeat until it passes") over a long return arrow.
- **Busy boxes.** A box with more than four arrows needs a hub or bus box (`"hub": true`) or a split diagram.
- **Edge labels.** Prefer none: put the meaning in the box subtitle, a legend or the prose. When a label is needed, keep it to three words and place it on the longest segment in clear gutter space.
- **Labels in boxes.** A short title plus an optional subtitle, at most three lines. Longer explanation belongs in the reply text.
- **Color.** At most four fill colors, the same color for the same kind of thing, and a one-line legend whenever there is more than one fill or line style. Do not let color alone carry meaning.

## Checks the script runs

| Id | Rule (default threshold) |
|---|---|
| T1 | Text fits inside 80% of the box width and height |
| T2 | At most 3 lines per box |
| T3 | Every font is at least 12 px after scaling to `view_width` |
| T4 | Warns when characters had to be measured by estimate |
| G1 | No overlapping boxes or text blocks; boxes at least 30 px apart |
| G2 | Everything at least 20 px inside the canvas |
| G3 | Boxes of one `kind` share one size |
| G4 | At most 15 boxes |
| G5 | Children sit inside their container with a 10 px margin |
| E1 | Every arrow has existing ends and an explicit route |
| E2 | Route starts and ends on the borders of its boxes |
| E3 | No arrow through, or within 6 px of, another box |
| E4 | No arrow over a text block, container title or another arrow's label |
| E5 | No arrow crossings |
| E6 | No arrows on top of each other or closer than 12 px in parallel |
| E7 | At most 2 bends per arrow |
| E8 | Route at most 1.5 times the straight distance (back edges exempt) |
| E9 | At most 2 back edges |
| E10 | At most 4 arrows per box (hubs exempt) |
| E11 | Last segment at least 20 px |
| E12 | A label sits on its own arrow and overlaps nothing |
| S1 | No unconnected box unless marked `standalone` |
| S2 | Every `requested` element appears |
| S3 | Decisions have at least 2 labeled exits; a flow has a start |
| S4 | A title exists |
| S5 | A legend exists when fills or line styles differ |
| S6 | At most 4 fill colors |
| S7 | Text to fill contrast at least 4.5:1 (dark pair too when given) |
| X1 | Ids are present and unique |

The script cannot judge three things, so check them yourself: labels are in the user's language, arrow directions and order match what the user described, and the rendered image looks right when you can view it.

Change a threshold through `thresholds` only when the user asks for it, and say so in the reply.

## Running the script

The script ships with this skill as `scripts/diagram_lint.py`:

```bash
python3 "<this skill's base directory>/scripts/diagram_lint.py" spec.json --sizes
python3 "<this skill's base directory>/scripts/diagram_lint.py" spec.json
```

Install Pillow (`pip install pillow`) if it is missing; without it the script falls back to conservative width estimates. Text is measured with the widest font available locally, which lands within about 8% of common UI fonts; the 80% fit rule absorbs that difference.

If no code can be run at all, apply the table by hand with these estimates: 0.62 em per Latin or Vietnamese character, 1.08 em per CJK character, 1.3 em per line, and tell the user the checks were estimated.

## Emitting from the spec

**draw.io XML.** Use the spec's `x`, `y`, `w`, `h` and font size for every vertex, with `whiteSpace=wrap;html=1` and the lines joined by `<br>` exactly as in `lines`. Children of a container use coordinates relative to the container. Draw each arrow with no `edgeStyle`, the interior route points as waypoints (`<Array as="points">`), and `exitX/exitY/entryX/entryY` computed from the first and last point as a fraction of the box. Do not request automatic routing or layout, because they move what the lint approved. Draw an edge label as its own text cell at the linted `label_box`.

**Inline SVG.** Set `view_width` and `canvas.w` to the SVG's display width. One `<text>` or `<tspan>` per entry in `lines`; each arrow is a `<path>` through the route points with `fill="none"`.

**HTML widget (browser layout).** Let the browser size the boxes (CSS grid, boxes grow with their text) and compute arrow coordinates at runtime from the boxes' real positions. Because the final geometry is not known in advance, keep the design inside what cannot go wrong: every arrow joins two boxes that are neighbours in the same row or column, gutters are at least 40 px, and there are no labels on arrows. Still lint a nominal spec for the structure checks.

**Auto-layout grammars (Mermaid and similar).** Geometry cannot be linted. Limit the input instead: at most 12 boxes, labels within 160 px measured by `--sizes`, line breaks placed by you, at most one back edge, and about as many arrows as boxes. Tell the user that the geometry checks could not be run.

**A tool not listed here.** Classify it as explicit-coordinate, browser-layout or auto-layout and follow that family's rule.

## Click to highlight

When the user wants to click an arrow and see what it connects, build an HTML widget:

- Each arrow is an SVG group with a visible line and a transparent hit line at least 20 px wide.
- Clicking an arrow highlights the arrow and its two end boxes and dims everything else. Clicking a box highlights the box, its arrows and their other ends. Clicking again clears the selection.
- Show what the selected arrow carries in a detail line below the diagram instead of a label on the arrow.
- Make boxes and arrows reachable by keyboard (focusable, Enter or Space selects).

## When the user reports a defect

Reproduce it in the spec and name the check that should have caught it. If no check covers it, say that this is a gap in the lint so the user can decide to extend this skill.
