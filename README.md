# Sunday 22 November 2026 — world news in one image

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/borcyondo-art/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/borcyondo-art/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

`main.py` (Python 3, standard library only, no network) draws the image
procedurally and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`
(or `/output/entry.png`). It is deterministic: two runs write
byte-identical PNG bytes (1024x1024, under 1 MiB). Everything in the
picture — globe, flags, port, crowd, charts — is drawn from flat
geometric shapes, and all lettering uses a small 5x7 bitmap font
defined in `main.py` itself. No image, photo, or artwork was copied.

## The picture

A newspaper-style front page. The banner names the day it sums up:
**Sunday 22 November 2026**. The lead panel is the climate summit;
five supporting panels cover conflict, Europe, protest, and sport.
The footer reads "News reported on 22 November 2026", because the
stories below are the ones in the news cycle of that morning (the
build ran just after midnight UTC, when most of the world was still
asleep). Each story is labelled only with what reporting had
established by then; nothing is presented as happening on 22 November
that the sources date to an earlier day.

## Stories in the image

1. **COP31 — still no deal (lead).** Talks at the UN climate summit
   in Antalya, Turkey, ran into overtime with no final agreement:
   nearly 200 countries were divided over whether the text mentions
   fossil fuels and over finance for poorer countries. Reported by
   Reuters ("COP31 climate summit risks failure as talks go deep
   into overtime", 21 Nov 2026) and the BBC ("Fight over fossil
   fuels leaves COP31 climate talks in deadlock", 21 Nov 2026), and
   still unresolved in the SBS morning bulletin of 22 November 2026.

2. **Ukraine — ceasefire plan.** President Volodymyr Zelensky
   proposed temporary localised ceasefires to evacuate civilians
   from 15 settlements along or near the Dnipro River in occupied
   Kherson and Zaporizhzhia oblasts. Institute for the Study of War,
   "Russian Offensive Campaign Assessment, Nov. 21, 2026".

3. **Yemen — port strikes, aid warning.** The Saudi-led coalition
   struck the Red Sea port of Hodeidah (Hudaydah) on 20 November
   2026; the United Nations warned on Friday that strikes on the
   port endanger a lifeline for humanitarian aid. UN warning as
   reported 21 November 2026 (UN deputy spokesperson Farhan Haq,
   via The Chronicle); strikes dated 20 November 2026.

4. **Europe — budget cut.** European Council President Antonio
   Costa proposed a 2028–2034 EU long-term budget EUR 204 billion
   below the European Commission's plan, including a tax on large
   digital companies. European Council press release, 21 November
   2026; Bloomberg Law, 21 November 2026. A proposal, not an agreed
   budget — the image says "plan" and "less", not "agreed".

5. **France — protests, week 6.** A sixth consecutive Saturday of
   demonstrations over the cost of living and related demands.
   Reuters, "Lower turnout at largely peaceful marches across
   France", 21 November 2026: the Interior Ministry counted 82,500
   demonstrators nationwide (organisers put it higher). The image
   gives no crowd number, to avoid picking one side's count.

6. **Sport — Australia win T20 opener.** Australia chased 188 to
   beat England by three wickets with one ball to spare in the
   first T20 international at the MCG, Melbourne; Nikhil Chaudhary
   made 66. Reuters / AAP / cricket.com.au, 21 November 2026
   (Saturday night, Melbourne).

## Stories checked and left out

Several prominent stories were deliberately excluded after checking
their dates: the magnitude 6.9 Peru earthquake (20 November local
time), the capture of cartel figure "El Chapo Isidro" in Mexico
(20 November, announced 21 November), the Nigeria boat capsizing
(20 November, with conflicting early death tolls), the Russian
missiles landing in Poland and the large Ukraine air attacks
(19–20 November), and the claimed AI-assisted proof of the Riemann
hypothesis (announced 20 November, with conflicting accounts of
whether it had been verified). None of those is presented here as
22 November news.

## How to run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs produce the same sha256. The program reads nothing from
disk and contacts no network.

## License

MIT (see LICENSE).
