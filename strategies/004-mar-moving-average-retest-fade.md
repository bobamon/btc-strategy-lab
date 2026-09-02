# 004 — MAR-1 "Moving-Average Retest Fade"
Universe: BTCUSDT · Timeframes: 15m and 5m
Status: **REJECTED** — ladder rung A, PF 0.65
Family consumed: `trend-anchored MA retest` (new family, added this cycle)
Source: mechanized from a charted XBTUSD setup supplied by the user

## The setup as charted
A slow moving average slopes down across the frame and acts as resistance. Price rallies up, **tags
the MA from below, and rejects back under it** — that is the short. The target is the **lower band**
of a volatility channel. Mirrored when the MA slopes up. The MA's slope is the regime switch: it
decides whether you are fading rallies or fading dips, and nothing else needs deciding.

## Mechanical rules as tested
- `slowMA = ta.ema(close, 200)`; `slopePct = (slowMA - slowMA[20]) / close * 100`
- **DOWN regime:** `slopePct <= -0.10`  ·  **UP regime:** `slopePct >= +0.10`
- **SHORT:** DOWN regime **and** `high >= slowMA` **and** `close < slowMA` **and** `close < open`
- **LONG:** UP regime **and** `low <= slowMA` **and** `close > slowMA` **and** `close > open`
- **Stop:** just beyond the MA — `(slowMA + 0.25*ATR14) - close` for shorts, mirrored for longs,
  clamped to [0.8%, 3.0%] of price (HARD LESSON 3)
- **Target:** the opposite Bollinger band (20, 2.0) **measured at entry and never moved**, clamped to
  between 1R and 4R
- **Time stop:** flat after 96 bars
- One position at a time, `pyramiding = 1`. No trailing stop, no averaging down, no grid, no martingale.

## Commission gate (pre-registered)
Estimated 500–1,500 trades. **Actual: 844.** Inside the range — a better calibration than 003, which
missed by 4–10x. But the gate was marginal on paper: at R = 0.8% and a 2R target, break-even needs a
~33% win rate, leaving little headroom. That marginality turned out to be the story.

## RESULT — BTCUSDT 15m, 2022-01-01 → 2026-09-01
| Net | PF | Trades | Win rate | avgWin/avgLoss | Max DD |
|---|---|---|---|---|---|
| −80.6% | **0.65** | 844 | 23.8% | 2.07 | 82.7% |

Ladder stopped at rung A (PF < 0.95). No 5m run, no sensitivity sweep. 1 credit.

## Why it failed — and it is not the idea
The payoff ratio was **fine**: 2.07:1, the risk geometry worked exactly as designed. Break-even at
that ratio needs ~33% wins; it delivered 23.8%.

The tell is in the holding times: **`avgBarsWinning` 27.1 vs `avgBarsLosing` 12.3.** Losers die in
half the time winners take. That is the signature of a stop sitting inside the noise.

**HARD LESSON 5 — never place the stop just beyond the level you entered at.**
Entry is at the MA. The stop is a fraction of an ATR beyond the MA. But price *oscillates around a
moving average by construction* — that is what a moving average is. So the stop was planted in the
single noisiest location on the chart, and 76% of trades were shaken out before the thesis had room
to resolve. The R floor stopped the fee from eating the trade, but it could not stop the market from
brushing the stop on its way to being right.

## What the chart actually shows that this build missed
On the supplied chart, each "Short" is circled at a **cluster** of bars at the MA, not a single tag —
price spends several bars up there being rejected before it goes. This build fired on the **first**
touch. Two changes worth testing before the family is written off:
1. **Confirm the rejection.** Require N consecutive closes back below the MA, or a close below the
   *prior bar's low*, rather than entering on the first tag.
2. **Stop above the structure, not above the MA.** Use the swing high of the rejection cluster
   (`ta.highest(high, 10)` + buffer), which sits outside the oscillation band instead of inside it.

Either change moves the stop out of the noise. Both are testable in one run each.

## Falsifiable claim
Fading a retest of a sloped EMA200 beats a coin flip on direction. The 23.8% win rate at a 2.07:1
payoff says it does not — **as entered here**. The claim is not yet settled for a confirmed-rejection
entry with a structural stop.
