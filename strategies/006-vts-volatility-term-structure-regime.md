# 006 — VTS-1 "Volatility Term-Structure Regime"
Universe: BTCUSDT · Timeframes: 15m and 5m
Status: **REJECTED** — cleared rung A, failed rung C
Family consumed: `volatility-term-structure`

## Idea
Bitcoin shows **inverted volatility asymmetry**: volatility reacts more to *positive* returns than
negative ones, the opposite of the equity leverage effect. If BTC's real up-moves arrive loud and its
distribution arrives quiet, the two legs should not be mirror images — so they aren't.

`vts = ATR(5) / ATR(50)` is the term structure. Above 1.40 is expansion, below 0.75 compression.
- **LONG — the loud breakout.** 50-bar high breakout *during vol expansion*.
- **SHORT — the quiet breakdown.** 50-bar low breakdown *during vol compression*.

Different premise, different trigger condition, not a sign flip.

## Flip signal (standing objective B)
The regime variable is `expansion ? 1 : compression ? -1 : 0`. A **flip** is that value changing.
On a flip, `sinceFlip` resets and **no new entries fire for 20 bars** — during a transition neither
leg's premise holds. This is an explicit, mechanical response to the market changing, not a filter.

## Risk — pre-run audit (LESSONS 3, 5, 6)
| Leg | Stop | Structural? | R floor |
|---|---|---|---|
| LONG | 20-bar swing low − 0.25×ATR14 | yes — swing extreme, not the breakout level | 0.8% |
| SHORT | 20-bar swing high + 0.25×ATR14 | yes — swing extreme, not the breakdown level | 0.8% |

Target 2R both sides, both fixed at entry. Time stop 96 bars. `pyramiding = 1`.
Both legs audited separately; neither reuses the other's geometry.

## Commission gate (pre-registered)
Estimated **300–800 trades**. **Actual: 44 on 15m, 77 on 5m.** Missed low by ~4–7x — the third
straight miss, and again in a different direction than the last one.

## RESULTS
### Rung A — 15m, 2022-01-01 → 2026-09-01
| Net | PF | Trades | Win rate | avgWin/avgLoss | Max DD |
|---|---|---|---|---|---|
| +0.5% | **1.04** | 44 | 18.2% | 4.67 | 7.9% |

Leg split — **longs 4 trades (2 winners, +$309), shorts 40 trades (6 winners, −$261)**.
Cleared the 0.95 threshold, so the ladder advanced.

### Rung C — 5m, 2024-06-08 → 2026-09-01 (5m coverage starts 2024, not 2022)
| Net | PF | Trades | Win rate | Max DD |
|---|---|---|---|---|
| −20.2% | **0.36** | 77 | 23.4% | 22.9% |

Leg split — longs 24 trades (5 winners, −$1,163), shorts 53 trades (13 winners, −$854).
**Both legs lose on 5m.** One-timeframe-only → rejected.

## What this cycle proved
**The ladder works, and rung C is the rung that matters.** A PF of 1.04 on 44 trades over 4.7 years
is +0.5% total — statistically indistinguishable from zero. It cleared rung A anyway. The 5m run
settled it in one credit: the same rules lose 20% on a different timeframe, so the 15m number was
noise dressed as an edge.

**Objective C paid for itself immediately.** The blended 1.04 concealed a 4-trade long leg carrying
all the profit and a 40-trade short leg losing money. Without the leg split I would have recorded
"marginally profitable" instead of "one leg has an unusable sample and the other is broken".

## Falsifiable claim
BTC's inverted vol asymmetry is tradeable: breakouts during expansion outperform, breakdowns during
compression outperform. On 15m the long leg fired only 4 times in 4.7 years — the expansion gate at
1.40 combined with a 50-bar breakout is far too restrictive to test the claim at all. On 5m both legs
lost. **The claim remains untested rather than disproven**, but the thresholds as chosen do not
produce a tradeable sample.
