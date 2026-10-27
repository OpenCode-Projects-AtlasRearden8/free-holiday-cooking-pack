# STATUS

Feast Without Dread — free holiday cooking printables pack
(Built for Asdale Dynamics, LLC; project status as of Oct 27, 2026)

## What was built

Seven complete printable PDF sheets for cooking a big family meal without panic.
Each sheet is plain HTML/CSS under `sheets/` and builds to an unbranded PDF in
`printables/`. Every PDF opens with a warm, sheet-specific "Getting started"
page (what it's for, three steps to use it, print tips) followed by the usable
pages. No branding, no signups, no emails anywhere inside the PDFs.

1. `01-potluck-signup.pdf` — potluck sign-up grid by category, plus a
   coordinator page (copy-paste invite blurb, week-of confirmation checklist,
   arrivals & appliance-need table). 3 pages.
2. `02-shopping-by-aisle.pdf` — one-minute quantity planner (guests, turkey
   size, potatoes, pies, butter) and a store-order mega list: produce, meat,
   dairy & eggs, bakery, pantry & canned, spices & baking, frozen, drinks,
   paper & household, plus a backup-plan box. 4 pages.
3. `03-thawing-safety-card.pdf` — fridge-hangable card: never-on-counter rule,
   three safe thaw methods (fridge / cold water / microwave) with USDA weight
   tables, safe-and-not-safe list, and a thaw-day worksheet with quick
   answers (07 am rescues included). 3 pages.
4. `04-turkey-timing-chart.pdf` — 325°F roasting table (USDA stuffed and
   unstuffed times) with a "dinner at 4:00 pm → start about" column, the
   start-time math box, oven-notes table, and a trust page (thermometer
   placement, 165°F temps, 20–30 min rest, running-late playbook). 3 pages.
5. `05-hours-back-countdown.pdf` — hour-back countdown blocks from
   "day before" to "T+30 min (after)" with pre-printed moves and checkboxes,
   plus oven/stove traffic-control grid and "if things slip" recovery tips.
   3 pages.
6. `06-dietary-dish-cards.pdf` — six cut-out buffet truth tags (contains /
   friendly-for / serving-spoon number), allergy-smart swaps table,
   read-the-label watchlist, cross-contact care, and four spare small cards.
   3 pages.
7. `07-leftover-labels.pdf` — twelve cut-out labels (dish, made-on, use-by,
   freeze flag, reheat notes) plus the USDA-based keep-or-toss table and a
   leftover-station checklist. 3 pages.

Supporting files:

- `build.sh` — the one build script. Cleans `printables/`, renders every
  `sheets/*.html` to PDF (Google Chrome/Chromium headless with automatic
  WeasyPrint fallback), and validates every PDF before exiting green.
- `tests/run_tests.sh` — full test suite (3 stages: fresh build, PDF
  re-validation, pack-wide checks).
- `tests/validate.py` — per-PDF validation (header, trailer, pypdf open,
  page count); also usable standalone on any PDF folder.
- `tests/checks.py` — pack-wide: sheet↔PDF mapping, getting-started page
  text on page 1 of every PDF, unbranded guarantee ("Asdale"/domain absent
  from all PDF text), exact LICENSE copyright line, README credit, and a
  no-credentials scan over all source files.
- `README.md`, `LICENSE` (MIT, Copyright (c) 2026 Asdale Dynamics, LLC),
  `.gitignore` (generated `printables/` PDFs stay out of git; rebuild via
  `./build.sh`).

## How to run

```sh
./build.sh                 # build all PDFs into printables/
bash tests/run_tests.sh    # build + validate + 59 pack-wide checks
```

Requirements: Google Chrome/Chromium (primary) or WeasyPrint (fallback,
`python3 -m pip install weasyprint`); Python 3 with `pypdf` for validation.

## Verification results (actual, from the final run)

- `build.sh`: renderer = chrome (google-chrome, Chrome 156.0.8078.47); all 7
  sheets rendered.
- `tests/validate.py`: `all 7 PDFs valid` —
  01 (3 pages, 160 KB), 02 (4 pages, 179 KB), 03 (3 pages, 169 KB),
  04 (3 pages, 179 KB), 05 (3 pages, 116 KB), 06 (3 pages, 200 KB),
  07 (3 pages, 188 KB).
- `tests/checks.py`: `59 of 59 checks passed` (sheet↔PDF mapping, per-PDF
  page-1 "Getting started", unbranded guarantees, LICENSE exact line,
  README credit, credential scan).
- Full suite output ends with: `ALL TESTS PASSED`.
- Fallback renderer verified outside the default path: all 7 sheets also
  render green under WeasyPrint 70.0 (files opened, page counts 3–4).
- Visual QA: every rendered page was rasterized and inspected; page breaks,
  cut-lines, fill-blanks, and stack overflow issues found on the first pass
  were fixed (table compaction and a deliberate 4-page layout for the
  shopping list), then re-rendered and re-checked.

## Fixed along the way

- Seven sheets initially overflowed their designed page counts; page 2 tables
  were compacted (`.compact` styles) and the shopping list was rebalanced
  into deliberate pages (intro + planner/produce/meat, dairy/bakery/pantry,
  spices/frozen/drinks/paper + backup plan).
- Test-harness bug: a tuple-expression precedence error in `checks.py`
  (`print(...).rstrip()` on a tuple) — fixed to parenthesized format.
- Food-safety figures verified against USDA/FSIS pages at build time:
  325°F roasting tables, 165°F minimum internal temperature, 20-minute
  rest, fridge thaw of 24 h per 4–5 lb (weight brackets), cold-water thaw
  of 30 min per lb, 2-hour rule, 3–4-day leftovers (gravy 1–2 days),
  reheat to 165°F / rolling boil for gravy, cooking-from-frozen +50% time.

## Known gaps

- Page-fit is tuned for the primary renderer (Chrome). Under the WeasyPrint
  fallback, three sheets (01, 04, 05) gain one overflow page; still valid,
  but a hair less tidy.
- Label/card tiles are printer-friendly dashed cut-outs, not pre-positioned
  Avery/OfficeMax template grids (no adhesive-sheet alignment).
- US-centric units and defaults (US Letter, °F, pounds); an A4/°C variant
  would be a nice follow-up.
- No automated visual regression (images aren't diffed across rebuilds);
  page-overflow is only caught by manual/eyeball review or the page-count
  expectations in this file.
- Content is educational and USDA-aligned, not professional food-service or
  medical advice (stated inside the PDFs as well).
- No website/landing page; PDFs are produced locally by design.
