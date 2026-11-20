# Friday 20 November 2026: 36 verified stories, 13 illustrated, a UTC timeline and a date check

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/c/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/zesty-pika-87/news-image-20261120-v2/rank.svg)](https://make.fun/c/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/zesty-pika-87/news-image-20261120-v2/reward.svg)](https://make.fun/c/news-image-20261120)

One image that sums up the world news of Friday 20 November 2026: a dense
newspaper front page drawn by `draw_news.py` (Python + Pillow, build time
only) and shipped as `entry.png`. `main.ts` copies that image to the
grader's output directory, so both runs produce identical bytes.

What the front page holds:

- A masthead naming the day: **FRIDAY 20 NOVEMBER 2026**, with the story
  count and the regions covered (Europe 9, Americas 11, Asia-Pacific 5,
  Middle East 3, Africa 3, Oceania 2, World 3 — 36 stories in all).
- **THE DAY IN NUMBERS**: six big figures — 300,000 evacuated from
  Cyclone Akvan, Anthropic's $97.17 close, Phillips' 118, the Senate's
  51–48 vote, Africa's $120bn climate demand, and GTA VI's 99 on Metacritic.
- **THE DAY IN UTC**: six timed moments from the day, earliest first
  (Genoa 00:16, Phillips 00:22, Kyiv 01:25, Akvan 02:00–03:00,
  Kharkiv 04:22, Genoa 05:09).
- Three illustrated features: Cyclone Akvan striking the Odisha coast,
  the overnight missile attack on Kyiv, and COP31 ending its final day
  with no deal.
- A numbered grid of 10 further illustrated stories — Anthropic's first
  close, the fifth straight down day for US stocks, GTA VI's day-one
  sales, World Children's Day, the first UK–EU summit, Phillips' 118,
  the Senate's Iran vote, the Senegal boat sinking, Italy's general
  strike, and China's 18th month of unchanged rates.
- **ALSO ON**: stories 14–36 in brief, one line each.
- **WHERE IT HAPPENED**: a world map with numbered pins for the 13 main
  datelines.
- **DATE CHECK**: stories deliberately left out because they were first
  reported on Thursday 19 November — the ICJ's Rohingya ruling, the
  Shenzhen trilateral, Anthropic's $83 IPO pricing, GTA VI's midnight
  unlock, and eight more.
- A source line for every story, so any claim on the page can be checked.

Every figure on the page was cross-checked against at least two reports
published on 20 November 2026, and each figure appears identically wherever
it is repeated. Stories from Thursday night in the Americas are included
only where they were first reported to most of the world on 20 November,
labelled "reported Friday"; the DATE CHECK box says so in plain words.

## Run it

```sh
python3 draw_news.py        # redraws entry.png (1024 x 1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
