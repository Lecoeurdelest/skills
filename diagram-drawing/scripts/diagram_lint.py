#!/usr/bin/env python3
"""diagram_lint.py: lint a diagram layout spec (JSON) before it is drawn.
Usage: python3 diagram_lint.py spec.json [--sizes] [--json]
Exit code 0 = no FAIL, 1 = at least one FAIL, 2 = bad input."""
import json, math, os, sys, unicodedata
from itertools import combinations

T = dict(fit=0.80, max_lines=3, min_font=12, view_w=800, margin=20, gap=30,
         child_margin=10, max_nodes=15, max_bends=2, detour=1.5, max_back=2,
         max_degree=4, par_gap=12, last_seg=20, max_fills=4, contrast=4.5,
         node_clear=6, text_clear=4, label_dist=14, anchor_tol=6, line_h=1.3,
         label_font=12, header_h=28)

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

def min_sizes(spec):
    size0 = spec.get('font_size', 14)
    out = {}
    for n in spec.get('nodes', []):
        w, h, _ = text_size(n.get('lines', []), n.get('font_size', size0), n.get('bold_first', True))
        out[n['id']] = (int(math.ceil(w / T['fit'] / 10.0)) * 10, int(math.ceil(h / T['fit'] / 10.0)) * 10)
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
    ids = [o.get('id') for o in nodes + edges + texts]
    ran('X1')
    for i in sorted({i for i in ids if ids.count(i) > 1 or not i}, key=str):
        add('FAIL', 'X1', str(i), 'missing or duplicate id')
    N = {n['id']: n for n in nodes}
    leaves = [n for n in nodes if not n.get('container')]

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
            title_boxes.append((o['id'], (cx - w / 2, o['y'], cx + w / 2, o['y'] + hh)))
            if w > T['fit'] * o['w'] or h > hh:
                add('FAIL', 'T1', o['id'], f'container title needs {w:.0f}x{h:.0f}px, header allows {T["fit"] * o["w"]:.0f}x{hh}px')
            continue
        aw, ah = T['fit'] * o['w'], T['fit'] * o['h']
        if w > aw or h > ah:
            add('FAIL', 'T1', o['id'], f'text needs {w:.0f}x{h:.0f}px but box allows {aw:.0f}x{ah:.0f}px; '
                f'make box at least {math.ceil(w / T["fit"])}x{math.ceil(h / T["fit"])}px or shorten/split lines')
        if is_node and len(lines) > T['max_lines']:
            add('FAIL', 'T2', o['id'], f'{len(lines)} lines, max {T["max_lines"]}')

    # ---- canvas and scale
    ext = [rect(o) for o in nodes + texts]
    pts_all = [p for e in edges for p in e.get('points', [])]
    max_x = max([r[2] for r in ext] + [p[0] for p in pts_all] + [0])
    max_y = max([r[3] for r in ext] + [p[1] for p in pts_all] + [0])
    cv = spec.get('canvas') or {'w': max_x + T['margin'], 'h': max_y + T['margin']}
    view_w = spec.get('view_width', T['view_w'])
    scale = min(1.0, view_w / cv['w'])
    ran('G2', 'T3')
    m = T['margin']
    for o in nodes + texts:
        r = rect(o)
        if r[0] < m - 0.5 or r[1] < m - 0.5 or r[2] > cv['w'] - m + 0.5 or r[3] > cv['h'] - m + 0.5:
            add('FAIL', 'G2', o['id'], f'closer than {m}px to the canvas edge or outside it')
        if o.get('font_size', size0) * scale < T['min_font'] - 0.01:
            add('FAIL', 'T3', o['id'], f'font {o.get("font_size", size0)}px shows at {o.get("font_size", size0) * scale:.1f}px '
                f'(canvas {cv["w"]:.0f}px in a {view_w}px view); narrow the canvas or raise the font')
    for e in edges:
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
            if overlap(ra, rb):
                add('FAIL', 'G1', f'{a["id"]}/{b["id"]}', 'boxes overlap')
            elif not a.get('container') and not b.get('container') and rect_gap(ra, rb) < T['gap']:
                add('FAIL', 'G1', f'{a["id"]}/{b["id"]}', f'gap {rect_gap(ra, rb):.0f}px, min {T["gap"]}px')
    for t in texts:
        for n in leaves:
            if overlap(grow(rect(t), T['text_clear']), rect(n)):
                add('FAIL', 'G1', f'{t["id"]}/{n["id"]}', 'text block overlaps a box')
    for a, b in combinations(texts, 2):
        if overlap(rect(a), rect(b)):
            add('FAIL', 'G1', f'{a["id"]}/{b["id"]}', 'text blocks overlap')
    kinds = {}
    for n in leaves:
        if n.get('kind'):
            kinds.setdefault(n['kind'], set()).add((n['w'], n['h']))
    for k, s in kinds.items():
        if len(s) > 1:
            add('FAIL', 'G3', k, f'boxes of kind "{k}" have {len(s)} different sizes {sorted(s)}; use one size')
    if len(leaves) > T['max_nodes']:
        add('FAIL', 'G4', 'diagram', f'{len(leaves)} boxes, max {T["max_nodes"]}; split into several diagrams')

    # ---- edges
    ran('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12')
    segs, labels, deg, back = [], [], {}, 0
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
            d, inside = boundary_dist(end, rect(node))
            if (inside and d > 2) or (not inside and d > T['anchor_tol']):
                add('FAIL', 'E2', e['id'], f'{name} point {end} is not on the border of {node["id"]}')
        es = list(zip(pts, pts[1:]))
        for a, b in es:
            for n in leaves:
                r = grow(rect(n), -3) if n is s or n is t else grow(rect(n), T['node_clear'])
                if seg_in_rect(a, b, r) > 0.5:
                    add('FAIL', 'E3', e['id'], f'runs through or within {T["node_clear"]}px of box {n["id"]}' if n is not s and n is not t
                        else f'runs through its own endpoint box {n["id"]}')
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
        if not is_back and length / straight > T['detour']:
            add('FAIL', 'E8', e['id'], f'route is {length / straight:.2f}x the straight distance, max {T["detour"]}; move the boxes closer or mark "back": true')
        if math.dist(*es[-1]) < T['last_seg']:
            add('FAIL', 'E11', e['id'], f'last segment {math.dist(*es[-1]):.0f}px, min {T["last_seg"]}px for the arrowhead')
        segs += [(e['id'], a, b) for a, b in es]
        if e.get('label'):
            fs = e.get('label_font_size', T['label_font'])
            if fs * scale < T['min_font'] - 0.01:
                add('FAIL', 'T3', e['id'], f'label font {fs}px shows at {fs * scale:.1f}px')
            lw, _ = measure(e['label'], fs)
            lb = e.get('label_box')
            if lb:
                box = (lb[0], lb[1], lb[0] + lb[2], lb[1] + lb[3])
                if lw > lb[2]:
                    add('FAIL', 'T1', e['id'], f'label needs {lw:.0f}px, label_box is {lb[2]}px wide')
            else:
                a, b = max(es, key=lambda ab: math.dist(*ab))
                cx, cy, hw, hh = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, lw / 2 + 4, fs * T['line_h'] / 2 + 2
                box = (cx - hw, cy - hh, cx + hw, cy + hh)
            c = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            if min(point_seg_dist(c, a, b) for a, b in es) > T['label_dist']:
                add('FAIL', 'E12', e['id'], 'label is not on its own edge')
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
    allowed = 0 if len(leaves) <= T['max_nodes'] else 2
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

    # ---- structure and style
    ran('S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7')
    for n in leaves:
        if not deg.get(n['id']) and not n.get('standalone'):
            add('FAIL', 'S1', n['id'], 'box has no edge; connect it or mark "standalone": true')
    blob = unicodedata.normalize('NFC', ' '.join(
        [' '.join(o.get('lines', [])) for o in nodes + texts] + [e.get('label', '') for e in edges] + [spec.get('title', '')])).casefold()
    for req in spec.get('requested', []):
        if unicodedata.normalize('NFC', req).casefold() not in blob:
            add('FAIL', 'S2', req, 'requested element is missing from the diagram')
    for n in leaves:
        if n.get('kind') == 'decision':
            outs = [e for e in edges if e.get('from') == n['id']]
            if len(outs) < 2 or any(not e.get('label') for e in outs):
                add('FAIL', 'S3', n['id'], 'a decision needs at least 2 outgoing edges, each with a label')
    if spec.get('type') == 'flow' and edges:
        indeg = {e.get('to') for e in edges}
        if not any(n.get('start') or n['id'] not in indeg for n in leaves):
            add('FAIL', 'S3', 'diagram', 'no start point; a cycle needs one box marked "start": true and drawn as the start')
    if not spec.get('title') and not any(x.get('role') == 'title' for x in texts):
        add('FAIL', 'S4', 'diagram', 'no title')
    fills = {n['fill'].lower() for n in leaves if n.get('fill')}
    styles = {e.get('style', 'solid') for e in edges}
    if (len(fills) > 1 or len(styles) > 1) and not any(x.get('role') == 'legend' for x in texts):
        add('FAIL', 'S5', 'diagram', f'{len(fills)} fill colors / {len(styles)} line styles but no legend text (role "legend")')
    if len(fills) > T['max_fills']:
        add('FAIL', 'S6', 'diagram', f'{len(fills)} fill colors, max {T["max_fills"]}')
    for n in nodes + texts:
        for f, c in (('fill', 'text_color'), ('fill_dark', 'text_dark')):
            if n.get(f) and n.get(c):
                r = contrast(n[f], n[c])
                if r < T['contrast']:
                    add('FAIL', 'S7', n['id'], f'contrast {r:.1f}:1 between {n[c]} and {n[f]}, min {T["contrast"]}:1')
    return dict(canvas=cv, scale=round(scale, 3), measured_with='fonts' if ImageFont and fonts_for('L', 0, 14) else 'estimate',
                checks_run=sorted(checks), issues=issues,
                fails=sum(1 for i in issues if i['level'] == 'FAIL'), warns=sum(1 for i in issues if i['level'] == 'WARN'))

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
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
