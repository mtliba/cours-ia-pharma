"""Interactive course website: index.html (shell, styles, widgets) + one HTML fragment per session."""
import sys, os, json, html, importlib
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
import numpy as np
import a1, a2, a3, b2, b3

HERE = os.path.dirname(__file__); ROOT = os.path.dirname(HERE); OUT = f"{ROOT}/site"
ALL = ["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4", "b5", "b6"]
DECKS = ["Xq6tJhebuf8ArARsj5aXX2", "4NdADrgJEkTtUeWNv89fp1", "Qst4iKHjrY2ek3W8Po4dMF", "DzW81LcqgVhyH5LZvt8XVB", "XuV2c623X6NGzzJn8FS18m",
         "DRQkqojLb3opri6GuLrzy6", "BcnMfs9xUFhyqgaEJ3mdyi", "PkJfc22t1g3RFvmSjWykAs", "X79u9Tt6wchREaG9RLP7DC", "9x1yt8pra8k6d4eKwg5mxH"]
# interactive figure attached to a slide: (session number, slide title) -> widget name
WIDGETS = {(1, "Douze patients, deux colonnes"): "fitline", (2, "De la droite à la probabilité"): "logistic", (3, "Trois modèles pour dix mesures"): "overfit",
           (4, "Pourquoi une fonction d’activation ?"): "neuron", (5, "The learning rate decides everything"): "lr", (6, "Reading an attention map"): "attention",
           (7, "What the temperature does"): "temperature", (8, "Diffusion: destroy, then learn to rebuild"): "diffusion", (9, "Low-rank adaptation (LoRA)"): "lora",
           (10, "What pharmacology already knows"): "pk"}
TRY = {"fr": "À vous de manipuler", "en": "Try it"}
SHOW = {"fr": "Voir la correction", "en": "Show the solution"}

def fig_html(f):
    return f'<div class="figwrap" data-w="{f.w}" data-h="{f.h}">{f.html()}</div>'

def eq_html(tex):
    return "".join(f'<div class="eq-l">{math_svg(t.replace(chr(92) + "frac", chr(92) + "dfrac"), 30, INK)[0]}</div>' for t in tex)

def legend(leg):
    rows = "".join(f'<div class="sy-r"><div class="sy-s">{math_svg(s, 22, BLUE)[0] if s else ""}</div><p class="sy-t">{m}</p></div>' for s, m in leg)
    return f'<div class="sy">{rows}</div>'

def ul(items, cls="pts"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def block(S, sl):
    T = S.T; k = sl["kind"]; say = f'<p class="say">{html.escape(strip(sl["notes"]), quote=False)}</p>'
    band = f'<p class="band">{sl["band"]}</p>' if sl.get("band") else ""
    lead = f'<p class="lead">{sl["lead"]}</p>' if sl.get("lead") else ""
    fig = fig_html(sl["fig"]) if sl.get("fig") else ""
    w = WIDGETS.get((S.n, strip(sl.get("title", ""))))
    wid = f'<div class="widget" data-w="{w}"><p class="wk">{TRY[S.lang]}</p></div>' if w else ""
    h = lambda t: f"<h3>{t}</h3>"
    if k in ("cover", "end"): return ""
    if k == "sit": body = f'<p class="tag">{T["start"]}</p>{h(sl["title"])}<p class="sit">{sl["text"]}</p><p class="qz">{sl["q"]}</p>'
    elif k == "obj": body = h(sl["title"]) + lead + ul(sl["items"], "obj")
    elif k == "plan": body = h(sl["title"]) + '<ol class="plan">' + "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in sl["items"]) + "</ol>"
    elif k == "pts": body = h(sl["title"]) + lead + fig + wid + ul(sl["items"]) + band
    elif k == "wide": body = h(sl["title"]) + lead + fig + wid + band
    elif k == "cols": body = h(sl["title"]) + lead + '<div class="cards">' + "".join(f'<div class="card"><h4>{a}</h4><p>{b}</p></div>' for a, b in sl["cols"]) + "</div>" + band
    elif k == "eq": body = h(sl["title"]) + lead + (fig if sl.get("figtop") else "") + f'<div class="eqb">{eq_html(sl["tex"])}</div><p class="k">{T["sym"]}</p>' + legend(sl["legend"]) + ("" if sl.get("figtop") else fig) + wid + band
    elif k == "tbl":
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in sl["rows"])
        body = h(sl["title"]) + lead + f'<div class="tw"><table><thead><tr>{"".join(f"<th>{c}</th>" for c in sl["head"])}</tr></thead><tbody>{rows}</tbody></table></div>' + band
    elif k == "st": body = f'<p class="stt">{sl["text"]}</p><p class="lead">{sl["sub"]}</p>'
    elif k == "nums": body = h(sl["title"]) + lead + '<div class="nums">' + "".join(f'<div><p class="bn">{a}</p><p>{b}</p></div>' for a, b in sl["nums"]) + "</div>" + band
    elif k == "code": body = h(sl["title"]) + lead + f'<div class="tw"><pre><code>{html.escape(sl["code"], quote=False)}</code></pre></div>' + ul(sl["items"])
    elif k == "ex":
        m = sl["meta"]; meta = " · ".join(f'{T[a]} : {m[a]}' if S.lang == "fr" else f'{T[a]}: {m[a]}' for a in ("time", "mat", "out") if a in m)
        return f'<section class="blk ex"><p class="tag">{T["ex"]}</p>{h(sl["title"])}<ol class="steps">' + "".join(f"<li>{s}</li>" for s in sl["steps"]) + f'</ol><p class="meta">{meta}</p></section>'
    elif k == "sol":
        return f'<details class="blk sol"><summary>{SHOW[S.lang]}</summary>{fig}{ul(sl["items"])}{band}{say}</details>'
    elif k == "quiz":
        qs = ""
        for j, (q, opts, ok, why) in enumerate(sl["items"]):
            ob = "".join(f'<button type="button" class="qopt" data-i="{a}">{"ABCD"[a]}. {o}</button>' for a, o in enumerate(opts))
            qs += f'<div class="qcard" data-ok="{ok}"><p class="qq">{j + 1}. {q}</p><div class="qopts">{ob}</div><p class="qwhy" hidden>{why}</p></div>'
        return f'<section class="blk"><p class="tag">{sl["title"]}</p><p class="lead">{sl["lead"]}</p><div class="quiz">{qs}</div></section>'
    elif k == "take": body = h(sl["title"]) + '<ol class="take">' + "".join(f"<li>{i}</li>" for i in sl["items"]) + "</ol>"
    elif k == "refs": return f'<section class="blk">{h(sl["title"])}{ul(sl["items"], "refs")}</section>'
    else: raise ValueError(k)
    return f'<section class="blk">{body}{say}</section>'

def session_html(S):
    deck = f"https://claude.ai/artifact/{DECKS[S.n - 1]}"
    lab = "Diapositives de la séance" if S.lang == "fr" else "Slides for this session"
    head = (f'<header class="sh"><p class="tag">{S.part} · {S.T["sess"]} {S.n} {S.T["of"]} {S.total}</p><h2>{S.title}</h2><p class="lead">{S.sub}</p>'
            f'<p><a class="btn" href="{deck}">{lab}</a></p></header>')
    nxt = ""
    if S.n < S.total:
        nxt = f'<p class="next"><a class="btn" href="#session-{S.n + 1}">{"Séance suivante" if S.lang == "fr" and S.n < 4 else "Next session"} →</a></p>'
    return head + "".join(block(S, sl) for sl in S.slides) + nxt

def data():
    fits = {}
    xs = np.linspace(0.6, 23.2, 120)
    for d in range(1, 10): fits[d] = [round(float(v), 2) for v in np.polyval(a3.FITS[d], a3.sc(xs))]
    r = np.random.default_rng(3); th = r.uniform(0, 2 * np.pi, 90)
    ring = (np.c_[np.cos(th), np.sin(th)] + r.normal(0, 0.06, (90, 2))).round(3).tolist(); eps = r.normal(0, 1, (90, 2)).round(3).tolist()
    return {"a1": {"x": a1.DOSE.tolist(), "y": a1.C0.tolist(), "w": round(float(a1.W), 3), "b": round(float(a1.B), 3)},
            "a2": {"x": a2.D.tolist(), "y": a2.Y.tolist(), "w": round(float(a2.WL), 3), "b": round(float(a2.BL), 3)},
            "a3": {"x": a3.CTR.tolist(), "y": [round(float(v), 2) for v in a3.ETR], "xs": [round(float(v), 2) for v in xs], "fits": fits,
                   "tr": {d: round(a3.TR[d], 2) for d in a3.TR}, "te": {d: round(a3.TE[d], 2) for d in a3.TE}},
            "b2": {"tok": b2.TOK, "sc": b2.SC.tolist()}, "b3": {"sims": b3.SIMS}, "b4": {"ring": ring, "eps": eps}}

def build():
    os.makedirs(f"{OUT}/sessions", exist_ok=True)
    Ss = [importlib.import_module(n).build() for n in ALL]
    for S in Ss:
        json.dump({"n": S.n, "title": S.title, "html": session_html(S)}, open(f"{OUT}/sessions/s{S.n:02d}.json", "w"), ensure_ascii=False)
    cards = lambda part: "".join(
        f'<a class="sc" href="#session-{S.n}"><span class="scn">{S.n}</span><span class="sct"><b>{S.title}</b><span>{S.sub}</span></span></a>' for S in Ss if (S.n <= 4) == part)
    nav = "".join(f'<a href="#session-{S.n}" data-n="{S.n}"><span>{S.n}</span>{S.title}</a>' + ('<p class="navk">Part II · Advanced track (English)</p>' if S.n == 4 else "") for S in Ss)
    tpl = open(f"{HERE}/site_tpl.html").read()
    page = (tpl.replace("/*DATA*/", "const DATA = " + json.dumps(data(), ensure_ascii=False) + ";").replace("<!--NAV-->", nav)
            .replace("<!--PART1-->", cards(True)).replace("<!--PART2-->", cards(False)).replace("/*WIDGETS*/", open(f"{HERE}/widgets.js").read()))
    open(f"{OUT}/index.html", "w").write(page)
    tot = sum(os.path.getsize(f"{OUT}/sessions/{f}") for f in os.listdir(f"{OUT}/sessions"))
    print("index", os.path.getsize(f"{OUT}/index.html") // 1024, "KB; sessions", tot // 1024, "KB")

if __name__ == "__main__":
    build()
