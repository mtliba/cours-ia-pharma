# Axe 3 — IA pour les sciences pharmaceutiques

Ten sessions, 226 slides, two levels:

- **Partie I · Fondamentaux** (sessions 1–4): in French, for everyone, no programming needed.
- **Part II · Advanced track** (sessions 5–10): in English, for research master's students, PhD students and researchers.

Running example: tacrolimus monitoring after kidney transplantation, continuing Axis 2 (the data) and leading
to Axis 4 (assessing a tool).

| # | Source | Title | Slides | Speech | Deck on claude.ai (private until shared) |
| --- | --- | --- | --- | --- | --- |
| 1 | `src/a1.py` | Apprendre à partir de données | 19 | 9 min | https://claude.ai/artifact/Xq6tJhebuf8ArARsj5aXX2 |
| 2 | `src/a2.py` | Prédire : régression, classification et arbres | 20 | 10 min | https://claude.ai/artifact/4NdADrgJEkTtUeWNv89fp1 |
| 3 | `src/a3.py` | Généraliser : surapprentissage et évaluation | 19 | 9 min | https://claude.ai/artifact/Qst4iKHjrY2ek3W8Po4dMF |
| 4 | `src/a4.py` | Réseaux de neurones et apprentissage profond | 21 | 10 min | https://claude.ai/artifact/DzW81LcqgVhyH5LZvt8XVB |
| 5 | `src/b1.py` | Optimization and generalization in deep networks | 24 | 15 min | https://claude.ai/artifact/XuV2c623X6NGzzJn8FS18m |
| 6 | `src/b2.py` | Attention and transformers | 23 | 13 min | https://claude.ai/artifact/DRQkqojLb3opri6GuLrzy6 |
| 7 | `src/b3.py` | Representation learning and self-supervision | 26 | 15 min | https://claude.ai/artifact/BcnMfs9xUFhyqgaEJ3mdyi |
| 8 | `src/b4.py` | Deep generative models | 25 | 15 min | https://claude.ai/artifact/PkJfc22t1g3RFvmSjWykAs |
| 9 | `src/b5.py` | Foundation models and adaptation | 24 | 14 min | https://claude.ai/artifact/X79u9Tt6wchREaG9RLP7DC |
| 10 | `src/b6.py` | Multimodal and longitudinal health data: from models to decisions | 25 | 15 min | https://claude.ai/artifact/9x1yt8pra8k6d4eKwg5mxH |

Interactive site (one view per session, `#session-1` … `#session-10`): `site/`, also at
https://claude.ai/artifact/NSzqhKifpPG5cRPRf7MtSV. Ten figures can be manipulated: adjustable line and gradient
descent (1), logistic curve (2), polynomial degree and overfitting (3), ReLU neuron (4), learning rate (5),
attention (6), contrastive temperature (7), diffusion noising (8), LoRA parameter count (9), pharmacokinetic
simulator (10).

Every session follows the same progression: starting situation, objectives, plan, notions with figures,
formulas with the meaning of each symbol, a real example when there is one, one exercise with its correction,
three quiz questions, key points, references. Sessions 5–10 add a PyTorch code slide. The notes of each slide
hold the text to say, preceded by the number of clicks.

## Files

```
src/lib.py        the slide vocabulary (class Session), the figure helper (class Fig), deck writer, test page
src/mathsvg.py    equations rendered to SVG paths with matplotlib mathtext (no math library at display time)
src/deck.css      slide stylesheet
src/a1.py … b6.py one file per session: build() -> Session, with its figures and the numbers they show
src/build.py      builds out/<name>/project/{deck.json, deck.css, slides/sNN.html} and runs the layout checks
src/site.py       builds site/index.html and site/sessions/sNN.json from the same sessions
src/site_tpl.html site shell          src/widgets.js   the ten interactive figures
src/sitetest.py   browser smoke test  src/sheet.py     contact sheets from test/<name>/sNN.png
out/              built decks (the format of the Slides pages on claude.ai)
site/             built site
```

Commands are in the README at the root of the repository and in `CLAUDE.md`.

## To check before use

- Rendering was checked on a local render of every slide (overflow, figure labels), not in the presentation
  mode of the app: click steps and fonts are to be tested before recording.
- Speech lasts 9 to 15 minutes per session, below the 20-minute target used for Axis 4.
- The numbers of the fictitious examples are computed by the code (fits, training and test errors, attention
  weights, losses, pharmacokinetic simulation). The "double descent" and "label efficiency" figures are
  schematic and labelled as such; the attention weights of session 6 are illustrative.
- References checked in PubMed in November 2026: Woillard et al. 2021 (doi:10.1002/cpt.2123 and
  doi:10.1016/j.phrs.2021.105578), Stokes et al. 2020 (doi:10.1016/j.cell.2020.01.021), Shmatko et al. 2025
  (doi:10.1038/s41586-025-09529-3), Hollmann et al. 2025 (doi:10.1038/s41586-024-08328-6), Janssen et al. 2022
  (doi:10.1002/psp4.12808), Collins et al. 2024 (doi:10.1136/bmj-2023-078378), Abramson et al. 2024
  (doi:10.1038/s41586-024-07487-w), Watson et al. 2023 (doi:10.1038/s41586-023-06415-8), Lin et al. 2023
  (doi:10.1126/science.ade2574), Gómez-Bombarelli et al. 2018 (doi:10.1021/acscentsci.7b00572).
- Cited from memory, not rechecked online: the machine-learning conference papers (NeurIPS, ICML, ICLR, CVPR,
  NAACL, KDD), the arXiv preprints, the textbooks, Kapoor and Narayanan 2023, Belkin et al. 2019,
  Hernán and Robins 2016, Vickers and Elkin 2006.
- The two examples from the unit (Woillard et al.) are presented from their published abstracts: to be read by
  their authors before the course is shared.
- Pharmacokinetic parameters, the 15 ng/mL threshold and the 5–10 ng/mL target are illustrative; the simulator
  of session 10 says so on screen.
- Session 10: the part on causality is an introduction; build it with a biostatistician if it is taught.
