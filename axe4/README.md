# Axe 4 — IA responsable et santé numérique

Seven sessions in French for pharmacy students, 178 slides, written to be recorded as videos: the notes of each
slide hold the text to say, word for word, preceded by the number of clicks of the slide.

Running example: a fictitious AI tool, "TacroAlerte" (risk of tacrolimus over-exposure after kidney
transplantation), assessed session after session on a seven-line form; verdict in session 7. All its numbers
are invented and consistent across sessions.

| Session | Title | Slides | Speech (150 words/min) | Deck on claude.ai (private until shared) |
| --- | --- | --- | --- | --- |
| 1 | Lire une étude d'IA en santé | 28 | 12 min 30 | https://claude.ai/artifact/5vtWqaY7vZ4WUhgvFxTqU5 |
| 2 | Mesurer la performance | 28 | 12 min 20 | https://claude.ai/artifact/GQPfygdaLb4AqD5sikev98 |
| 3 | Biais et équité | 25 | 10 min | https://claude.ai/artifact/6VxbQUmWqbNyReYABTkUQX |
| 4 | Incertitude et calibration | 23 | 9 min 40 | https://claude.ai/artifact/PetWaguG6uh4jfhz1bZbBY |
| 5 | IA générative et information sur le médicament | 25 | 10 min | https://claude.ai/artifact/NkiwCUWctKimZjyAEtyHNT |
| 6 | Données de santé et cadre réglementaire | 25 | 10 min 40 | https://claude.ai/artifact/WYTPziaEvzsF915wRP2vfm |
| 7 | Supervision humaine et responsabilité | 24 | 9 min 50 | https://claude.ai/artifact/P5kZRiwCzw6oznW4wa9oU3 |

Each video: starting situation, objectives, plan, a multiple-choice question before the explanation, figures
built click by click, an example brought down to a few patients, two "pause the video" exercises with their
correction, sentences one hears and how to answer them, the form, three quiz questions, key points, end screen.

## Files

```
site/index.html           the student site in one file (one view per session, corrected exercises, quizzes,
                          simulator, the assessment form to fill in); routes #seance-1 … #seance-7 and #fiche
site/decks/seanceN.json   {"n", "sections": [{"start", "label"}], "slides": [{"title", "html", "notes"}]}
                          html is one <section id="sNN"> per slide, 1920 × 1080, same markup as the claude.ai decks
site/decks/deck.css       slide stylesheet (the design Axis 3 reuses)
```

This folder is the built site exported from https://claude.ai/artifact/TEA2LgQfeUZURtT8uZePMR (19 Nov 2026).
The script that generated it is not in the repository; `site/decks/seanceN.json` is the best source for the
slide text and the script to read aloud.

Not in the repository: `kit-youtube.md` (titles, descriptions, chapters, sources) and `texte-a-dire.md` (full
script), both delivered in the conversation where the course was built.

## To check before publishing

- Click steps and animations were checked on a local render only, not in the presentation mode of the app:
  test before recording.
- Speech lasts 10 to 12 minutes per video, below the 20-minute target.
- References checked online in November 2026: Wong 2021, Obermeyer 2019, Sjoding 2020, Zech 2018,
  van der Sijs 2006, article L. 4001-3 of the code de la santé publique, the timetable of the AI regulation.
  Not rechecked: Goddard 2012.
- Session 6: have it read by a lawyer or the data protection officer; recheck the timetable every year. The
  example "480 patients, 9 born the same year, 1 the same day" is an invented order of magnitude.
- Session 5: check the interaction constraint levels against the current ANSM Thesaurus.
