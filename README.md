# Feast Without Dread

Free, printable PDF pack for cooking a big family meal without the panic. Seven warm, down-to-earth printables that cover the whole arc of the big-cooking day: plan the potluck, shop by aisle, thaw safely, time the turkey, count backwards to dinnertime, label dishes for dietary needs, and label the leftovers on the way out the door.

A project by Asdale Dynamics, LLC. Built beginner-first: no signups, no accounts, no tracking — just HTML sheets that render to clean, unbranded PDFs on your own machine.

## The seven printables

| # | Sheet | What it solves |
|---|-------|----------------|
| 01 | Potluck Sign-Up Sheet | One master list so guests claim dishes instead of multiplying them, plus a coordinator page with a copy-paste invite blurb and arrivals table |
| 02 | Shopping-by-Aisle Mega List | Grocery trip grouped the way stores actually are, with a one-minute quantity planner and a calm backup-plan box |
| 03 | Turkey Thawing Card | Fridge-hangable card with the three safe thaw methods, weight tables, and a thaw-day worksheet |
| 04 | Turkey Timing Chart | USDA-based 325°F roasting times (stuffed and unstuffed) with a "when do I actually start?" column for a 4:00 pm dinner |
| 05 | Hours-Back Countdown Plan | The whole cooking day as one column of hour-back blocks — one move at a time, with oven/stove traffic control |
| 06 | Dietary Dish Cards | Cut-out buffet "truth tags" for allergens and friendly-for diets, plus easy ingredient swap ideas |
| 07 | Leftover Labels | Twelve cut-out labels with use-by fields, plus the keep-or-toss table that settles the fourth-day debate |

Every PDF opens with a friendly "Getting started" page for that exact sheet — what it's for and how to use it in three steps — followed by the printable pages themselves. Nothing in the PDFs is branded; they're yours to print and pass around.

## Build the PDFs yourself

Requirements: any one of the following renders the HTML sheets to PDF.

- Google Chrome or Chromium (recommended, used automatically when present)
- WeasyPrint (`python3 -m pip install weasyprint`) as an automatic fallback

One command builds everything, freshly and locally, into `printables/`:

```sh
./build.sh
```

That's it. No network is used for content, no data leaves your machine, and the script prints a step-by-step log of what it rendered.

## Run the tests

```sh
bash tests/run_tests.sh
```

The test suite builds the pack from scratch, then verifies every sheet produced a valid PDF (loaded with pypdf, at least two pages, correct file mapping), confirms each PDF opens with its getting-started page and stays unbranded, and checks that the pack's docs and hygiene pass (exact license line, README credit, no credential-looking strings anywhere in the sources).

`tests/validate.py` can also be run directly against any folder of PDFs:

```sh
python3 tests/validate.py printables/
```

## Making it yours

Every sheet is plain HTML plus a small shared stylesheet in `sheets/`. Edit any sheet, run `./build.sh`, and your rebuilt PDF lands in `printables/` with the same name. Add your own sheet by dropping a new `.html` file into `sheets/` and following the same page structure; the build and tests pick it up automatically. Print at 100% (Actual Size) on US Letter; everything prints fine in black and white.

## Project layout

```
build.sh          one-command local build (Chrome, with WeasyPrint fallback)
sheets/           7 HTML sources + shared.css
printables/       generated PDFs (rebuilt by ./build.sh)
tests/            run_tests.sh, validate.py, checks.py
```

## Safety notes

The timing, thawing, and storage content follows USDA food-safety basics (325°F roasting tables, 165°F safe minimum internal temperature, the 2-hour rule, and cold-thawing guidance). The pack is educational and friendly — it isn't medical, veterinary, or professional food-service advice, and serious allergies always deserve a direct conversation with the cook.

## License & credits

MIT licensed — free to print, share, adapt, and sell-with-modifications, per `LICENSE` (Copyright (c) 2026 Asdale Dynamics, LLC).

Made with care by Asdale Dynamics, LLC, which publishes beginner-friendly AI guides, books, and practical tools at dylanasdale.github.io by Dylan Asdale. This pack follows the house style: plain English, step by step, never condescending, tested, local-first, and no signups.
