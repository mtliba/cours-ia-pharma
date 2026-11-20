# Instructions for Claude Code

This repository holds three university courses written by Marouane Tliba (Inserm U1248, Université de Limoges)
as his teaching project (projet pédagogique). Your job here is to keep improving the three courses and the
page that introduces them. Read this file, then the README of the axis you
are asked to work on.

## The three courses

| Folder | Course | Audience | Language | State in this repository |
| --- | --- | --- | --- | --- |
| `axe2/` | Programmation et analyse de données, 4 sessions of 2 h | pharmacy students who have never programmed | French | built site only (slides and notes inside) |
| `axe3/` | IA pour les sciences pharmaceutiques, 10 sessions | sessions 1–4 everyone; 5–10 research master's, PhD students, researchers | French 1–4, English 5–10 | full Python source, built decks, built site |
| `axe4/` | IA responsable et santé numérique, 7 sessions for video | pharmacy students | French | built site only (slide HTML and word-for-word notes inside) |

The three courses share one example: therapeutic drug monitoring of tacrolimus after kidney transplantation.
Axis 2 provides the data (40 fictitious patients, 6 visits), Axis 3 builds models on it, Axis 4 assesses a
fictitious alert tool ("TacroAlerte") on a seven-line form. Keep that thread and keep the numbers consistent
with what earlier sessions already showed.

`index.html` at the root introduces the three courses. It is generated: edit `tools/make_index.py`, never the
HTML. Session titles and slide counts are listed at the top of that script; update them when a course changes.

## Commands

```bash
python3 -m http.server 8000            # view everything at http://localhost:8000/ (fetch needs a server)
python3 tools/make_index.py            # rebuild the landing page

cd axe3
npm install                            # once: fonts for the local test pages
python3 src/build.py                   # all ten decks + checks; must end with "overflow: none" for each
python3 src/build.py b3 --shots        # one deck, plus one PNG per slide in test/b3/
(cd src && python3 sheet.py b3)        # contact sheet of those PNGs
python3 src/site.py                    # rebuild the Axis 3 site from the same sessions
python3 src/sitetest.py                # browser smoke test of the site
```

Python needs `numpy`, `matplotlib`, `pillow`, `playwright` (`pip install -r requirements.txt`). The checks use
Google Chrome if it is installed, otherwise Playwright's Chromium (`python3 -m playwright install chromium`);
set `CHROME=/path/to/chrome` to force one. `axe3/test/` and `node_modules/` are not versioned.

## How Axis 3 is written

One Python file per session (`axe3/src/a1.py` … `a4.py` in French, `b1.py` … `b6.py` in English). Each exposes
`build() -> Session`. The same `Session` produces the slide deck and the page of the site, so text is written
once. Never edit `axe3/out/` or `axe3/site/` by hand: change the source and rebuild both.

`Session(n, lang, part, title, sub)` then one call per slide. The last argument `n` is always the speaker
notes (the text to say). Slide kinds, all in `src/lib.py`:

- structure: `sec(desc)` starts a section, `cover`, `sit` (starting situation and question), `obj`, `plan`, `st` (one-sentence statement), `take` (key points), `refs`, `end`;
- content: `pts` (points, optional `fig=`), `cols`, `tbl`, `nums`, `wide` (full-width figure), `eq` (formula with a legend that explains every symbol), `code`;
- practice: `ex` (exercise), `sol` (its correction), `quiz` (three questions: `(question, options, index_of_right_answer, why)`).

Figures are drawn with `Fig(w, h, alt)`: SVG shapes plus HTML labels (`lab`, `labc`, `box`, `axes`, `curve`,
`dots`, `arrow`). Equations go through `mathsvg.math_svg` (matplotlib mathtext, Computer Modern) and become
SVG paths, so there is no math library at display time; use `\dfrac` for display fractions. Numbers shown on a
slide are computed in the session file with numpy from a fixed seed: when you change data, recompute, do not
type a number by hand, and make sure the sentence around it is still true.

The interactive figures of the site are in `src/widgets.js`; `WIDGETS` in `src/site.py` attaches one to a
slide by `(session number, slide title)`, so renaming that slide requires updating the map.

Limits enforced by the deck format (the build asserts or reports them): 1920 × 1080 canvas, one `<section>`
per slide, notes ≤ 4000 characters, no `<text>` inside SVG (labels are HTML), ≤ 23 labels per figure, SVG
≤ 52 KB, ≤ 200 elements per slide, click steps with `class="fragment"`.

## How Axes 2 and 4 are stored

Their generators were not kept; the repository has the finished sites.

- Axis 2: `axe2/site/seances/sN.html` holds 30 `<section data-id="sNN">` slides per session with the notes in
  `<aside>`; `data-fig` marks an interactive figure implemented in `site.js`, `data-answer` a question.
  `data.json` holds the session outline and the 230 rows of the data set.
- Axis 4: `axe4/site/decks/seanceN.json` holds `{"n", "sections", "slides": [{"title", "html", "notes"}]}`;
  `index.html` is a single-file site that renders them.

For a small change, edit those files directly and reload. For a large rewrite, first port the course to the
Axis 3 pipeline (a `Session` per session, reusing `lib.py` and `deck.css`), then rebuild. Ask before doing
that port: it changes the look of Axis 2, which currently has its own design.

## Writing rules (the author's standing requests)

- Write for the student in the room. Plain, concrete sentences; define a term the first time it appears; one idea per slide.
- No "AI style": no slogans, no decorative triads, no rhetorical questions followed by their answer, no em-dash asides, no filler such as "il est important de noter".
- Many figures. A notion that has a shape (a curve, a pipeline, a table) gets a figure, and the figure carries real computed values.
- Every formula is followed by the meaning of each symbol and by a worked number.
- Each session keeps the same progression: situation, objectives, plan, notions, a real example when one exists, one exercise with its correction, three quiz questions, key points, references.
- Sessions 1–4 of Axis 3, all of Axes 2 and 4: French, with French typography (non-breaking space before `: ; ? !`, decimal comma, « »). Sessions 5–10 of Axis 3: English, researcher level (representation learning, generative models, foundation models), still with everything explained.
- Notes are a script to read aloud at about 150 words per minute. Axis 4 targets 20 minutes per video and is currently at 10–12.
- Fictitious patients, tools and thresholds must be labelled as fictitious or illustrative on the slide where they appear.
- A reference goes on a slide only with its DOI checked against the publisher or PubMed. The axis READMEs list which references are verified and which are still cited from memory; update those lists when you check one. Do not add a citation you have not opened.

## Design

Axes 3 and 4 and the landing page: white paper, navy ink `#101B3F`, blue `#2A46C8` for what is being shown,
red `#D22B3A` for the error only, grey `#5A6379`, rule `#D9DDE6`, pale blue `#E9EDFB`, pink `#FBE6E8`, amber
`#C77700`. Source Sans 3 for text, Caveat only for what is added by hand during the lesson (corrections,
annotations, worked numbers), JetBrains Mono for code. Blue slides for the opening, the exercises and the end.
Axis 2 uses Bricolage Grotesque and IBM Plex with teal and orange.

## Before you say a change is done

1. `python3 src/build.py` reports `overflow: none` for every deck you touched, and you have looked at the
   slides you changed (`--shots`, then open the PNGs): overlapping labels do not show up in the automatic check.
2. `python3 src/site.py` then `python3 src/sitetest.py` runs clean (a favicon 404 is expected).
3. `python3 tools/make_index.py` if titles, counts or links changed, and the landing page still opens every session.
4. The README of the axis reflects what changed (session table, verified references, open points).

## Open points

- Click steps and fonts of the decks were only checked on local renders, never in the presentation mode of the claude.ai Slides pages.
- The decks on claude.ai are published copies of `axe3/out/` and of the Axis 4 slides; they cannot be updated from here. After a change, the sites in this repository are the up-to-date version.
- Axis 2: the four PowerPoint files used in class and the two CSV files are not in the repository.
- Axis 4: `kit-youtube.md` and `texte-a-dire.md` are not in the repository; session 6 needs a legal read; session 5 needs a check against the current ANSM Thesaurus.
- Axis 3: references cited from memory to verify; the two Woillard et al. examples to be read by their authors; session 10's causality part to be built with a biostatistician; speech is 9–15 minutes per session.
- No licence chosen yet.
