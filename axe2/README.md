# Axe 2 — Programmation et analyse de données

Four sessions of 2 h (lecture and practical in one), 30 slides each, in French, with speaker notes.
Running example: a fictitious tacrolimus monitoring data set (40 simulated patients, 6 visits, 230 measurements).

| Session | Title | Content |
| --- | --- | --- |
| 1 | Du tableur au notebook : premiers pas en Python | Limits of the spreadsheet, notebook, variables, lists, dictionaries, conditions, loops, functions, a test on a hand-computed case (Cockcroft-Gault) |
| 2 | Manipuler un jeu de données avec pandas | Reading a French CSV, selecting, filtering, sorting, cleaning (duplicates, missing values, implausible values, codings), cleaning log, groupby, merge |
| 3 | Visualiser et explorer les données | Choosing a figure, histogram, box plots, scatter plot, curves, between- and within-patient variability, misleading figures, checklist |
| 4 | Analyse reproductible et usage critique des assistants d'IA | Project layout, paths, versions, random seed, typical assistant errors, checking by test, protecting health data, final mini-project |

## Files

```
site/index.html      shell of the site (home page with the 40-patient chart, "Lire" and "Présenter" modes)
site/site.js         routing (#seance-1 … #seance-4), presentation mode, the nine interactive figures, the Run button on code
site/slides.css      slide styles
site/seances/sN.html one file per session: 30 <section data-id="sNN"> slides, notes in <aside>,
                     data-fig="…" marks an interactive figure, data-answer marks a question with its answer
site/data.json       {"seances": [...titles, parts...], "rows": [{p, j, d, c, g}]}  patient, day, dose (mg/d), C0 (ng/mL), CYP3A5 group
site/figs/*.png      the 12 charts of session 3, produced by the course code
```

This folder is the built site exported from https://claude.ai/artifact/TmJSX7ddsTNtPRpFU7vvMN (19 Nov 2026).
The script that generated it is not in the repository. To change a slide, edit `site/seances/sN.html` directly.

Not in the repository:

- the four PowerPoint files (`Seance1_Du_tableur_au_notebook.pptx`, `Seance2_Manipuler_un_jeu_de_donnees.pptx`,
  `Seance3_Visualiser_et_explorer.pptx`, `Seance4_Reproductibilite_et_assistants_IA.pptx`), which are the
  version used in class; put them in `axe2/pptx/` if they should be versioned here;
- the course data files `suivi_tacrolimus.csv` and `patients.csv` (the same data are in `site/data.json`).

An earlier version exists as slide decks on claude.ai (older text, fewer figures): session 1
https://claude.ai/artifact/6vDFF3yiqeF6Hr1ALz2Yfr · 2 https://claude.ai/artifact/FnDSq4cwUoqbdCuwcghTuw ·
3 https://claude.ai/artifact/TD6defFp9FiSZAAUb3jKHA · 4 https://claude.ai/artifact/CN9xEUGYrpG9DL5Er4Sy7W

## To check before use

- The teacher's notes are readable by anyone who opens the site.
- To adapt: the faculty's notebook environment, the AI tools the institution allows, the 5–10 ng/mL target
  (illustrative), the time per part.
- This site uses its own look (Bricolage Grotesque and IBM Plex, teal and orange), different from Axes 3 and 4.
