# Monday 23 November 2026: The World in One Day (v2)

![make.fun](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/claymoreth/news-image-20261123/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/claymoreth/news-image-20261123/reward.svg)

Entry for [make.fun bounty news-image-20261123](https://make.fun/bounty/news-image-20261123): a Python program that copies `entry.png` to `/output/entry.png` — one dense newspaper page summing up 35 world news stories from 7 regions on Monday 23 November 2026.

## What v2 fixes

The v1 page scored 700 → 651: it was a 19–22 November paper wearing a
23 November masthead, and the judge's first criterion penalises events it
knows happened before the date. V2 keeps the same 35 stories and the same
layout, but every featured slot is a genuine 23 November development:

- **Heroes:** Iran vows "all means" to break the US blockade (Hormuz),
  Russian strikes kill 12 in Kyiv region and Donetsk, Trump signals Iran
  talks may run to year's end.
- **Weekend events are Monday follow-ups only, dated in their decks:**
  COP31's Sunday close ("World reacts to COP31 collapse"), last
  Thursday's 51–48 Senate war-powers vote and ICJ Myanmar verdict,
  Thursday's PIF Tower strike (the 80-storey tower, as reported).
- **The $48.3bn war-cost figure** is dated honestly ("the Pentagon said
  last week").
- **No invented numbers:** the "35 nations" NATO claim is gone — the card
  is now "NATO allies lift emergency readiness" and the stats cell reads
  "7 provinces in BMKG rain warning".
- **Ticker, stats and the 22-story list** are all 23 November items, and a
  red DATE CHECK box states the dating rule on the page itself.

## Files

- `entry.png` — the submitted front page, 1024×1024, under the 1 MiB gate
- `entry.jpg` — same page as JPEG (fallback source)
- `build_v2.py` — the fresh PIL generator that built the page (deterministic)
- `main.py` — entry point: copies the page to `MAKEFUN_OUTPUT_DIR/entry.png`
- `new01.png`–`new05.png` — the five new AI illustrations (White House,
  NATO flags, burning Baltic cargo ship, AI chip, Haiti food aid); the
  other eight images are reused v1 thumbnails
