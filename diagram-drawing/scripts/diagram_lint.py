#!/usr/bin/env python3
"""diagram_lint.py: lint a diagram layout spec (JSON) before it is drawn.
Usage: python3 diagram_lint.py spec.json [--sizes] [--styles] [--json]
       python3 diagram_lint.py --types          list the diagram types
       python3 diagram_lint.py --check-types    validate every type file
Exit code 0 = no FAIL, 1 = at least one FAIL, 2 = bad input."""
import json, math, os, re, sys, unicodedata
from itertools import combinations

T = dict(fit=0.80, max_lines=3, min_font=12, view_w=800, margin=20, gap=30,
         child_margin=10, max_nodes=15, max_bends=2, detour=1.5, max_back=2,
         max_degree=4, par_gap=12, last_seg=20, max_fills=4, contrast=4.5,
         node_clear=6, text_clear=4, label_dist=8, anchor_tol=6, line_h=1.3,
         label_font=12, header_h=28, head_gap=16, bar_half=5)
TYPES_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references', 'types'))
SHAPES = {
    'rect': 1, 'rounded': 1, 'pill': .85, 'ellipse': .85, 'diamond': .6, 'parallelogram': .75, 'hexagon': .75,
    'document': .75, 'subroutine': .8, 'manual-input': .8, 'trapezoid': .75, 'cylinder': .7, 'circle': .7,
    'pentagon': .75, 'signal-send': .75, 'signal-accept': .75, 'hourglass': 1, 'bracket': 1, 'dot': 1,
    'bullseye': 1, 'circle-x': 1, 'x': 1, 'bar': 1, 'actor': 1, 'note': .85, 'folder': .85, 'cube': .85,
    'component': .85, 'compartments': 1, 'frame': 1, 'port': 1, 'lollipop': 1, 'socket': 1,
    'dashed-ellipse': .7, 'dashed-rect': 1, 'lane': 1, 'band': 1, 'text': 1}
LINES = ('solid', 'dashed')
ENDS = ('none', 'open', 'filled', 'hollow', 'diamond', 'hollow-diamond', 'dot', 'x', 'circle-plus')
EDGE_DEFAULT = {'line': 'solid', 'head': 'none', 'tail': 'none'}
BASES = ('standard', 'convention')
CRIT = re.compile(r'^\|\s*([A-Z]+-\d+)\s*\|.*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*$', re.M)

try:
    from PIL import ImageFont
except Exception:
    ImageFont = None

FONT_DIRS = ['/usr/share/fonts', '/usr/local/share/fonts', '~/.fonts',
             '~/.local/share/fonts', '/System/Library/Fonts', '/Library/Fonts',
             'C:/Windows/Fonts']
WANT = {
    ('L', 0): ['DejaVuSans.ttf', 'Inter-Regular.otf', 'Arial.ttf', 'arial.ttf'],
    ('L', 1): ['DejaVuSans-Bold.ttf', 'Inter-Bold.otf', 'Arial Bold.ttf', 'arialbd.ttf'],
    ('W', 0): ['NotoSansCJK-Regular.ttc', 'NotoSansCJKsc-Regular.otf', 'PingFang.ttc', 'msyh.ttc', 'ipag.ttf'],
    ('W', 1): ['NotoSansCJK-Bold.ttc', 'NotoSansCJKsc-Bold.otf', 'msyhbd.ttc'],
}
_files, _fonts = None, {}

def font_files():
    global _files
    if _files is None:
        _files = {}
        for d in FONT_DIRS:
            for root, _, names in os.walk(os.path.expanduser(d)):
                for n in names:
                    _files.setdefault(n, os.path.join(root, n))
    return _files

def fonts_for(cls, bold, size):
    key = (cls, bold, size)
    if key not in _fonts:
        out = []
        if ImageFont:
            names = WANT.get((cls, bold)) or []
            if not any(n in font_files() for n in names):
                names = WANT[(cls, 0)]
            for n in names:
                p = font_files().get(n)
                if p:
                    try:
                        out.append(ImageFont.truetype(p, size))
                    except Exception:
                        pass
        _fonts[key] = out
    return _fonts[key]

def char_class(ch):
    o = ord(ch)
    if unicodedata.east_asian_width(ch) in 'WF':
        return 'W'
    if o < 0x530 or 0x1E00 <= o < 0x2000 or 0x2000 <= o < 0x2070 or 0x2190 <= o < 0x2200:
        return 'L'
    return 'U'

def measure(text, size, bold=False):
    """Return (width_px, estimated_chars). Widest available font wins, so the result is conservative."""
    text = unicodedata.normalize('NFC', text)
    width, est, run, cls = 0.0, 0, '', None

    def flush():
        nonlocal width, est
        if not run:
            return
        fs = fonts_for(cls, 1 if bold else 0, size) if cls in 'LW' else []
        if fs:
            width += max(f.getlength(run) for f in fs) * (1.08 if cls == 'W' else 1.0)
        else:
            width += sum((1.0 if c == 'W' else 0.62) * size for c in map(char_class, run)) * (1.08 if bold else 1)
            est += len(run)

    for ch in text:
        c = char_class(ch)
        if c != cls:
            flush()
            run, cls = '', c
        run += ch
    flush()
    return width, est

def text_size(lines, size, bold_first=False):
    w, est = 0.0, 0
    for i, ln in enumerate(lines):
        lw, e = measure(ln, size, bold_first and i == 0)
        w, est = max(w, lw), est + e
    return w, len(lines) * size * T['line_h'], est

def rect(o):
    return (o['x'], o['y'], o['x'] + o['w'], o['y'] + o['h'])

def grow(r, d):
    return (r[0] - d, r[1] - d, r[2] + d, r[3] + d)

def overlap(a, b):
    return min(a[2], b[2]) - max(a[0], b[0]) > 0.5 and min(a[3], b[3]) - max(a[1], b[1]) > 0.5

def rect_gap(a, b):
    dx = max(a[0] - b[2], b[0] - a[2], 0)
    dy = max(a[1] - b[3], b[1] - a[3], 0)
    return math.hypot(dx, dy)

def seg_in_rect(p, q, r):
    """Length of segment p-q inside rect r (Liang-Barsky)."""
    t0, t1, dx, dy = 0.0, 1.0, q[0] - p[0], q[1] - p[1]
    for pp, qq in ((-dx, p[0] - r[0]), (dx, r[2] - p[0]), (-dy, p[1] - r[1]), (dy, r[3] - p[1])):
        if abs(pp) < 1e-9:
            if qq < 0:
                return 0.0
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
    return max(0.0, t1 - t0) * math.hypot(dx, dy)

def seg_cross(a, b, c, d):
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if abs(den) < 1e-9:
        return False
    t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
    u = ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) / den
    e = 1e-6
    return (e < t < 1 - e and -e <= u <= 1 + e) or (e < u < 1 - e and -e <= t <= 1 + e)

def boundary_dist(p, r):
    inside = r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]
    if inside:
        return min(p[0] - r[0], r[2] - p[0], p[1] - r[1], r[3] - p[1]), True
    return math.hypot(max(r[0] - p[0], 0, p[0] - r[2]), max(r[1] - p[1], 0, p[1] - r[3])), False

def point_seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)

def rect_seg_dist(r, a, b):
    if seg_in_rect(a, b, r) > 0:
        return 0.0
    corners = [(r[0], r[1]), (r[2], r[1]), (r[0], r[3]), (r[2], r[3])]
    return min([point_seg_dist(c, a, b) for c in corners] + [boundary_dist(p, r)[0] for p in (a, b)])

def as_lines(v):
    return v if isinstance(v, list) else [v]

def simplify(pts):
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = out[-1], pts[i], pts[i + 1]
        if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) > 1e-6:
            out.append(b)
    out.append(pts[-1])
    return out

def luminance(hexc):
    h = hexc.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    v = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    v = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

def list_types():
    if not os.path.isdir(TYPES_DIR):
        return []
    return sorted(f[:-3] for f in os.listdir(TYPES_DIR) if f.endswith('.md') and f != 'README.md' and not f.startswith('_'))

def load_type(tid):
    """Read references/types/<tid>.md. Its first ```json block holds the rules. Returns (rules, error)."""
    path = os.path.join(TYPES_DIR, f'{tid}.md')
    if not tid or not os.path.isfile(path):
        return None, f'no type file for {tid!r}; set "type" to one of: {", ".join(list_types())}'
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    m = re.search(r'```json\s*\n(.*?)\n```', txt, re.S)
    if not m:
        return None, f'{tid}.md has no json rules block'
    try:
        rules = json.loads(m.group(1))
    except ValueError as ex:
        return None, f'{tid}.md rules are not valid JSON: {ex}'
    rules['_own'] = {i: (basis, chk) for i, basis, chk in CRIT.findall(txt)}
    rules['_criteria'] = dict(rules['_own'])
    rules['_rows'] = {m.group(1): m.group(0).strip() for m in re.finditer(r'^\|\s*([A-Z]+-\d+)\s*\|.*$', txt, re.M)}
    return rules, None

def node_shape(n, rules):
    d = (rules or {}).get('nodes', {}).get(n.get('kind')) or {}
    return n.get('shape') or (d.get('shapes') or ['rect'])[0]

def edge_style(e, rules):
    d = (rules or {}).get('edges', {}).get(e.get('kind')) or {}
    return {f: e.get(f, e.get('style') if f == 'line' else None) or as_lines(d.get(f, EDGE_DEFAULT[f]))[0] for f in EDGE_DEFAULT}

def notation(rules, add, nodes, edges, texts, GD):
    """Checks N1-N5: the spec uses only this type's elements, drawn and connected the way its type file says."""
    nd, ed, td, name = rules.get('nodes', {}), rules.get('edges', {}), rules.get('texts', {}), rules.get('name', rules['id'])
    closed = f'{rules["rule_kinds"]}: ' if rules.get('rule_kinds') else ''
    tag = lambda d, key='rule': f'{d[key]}: ' if d.get(key) else ''
    words = lambda v: ' '.join(as_lines(v or ''))
    a = lambda k: f'{"an" if k[:1] in "aeio" else "a"} {k}'
    pairs = lambda ps: ' or '.join(f'two {p[0]}s' if len(p) == 1 else f'{a(p[0])} and {a(p[1])}' for p in ps)
    kind = {}
    for n in nodes:
        if n.get('kind') in nd:
            kind[n['id']] = n['kind']
        else:
            add('FAIL', 'N1', n['id'], f'{closed}kind {n.get("kind")!r} is not an element of {a(name)}; use one of: {", ".join(sorted(nd))}')

    def holders(n, kinds):
        cx, cy = n['x'] + n['w'] / 2, n['y'] + n['h'] / 2
        return [m['id'] for m in nodes if m is not n and kind.get(m['id']) in kinds
                and m['x'] <= cx <= m['x'] + m['w'] and m['y'] <= cy <= m['y'] + m['h']]

    for n in nodes:
        k = kind.get(n['id'])
        if not k:
            continue
        d, label, shape = nd[k], words(n.get('lines')), node_shape(n, rules)
        if shape not in d['shapes']:
            add('FAIL', 'N2', n['id'], f'{tag(d)}{a(k)} is drawn as {" or ".join(d["shapes"])}, the spec says {shape}')
        want = (d.get('label_by_shape') or {}).get(shape, d.get('label'))
        if want and not re.search(want, label, re.I):
            add('FAIL', 'N2', n['id'], f'{tag(d)}label {label!r} of {a(k)} must look like {d.get("hint", want)}')
        if d.get('text') is False and label.strip():
            add('FAIL', 'N2', n['id'], f'{tag(d)}{a(k)} symbol carries no text; put the words on a flow or in a note')
        if d.get('inside') and not holders(n, d['inside']):
            add('FAIL', 'N2', n['id'], f'{tag(d)}{a(k)} sits inside {" or ".join(a(x) for x in d["inside"])}')
        if d.get('not_inside') and holders(n, d['not_inside']):
            add('FAIL', 'N2', n['id'], f'{tag(d)}{a(k)} stays outside {holders(n, d["not_inside"])[0]}')
    for t in texts:
        d = td.get(t.get('role'))
        if d and d.get('label') and not re.search(d['label'], words(t.get('lines')), re.I):
            add('FAIL', 'N2', t['id'], f'{tag(d)}{t["role"]} text {words(t.get("lines"))!r} must look like {d.get("hint", d["label"])}')
    out, inc = {}, {}
    for e in edges:
        k, d = e.get('kind'), ed.get(e.get('kind'))
        out.setdefault(e.get('from'), []).append(e)
        inc.setdefault(e.get('to'), []).append(e)
        if d is None:
            add('FAIL', 'N3', e['id'], f'{closed}kind {k!r} is not a relationship of {a(name)}; use one of: {", ".join(sorted(ed))}')
            continue
        for f in EDGE_DEFAULT:
            ok, got = as_lines(d.get(f, EDGE_DEFAULT[f])), e.get(f, e.get('style') if f == 'line' else None)
            if got is not None and got not in ok:
                add('FAIL', 'N4', e['id'], f'{tag(d)}{a(k)} has {f} {" or ".join(ok)}, the spec says {got}')
        if d.get('label') and not re.search(d['label'], words(e.get('label')), re.I):
            add('FAIL', 'N4', e['id'], f'{tag(d)}{a(k)} is labelled like {d.get("hint", d["label"])}, the spec says {words(e.get("label"))!r}')
        sk, tk = kind.get(e.get('from')), kind.get(e.get('to'))
        if sk and tk:
            if d.get('from') and sk not in d['from']:
                add('FAIL', 'N4', e['id'], f'{tag(d)}{a(k)} starts at {" or ".join(a(x) for x in d["from"])}, not at {a(sk)}')
            if d.get('to') and tk not in d['to']:
                add('FAIL', 'N4', e['id'], f'{tag(d)}{a(k)} ends at {" or ".join(a(x) for x in d["to"])}, not at {a(tk)}')
            if d.get('between') and not any({sk, tk} == set(p) for p in d['between']):
                add('FAIL', 'N4', e['id'], f'{tag(d, "rule_between") or tag(d)}{a(k)} joins {pairs(d["between"])}, not {a(sk)} and {a(tk)}')
            if d.get('touches') and not {sk, tk} & set(d['touches']):
                add('FAIL', 'N4', e['id'], f'{tag(d)}one end of {a(k)} is {" or ".join(a(x) for x in d["touches"])}')

    of_kinds = lambda ks: [n for n in nodes if kind.get(n['id']) in ks]

    def span(c):
        lo, hi = c.get('min', 0), c.get('max')
        if hi is None:
            return f'at least {lo}'
        return ('no' if hi == 0 else f'exactly {lo}') if lo == hi else f'at most {hi}' if lo == 0 else f'{lo} to {hi}'
    within = lambda c, v: c.get('min', 0) <= v <= c.get('max', 10 ** 9)
    leaves = [n for n in nodes if not n.get('container') and n['id'] in kind]

    def walk(starts, table, end):
        seen, todo = set(starts), list(starts)
        while todo:
            for e in table.get(todo.pop(), []):
                if e.get(end) not in seen:
                    seen.add(e.get(end))
                    todo.append(e.get(end))
        return seen

    for c in rules.get('checks', []):
        r, ch = (f'{c["rule"]}: ' if c.get('rule') else ''), c['check']
        if ch == 'count':
            groups = {None: []}
            for n in of_kinds(c['kinds']):
                if c.get('where') == 'no_in' and inc.get(n['id']) or c.get('where') == 'no_out' and out.get(n['id']):
                    continue
                groups.setdefault(n.get('parent') if c.get('per') == 'parent' else None, []).append(n)
            for g, ns in groups.items():
                if not within(c, len(ns)):
                    add('FAIL', 'N5', g or 'diagram', f'{r}{len(ns)} {c.get("what", "/".join(c["kinds"]))}, expected {span(c)}')
        elif ch == 'degree':
            for n in of_kinds(c['kinds']):
                es = [e for e in (out if c['dir'] == 'out' else inc).get(n['id'], []) if not c.get('edge_kinds') or e.get('kind') in c['edge_kinds']]
                if not within(c, len(es)):
                    add('FAIL', 'N5', n['id'], f'{r}{a(kind[n["id"]])} has {span(c)} flow(s) going {c["dir"]}, this one has {len(es)}')
        elif ch == 'not_both':
            for n in of_kinds(c['kinds']):
                if inc.get(n['id']) and out.get(n['id']):
                    add('FAIL', 'N5', n['id'], f'{r}{a(kind[n["id"]])} either starts or ends the flow; this one has flow both in and out')
        elif ch == 'edge_labels':
            for n in of_kinds(c['kinds']):
                es = (inc if c.get('dir') == 'in' else out).get(n['id'], [])
                bad = [e['id'] for e in es if not re.search(c['pattern'], words(e.get('label')), re.I)]
                if bad:
                    add('FAIL', 'N5', n['id'], f'{r}every flow {"entering" if c.get("dir") == "in" else "leaving"} {a(kind[n["id"]])} is labelled like {c.get("hint", c["pattern"])}; fix {", ".join(bad)}')
                if c.get('at_most_one') and sum(bool(re.search(c['at_most_one'], words(e.get('label')), re.I)) for e in es) > 1:
                    add('FAIL', 'N5', n['id'], f'{r}more than one exit is labelled {c.get("one_hint", c["at_most_one"])}')
        elif ch == 'operand_guards':
            for n in of_kinds(c['kinds']):
                if not words(n.get('lines')).strip():
                    continue
                bad = [e['id'] for e in out.get(n['id'], []) if not re.search(c['pattern'], words(e.get('label')), re.I)]
                if bad:
                    add('FAIL', 'N5', n['id'], f'{r}the text in {a(kind[n["id"]])} is the left operand its guards share, so each guard holds only the rest, '
                        f'like {c.get("hint", c["pattern"])}; fix {", ".join(bad)}')
        elif ch in ('reachable', 'reaches'):
            fwd = ch == 'reachable'
            ends = [n['id'] for n in of_kinds(c['kinds']) if not (inc if fwd else out).get(n['id'])]
            seen = walk(ends, out if fwd else inc, 'to' if fwd else 'from')
            for n in leaves:
                if n['id'] not in seen and kind[n['id']] not in c.get('skip_kinds', []) and not n.get('standalone'):
                    add('FAIL', 'N5', n['id'], f'{r}{"cannot be reached from" if fwd else "cannot reach"} {a(c.get("what", "/".join(c["kinds"])))}')
        elif ch == 'paired_labels':
            seen = {}
            for n in of_kinds(c['kinds']):
                seen.setdefault(words(n.get('lines')), []).append(n['id'])
            for label, ns in seen.items():
                if len(ns) < 2 or (c.get('exact', True) and len(ns) != 2):
                    add('FAIL', 'N5', ns[0], f'{r}label {label!r} is on {len(ns)} {"/".join(c["kinds"])}(s); a jump needs a matching partner')
        elif ch == 'text_in':
            for n in of_kinds(c['kinds']):
                got = [t for t in texts if t.get('role') == c['role'] and n['x'] <= t['x'] + t['w'] / 2 <= n['x'] + n['w']
                       and n['y'] <= t['y'] + t['h'] / 2 <= n['y'] + n['h']]
                if not within(c, len(got)):
                    add('FAIL', 'N5', n['id'], f'{r}{a(kind[n["id"]])} holds {span(c)} text(s) with role "{c["role"]}", this one has {len(got)}')
        elif ch == 'unique_texts':
            seen = {}
            for t in texts:
                if t.get('role') == c['role']:
                    m = re.match(c.get('key', '.*'), words(t.get('lines')))
                    key = (m.group(0) if m else words(t.get('lines'))).strip()
                    seen.setdefault(key, []).append(t['id'])
            for key, ts in seen.items():
                if len(ts) > 1:
                    add('FAIL', 'N5', '/'.join(ts), f'{r}{c["role"]} {key!r} is used {len(ts)} times')
        elif ch == 'has_guide':
            for n in of_kinds(c['kinds']):
                if n['id'] not in GD:
                    add('FAIL', 'N5', n['id'], f'{r}{a(kind[n["id"]])} needs its line: add a guide with "of": "{n["id"]}"')
        elif ch == 'sequence':
            R = lambda key: f'{c["rules"][key]}: ' if c.get('rules', {}).get(key) else ''
            msgs = [e for e in edges if e.get('anchor') == 'guide' and len(e.get('points') or []) >= 2]
            bars = of_kinds(['execution'])
            for b in bars:
                g = GD.get(b.get('of'))
                if not g or not b.get('on_guide'):
                    add('FAIL', 'N5', b['id'], f'{R("execution")}an execution bar needs "of": <its lifeline head> and "on_guide": true')
                elif abs(b['x'] + b['w'] / 2 - g['points'][0][0]) > b['w']:
                    add('FAIL', 'N5', b['id'], f'{R("execution")}execution bar is not on the lifeline of {b["of"]}')
            for e in msgs:
                pts = e['points']
                if any(q[1] < p[1] - 0.5 for p, q in zip(pts, pts[1:])):
                    add('FAIL', 'N5', e['id'], f'{R("downward")}a message line runs horizontally or downward, never upward')
                if e.get('kind') == 'sync' and not any(b.get('of') == e.get('to') and b['y'] - 1 <= pts[-1][1] <= b['y'] + b['h'] + 1 for b in bars):
                    add('FAIL', 'N5', e['id'], f'{R("activation")}a synchronous call ends on an execution bar of {e.get("to")}')
                if e.get('kind') == 'reply' and not any(m.get('kind') == 'sync' and m.get('from') == e.get('to') and m.get('to') == e.get('from')
                                                         and m['points'][0][1] < pts[0][1] for m in msgs):
                    add('FAIL', 'N5', e['id'], f'{R("reply")}a reply answers an earlier synchronous call from {e.get("to")} to {e.get("from")}; none is drawn above it')
            for x in of_kinds(['destruction']):
                for e in msgs:
                    for p, who in ((e['points'][0], e.get('from')), (e['points'][-1], e.get('to'))):
                        if who == x.get('of') and p[1] > x['y'] + x['h'] + 0.5:
                            add('FAIL', 'N5', e['id'], f'{R("destruction")}nothing happens on the lifeline of {who} below its destruction X')

CHECKS = ('count', 'degree', 'not_both', 'edge_labels', 'operand_guards', 'reachable', 'reaches', 'paired_labels', 'text_in', 'unique_texts', 'has_guide', 'sequence')

def check_types():
    """Validate every type file: the rules parse, use known words, and agree with the criteria table."""
    names = sorted(f[:-3] for f in os.listdir(TYPES_DIR) if f.endswith('.md') and f != 'README.md') if os.path.isdir(TYPES_DIR) else []
    bad, wording = 0, {}
    for tid in names:
        rules, err = load_type(tid)
        for i, row in ((rules or {}).get('_rows') or {}).items():
            wording.setdefault(i, {}).setdefault(row, []).append(tid)
        p = [err] if err else []
        if rules:
            nd, used = rules.get('nodes', {}), {rules.get('rule_kinds')} | set(rules.get('generic', {}))
            if rules.get('id') != tid:
                p.append(f'"id" is {rules.get("id")!r}, the file is {tid}.md')
            missing = lambda ks: [k for k in ks if k not in nd]
            for k, d in nd.items():
                used |= {d.get('rule')}
                p += [f'node {k}: unknown shape {s}' for s in d.get('shapes', []) if s not in SHAPES] + ([] if d.get('shapes') else [f'node {k}: no shapes'])
                p += [f'node {k}: unknown kind {x} in inside/not_inside' for x in missing(d.get('inside', []) + d.get('not_inside', []))]
            for k, d in rules.get('edges', {}).items():
                used |= {d.get('rule'), d.get('rule_between')}
                for f, vocab in (('line', LINES), ('head', ENDS), ('tail', ENDS)):
                    p += [f'edge {k}: unknown {f} {v}' for v in as_lines(d.get(f, [])) if v not in vocab]
                ends = d.get('from', []) + d.get('to', []) + d.get('touches', []) + [x for pair in d.get('between', []) for x in pair]
                p += [f'edge {k}: unknown node kind {x}' for x in missing(ends)]
            for d in rules.get('texts', {}).values():
                used |= {d.get('rule')}
            for c in rules.get('checks', []):
                used |= {c.get('rule')} | set((c.get('rules') or {}).values())
                if c.get('check') not in CHECKS:
                    p.append(f'unknown check {c.get("check")!r}')
                p += [f'check {c.get("check")}: unknown node kind {x}' for x in missing(c.get('kinds', []) + c.get('skip_kinds', []))]
            for sec in ('nodes', 'edges', 'texts'):
                for k, d in rules.get(sec, {}).items():
                    for rx in [d.get('label')] + list((d.get('label_by_shape') or {}).values()):
                        try:
                            re.compile(rx or '')
                        except re.error as ex:
                            p.append(f'{sec} {k}: bad pattern {rx!r}: {ex}')
            used.discard(None)
            p += [f'rule {u} is used in the rules but is not a row of a criteria table' for u in sorted(used - set(rules['_criteria']))]
            for i, (basis, chk) in sorted(rules['_own'].items()):
                if basis not in BASES or chk not in ('script', 'you'):
                    p.append(f'{i}: the last two columns must be standard|convention and script|you')
                elif chk == 'script' and i not in used:
                    p.append(f'{i} is marked script but no rule enforces it')
                elif chk == 'you' and i in used:
                    p.append(f'{i} is enforced by a rule but marked you')
            if not rules['_own']:
                p.append('no criteria table rows')
        bad += bool(p)
        print(f'{"FAIL" if p else "ok  "} {tid}' + ''.join(f'\n     {x}' for x in p))
    for i, rows in sorted(wording.items()):
        if len(rows) > 1:
            bad += 1
            print(f'FAIL {i} is worded differently in: ' + ' | '.join(', '.join(v) for v in rows.values()) + '; a shared id must read the same in every file')
    print(f'{len(names) - min(bad, len(names))}/{len(names)} type files valid' + ('' if not bad else f', {bad} problem(s)'))
    return 1 if bad or not names else 0

def min_sizes(spec):
    size0 = spec.get('font_size', 14)
    rules = load_type(spec.get('type'))[0]
    out = {}
    for n in spec.get('nodes', []):
        w, h, _ = text_size(n.get('lines', []), n.get('font_size', size0), n.get('bold_first', True))
        f = T['fit'] * SHAPES.get(node_shape(n, rules), 1)
        out[n['id']] = (int(math.ceil(w / f / 10.0)) * 10, int(math.ceil(h / f / 10.0)) * 10)
    return out

def lint(spec):
    T.update(spec.get('thresholds', {}))
    issues, checks = [], set()

    def add(level, cid, where, msg):
        item = dict(level=level, check=cid, where=where, msg=msg)
        if item not in issues:
            issues.append(item)

    def ran(*ids):
        checks.update(ids)

    size0 = spec.get('font_size', 14)
    nodes, edges, texts = spec.get('nodes', []), spec.get('edges', []), spec.get('texts', [])
    guides = spec.get('guides', [])
    GD = {g['of']: g for g in guides if g.get('of')}
    ids = [o.get('id') for o in nodes + edges + texts + guides]
    ran('X1')
    for i in sorted({i for i in ids if ids.count(i) > 1 or not i}, key=str):
        add('FAIL', 'X1', str(i), 'missing or duplicate id')
    N = {n['id']: n for n in nodes}
    leaves = [n for n in nodes if not n.get('container')]
    ran('N0')
    rules, err = load_type(spec.get('type'))
    if err:
        add('FAIL', 'N0', 'type', err)
    ndef = lambda n: (rules or {}).get('nodes', {}).get(n.get('kind')) or {}

    # ---- text
    ran('T1', 'T2', 'T4')
    title_boxes = []
    for o in nodes + texts:
        fs, lines = o.get('font_size', size0), o.get('lines', [])
        is_node = o in nodes
        w, h, est = text_size(lines, fs, o.get('bold_first', is_node))
        if est:
            add('WARN', 'T4', o['id'], f'{est} character(s) measured by estimate, no font covers them here; leave extra room')
        if o.get('container'):
            hh = o.get('header_h', T['header_h'])
            cx = o['x'] + o['w'] / 2
            if lines:
                title_boxes.append((o['id'], (cx - w / 2, o['y'], cx + w / 2, o['y'] + hh)))
            if w > T['fit'] * o['w'] or h > hh:
                add('FAIL', 'T1', o['id'], f'container title needs {w:.0f}x{h:.0f}px, header allows {T["fit"] * o["w"]:.0f}x{hh}px')
            continue
        fit = T['fit'] * SHAPES.get(node_shape(o, rules) if is_node else 'rect', 1)
        aw, ah = fit * o['w'], fit * o['h']
        if w > aw or h > ah:
            add('FAIL', 'T1', o['id'], f'text needs {w:.0f}x{h:.0f}px but box allows {aw:.0f}x{ah:.0f}px; '
                f'make box at least {math.ceil(w / fit)}x{math.ceil(h / fit)}px or shorten/split lines')
        cap = ndef(o).get('max_lines', T['max_lines']) if is_node else 0
        if is_node and len(lines) > cap:
            add('FAIL', 'T2', o['id'], f'{len(lines)} lines, max {cap}')

    # ---- canvas and scale
    ext = [rect(o) for o in nodes + texts]
    pts_all = [p for e in edges + guides for p in e.get('points', [])]
    max_x = max([r[2] for r in ext] + [p[0] for p in pts_all] + [0])
    max_y = max([r[3] for r in ext] + [p[1] for p in pts_all] + [0])
    cv = spec.get('canvas') or {'w': max_x + T['margin'], 'h': max_y + T['margin']}
    view_w, view_h = spec.get('view_width', T['view_w']), spec.get('view_height')
    scale = min(1.0, view_w / cv['w'], view_h / cv['h'] if view_h else 1.0)
    ran('G2', 'T3')
    m = T['margin']
    for o in nodes + texts:
        r = rect(o)
        if r[0] < m - 0.5 or r[1] < m - 0.5 or r[2] > cv['w'] - m + 0.5 or r[3] > cv['h'] - m + 0.5:
            add('FAIL', 'G2', o['id'], f'closer than {m}px to the canvas edge or outside it')
        if o.get('font_size', size0) * scale < T['min_font'] - 0.01:
            add('FAIL', 'T3', o['id'], f'font {o.get("font_size", size0)}px shows at {o.get("font_size", size0) * scale:.1f}px '
                f'(canvas {cv["w"]:.0f}x{cv["h"]:.0f}px in a {view_w}x{view_h or "any"}px view); shrink the canvas or raise the font')
    for e in edges + guides:
        for p in e.get('points', []):
            if not (m - 0.5 <= p[0] <= cv['w'] - m + 0.5 and m - 0.5 <= p[1] <= cv['h'] - m + 0.5):
                add('FAIL', 'G2', e['id'], f'point {p} closer than {m}px to the canvas edge or outside it')
                break

    # ---- node geometry
    ran('G1', 'G3', 'G4', 'G5')
    for a, b in combinations(nodes, 2):
        ra, rb = rect(a), rect(b)
        for par, ch in ((a, b), (b, a)):
            if ch.get('parent') == par['id']:
                rp, rc = rect(par), rect(ch)
                cm = T['child_margin']
                if rc[0] < rp[0] + cm or rc[1] < rp[1] + cm or rc[2] > rp[2] - cm or rc[3] > rp[3] - cm:
                    add('FAIL', 'G5', ch['id'], f'not inside container {par["id"]} with {cm}px margin')
                break
        else:
            anc = lambda n, t: n.get('parent') and (n['parent'] == t['id'] or (n['parent'] in N and anc(N[n['parent']], t)))
            if anc(a, b) or anc(b, a):
                continue
            mg = T['head_gap'] if a['id'] in GD and b['id'] in GD else T['gap']
            if overlap(ra, rb):
                if not ((a.get('container') and b.get('on_guide')) or (b.get('container') and a.get('on_guide'))):
                    add('FAIL', 'G1', f'{a["id"]}/{b["id"]}', 'boxes overlap')
            elif not (a.get('container') or b.get('container') or a.get('on_guide') or b.get('on_guide')) and rect_gap(ra, rb) < mg:
                add('FAIL', 'G1', f'{a["id"]}/{b["id"]}', f'gap {rect_gap(ra, rb):.0f}px, min {mg}px')
    for t in texts:
        for n in leaves:
            if overlap(grow(rect(t), T['text_clear']), rect(n)):
                add('FAIL', 'G1', f'{t["id"]}/{n["id"]}', 'text block overlaps a box')
    for a, b in combinations(texts, 2):
        if overlap(rect(a), rect(b)):
            add('FAIL', 'G1', f'{a["id"]}/{b["id"]}', 'text blocks overlap')
    kinds = {}
    for n in leaves:
        if n.get('kind') and ndef(n).get('uniform', not rules):
            kinds.setdefault(n['kind'], set()).add((n['w'], n['h']))
    for k, s in kinds.items():
        if len(s) > 1:
            add('FAIL', 'G3', k, f'boxes of kind "{k}" have {len(s)} different sizes {sorted(s)}; use one size')
    n_boxes = sum(1 for n in leaves if not n.get('on_guide'))
    if n_boxes > T['max_nodes']:
        add('FAIL', 'G4', 'diagram', f'{n_boxes} boxes, max {T["max_nodes"]}; split into several diagrams')

    # ---- edges
    ran('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12')
    segs, labels, deg, back, masked = [], [], {}, 0, set()
    direction = spec.get('direction')
    for e in edges:
        s, t, pts = N.get(e.get('from')), N.get(e.get('to')), e.get('points') or []
        if not s or not t or len(pts) < 2:
            add('FAIL', 'E1', e['id'], 'needs existing from/to nodes and at least 2 points (explicit route)')
            continue
        deg[s['id']] = deg.get(s['id'], 0) + 1
        deg[t['id']] = deg.get(t['id'], 0) + 1
        pts = simplify([tuple(p) for p in pts])
        for end, node, name in ((pts[0], s, 'start'), (pts[-1], t, 'end')):
            if e.get('anchor') == 'guide':
                g = GD.get(node['id'])
                on_line = g and min(point_seg_dist(end, a, b) for a, b in zip(g['points'], g['points'][1:])) <= T['bar_half'] + 1
                if not on_line and boundary_dist(end, rect(node))[0] > 2:
                    add('FAIL', 'E2', e['id'], f'{name} point {end} is neither on the lifeline of {node["id"]} nor on its border')
                continue
            d, inside = boundary_dist(end, rect(node))
            if (inside and d > 2) or (not inside and d > T['anchor_tol']):
                add('FAIL', 'E2', e['id'], f'{name} point {end} is not on the border of {node["id"]}')
        es = list(zip(pts, pts[1:]))
        for a, b in es:
            for n in leaves:
                own = n is s or n is t or (n.get('of') in (s['id'], t['id']) and n.get('on_guide'))
                r = grow(rect(n), -3) if own else grow(rect(n), T['node_clear'])
                if seg_in_rect(a, b, r) > 0.5:
                    add('FAIL', 'E3', e['id'], f'runs through its own endpoint box {n["id"]}' if own
                        else f'runs through or within {T["node_clear"]}px of box {n["id"]}')
            for tid, r in [(x['id'], rect(x)) for x in texts] + title_boxes:
                if seg_in_rect(a, b, grow(r, T['text_clear'])) > 0.5:
                    add('FAIL', 'E4', e['id'], f'runs over text {tid}')
        bends = len(pts) - 2
        if bends > T['max_bends']:
            add('FAIL', 'E7', e['id'], f'{bends} bends, max {T["max_bends"]}')
        length = sum(math.dist(a, b) for a, b in es)
        straight = math.dist(pts[0], pts[-1]) or 1
        is_back = e.get('back') or (direction == 'LR' and pts[-1][0] < pts[0][0] - 1) or (direction == 'TB' and pts[-1][1] < pts[0][1] - 1)
        back += 1 if is_back else 0
        if not is_back and s is not t and length / straight > T['detour']:
            add('FAIL', 'E8', e['id'], f'route is {length / straight:.2f}x the straight distance, max {T["detour"]}; move the boxes closer or mark "back": true')
        if math.dist(*es[-1]) < T['last_seg']:
            add('FAIL', 'E11', e['id'], f'last segment {math.dist(*es[-1]):.0f}px, min {T["last_seg"]}px for the arrowhead')
        segs += [(e['id'], a, b) for a, b in es]
        if e.get('label'):
            fs = e.get('label_font_size', T['label_font'])
            if fs * scale < T['min_font'] - 0.01:
                add('FAIL', 'T3', e['id'], f'label font {fs}px shows at {fs * scale:.1f}px')
            ll = as_lines(e['label'])
            lw, lh = max(measure(x, fs)[0] for x in ll), len(ll) * fs * T['line_h'] + 4
            lb = e.get('label_box')
            if lb:
                box = (lb[0], lb[1], lb[0] + lb[2], lb[1] + lb[3])
                if lw > lb[2] or lh > lb[3] + 0.5:
                    add('FAIL', 'T1', e['id'], f'label needs {lw:.0f}x{lh:.0f}px, label_box is {lb[2]:.0f}x{lb[3]:.0f}px')
            else:
                a, b = max(es, key=lambda ab: math.dist(*ab))
                cx, cy, hw, hh = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, lw / 2 + 4, lh / 2
                box = (cx - hw, cy - hh, cx + hw, cy + hh)
            if min(rect_seg_dist(box, a, b) for a, b in es) > T['label_dist']:
                add('FAIL', 'E12', e['id'], f'label is more than {T["label_dist"]}px away from its own edge')
            if e.get('anchor') == 'guide' and s is not t and s['id'] in GD and t['id'] in GD:
                lo, hi = sorted((GD[s['id']]['points'][0][0], GD[t['id']]['points'][0][0]))
                if box[0] < lo + 4 or box[2] > hi - 4:
                    add('FAIL', 'E12', e['id'], f'label is {box[2] - box[0]:.0f}px wide but its arrow spans {hi - lo:.0f}px; break it into lines so it stays between the two lifelines')
                if abs((box[0] + box[2]) / 2 - (lo + hi) / 2) > 2:
                    add('FAIL', 'E12', e['id'], 'label of a sequence message must be centered over its arrow')
            if e.get('label_mask'):
                masked.add(e['id'])
            labels.append((e['id'], box))
    if back > T['max_back']:
        add('FAIL', 'E9', 'diagram', f'{back} edges run against the main direction, max {T["max_back"]}')
    for nid, d in deg.items():
        if d > T['max_degree'] and not N[nid].get('hub'):
            add('FAIL', 'E10', nid, f'{d} edges on one box, max {T["max_degree"]}; route through a hub or split')
    crossings = 0
    for (i, a, b), (j, c, d) in combinations(segs, 2):
        if i == j:
            continue
        if seg_cross(a, b, c, d):
            crossings += 1
            add('INFO', 'E5', f'{i}/{j}', 'edges cross')
        for ax in (0, 1):
            o = 1 - ax
            if abs(a[o] - b[o]) < 0.5 and abs(c[o] - d[o]) < 0.5:
                ov = min(max(a[ax], b[ax]), max(c[ax], d[ax])) - max(min(a[ax], b[ax]), min(c[ax], d[ax]))
                dist = abs(a[o] - c[o])
                if ov > 4 and dist < T['par_gap']:
                    add('FAIL', 'E6', f'{i}/{j}', 'edges overlap on the same line' if dist < 0.5 else f'parallel edges {dist:.0f}px apart, min {T["par_gap"]}px')
    allowed = 0 if n_boxes <= T['max_nodes'] else 2
    if crossings > allowed:
        add('FAIL', 'E5', 'diagram', f'{crossings} edge crossing(s), max {allowed}; reorder boxes or reroute')
    for (i, box) in labels:
        for n in leaves:
            if overlap(box, rect(n)):
                add('FAIL', 'E12', i, f'label overlaps box {n["id"]}')
        for x in texts:
            if overlap(box, rect(x)):
                add('FAIL', 'E12', i, f'label overlaps text {x["id"]}')
        for j, a, b in segs:
            if j != i and seg_in_rect(a, b, grow(box, 2)) > 0.5:
                add('FAIL', 'E4', j, f'runs over the label of edge {i}')
    for (i, b1), (j, b2) in combinations(labels, 2):
        if overlap(b1, b2):
            add('FAIL', 'E12', f'{i}/{j}', 'edge labels overlap')

    # ---- guides (lifelines): edges may cross them, text may not sit on them
    ran('E13')
    for g in guides:
        for a, b in zip(g['points'], g['points'][1:]):
            for x in texts:
                if seg_in_rect(a, b, grow(rect(x), T['text_clear'])) > 0.5:
                    add('FAIL', 'E13', g['id'], f'lifeline runs over text {x["id"]}')
            for i, box in labels:
                if i not in masked and seg_in_rect(a, b, grow(box, T['text_clear'])) > 0.5:
                    add('FAIL', 'E13', g['id'], f'lifeline runs over the label of edge {i}; give the label an opaque background and set "label_mask": true')
            for tid, r in title_boxes:
                if seg_in_rect(a, b, grow(r, T['text_clear'])) > 0.5:
                    add('FAIL', 'E13', g['id'], f'lifeline runs over the title of {tid}')
            for n in leaves:
                if n['id'] != g.get('of') and not n.get('on_guide') and seg_in_rect(a, b, grow(rect(n), T['node_clear'])) > 0.5:
                    add('FAIL', 'E13', g['id'], f'lifeline runs through box {n["id"]}; mark the box "on_guide": true if it is a note on that lifeline')

    # ---- structure and style
    ran('S1', 'S2', 'S4', 'S5', 'S6', 'S7')
    for n in leaves:
        if not deg.get(n['id']) and not n.get('standalone'):
            add('FAIL', 'S1', n['id'], 'box has no edge; connect it or mark "standalone": true')
    blob = unicodedata.normalize('NFC', ' '.join(
        [' '.join(o.get('lines', [])) for o in nodes + texts] + [' '.join(as_lines(e.get('label', ''))) for e in edges] + [spec.get('title', '')])).casefold()
    for req in spec.get('requested', []):
        if unicodedata.normalize('NFC', req).casefold() not in blob:
            add('FAIL', 'S2', req, 'requested element is missing from the diagram')
    if not spec.get('title') and not any(x.get('role') == 'title' for x in texts):
        add('FAIL', 'S4', 'diagram', 'no title')
    fills = {n['fill'].lower() for n in leaves if n.get('fill')}
    styles = set() if rules else {e.get('style', 'solid') for e in edges}
    if (rules or {}).get('legend', True) and (len(fills) > 1 or len(styles) > 1) and not any(x.get('role') == 'legend' for x in texts):
        add('FAIL', 'S5', 'diagram', f'{len(fills)} fill colors but no legend text (role "legend") that says what each one means')
    if len(fills) > T['max_fills']:
        add('FAIL', 'S6', 'diagram', f'{len(fills)} fill colors, max {T["max_fills"]}')
    for n in nodes + texts:
        for f, c in (('fill', 'text_color'), ('fill_dark', 'text_dark')):
            if n.get(f) and n.get(c):
                r = contrast(n[f], n[c])
                if r < T['contrast']:
                    add('FAIL', 'S7', n['id'], f'contrast {r:.1f}:1 between {n[c]} and {n[f]}, min {T["contrast"]}:1')
    if rules:
        ran('N1', 'N2', 'N3', 'N4', 'N5')
        notation(rules, add, nodes, edges, texts, GD)
    return dict(canvas=cv, scale=round(scale, 3), measured_with='fonts' if ImageFont and fonts_for('L', 0, 14) else 'estimate',
                checks_run=sorted(checks), issues=issues,
                fails=sum(1 for i in issues if i['level'] == 'FAIL'), warns=sum(1 for i in issues if i['level'] == 'WARN'))

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == '--types':
        for tid in list_types():
            print(f'{tid}: {(load_type(tid)[0] or {}).get("name", "unreadable")}')
        return 0
    if argv[1] == '--check-types':
        return check_types()
    try:
        with open(argv[1], encoding='utf-8') as f:
            spec = json.load(f)
    except Exception as ex:
        print(f'cannot read spec: {ex}')
        return 2
    if '--sizes' in argv:
        for nid, (w, h) in min_sizes(spec).items():
            print(f'{nid}: min {w}x{h}')
        return 0
    if '--styles' in argv:
        rules = load_type(spec.get('type'))[0]
        for n in spec.get('nodes', []):
            print(f'node {n["id"]}: {n.get("kind")} -> shape {node_shape(n, rules)}')
        for e in spec.get('edges', []):
            st = edge_style(e, rules)
            print(f'edge {e["id"]}: {e.get("kind")} -> line {st["line"]}, head {st["head"]}, tail {st["tail"]}')
        return 0
    rep = lint(spec)
    if '--json' in argv:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        for i in rep['issues']:
            if i['level'] != 'INFO':
                print(f'{i["level"]} {i["check"]} [{i["where"]}] {i["msg"]}')
        failed = sorted({i['check'] for i in rep['issues'] if i['level'] == 'FAIL'})
        print(f'canvas {rep["canvas"]["w"]:.0f}x{rep["canvas"]["h"]:.0f}, scale {rep["scale"]}, text measured with {rep["measured_with"]}')
        print(f'{"FAIL" if rep["fails"] else "PASS"}: {len(rep["checks_run"]) - len(failed)}/{len(rep["checks_run"])} checks passed, '
              f'{rep["fails"]} failure(s), {rep["warns"]} warning(s)' + (f'; failed: {", ".join(failed)}' if failed else ''))
    return 1 if rep['fails'] else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
