# DetectiveGirl

A browser detective game with maths for kids around age 11. Eleven cases, each with suspects or competing theories, a false trail, an evidence notebook, hints and an explanation for every wrong answer.

Play it here: https://shumer.github.io/DetectiveGirl/

## Languages

The start screen offers **Русский / Polski / English / Українська**. The interface, story, tasks, hints, feedback and endings are all translated. You can switch language mid-game: answers and the current step are kept. The chosen language is remembered in this browser. Reloading the page restarts the investigation.

## Running locally

Requires Node.js 24 and npm.

```sh
npm ci
npm run dev
```

```sh
npm test
npm run lint
npm run build
npm run preview
```

The build lands in `dist/`. It is a static site: no server, API keys or accounts are needed. Relative paths let the game live in a GitHub Pages subfolder.

## GitHub Pages

In the `shumer/DetectiveGirl` repository choose **Settings → Pages → Build and deployment → Source: GitHub Actions**. Every push to `main` runs `.github/workflows/pages.yml`, which tests, builds and deploys `dist/`.

The site is published at https://shumer.github.io/DetectiveGirl/ . Free GitHub Pages requires a public repository.

Build reference: https://vite.dev/guide/static-deploy.html#github-pages

## Start screen

The start screen is a gallery of case cards: scene image, number, title, a one-line teaser and the status. Solved cases are marked with the number of mistakes; that progress is stored in the browser only. Choosing a card opens the case briefing with the “Accept the case” button, and every screen has a link back to the gallery.

## Content

Eleven cases: the golden owl, the forest lanterns, a parcel for Cloud Island, the museum of mixed-up shadows, the Moon greenhouse, the theatre of the lost finale, the aquarium bubbles, the moon cookie bakery, the lighthouse tune, two bookmarks in a library and the park parade. Each has four connected steps, three hints per step, feedback for every wrong option, a mistake counter, a findings notebook and an ending. The maths is roughly fifth grade: clock corrections in both directions, time gaps against walking times, map scale, speed and distance, fractions of a whole, timetables with intervals. The difficulty rules live in `docs/difficulty.ru.md`.

- `app/page.tsx` - case and language selection, scene styling.
- `app/CaseGallery.tsx` - the start screen with case cards.
- `app/RevisionCase.tsx` - the shared game interface.
- `app/progress.ts` - solved-case storage and card teasers.
- `app/revision-game.ts` - answer validation and the rating at the end.
- `app/revised/*.json` - the playable cases in all four languages.
- `docs/stories.ru.md` - all eleven scripts in Russian, generated from the JSON.
- `docs/difficulty.ru.md` - difficulty and mechanics rules (Russian).
- `scripts/backgrounds.py` - generates the stylised SVG backgrounds for cases 005-011 until painted artwork exists (see `docs/art-direction.ru.md`).
- `tests/revision.test.ts`, `tests/reviewed-content.test.ts` - answer validation, structure and translation consistency, hints that do not leak the answer, background assets.

Answer kinds: single choice (at least four options), multi-select, ordering cards, a number and a time. After two wrong answers in a row on a step, the next hint opens by itself.

The original prototype was built for Sites. This version is a static Vite + React + TypeScript build without the Sites server configuration. The original template's dependencies are kept in the lockfile.

## Backgrounds and music

Colours and illustrations change with the location. Cases 001-004 have painted backgrounds; cases 005-011 use generated SVG scenes for now. Settings are in `app/themes.ts`; art direction and scene briefs are in `docs/art-direction.ru.md`. The track Sneaky Snitch plays by default at 18% volume, loops, and pauses when the tab is hidden. If the browser blocks autoplay, playback starts on the first tap or key press. A button turns the music off. Credit and licence are shown in the interface and in `MUSIC-LICENSE.md`. All audio and backgrounds ship with the build; no external players are used.

## Story structure

Every step shows the known facts and one concrete question. After answering, the player gets an explanation, a notebook entry and the next action. Guesses are kept apart from confirmed facts, and having no alibi is never treated as proof. Times, routes and constraints are given before the solution, and the ending relies only on what was collected.
