# Shapes, lines and arrowheads

The words a spec and a type file use for symbols, and how to draw each one. Run the lint with `--styles` to get, for every node and edge of a spec, the shape, line and arrowheads its kind requires; draw exactly those.

The draw.io column gives style keys taken from the draw.io reference. Where it says "primitives", build the symbol from rectangles, ellipses and lines as described, or use the tool's own shape once you have confirmed its name in the tool's documentation. A guessed shape name that the tool does not know renders as a plain rectangle, which silently turns the diagram into the wrong notation.

## Shapes

| `shape` | Looks like | draw.io |
|---|---|---|
| `rect` | rectangle with square corners | default vertex |
| `rounded` | rectangle with rounded corners | `rounded=1` (states: `rounded=1;arcSize=40`) |
| `pill` | stadium: rectangle whose short sides are half circles | `rounded=1;arcSize=50` |
| `ellipse` | ellipse | `ellipse` |
| `diamond` | diamond | `rhombus` |
| `cylinder` | upright cylinder | `shape=cylinder3` |
| `document` | rectangle with a wavy base | `shape=mxgraph.flowchart.document` |
| `actor` | stick figure, the name below it | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top` |
| `dot` | small solid circle, 16 to 20 px | `ellipse;fillColor=#000000;strokeColor=none` |
| `bullseye` | small solid circle inside a ring, about 24 px | `ellipse;shape=endState;fillColor=#000000` |
| `lane` | swimlane: a band with its name in a box at one end | `swimlane;horizontal=0;startSize=...` |
| `compartments` | rectangle split by horizontal lines; a line `---` in `lines` starts the next compartment | primitives: a rectangle, one line per separator, one text cell per compartment |
| `parallelogram` | rectangle slanted to the right | primitives |
| `subroutine` | rectangle with a second vertical line just inside each short side | primitives: a rectangle and two lines |
| `hexagon` | elongated hexagon, pointed left and right | primitives |
| `manual-input` | quadrilateral whose top edge slopes up from left to right | primitives |
| `trapezoid` | trapezoid with the longer side on top | primitives |
| `pentagon` | home plate: rectangle with a point at the bottom | primitives |
| `signal-send` | rectangle with a point on its right side | primitives |
| `signal-accept` | rectangle with a notch cut into its left side | primitives |
| `hourglass` | two triangles meeting at their tips | primitives |
| `bracket` | open rectangle: the left, top and bottom sides only | primitives: three lines |
| `circle` | small circle holding a letter or name, 24 to 30 px | `ellipse` |
| `circle-x` | small circle with an X through it | primitives: an ellipse and two lines |
| `x` | an X of two crossing lines, about 20 px | primitives: two lines |
| `bar` | thick straight bar, about 6 px by the length needed | a rectangle filled with the line color |
| `note` | rectangle with its top-right corner folded | primitives |
| `folder` | rectangle with a small tab on the left of its top edge | primitives: two rectangles |
| `cube` | three-dimensional box: a rectangle with a top face and a side face | primitives |
| `component` | rectangle with the component icon (a small rectangle with two smaller ones on its left side) in the top-right corner | primitives |
| `frame` | rectangle with a heading compartment in its top-left corner whose lower-right corner is cut off | primitives: a rectangle, a pentagon outline and a text cell |
| `port` | small square, about 12 px, centred on the border of its owner | a small rectangle |
| `lollipop` | small circle at the end of a short line | an ellipse and a line |
| `socket` | half circle, open away from its owner, at the end of a short line | primitives: an arc and a line |
| `dashed-ellipse` | ellipse with a dashed outline | `ellipse;dashed=1` |
| `dashed-rect` | rectangle with a dashed outline | `dashed=1` |
| `band` | wide horizontal band with its name at the left | a rectangle, or `swimlane;horizontal=0` |
| `text` | text only, no outline | `text;strokeColor=none;fillColor=none` |

Symbols without text (`dot`, `bullseye`, `circle-x`, `x`, `bar`) take `"lines": []`. Whatever needs saying goes on a flow, in a note, or beside the symbol as a text block.

## Lines

| `line` | Looks like | draw.io |
|---|---|---|
| `solid` | continuous line | default |
| `dashed` | dashed line | `dashed=1` |

## Arrowheads

`head` is the end at `to`, `tail` the end at `from`.

| Value | Looks like | draw.io (`endArrow` for head, `startArrow` for tail) |
|---|---|---|
| `none` | plain line end | `endArrow=none` |
| `open` | two strokes forming an open V | `endArrow=open` |
| `filled` | solid triangle | `endArrow=block;endFill=1` |
| `hollow` | hollow triangle | `endArrow=block;endFill=0` |
| `diamond` | solid diamond | `startArrow=diamondThin;startFill=1` |
| `hollow-diamond` | hollow diamond | `startArrow=diamondThin;startFill=0` |
| `dot` | small solid circle | `endArrow=oval;endFill=1` |
| `x` | small x across the line end | primitives: two short lines |
| `circle-plus` | small circle with a plus in it | primitives: an ellipse and two short lines |

Keep arrowheads small on sequence messages (`endSize=6`).

## Sources

The draw.io keys in this file come from the draw.io diagram generation reference returned by the draw.io connector (styles, arrowheads, state, use case and class diagram notes). Shapes marked "primitives" have draw.io stencils of their own, but their names were not confirmed for this file.
