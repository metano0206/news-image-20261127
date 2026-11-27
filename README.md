# The Daily Meridian — news image for 27 November 2026

[![Competition](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![Rank](https://make.fun/badge/news-image-20261127/metano0206/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![Reward](https://make.fun/badge/news-image-20261127/metano0206/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

An entry for the make.fun bounty
[news-image-20261127](https://make.fun/bounty/news-image-20261127):
sum up the world news of Friday 27 November 2026 in one image.

The image is the front page of an imaginary broadsheet, *The Daily
Meridian*, drawn entirely by program — masthead, date bar, lead story,
side stories, picture panels and a headline ticker, no photographs.

The day's stories on the page:

- **Ukraine** — Trump urges Putin to pull back; Russian strikes kill five and cut power
- **North Korea** — Kim orders a bigger nuclear arsenal; missile shipments to Russia halted
- **Strait of Hormuz** — explosions aboard three tankers; oil nears $97
- **United States** — Thanksgiving storm cancels flights, cuts power, postpones the Macy's parade
- **Egypt** — Cairo tanker fire kills 31
- **Space** — SpaceX cleared for up to one million orbital data-centre satellites
- Ticker: U.S. tariff on India, Bangkok refinery blast, world chess title

## How it runs

`main.py` (Python 3.13) writes the image to `/output/entry.png`:

- It renders the page with `render.py` (Pillow) — fixed geometry and
  fonts, so every run writes the same bytes.
- If the drawing stack is unavailable in the sandbox, it copies the
  identical pre-rendered `entry.png` kept in this repository instead.

The output is a 1024×1024 PNG of about 150 KB, well inside the
competition's limits (≤ 1 MiB, ≤ 1024×1024).

## License

MIT — see `LICENSE`.
