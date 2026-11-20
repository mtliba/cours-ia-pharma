"""Build the landing page that introduces the three courses.

    python3 tools/make_index.py            -> index.html   (links to the sites in this repository)
    python3 tools/make_index.py --online   -> index.online.html (links to the pages hosted on claude.ai)

The figure at the top is drawn from axe2/site/data.json (the fictitious tacrolimus follow-up
data set shared by the three courses), so it never drifts from the data the students use.
"""
import json, os, statistics, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONLINE = "--online" in sys.argv

SITES = {
    "axe2": ("axe2/site/index.html", "https://claude.ai/artifact/TmJSX7ddsTNtPRpFU7vvMN"),
    "axe3": ("axe3/site/index.html", "https://claude.ai/artifact/NSzqhKifpPG5cRPRf7MtSV"),
    "axe4": ("axe4/site/index.html", "https://claude.ai/artifact/TEA2LgQfeUZURtT8uZePMR"),
}
TARGET = ' target="_blank" rel="noopener"' if ONLINE else ""


def url(axe, frag=""):
    return SITES[axe][1 if ONLINE else 0] + frag


# ---------------------------------------------------------------- content
AXE2 = [
    ("Du tableur au notebook : premiers pas en Python", 30),
    ("Manipuler un jeu de données avec pandas", 30),
    ("Visualiser et explorer les données", 30),
    ("Analyse reproductible et usage critique des assistants d’IA", 30),
]
AXE3_I = [
    ("Apprendre à partir de données", 19),
    ("Prédire : régression, classification et arbres", 20),
    ("Généraliser : surapprentissage et évaluation", 19),
    ("Réseaux de neurones et apprentissage profond", 21),
]
AXE3_II = [
    ("Optimization and generalization in deep networks", 24),
    ("Attention and transformers", 23),
    ("Representation learning and self-supervision", 26),
    ("Deep generative models", 25),
    ("Foundation models and adaptation", 24),
    ("Multimodal and longitudinal health data: from models to decisions", 25),
]
AXE4 = [
    ("Lire une étude d’IA en santé", 28),
    ("Mesurer la performance", 28),
    ("Biais et équité", 25),
    ("Incertitude et calibration", 23),
    ("IA générative et information sur le médicament", 25),
    ("Données de santé et cadre réglementaire", 25),
    ("Supervision humaine et responsabilité", 24),
]
N_SESS = len(AXE2) + len(AXE3_I) + len(AXE3_II) + len(AXE4)
N_SLIDES = sum(n for _, n in AXE2 + AXE3_I + AXE3_II + AXE4)


def sessions(axe, items, start=1, frag="#seance-", unit="diapositives", lang=None):
    out = []
    for i, (t, n) in enumerate(items, start):
        la = f' lang="{lang}"' if lang else ""
        out.append(
            f'<li><a href="{url(axe, frag + str(i))}"{TARGET}><span class="n">{i}</span>'
            f'<span class="t"{la}>{html.escape(t, quote=False)}</span><span class="m">{n} {unit}</span></a></li>'
        )
    return "\n".join(out)


# ---------------------------------------------------------------- figure
def figure():
    rows = json.load(open(f"{ROOT}/axe2/site/data.json", encoding="utf-8"))["rows"]
    days = sorted({r["j"] for r in rows})
    W, H, x0, x1, y0, y1, ymax = 620, 372, 54, 600, 18, 318, 26.0
    X = lambda j: x0 + 22 + (x1 - x0 - 44) * days.index(j) / (len(days) - 1)
    Y = lambda c: y1 - (y1 - y0) * c / ymax
    by = {}
    for r in rows:
        by.setdefault(r["p"], []).append((r["j"], r["c"]))
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="figt figd">',
         '<title id="figt">Concentration résiduelle de tacrolimus de 40 patients fictifs, de J7 à J180</title>',
         '<desc id="figd">Une courbe par patient, la médiane en trait épais et la zone cible de 5 à 10 ng/mL. '
         'Les concentrations sont dispersées la première semaine, puis se resserrent vers la cible.</desc>',
         f'<rect x="{x0}" y="{Y(10):.1f}" width="{x1 - x0}" height="{Y(5) - Y(10):.1f}" class="band"/>']
    for v in (0, 5, 10, 15, 20, 25):
        s.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="grid"/>')
        s.append(f'<text x="{x0 - 10}" y="{Y(v) + 5:.1f}" class="tick" text-anchor="end">{v}</text>')
    for j in days:
        s.append(f'<text x="{X(j):.1f}" y="{y1 + 24}" class="tick" text-anchor="middle">J{j}</text>')
    for p, pts in sorted(by.items()):
        pts.sort()
        d = " ".join(f"{X(j):.1f},{Y(c):.1f}" for j, c in pts)
        s.append(f'<polyline points="{d}" class="pat"/>')
    med = [(j, statistics.median(r["c"] for r in rows if r["j"] == j)) for j in days]
    s.append('<polyline points="' + " ".join(f"{X(j):.1f},{Y(c):.1f}" for j, c in med) + '" class="med"/>')
    for j, c in med:
        s.append(f'<circle cx="{X(j):.1f}" cy="{Y(c):.1f}" r="4.5" class="medp"/>')
    s.append(f'<text x="{x0 + 4}" y="{y0 - 4}" class="axl">C0 (ng/mL)</text>')
    s.append(f'<text x="{x1}" y="{H - 6}" class="axl" text-anchor="end">visite après la greffe</text>')
    # handwritten annotations
    s.append(f'<text x="{X(180) - 4:.1f}" y="{Y(5) + 26:.1f}" class="hand amber" text-anchor="end">cible : 5 à 10 ng/mL</text>')
    mj, mc = med[3]
    s.append(f'<path d="M{X(60) + 62:.1f},{Y(17.2):.1f} Q{X(60) + 30:.1f},{Y(15.5):.1f} {X(60) + 8:.1f},{Y(mc) - 8:.1f}" class="arr"/>')
    s.append(f'<text x="{X(60) + 66:.1f}" y="{Y(17.2) + 6:.1f}" class="hand">médiane</text>')
    s.append("</svg>")
    n_pat = len(by)
    return "\n".join(s), n_pat, len(rows), med


FIG, N_PAT, N_ROWS, MED = figure()
fr = lambda v: f"{v:.1f}".replace(".", ",")

PAGE = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trois cours : données, modèles, évaluation de l’IA en pharmacie</title>
<meta name="description" content="Trois cours qui se suivent : programmation et analyse de données, IA pour les sciences pharmaceutiques, IA responsable et santé numérique.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
:root{{--ink:#101B3F;--blue:#2A46C8;--red:#D22B3A;--mute:#5A6379;--rule:#D9DDE6;--pale:#E9EDFB;--amber:#C77700;--paper:#fff;--soft:#F6F7FB}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 18px/1.55 "Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif}}
a{{color:var(--blue)}}
a:focus-visible{{outline:3px solid var(--blue);outline-offset:3px;border-radius:4px}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 28px}}
header.top{{border-bottom:1px solid var(--rule)}}
header.top .wrap{{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-top:16px;padding-bottom:16px;font-size:15px;color:var(--mute)}}
header.top nav{{display:flex;gap:22px}}
header.top nav a{{color:var(--ink);text-decoration:none;font-weight:600}}
header.top nav a:hover{{color:var(--blue)}}

.hero{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:center;padding:64px 0 40px}}
.tag{{margin:0 0 14px;font-size:14px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--blue)}}
h1{{margin:0;font-size:clamp(38px,5.2vw,60px);line-height:1.04;font-weight:700;letter-spacing:-.015em;text-wrap:balance}}
.lead{{margin:22px 0 0;font-size:21px;line-height:1.5;color:#2B3558;max-width:34em}}
.counts{{display:flex;flex-wrap:wrap;gap:10px 34px;margin:30px 0 0;padding:0;list-style:none}}
.counts li{{font-size:15px;color:var(--mute)}}
.counts b{{display:block;font-size:30px;line-height:1.1;color:var(--ink);font-variant-numeric:tabular-nums}}

figure{{margin:0}}
figure svg{{display:block;width:100%;height:auto}}
figcaption{{margin-top:8px;font-size:15px;color:var(--mute)}}
.band{{fill:var(--amber);opacity:.13}}
.grid{{stroke:var(--rule);stroke-width:1}}
.tick{{font-size:13px;fill:var(--mute);font-variant-numeric:tabular-nums}}
.axl{{font-size:13px;fill:var(--mute)}}
.pat{{fill:none;stroke:var(--blue);stroke-width:1.5;opacity:.24;stroke-linejoin:round}}
.med{{fill:none;stroke:var(--ink);stroke-width:4;stroke-linejoin:round;stroke-linecap:round}}
.medp{{fill:var(--paper);stroke:var(--ink);stroke-width:3}}
.hand{{font-family:Caveat,cursive;font-weight:700;font-size:23px;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}}
.hand.amber{{fill:var(--amber)}}
.arr{{fill:none;stroke:var(--ink);stroke-width:1.6;stroke-linecap:round}}

.thread{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin:8px 0 0;padding:0;list-style:none;border-top:2px solid var(--ink)}}
.thread li{{padding:20px 26px 6px 0;position:relative}}
.thread li+li{{padding-left:26px;border-left:1px solid var(--rule)}}
.thread a{{color:inherit;text-decoration:none;display:block}}
.thread .k{{font-size:14px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--blue)}}
.thread .v{{display:block;margin-top:4px;font-size:25px;font-weight:700;line-height:1.15}}
.thread .d{{display:block;margin-top:8px;font-size:17px;color:#2B3558}}
.thread a:hover .v{{color:var(--blue)}}

.course{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;padding:64px 0;border-top:1px solid var(--rule);margin-top:56px}}
.course+.course{{margin-top:0}}
h2{{margin:0;font-size:clamp(28px,3.4vw,38px);line-height:1.12;font-weight:700;letter-spacing:-.01em;text-wrap:balance}}
.c-lead{{margin:16px 0 0;color:#2B3558}}
dl.facts{{margin:22px 0 0;display:grid;grid-template-columns:auto 1fr;gap:6px 18px;font-size:16px}}
dl.facts dt{{color:var(--mute)}}
dl.facts dd{{margin:0}}
.btn{{display:inline-block;margin-top:26px;padding:12px 22px;border-radius:8px;background:var(--blue);color:#fff;font-weight:700;text-decoration:none}}
.btn:hover{{background:#1F369F}}
.btn span{{display:inline-block;margin-left:8px;transition:transform .15s}}
.btn:hover span{{transform:translateX(3px)}}
.part{{margin:34px 0 6px;font-size:14px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--mute)}}
ol.sessions{{margin:0;padding:0;list-style:none;border-top:1px solid var(--rule)}}
.part:first-child{{margin-top:0}}
ol.sessions a{{display:grid;grid-template-columns:34px 1fr auto;gap:10px;align-items:baseline;padding:13px 6px 13px 0;border-bottom:1px solid var(--rule);color:var(--ink);text-decoration:none}}
ol.sessions a:hover{{background:var(--soft)}}
ol.sessions a:hover .t{{color:var(--blue)}}
ol.sessions .n{{font-weight:700;color:var(--blue);font-variant-numeric:tabular-nums;padding-left:6px}}
ol.sessions .t{{font-weight:600;line-height:1.3}}
ol.sessions .m{{font-size:14px;color:var(--mute);white-space:nowrap}}

.start{{padding:64px 0;border-top:1px solid var(--rule)}}
.start h2{{margin-bottom:22px}}
.paths{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:0;padding:0;list-style:none}}
.paths a{{display:block;height:100%;padding:20px 22px;border:1px solid var(--rule);border-radius:10px;color:var(--ink);text-decoration:none}}
.paths a:hover{{border-color:var(--blue);background:var(--soft)}}
.paths .q{{display:block;font-weight:700;font-size:19px;line-height:1.3}}
.paths .a{{display:block;margin-top:6px;color:var(--blue);font-weight:600}}

footer{{border-top:1px solid var(--rule);padding:30px 0 56px;font-size:15px;color:var(--mute)}}
footer p{{margin:0 0 8px;max-width:60em}}

@media (max-width:880px){{
  body{{font-size:17px}}
  .wrap{{padding:0 20px}}
  header.top nav{{display:none}}
  .hero,.course{{grid-template-columns:1fr;gap:30px}}
  .hero{{padding:40px 0 28px}}
  .course,.start{{padding:44px 0}}
  .thread{{grid-template-columns:1fr}}
  .thread li,.thread li+li{{padding:16px 0;border-left:0}}
  .thread li+li{{border-top:1px solid var(--rule)}}
  .paths{{grid-template-columns:1fr}}
  ol.sessions a{{grid-template-columns:28px 1fr}}
  ol.sessions .m{{grid-column:2}}
}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}.btn span{{transition:none}}}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <span>Marouane Tliba · Inserm U1248 · Université de Limoges</span>
  <nav aria-label="Cours"><a href="#axe2">Axe 2</a><a href="#axe3">Axe 3</a><a href="#axe4">Axe 4</a><a href="#debut">Par où commencer</a></nav>
</div></header>

<main class="wrap">
<section class="hero">
  <div>
    <p class="tag">Projet pédagogique · trois cours</p>
    <h1>Des données aux décisions</h1>
    <p class="lead">Trois cours qui se suivent : programmer et analyser des données, comprendre et construire des modèles d’IA, puis juger si un outil d’IA mérite d’être utilisé en santé. Un même exemple les relie, le suivi du tacrolimus après une greffe rénale.</p>
    <ul class="counts">
      <li><b>3</b>cours</li>
      <li><b>{N_SESS}</b>séances</li>
      <li><b>{N_SLIDES}</b>diapositives</li>
    </ul>
  </div>
  <figure>
    {FIG}
    <figcaption>Le jeu de données commun aux trois cours : {N_PAT} patients fictifs, {N_ROWS} dosages. La médiane passe de {fr(MED[0][1])} ng/mL à J7 à {fr(MED[-1][1])} ng/mL à J180.</figcaption>
  </figure>
</section>

<ol class="thread" aria-label="Ce que chaque cours fait de cet exemple">
  <li><a href="#axe2"><span class="k">Axe 2 · les données</span><span class="v">Lire, nettoyer, tracer</span><span class="d">On part du tableur et on arrive à cette figure, écrite en Python et refaisable par quelqu’un d’autre.</span></a></li>
  <li><a href="#axe3"><span class="k">Axe 3 · les modèles</span><span class="v">Prédire</span><span class="d">De la droite ajustée à douze patients jusqu’aux transformers, aux modèles génératifs et aux modèles de fondation.</span></a></li>
  <li><a href="#axe4"><span class="k">Axe 4 · l’évaluation</span><span class="v">Décider</span><span class="d">Un outil d’alerte fictif est examiné séance après séance, sur une fiche de sept lignes, jusqu’au verdict.</span></a></li>
</ol>

<section class="course" id="axe2">
  <div>
    <p class="tag">Axe 2</p>
    <h2>Programmation et analyse de données</h2>
    <p class="c-lead">Pour qui n’a jamais programmé. Chaque notion est introduite sur le fichier de suivi du tacrolimus : variables et fonctions, lecture et nettoyage d’un tableau, figures, puis analyse reproductible et usage critique des assistants d’IA pour coder.</p>
    <dl class="facts">
      <dt>Format</dt><dd>4 séances de 2 h, cours et TD intégrés</dd>
      <dt>Langue</dt><dd>français</dd>
      <dt>Sur le site</dt><dd>mode lecture et mode présentation, code exécutable, 9 figures à manipuler</dd>
    </dl>
    <a class="btn" href="{url('axe2')}"{TARGET}>Ouvrir le cours<span aria-hidden="true">→</span></a>
  </div>
  <ol class="sessions">
{sessions('axe2', AXE2)}
  </ol>
</section>

<section class="course" id="axe3">
  <div>
    <p class="tag">Axe 3</p>
    <h2>IA pour les sciences pharmaceutiques</h2>
    <p class="c-lead">Deux niveaux. La première partie explique sans prérequis ce qu’est un modèle, comment il apprend et comment savoir s’il généralise. La seconde, en anglais, s’adresse aux étudiants de master recherche, aux doctorants et aux chercheurs. Chaque formule est lue symbole par symbole.</p>
    <dl class="facts">
      <dt>Format</dt><dd>10 séances, avec exercice corrigé et QCM</dd>
      <dt>Langue</dt><dd>français (1 à 4), anglais (5 à 10)</dd>
      <dt>Sur le site</dt><dd>10 figures à manipuler, de la descente de gradient au simulateur pharmacocinétique</dd>
    </dl>
    <a class="btn" href="{url('axe3')}"{TARGET}>Ouvrir le cours<span aria-hidden="true">→</span></a>
  </div>
  <div>
    <p class="part">Partie I · Fondamentaux, tous publics</p>
    <ol class="sessions">
{sessions('axe3', AXE3_I, 1, '#session-')}
    </ol>
    <p class="part" lang="en">Part II · Advanced track, for researchers</p>
    <ol class="sessions" start="5">
{sessions('axe3', AXE3_II, 5, '#session-', 'slides', 'en')}
    </ol>
  </div>
</section>

<section class="course" id="axe4">
  <div>
    <p class="tag">Axe 4</p>
    <h2>IA responsable et santé numérique</h2>
    <p class="c-lead">Pour les étudiants en pharmacie. Un outil fictif, TacroAlerte, prédit le risque de surexposition au tacrolimus. On apprend à lire l’étude qui le présente, à mesurer sa performance, à chercher ses biais, à interroger sa calibration, puis on aborde l’IA générative, le cadre réglementaire et la responsabilité du professionnel.</p>
    <dl class="facts">
      <dt>Format</dt><dd>7 séances courtes, conçues pour la vidéo</dd>
      <dt>Langue</dt><dd>français</dd>
      <dt>Sur le site</dt><dd>exercices corrigés, QCM, simulateur et fiche d’évaluation à remplir</dd>
    </dl>
    <a class="btn" href="{url('axe4')}"{TARGET}>Ouvrir le cours<span aria-hidden="true">→</span></a>
  </div>
  <ol class="sessions">
{sessions('axe4', AXE4)}
  </ol>
</section>

<section class="start" id="debut">
  <h2>Par où commencer</h2>
  <ul class="paths">
    <li><a href="{url('axe2', '#seance-1')}"{TARGET}><span class="q">Je n’ai jamais écrit une ligne de code.</span><span class="a">Axe 2, séance 1</span></a></li>
    <li><a href="{url('axe3', '#session-1')}"{TARGET}><span class="q">Je veux comprendre ce qu’est un modèle d’IA, sans programmer.</span><span class="a">Axe 3, partie I</span></a></li>
    <li><a href="{url('axe3', '#session-5')}"{TARGET}><span class="q">Je fais de la recherche et je veux le niveau avancé.</span><span class="a" lang="en">Axe 3, Part II (in English)</span></a></li>
    <li><a href="{url('axe4', '#seance-1')}"{TARGET}><span class="q">On me propose un outil d’IA et je dois me faire un avis.</span><span class="a">Axe 4, séance 1</span></a></li>
  </ul>
</section>
</main>

<footer><div class="wrap">
  <p>Tous les patients, toutes les mesures et l’outil TacroAlerte sont fictifs. La cible de 5 à 10 ng/mL et les seuils utilisés dans les exemples sont illustratifs et ne constituent pas une recommandation clinique.</p>
  <p>Supports de cours préparés par Marouane Tliba.</p>
</div></footer>
</body>
</html>
"""

out = f"{ROOT}/index.online.html" if ONLINE else f"{ROOT}/index.html"
open(out, "w", encoding="utf-8").write(PAGE)
print(out, len(PAGE) // 1024, "KB;", N_SESS, "sessions,", N_SLIDES, "slides,", N_PAT, "patients,", N_ROWS, "rows; median",
      [(j, round(c, 2)) for j, c in MED])
