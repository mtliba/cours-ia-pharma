"""Axe 3 course: one content source -> slide decks (Slides type files) + website blocks."""
import html, json, re, os, math
from mathsvg import math_svg

INK, BLUE, RED, MUTE, GRID, PALE, PINK, GREY, AMBER, WHITE = (
    "#101B3F", "#2A46C8", "#D22B3A", "#5A6379", "#D9DDE6", "#E9EDFB", "#FBE6E8", "#7F88A0", "#C77700", "#FFFFFF")
PALEA = "#FBEFD9"

L = {
 "fr": dict(start="Situation de départ", obj="Objectifs", objlead="À la fin de cette séance, vous saurez :", plan="Plan de la séance",
            ex="À vous", sol="Correction", quiz="Auto-évaluation", quizlead="Une seule bonne réponse par question.", take="À retenir",
            refs="Pour aller plus loin", next="Séance suivante", sess="Séance", of="sur", time="Durée", mat="Matériel", out="À produire",
            clicks="clic", sym="Lecture de la formule", code="Code", end="Fin de la séance", why="Explication", ans="Réponse"),
 "en": dict(start="Starting point", obj="Learning objectives", objlead="By the end of this session you will be able to:", plan="Outline",
            ex="Your turn", sol="Solution", quiz="Self-check", quizlead="One correct answer per question.", take="Key takeaways",
            refs="References and further reading", next="Next session", sess="Session", of="of", time="Time", mat="Material", out="Deliverable",
            clicks="click", sym="Reading the equation", code="Code", end="End of session", why="Explanation", ans="Answer"),
}

def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))

# ----------------------------------------------------------------- figures
class Fig:
    def __init__(s, w, h, alt=""):
        s.w, s.h, s.alt, s.sv, s.lb = w, h, alt, [], []
        s.ax = None
    # primitives
    def line(s, x1, y1, x2, y2, c=INK, sw=3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.sv.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"{d}/>')
    def rect(s, x, y, w, h, fill=PALE, stroke=None, sw=3, rx=0, op=None):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        s.sv.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{o}{st}/>')
    def circle(s, cx, cy, r, fill=BLUE, stroke=WHITE, sw=3, op=None):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        s.sv.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"{o}{st}/>')
    def poly(s, pts, c=BLUE, sw=4, fill="none", dash=None, close=False, op=None):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{op}"' if op is not None else ""
        tag = "polygon" if close else "polyline"
        st = f'stroke="{c}" stroke-width="{sw}"' if c else 'stroke="none"'
        s.sv.append(f'<{tag} points="{p}" fill="{fill}"{o} {st} stroke-linejoin="round" stroke-linecap="round"{d}/>')
    def path(s, d, c=BLUE, sw=4, fill="none", dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        s.sv.append(f'<path d="{d}" fill="{fill}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"{da}/>')
    def arrow(s, x1, y1, x2, y2, c=INK, sw=4, head=16, dash=None):
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
        s.line(x1, y1, bx, by, c, sw, dash)
        p = [(x2, y2), (bx - head * .5 * math.sin(a), by + head * .5 * math.cos(a)), (bx + head * .5 * math.sin(a), by - head * .5 * math.cos(a))]
        s.poly(p, None, 0, fill=c, close=True)
    # labels (HTML paragraphs over the drawing)
    def lab(s, x, y, t, w=240, al="left", cls="ax", color=None, bg=False):
        s.lb.append((x, y, w, al, cls, (color or "") + ("|bg" if bg else ""), t))
    def labc(s, cx, cy, t, w=240, cls="ax", color=None, lines=1):
        size = {"ax": 27, "ax ax-b": 27, "axw": 30, "axh": 46, "axw ax-b": 30}.get(cls, 27)
        lh = 1.0 if cls == "axh" else 1.2
        s.lab(cx - w / 2, cy - lines * size * lh / 2, t, w, "center", cls, color)
    def box(s, x, y, w, h, t, fill=PALE, stroke=BLUE, cls="axw", color=None, lines=1, rx=10):
        s.rect(x, y, w, h, fill, stroke, 3, rx)
        s.labc(x + w / 2, y + h / 2, t, w - 16, cls, color, lines)
    # data axes
    def axes(s, x0, y0, x1, y1, xr, yr, xt=(), yt=(), xl="", yl="", grid=True, fmt=str, frame=True, fmty=None):
        fmty = fmty or fmt
        s.ax = (x0, y0, x1, y1, xr, yr)
        if grid:
            for v in xt: s.line(s.X(v), y0, s.X(v), y1, GRID, 2)
            for v in yt: s.line(x0, s.Y(v), x1, s.Y(v), GRID, 2)
        s.line(x0, y1, x1, y1, MUTE, 3); s.line(x0, y0, x0, y1, MUTE, 3)
        for v in xt: s.lab(s.X(v) - 40, y1 + 10, fmt(v), 80, "center")
        for v in yt: s.lab(x0 - 112, s.Y(v) - 16, fmty(v), 100, "right")
        if xl: s.lab(x0, y1 + 48, xl, x1 - x0, "center", "ax ax-b")
        if yl: s.lab(x0 - 20, y0 - 50, yl, min(700, s.w - x0 + 20), "left", "ax ax-b")
    def X(s, v):
        x0, y0, x1, y1, xr, yr = s.ax; return x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0)
    def Y(s, v):
        x0, y0, x1, y1, xr, yr = s.ax; return y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0)
    def curve(s, xs, ys, c=BLUE, sw=5, dash=None):
        s.poly([(s.X(a), s.Y(b)) for a, b in zip(xs, ys)], c, sw, dash=dash)
    def dots(s, xs, ys, c=BLUE, r=10, op=None):
        for a, b in zip(xs, ys): s.circle(s.X(a), s.Y(b), r, c, WHITE, 3, op)
    def html(s):
        assert len(s.lb) <= 23, f"too many labels ({len(s.lb)}) in figure: {s.alt}"
        alt = html.escape(s.alt, quote=True)
        o = [f'<div class="plot" style="width:{s.w}px;height:{s.h}px"><svg class="ly" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}" aria-label="{alt}">{"".join(s.sv)}</svg>']
        for x, y, w, al, cls, color, t in s.lb:
            bg = color.endswith("|bg"); color = color.replace("|bg", "")
            col = (f";color:{color}" if color else "") + (";background:#FFFFFF" if bg else "")
            o.append(f'<p class="{cls}" style="left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;text-align:{al}{col}">{t}</p>')
        o.append("</div>")
        return "".join(o)

def flow(steps, w=1500, h=220, alt="", bw=None, colors=None, subs=None, gap=56):
    """Horizontal chain of boxes joined by arrows."""
    n = len(steps); f = Fig(w, h, alt)
    bw = bw or (w - gap * (n - 1)) / n
    bh = h - (96 if subs else 20); y = 10
    for i, t in enumerate(steps):
        x = i * (bw + gap)
        fill, stroke = (colors[i] if colors else (PALE, BLUE))
        f.box(x, y, bw, bh, t, fill, stroke, "axw ax-b", lines=t.count("<br>") + 1)
        if i < n - 1: f.arrow(x + bw + 6, y + bh / 2, x + bw + gap - 6, y + bh / 2, INK, 4)
        if subs and subs[i]: f.lab(x, y + bh + 12, subs[i], bw, "center", "ax")
    return f

# ----------------------------------------------------------------- sessions
class Session:
    def __init__(s, n, lang, part, title, sub, total=10):
        s.n, s.lang, s.part, s.title, s.sub, s.total = n, lang, part, title, sub, total
        s.slides = []; s.T = L[lang]; s.sections = []
    def _add(s, kind, n, **k):
        k.update(kind=kind, notes=n); s.slides.append(k); return k
    def sec(s, desc): s.sections.append((len(s.slides), desc))
    def cover(s, n): return s._add("cover", n)
    def sit(s, title, text, q, n, **k): return s._add("sit", n, title=title, text=text, q=q, **k)
    def obj(s, items, n): return s._add("obj", n, title=s.T["obj"], lead=s.T["objlead"], items=items)
    def plan(s, items, n): return s._add("plan", n, title=s.T["plan"], items=items)
    def pts(s, title, lead, items, n, fig=None, band=None, **k): return s._add("pts", n, title=title, lead=lead, items=items, fig=fig, band=band, **k)
    def cols(s, title, lead, cols, n, band=None, **k): return s._add("cols", n, title=title, lead=lead, cols=cols, band=band, **k)
    def eq(s, title, lead, tex, legend, n, band=None, **k):
        return s._add("eq", n, title=title, lead=lead, tex=[tex] if isinstance(tex, str) else tex, legend=legend, band=band, **k)
    def tbl(s, title, lead, head, rows, n, widths=None, hl=None, band=None, small=False, **k):
        return s._add("tbl", n, title=title, lead=lead, head=head, rows=rows, widths=widths, hl=hl, band=band, small=small, **k)
    def st(s, text, sub, n): return s._add("st", n, title=strip(text), text=text, sub=sub)
    def ex(s, title, steps, meta, n): return s._add("ex", n, title=title, steps=steps, meta=meta)
    def sol(s, title, items, n, fig=None, band=None): return s._add("sol", n, title=title, lead="", items=items, fig=fig, band=band)
    def quiz(s, items, n): return s._add("quiz", n, title=s.T["quiz"], lead=s.T["quizlead"], items=items)
    def code(s, title, lead, code, items, n, **k): return s._add("code", n, title=title, lead=lead, code=code, items=items, **k)
    def take(s, items, n): return s._add("take", n, title=s.T["take"], items=items)
    def refs(s, items, n): return s._add("refs", n, title=s.T["refs"], items=items)
    def end(s, nxt, n): return s._add("end", n, title=s.T["end"], nxt=nxt)
    def wide(s, title, lead, fig, n, band=None, **k): return s._add("wide", n, title=title, lead=lead, fig=fig, band=band, **k)
    def nums(s, title, lead, nums, n, band=None): return s._add("nums", n, title=title, lead=lead, nums=nums, band=band)

    @property
    def foot(s):
        return f'{s.T["sess"]} {s.n} {s.T["of"]} {s.total} · {s.title}'

# ----------------------------------------------------------------- deck rendering
def code_html(code):
    out = []
    esc = lambda t: html.escape(t, quote=False).replace(" ", "&#160;")
    for ln in code.strip("\n").split("\n"):
        ind = len(ln) - len(ln.lstrip(" ")); raw = ln.lstrip(" ")
        if "#" in raw:
            i = raw.index("#"); body = esc(raw[:i]) + f'<span style="color:#9FB0F0">{esc(raw[i:])}</span>'
        else:
            body = esc(raw)
        out.append(f'<p class="cd-l">{"&#160;" * ind}{body or "&#160;"}</p>')
    return '<div class="cd">' + "".join(out) + "</div>"

def _hd(sl, tag=None):
    t = f'<p class="tag">{tag}</p>' if tag else ""
    lead = f'<p class="lead">{sl["lead"]}</p>' if sl.get("lead") else ""
    return f'<div class="hd">{t}<h2>{sl["title"]}</h2>{lead}</div>'

def _rows(items, cls="pt", frag=False):
    o = []
    for i, it in enumerate(items):
        o.append(f'<div class="row{" row-0" if i == 0 else ""}"><p class="{cls}">{it}</p></div>')
    return '<div class="ptl">' + "".join(o) + "</div>"

def _band(sl, nfrag):
    if not sl.get("band"): return "", nfrag
    return f'<p class="band fragment">{sl["band"]}</p>', nfrag + 1

def legend_html(legend):
    o = []
    for i, (sym, mean) in enumerate(legend):
        sv = math_svg(sym, 36, BLUE, maxw=250)[0] if sym else ""
        o.append(f'<div class="sy-r{" sy-0" if i == 0 else ""}"><div class="sy-s">{sv}</div><p class="sy-t">{mean}</p></div>')
    return '<div class="sy">' + "".join(o) + "</div>"

def slide_html(S, i, sl):
    T = S.T; k = sl["kind"]; sid = f"s{i + 1:02d}"; nf = 0; cls = ""; body = ""
    if k == "cover":
        cls = "blue"
        pips = "".join(f'<div class="cv-i{" cv-on" if j + 1 == S.n else ""}"></div>' for j in range(S.total))
        body = (f'<p class="cv-k">Axe 3 · IA pour les sciences pharmaceutiques</p><p class="cv-k2">{S.part} · {T["sess"]} {S.n} {T["of"]} {S.total}</p>'
                f'<h1 class="cv-t">{S.title}</h1><p class="cv-s">{S.sub}</p><div class="sp"></div>'
                f'<div class="cv-b"><p class="cv-a">Marouane Tliba</p><div class="cv-p">{pips}</div></div>')
    elif k == "sit":
        body = (_hd(dict(title=sl["title"], lead=""), T["start"]) +
                f'<div class="bd"><div class="cols"><div class="sit-l"><p class="sit-p">{sl["text"]}</p></div>'
                f'<div class="sit-q"><p class="k">Question</p><p class="qz">{sl["q"]}</p></div></div></div>')
    elif k == "obj":
        rows = "".join(f'<div class="row{" row-0" if j == 0 else ""}"><div class="ob-b"></div><p class="ob-t">{it}</p></div>' for j, it in enumerate(sl["items"]))
        body = _hd(sl) + f'<div class="bd"><div class="rows">{rows}</div></div>'
    elif k == "plan":
        rows = "".join(f'<div class="row{" row-0" if j == 0 else ""}"><p class="pl-n">{j + 1}</p><div class="pl-m"><h3>{t}</h3><p class="pl-d">{d}</p></div></div>' for j, (t, d) in enumerate(sl["items"]))
        body = _hd(sl) + f'<div class="bd"><div class="rows">{rows}</div></div>'
    elif k in ("pts", "sol"):
        band, nf = _band(sl, nf)
        tag = T["sol"] if k == "sol" else None
        if sl.get("fig"):
            body = _hd(sl, tag) + f'<div class="bd"><div class="cols">{sl["fig"].html()}<div class="col-r">{_rows(sl["items"])}{band}</div></div></div>'
        else:
            body = _hd(sl, tag) + f'<div class="bd">{_rows(sl["items"])}{band}</div>'
    elif k == "wide":
        band, nf = _band(sl, nf)
        body = _hd(sl) + f'<div class="bd"><div class="ctr">{sl["fig"].html()}</div>{band}</div>'
    elif k == "cols":
        band, nf = _band(sl, nf)
        n = len(sl["cols"])
        cc = "".join(f'<div class="cc{" cc-0" if j == 0 else ""}"><h3>{h}</h3><p class="ct">{t}</p></div>' for j, (h, t) in enumerate(sl["cols"]))
        body = _hd(sl) + f'<div class="bd"><div class="cl c{n}">{cc}</div>{band}</div>'
    elif k == "eq":
        band, nf = _band(sl, nf)
        D = lambda t: t.replace(r"\frac", r"\dfrac")
        eqs = "".join(f'<div class="eq-l">{math_svg(D(t), 46, INK, maxw=1480)[0]}</div>' for t in sl["tex"])
        if sl.get("fig") and sl.get("figtop"):
            body = _hd(sl) + f'<div class="bd"><div class="ctr">{sl["fig"].html()}</div><div class="eqb">{eqs}</div>{legend_html(sl["legend"])}{band}</div>'
        elif sl.get("fig"):
            eqs = "".join(f'<div class="eq-l">{math_svg(D(t), 40, INK, maxw=700)[0]}</div>' for t in sl["tex"])
            body = _hd(sl) + f'<div class="bd"><div class="cols">{sl["fig"].html()}<div class="col-r"><div class="eqb">{eqs}</div>{legend_html(sl["legend"])}{band}</div></div></div>'
        else:
            body = _hd(sl) + f'<div class="bd"><div class="eqb">{eqs}</div>{legend_html(sl["legend"])}{band}</div>'
    elif k == "tbl":
        band, nf = _band(sl, nf)
        nc = len(sl["head"]); ws = sl["widths"] or [100 / nc] * nc
        hd = "".join(f'<p class="t-c" style="width:{w}%">{h}</p>' for h, w in zip(sl["head"], ws))
        rows = ""
        for j, r in enumerate(sl["rows"]):
            hl = " hl" if sl["hl"] is not None and j == sl["hl"] else ""
            rows += f'<div class="t-r{hl}">' + "".join(f'<p class="t-c{" t-1" if c == 0 else ""}" style="width:{w}%">{v}</p>' for c, (v, w) in enumerate(zip(r, ws))) + "</div>"
        body = _hd(sl) + f'<div class="bd"><div class="t{" t-s" if sl["small"] else ""}"><div class="t-r t-h">{hd}</div>{rows}</div>{band}</div>'
    elif k == "st":
        cls = "st"
        body = f'<p class="st-t">{sl["text"]}</p><div class="ul"></div><p class="st-s">{sl["sub"]}</p>'
    elif k == "ex":
        cls = "blue"
        steps = "".join(f'<div class="stp"><p class="stp-n">{j + 1}</p><p class="stp-t">{t}</p></div>' for j, t in enumerate(sl["steps"]))
        m = sl["meta"]
        meta = "".join(f'<div class="mt"><p class="k">{T[a]}</p><p class="mt-v">{m[a]}</p></div>' for a in ("time", "mat", "out") if a in m)
        body = (f'<div class="hd"><p class="ex-k">{T["ex"]}</p><h2>{sl["title"]}</h2></div>'
                f'<div class="bd"><div class="cols top"><div class="ex-s">{steps}</div><div class="ex-m">{meta}</div></div></div>')
    elif k == "quiz":
        qs = ""
        for j, (q, opts, ok, why) in enumerate(sl["items"]):
            os_ = "".join(f'<p class="qo{" ring fragment" if a == ok else ""}"{f' data-fragment-index="{j + 1}"' if a == ok else ""}>{"ABCD"[a]}. {o}</p>' for a, o in enumerate(opts))
            qs += f'<div class="cc{" cc-0" if j == 0 else ""}"><p class="qq">{j + 1}. {q}</p><div class="qs">{os_}</div></div>'
        nf = len(sl["items"])
        body = _hd(sl) + f'<div class="bd"><div class="cl c3 qz3">{qs}</div></div>'
    elif k == "code":
        body = _hd(sl) + f'<div class="bd"><div class="cols top">{code_html(sl["code"])}<div class="col-r">{_rows(sl["items"])}</div></div></div>'
    elif k == "take":
        rows = "".join(f'<div class="row{" row-0" if j == 0 else ""}"><p class="pl-n">{j + 1}</p><p class="rc-t">{it}</p></div>' for j, it in enumerate(sl["items"]))
        body = _hd(sl) + f'<div class="bd"><div class="rows">{rows}</div></div>'
    elif k == "refs":
        sm = " rf-s" if len(sl["items"]) > 6 else ""
        rows = "".join(f'<div class="row rf{sm}{" row-0" if j == 0 else ""}"><p class="rf-t">{it}</p></div>' for j, it in enumerate(sl["items"]))
        body = _hd(sl) + f'<div class="bd"><div class="rows">{rows}</div></div>'
    elif k == "nums":
        band, nf = _band(sl, nf)
        nn = "".join(f'<div class="nc"><p class="bn">{a}</p><p class="bl">{b}</p></div>' for a, b in sl["nums"])
        body = _hd(sl) + f'<div class="bd"><div class="nm n{len(sl["nums"])}">{nn}</div>{band}</div>'
    elif k == "end":
        cls = "blue st"
        nx = f'<div class="nx"><p class="cv-k">{T["next"]}</p><p class="nx-t">{sl["nxt"]}</p></div>' if sl.get("nxt") else ""
        body = f'<p class="cv-k">{S.foot}</p><h2 class="st-t">{sl["title"]}</h2><div class="sp"></div>{nx}'
    else:
        raise ValueError(k)
    notes = strip(sl["notes"])
    if nf: notes = f'[{nf} {T["clicks"]}{"s" if nf > 1 else ""}] ' + notes
    assert len(notes) < 3900, (S.n, i, len(notes))
    foot = "" if k == "cover" else f'<p class="foot">{S.foot}</p><p class="pg"></p>'
    c = f' class="{cls}"' if cls else ""
    return sid, f'<section id="{sid}"{c} data-transition="fade">\n{body}\n{foot}\n<aside>{html.escape(notes, quote=False)}</aside>\n</section>\n'

def build_deck(S, root, css):
    os.makedirs(f"{root}/project/slides", exist_ok=True)
    ids = []
    for i, sl in enumerate(S.slides):
        sid, h = slide_html(S, i, sl)
        ids.append(sid)
        open(f"{root}/project/slides/{sid}.html", "w").write(h)
    secs = {}
    for j, (start, desc) in enumerate(S.sections):
        secs[f"p{j}"] = {"description": desc, "start": ids[start]}
    deck = {"v": 5, "createdOnFiles": {"v": 1, "at": "2026-11-19T22:00:00Z"}, "lists": "css",
            "format": {"v": 1, "shared": ["project/deck.css"]},
            "title": f"Axe 3 · {S.T['sess']} {S.n} — {S.title}", "cover": ids[0], "order": ids, "sections": secs,
            "faces": {"source-sans-3": {"family": "Source Sans 3", "href": "https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;900&display=swap"},
                      "caveat": {"family": "Caveat", "href": "https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap"},
                      "jetbrains-mono": {"family": "JetBrains Mono", "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap"}},
            "designSystems": []}
    json.dump(deck, open(f"{root}/project/deck.json", "w"), ensure_ascii=False, indent=1)
    open(f"{root}/project/deck.css", "w").write(css)
    return ids

def harness(S, root, out):
    css = open(f"{root}/project/deck.css").read()
    secs = "".join(open(f"{root}/project/slides/s{i + 1:02d}.html").read() for i in range(len(S.slides)))
    page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>@font-face{{font-family:'Caveat';font-weight:700;src:url('../node_modules/@fontsource/caveat/files/caveat-latin-700-normal.woff2')}}
@font-face{{font-family:'JetBrains Mono';font-weight:400;src:url('../node_modules/@fontsource/jetbrains-mono/files/jetbrains-mono-latin-400-normal.woff2')}}
*{{margin:0;box-sizing:content-box}} body{{background:#888}} p,h1,h2,h3{{margin:0}}
section{{width:1920px;height:1080px;box-sizing:border-box;position:relative;overflow:hidden;margin:0 0 20px 0}} aside{{display:none}}
{css}
.fragment{{opacity:1 !important}} .ring.fragment{{border-color:#2A46C8 !important;background-color:#E9EDFB !important}}
*{{animation:none !important;transition:none !important}}</style></head><body>{secs}</body></html>"""
    open(out, "w").write(page)
