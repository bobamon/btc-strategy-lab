# BTC Lab — Champion Board

The lab's mandate changed on **2026-09-02**. Read this before the ledger.

> Research specifications for backtesting. Not trade recommendations.

## Why the mandate changed
Seven discovery cycles produced seven rejections:

| # | Strategy | PF |
|---|---|---|
| 002 | Variance-Ratio Regime Switch | 0.60 |
| 003 | Liquidation Cascade Reclaim | 0.69 |
| 004 | Moving-Average Retest Fade | 0.65 |
| 005 | Compression Release Volume Verdict | 0.52 |
| 006 | Volatility Term-Structure Regime | 1.04 → 0.36 on 5m |
| 007 | VWAP Value Migration | 0.89 |

Meanwhile the only thing in this project that has ever worked is the **War Formation v6** — PF 1.69 —
and it is **not a single mechanism**. It is five stacked filters, and the ablation proved the stack
*is* the edge: strip the cascade and PF collapses 1.40 → 0.68.

**The old mandate — "one genuinely new mechanism per cycle" — structurally cannot produce what
actually worked**, because a cascade is several mechanisms combined. So it is retired.

## THE NEW MANDATE — stack, measure, keep what earns its place
Each cycle takes the current **base** and changes **exactly one thing**: add a filter, remove a
filter, or alter one parameter. Then it runs the ladder and decides on evidence.

**A change is KEPT only if it improves profit factor AND does not worsen max drawdown.**
Anything else is reverted and recorded as tried. This is the ratchet that makes the lab get better
instead of merely different.

Every cycle must still satisfy the standing objectives (both directions built separately, an explicit
regime-flip response, legs reported separately) and every hard lesson in `STRATEGY-LEDGER.md`.

## CURRENT CHAMPION
**None yet.** Nothing has cleared the ladder (PF >= 0.95 on 15m, then 5m, then sensitivity).
The board is open.

## RATCHET PROGRESS
| Cycle | Base PF | Base DD | New PF | New DD | Verdict |
|---|---|---|---|---|---|
| Attack 1 — EMA200 trend filter | 0.89 | 35.0% | **0.91** | **28.8%** | **KEPT** |

## CURRENT BASE — what cycle 008 starts from
**007's LONG leg.** It has the best raw hit rate of anything tested in this lab: **38.3%** across 457
trades before costs, against a break-even of ~36% at its 1.76:1 payoff. It failed on *cost drag*
(18% of gross profit), not on signal quality — 564 trades was too many for the edge it had.

That makes it the right raw material: a signal that is nearly good enough, failing for a reason we
know how to attack.

**Base definition (updated after Attack 1):** VWAP with 2σ bands. Long only for now. Price stretched
to +2σ within the last 50 bars, then pulls back to within 0.5σ of VWAP and closes back above it,
while VWAP is rising over 50 bars, **and close is above the 200-period EMA**. Stop at the 20-bar
swing low − 0.25×ATR14, floored at 0.8% of price, target 2R, both fixed at entry. Flip signal: close
crossing VWAP, stand down 20 bars.

**Current base numbers:** PF 0.91 · max DD 28.8% · 433 trades · win rate 38.3% · net −23.0%
(BTCUSDT 15m, 2022-01-01 → 2026-09-01).

## THE ATTACK — ranked, one per cycle
The base loses to fee drag, so the first moves must **cut trade count without cutting edge**:

1. ~~Add a trend filter (EMA200)~~ — **DONE, KEPT.** PF 0.89→0.91, DD 35.0%→28.8%. Now part of the base.
2. **Require the pullback to be shallow.** A deep retrace to VWAP in an "accepted" uptrend may signal
   the acceptance failed. Test requiring the low to hold above VWAP entirely.
3. **Add the time-of-day filter** from the Oracle material (`war-formation/WAR-FORMATION.md`) —
   ban the 1–4am ET witching window, which has a documented downside bias.
4. **Raise the R floor** from 0.8% to 1.2%. HARD LESSON 3 says fees scale against R; the base spent
   18% of gross on fees, and a wider stop directly attacks that.
5. **Require volume confirmation on the pullback hold** — participation returning as price reclaims.
6. **Then, and only then, rebuild a short leg** on whatever survives, judged on its own profit factor
   (the mistake in 005 and E9 was bolting on a second leg before the first was sound).

## TRIED AND REVERTED
*(nothing yet — this table is the memory that stops a reverted change being retried)*

| Cycle | Change to the base | Result | Kept? |
|---|---|---|---|
| Attack 1 | Require close above EMA200 | PF 0.89→0.91, DD 35.0%→28.8%, trades 468→433 | **KEPT** |
