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
**None yet.** Nothing has cleared the full ladder (PF >= 0.95 on 15m, then 5m, then sensitivity).
The board is open.

## A fork in the base, and how it was resolved (cycle 009, 2026-09-02)
Two sessions ran the "stack and ratchet" mandate concurrently and both landed on the same attack —
EMA200 trend filter — independently, before either had committed real Pine source for the base
(HARD LESSON 8). That produced two different reconstructions of "007's long leg + EMA200," from
prose alone, with materially different numbers:

| Reconstruction | PF (15m) | Max DD (15m) | Trades | Source committed? |
|---|---|---|---|---|
| `vwm-attack1-ema200` (prior session) | 0.912 | 28.8% | 433 | No |
| `008-vwm-base-btcusdt-15m` (this session) | **0.9555** | 47.7% | 649 | **Yes** — `strategies/pine/008-vwm-base.pine` |

The second reconstruction additionally caps risk at 3% of price (min 0.8%), matching every sibling
leg elsewhere in this lab — the prior version had no cap. **Resolution: the version with committed,
reproducible Pine source is now canonical.** Per HARD LESSON 8, a reconstruction's real numbers
supersede a prose-only baseline. `strategies/pine/008-vwm-base.pine` is the base from here on.

That reconstruction also clears rung A on its own (PF 0.9555 >= 0.95) — but its 5m run
(`008-vwm-base-btcusdt-5m`) came back at **PF 0.7992, max DD 51.4%**, the same HARD LESSON 7 pattern
as 006: a 15m pass is not evidence. The base stays the base (007 itself became base at PF 0.89
without ever clearing rung A — the ratchet's bar for "stays base" is lower than the ladder's bar for
"champion"), but nothing built on it should be promoted to champion without a 5m-robust result.

## RATCHET PROGRESS
| Cycle | Base PF | Base DD | New PF | New DD | Verdict |
|---|---|---|---|---|---|
| 008 — EMA200 trend filter | 0.89 | 35.0%–60.1%* | 0.91–0.96* | 28.8%–47.7%* | **KEPT** (two independent reconstructions agree) |
| 009 — shallow pullback (low above VWAP) | 0.9555 | 47.7% | **0.8551** | **32.5%** | **REVERTED** — PF worsened |

*Range reflects the two independent 008 reconstructions above; both agree PF improved and DD did not
worsen relative to their own respective 007 baselines.

## CURRENT BASE — what cycle 010 starts from
**008 — 007's LONG leg + EMA200 trend filter + R capped at 0.8–3.0% of price.**
Source: `strategies/pine/008-vwm-base.pine` (canonical, committed).

**Base definition:** VWAP with 2σ bands (approximated as VWAP ± rolling-stdev of price deviation,
since this engine's `ta.vwap` has no native band output). Long only. Price stretched to +2σ within
the last 50 bars, then pulls back to within 0.5σ of VWAP and closes back above it, while VWAP is
rising over 50 bars, and price closes above a 200-period EMA. Stop at the 20-bar swing low −
0.25×ATR14, floored at 0.8% of price and capped at 3.0%, target 2R, both fixed at entry. Flip
signal: close crossing VWAP, stand down 20 bars.

**Current base numbers (15m, 2022-01-01 → 2026-09-01):** PF 0.9555 · max DD 47.65% · 649 trades ·
win rate 39.45% · net −17.70%. **5m (2024-06-08 → 2026-09-01, shorter window): PF 0.7992 · max DD
51.36% · 682 trades · net −44.35%** — fails generalization, see above.

## THE ATTACK — ranked, one per cycle
The base still loses to fee drag on 5m, so the next moves keep **cutting trade count without
cutting edge, and should be checked on 5m as soon as a candidate clears 15m rung A**:

1. ~~Add a trend filter (EMA200)~~ — **DONE, KEPT.** Now part of the base.
2. ~~Require the pullback to be shallow (low holds above VWAP)~~ — **DONE, REVERTED.** PF worsened
   0.9555→0.8551 despite DD improving; see TRIED AND REVERTED.
3. **Add the time-of-day filter** from the Oracle material (`war-formation/WAR-FORMATION.md`) —
   ban the 1–4am ET witching window, which has a documented downside bias.
4. **Raise the R floor** from 0.8% to 1.2%. HARD LESSON 3 says fees scale against R.
5. **Require volume confirmation on the pullback hold** — participation returning as price reclaims.
6. **Then, and only then, rebuild a short leg** on whatever survives, judged on its own profit factor
   (the mistake in 005 and E9 was bolting on a second leg before the first was sound).

## TRIED AND REVERTED
*(this table is the memory that stops a reverted change being retried)*

| Cycle | Change to the base | Result | Kept? |
|---|---|---|---|
| 008 | Require close above EMA200 | PF 0.89→0.91–0.96, DD improved in both reconstructions | **KEPT — became the base** |
| 009 | Require pullback LOW (not just close) to hold above VWAP | PF 0.9555→0.8551 (worsened), DD 47.7%→32.5% (improved) | **REVERTED — PF worsened, fails the ratchet's first test** |
