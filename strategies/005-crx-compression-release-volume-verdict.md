# 005 — CRX-1 "Compression Release, Volume Verdict"
Universe: BTCUSDT · Timeframes: 15m and 5m
Status: **REJECTED** — ladder rung A, PF 0.52
Family consumed: `range-compression expansion`

## Idea
A range compresses, price breaks out, and **volume decides whether the break is real**. Published
work on breakout filtering puts unfiltered breakouts at roughly 37% win rate and PF 0.92, with volume
the documented discriminator — a 200%+ surge marks the genuine ones. So: heavy volume, follow the
break; thin volume, fade it; in between, stand aside. The volume verdict is the regime switch.

## Mechanical rules as tested
- Box: `boxHi = ta.highest(high,48)[1]`, `boxLo = ta.lowest(low,48)[1]`, `boxW = boxHi - boxLo`
- **Compressed:** `boxW < 3.0 * ta.atr(100)`, and held for 5 consecutive bars
- **Release:** `ta.crossover(close, boxHi)` or `ta.crossunder(close, boxLo)`
- **Verdict:** `volume >= 2.0 * ta.sma(volume,50)` → follow · `volume < 1.0 *` → fade · else no trade
- **Stops:** follow = far side of the box; fade = beyond the breakout bar's extreme. Both + 0.25×ATR14,
  clamped to [0.8%, 3.0%] of price
- **Target:** 1.8R, fixed at entry · **Time stop:** 96 bars · `pyramiding = 1`

## Commission gate (pre-registered)
Estimated **200–600 trades**. **Actual: 93.** Missed low by ~2x — see the lesson below.

## RESULT — BTCUSDT 15m, 2022-01-01 → 2026-09-01
| Net | PF | Trades | Win rate | avgWin/avgLoss | Max DD |
|---|---|---|---|---|---|
| −16.9% | **0.52** | 93 | 18.3% | 2.33 | 21.4% |

Ladder stopped at rung A. No 5m run, no sensitivity sweep. 1 credit.

## Why it failed
The payoff ratio was again healthy (2.33:1, break-even ~30%), and the win rate was **18.3%** — worse
than the 37% the literature reports for *unfiltered* breakouts. The volume verdict did not just fail
to help; the filtered set performed worse than the unfiltered baseline. Either the thresholds select
the wrong tail, or the dead band between 1.0x and 2.0x removed the tradeable middle.

**I violated HARD LESSON 5 on the fade leg without noticing.** The follow leg got a genuinely
structural stop (the opposite side of the box, far from entry). The fade leg's stop sat just beyond
the breakout bar's extreme — a few ticks from entry, inside the noise, exactly the mistake 004 made.
And because thin-volume bars are far more common than 2x-volume bars, **fades likely dominated the
sample**. The same diagnostic shows up: `avgBarsWinning` 75.6 vs `avgBarsLosing` 31.7, losers dying
2.4x faster than winners.

## HARD LESSON 6 — apply the risk rule to EVERY leg, not the one you were thinking about
A strategy with two entry types has two stop placements, and a lesson applied to one is not applied to
the strategy. When a design has a follow leg and a fade leg, audit each leg against every hard lesson
separately before running it. Write the audit down — "leg A: structural stop, yes; leg B: ..." — because
the leg you designed second is the one that inherits none of your thinking.

## What is still open in this family
The compression detection itself is untested as a standalone edge — this run only tested compression
*plus* a volume verdict, and the verdict is what appears to be broken. Worth one run:
follow-only (drop the fade leg entirely), with the box stop on both directions.

## Falsifiable claim
Volume at the moment of release predicts whether a compression breakout continues. At 18.3% versus a
37% unfiltered baseline, the data says it does not — as thresholded here.
