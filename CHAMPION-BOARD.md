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
| 010 — ET witching-hour filter (ban 1–4am ET longs) | 0.9555 | 47.65% | **0.9614** | **45.78%** | **KEPT** — clears rung A, fails rung C (5m) |
| 011 — raise R floor 0.80%→1.20% of price | 0.9614 | 45.78% | **1.0211** | **40.67%** | **KEPT** — clears rung A, fails rung C (5m WORSE than base) |

*Range reflects the two independent 008 reconstructions above; both agree PF improved and DD did not
worsen relative to their own respective 007 baselines.

## CURRENT BASE — what cycle 012 starts from
**011 — 010's base (LONG leg + EMA200 + ET witching-hour filter) + R floor raised to 1.2% of price.**
Source: `strategies/pine/011-vwm-r-floor.pine` (canonical, committed).

**Base definition:** VWAP with 2σ bands (approximated as VWAP ± rolling-stdev of price deviation,
since this engine's `ta.vwap` has no native band output). Long only. Price stretched to +2σ within
the last 50 bars, then pulls back to within 0.5σ of VWAP and closes back above it, while VWAP is
rising over 50 bars, and price closes above a 200-period EMA. Entry banned when the bar's ET hour
(computed from the engine's UTC `time`, offset input default −4/EDT) falls in [1:00, 4:00) — the
Oracle's documented overnight-dump window (`war-formation/WAR-FORMATION.md`). **New this cycle: the
stop-distance floor is raised from 0.8% to 1.2% of price** — everything else about the stop (20-bar
swing low − 0.25×ATR14, capped at 3.0% of price, target 2R, both fixed at entry) is unchanged. Flip
signal: close crossing VWAP, stand down 20 bars.

**Current base numbers (15m, 2022-01-01 → 2026-09-01):** PF 1.0211 · max DD 40.67% · 598 trades ·
win rate 42.31% · net +10.21%. **This is the first time any variant of this base has cleared PF 1.0
on 15m.** **5m (2024-06-08 → 2026-09-01, shorter window): PF 0.7769 · max DD 57.02% · 622 trades ·
net −49.83%** — not only still fails generalization, it is *worse* than 010's own 5m run on both
metrics (PF 0.7883→0.7769, DD 52.22%→57.02%), the opposite of what HARD LESSON 9 predicted for a
change that raises R. See HARD LESSON 10 in `STRATEGY-LEDGER.md`. **The base is still not
champion-eligible — do not promote any variant of it without a 5m-robust result.**

## THE ATTACK — ranked, one per cycle
The base still loses to fee drag on 5m — every attempt so far has left the 5m result flat or worse,
and cycle 011 shows raising R can make it *actively worse* (see HARD LESSON 10) — so **the next
candidate that actually moves the 5m number should jump the queue** even if it isn't next on this
list:

1. **Require volume confirmation on the pullback hold** — participation returning as price reclaims.
   Unlike the R floor, this prunes bars rather than resizing every trade's risk, so it should not
   have the same 5m-specific side effect cycle 011 exposed.
2. **Make the R floor relative to volatility (e.g. a multiple of ATR%) instead of a flat % of
   price**, so it does not bind disproportionately on the timeframe with tighter swings. HARD LESSON
   10: a flat 1.2% floor binds far more often on 5m (tighter swing-based `rawR`) than on 15m,
   inflating nominal per-trade risk exactly where the strategy already loses. Only attempt this if
   item 1 doesn't clear rung C on its own — it's a bigger structural change to the risk model.
3. **Then, and only then, rebuild a short leg** on whatever survives, judged on its own profit factor
   (the mistake in 005 and E9 was bolting on a second leg before the first was sound).

~~Add a trend filter (EMA200)~~ — DONE, KEPT (cycle 008). ~~Require the pullback to be shallow~~ —
DONE, REVERTED (cycle 009). ~~Add the time-of-day filter (ban 1–4am ET)~~ — DONE, KEPT (cycle 010).
~~Raise the R floor from 0.8% to 1.2%~~ — DONE, KEPT on 15m ratchet but fails rung C, 5m got worse
(cycle 011).

## TRIED AND REVERTED
*(this table is the memory that stops a reverted change being retried)*

| Cycle | Change to the base | Result | Kept? |
|---|---|---|---|
| 008 | Require close above EMA200 | PF 0.89→0.91–0.96, DD improved in both reconstructions | **KEPT — became the base** |
| 009 | Require pullback LOW (not just close) to hold above VWAP | PF 0.9555→0.8551 (worsened), DD 47.7%→32.5% (improved) | **REVERTED — PF worsened, fails the ratchet's first test** |
| 010 | Ban longs 1–4am ET (witching hour) | 15m: PF 0.9555→0.9614, DD 47.65%→45.78% (both improved). 5m: PF 0.7992→0.7883, DD 51.36%→52.22% (both slightly worse) | **KEPT as base** (15m ratchet passes) — **but did not clear rung C**, so not promoted to champion |
