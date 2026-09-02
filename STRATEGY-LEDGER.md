# BTC Strategy Lab — Ledger

Autonomous researcher. Universe: **BTCUSDT** only (Bybit USDT linear perpetual, `BYBIT:BTCUSDT.P`)
on **15m and 5m**. One strategy per cycle. Every cycle must explore a **substantially different
mechanism** — not a reparameterization.

> These are research specifications for backtesting, not trade recommendations.

## Universe (verified coverage, 2026-09-01)
| Pair | 15m bars | History from |
|---|---|---|
| **BTCUSDT** | 211,327 | 2020-08-19 |

Standard backtest window: **2022-01-01 → present** (~163,700 bars on 15m). Deeper history back to
Aug 2020 is available if a mechanism needs a second regime era.

**Narrowed to BTC-only on 2026-09-01**, after a first pivot away from US30/NAS100/YM/NQ the same
day (see Archived note at the bottom). One pair means strategies no longer have to generalize
across instruments, so BTC-specific structure — its funding cycle, liquidation behaviour, weekend
regime, round-number magnetism — is now fair game and should be exploited rather than avoided.

## MANDATE CHANGED 2026-09-02 — read CHAMPION-BOARD.md first
The lab no longer invents one new mechanism per cycle. That mandate produced **seven rejections in
seven cycles**, and it structurally could not produce the only thing that has ever worked here —
the War Formation's five-filter cascade (PF 1.69), whose ablation proved the *stack* is the edge.

**New mandate: stack, measure, keep what earns its place.** Each cycle changes exactly ONE thing
about the current base, then keeps the change only if profit factor improves AND max drawdown does
not worsen. `CHAMPION-BOARD.md` holds the base, the champion, the ranked attack, and the
tried-and-reverted table. The mechanism registry below is now history, not a to-do list.

## STANDING OBJECTIVES — every strategy in this lab must satisfy these
1. **Both directions, built separately.** Long and short each need their own entry logic, level
   definition and risk geometry. **A short rule that is only a sign-flipped long rule does not count.**
   The War Formation learned this the expensive way: its mirrored short leg went 2 winners in 15 and
   removing it improved every metric. That is a verdict on mirroring, not on shorting.
2. **Handle the flip.** The strategy must mechanically detect when the regime *changes* and respond —
   not merely filter for one regime and sit out the other. State the flip signal and the response.
3. **Report the legs separately.** Long vs short, and bull-regime vs bear-regime where the design
   allows. A blended profit factor hides a dead leg, which is exactly how 005's fade leg escaped
   notice until after the credit was spent.

## Structural notes (apply to every strategy)
1. **24/7 market.** No opening bell, no RTH close, no session gaps. Any mechanism built on an
   opening range, a cash-session close, or an overnight gap does not transfer. Time-of-day effects
   *do* still exist (Asia / London / US overlap, CME futures hours) but they are soft, not structural.
2. **One pair, both timeframes.** A strategy must work on BTCUSDT 15m *and* 5m. That is now the only
   generalization test, so it must be a real one: no parameter set that only survives on one TF.
3. **Cross-symbol data is forbidden in Pine** (`request.security` blocked). Anything needing ETH,
   total-market cap, DXY, or a funding-rate feed as an input is external-backtest-only.
4. **Weekends are real.** BTC trades through them at lower volume with different behaviour. A
   mechanism should either handle weekends explicitly or state that it ignores them.

## Mechanism registry — do not reuse
| # | Strategy | Core mechanism | Regime flip driver | Status | Date |
|---|----------|----------------|--------------------|--------|------|
| 001 | RSB-1 Relative-Strength Baton | Cross-complex opening-range confirmation vs. non-confirmation | Partner-index confirmation sign | ARCHIVED — index-era, off-universe | 2026-09-01 |
| 002 | VRS-1 Variance-Ratio Regime Switch | Lo-MacKinlay variance ratio selects breakout vs. band-fade behaviour | VR above 1.15 / below 0.85 | **REJECTED** — backtested, no edge | 2026-09-01 |
| 003 | LCR-1 Liquidation Cascade Reclaim | Cascade bar (range + volume + new extreme); close position inside the bar picks fade vs. follow | closePos above 0.55 / below 0.25 | **REJECTED** — PF 0.69, ladder rung A | 2026-09-01 |
| 004 | MAR-1 Moving-Average Retest Fade | Fade the retest of a sloped EMA200; target the opposite band | Sign of the EMA200 slope | **REJECTED** — PF 0.65, ladder rung A | 2026-09-01 |
| 005 | CRX-1 Compression Release Volume Verdict | Compressed box releases; volume decides follow vs. fade | Volume >= 2x avg / < 1x avg | **REJECTED** — PF 0.52, ladder rung A | 2026-09-01 |
| 006 | VTS-1 Volatility Term-Structure Regime | ATR(5)/ATR(50) term structure; loud breakout long vs. quiet breakdown short | Term-structure regime change, 20-bar stand-down | **REJECTED** — 15m PF 1.04, 5m PF 0.36 | 2026-09-02 |
| 007 | VWM-1 VWAP Value Migration | VWAP 2-sigma bands; accepted-value pullback long vs. rejected-excursion short | Close crossing VWAP, 20-bar stand-down | **REJECTED** — PF 0.89, ladder rung A | 2026-09-02 |

## Mechanism families already consumed
- `cross-complex-OR-confirmation` (001, archived)
- `autocorrelation-sign regime` (002) — variance-ratio form, **rejected on real data**
- `liquidation-cascade signatures` (003) — closePos switch, **rejected on real data**
- `trend-anchored MA retest` (004, new family) — first-tag entry, **rejected on real data**; a confirmed-rejection variant is still untested
- `range-compression expansion` (005) — volume-verdict switch, **rejected on real data**; a follow-only variant is still untested
- `session-VWAP band mechanics` (007) — acceptance vs. rejection, **rejected on real data**
- `volatility-term-structure` (006) — expansion/compression asymmetry, **rejected**; thresholds too tight to give the long leg a testable sample

## Families still open for future cycles
volume/participation profile · time-of-day seasonality (Asia/London/US overlap) · order-flow imbalance proxies
· funding-rate / basis effects
· autocorrelation regime via other estimators (Hurst, ACF sign)
· microstructure round-number behaviour · realized-vs-implied vol spread

---

## HARD LESSON 1 — the commission budget (learned from 002, 2026-09-01)
The engine forces **0.05% commission** and **100%-of-equity sizing**. At 15m over ~4.7 years a
naive crossover strategy fires 4,000–6,500 times, and commission alone consumed **36–53% of gross
profit** in the 002 runs. Both symbols finished at −99%.

**Design rule for every future cycle:** a strategy must clear roughly **0.10% average gross profit
per trade** just to break even after fees. Before proposing a mechanism, estimate its trade
frequency. If it fires thousands of times with a sub-0.1% expected edge, it is dead on arrival —
either add selectivity (tighter regime gates, confirmation requirements) or move to a mechanism
with a larger per-trade payoff.

## HARD LESSON 2 — the parity profile is not your risk model
`quick_backtest` **overrides** the spec's position sizing. Whatever the spec says about risking
0.5% per trade, the engine runs `percent_of_equity: 100`, `margin 100/100`, `commission 0.05`.

Consequence: a backtest here tests the **signal**, not the spec's risk management. A −99% result
means the signal has no edge; it does *not* mean the spec's sizing was tested and failed. Always
record this caveat alongside the numbers.

## HARD LESSON 3 — commission sets a FLOOR on stop distance (from the War Formation, 2026-09-01)
The 0.05% fee is charged twice per round trip: **0.10% of notional**, a fixed cost. Its damage depends
entirely on how wide the stop is.

| Risk (R) as % of price | Fee as % of R | A nominal 2:1 becomes |
|---|---|---|
| 0.15% | ~66% | 0.89:1 — PF 0.47 |
| **0.80%+** | **~12%** | **1.89:1 — PF 1.40** |

Those two rows are the *same strategy* with one number changed. **R must be at least ~8x the
round-trip fee**, i.e. R >= 0.8%. This is HARD LESSON 1 seen from the other side: there, too many
trades killed it; here, too tight a stop.

## HARD LESSON 4 — measure trade frequency, never estimate it (from 003, 2026-09-01)
The commission gate depends on a trade-frequency estimate, and **that estimate was wrong by 4-10x**.
003 pre-registered 150-400 trades and took **1,532**. Bars meeting "range > 2.5x ATR + volume > 3x
average + new 50-bar extreme" occur on roughly **1% of bars**, not the 0.1-0.3% assumed. Rare-sounding
conjunctions are far more common than intuition suggests over 163k bars.

**Rule:** treat the pre-registered estimate as a hypothesis to be scored, not a fact. If the actual
count misses the estimate by more than 2x, say so explicitly in the record and re-derive the gate —
the economics of the design were computed on a number that turned out to be wrong.

**Also from 003:** a good payoff ratio does not rescue a bad signal. The R floor worked exactly as
intended (avgWin/avgLoss 1.68), but at 1.68:1 the strategy needs a ~37% win rate to break even and
delivered 29.2%. Getting the risk geometry right only buys the chance to be right about direction.

## HARD LESSON 5 — never put the stop just beyond the level you entered at (from 004, 2026-09-01)
004 entered at the EMA200 and stopped a fraction of an ATR beyond it. **Price oscillates around a
moving average by construction** — that is what a moving average is — so the stop was planted in the
noisiest location available. Result: 23.8% win rate against a perfectly healthy 2.07:1 payoff, which
needed ~33% to break even.

The diagnostic to watch for: **`avgBarsLosing` far below `avgBarsWinning`** (12.3 vs 27.1 here).
Losers dying in half the time winners take means trades are being shaken out before the thesis can
resolve — the stop is inside the noise, not outside the structure.

**Rule:** the stop belongs beyond the *structure* (a swing high/low, a prior extreme), not beyond the
*signal level*. And an entry level and a stop level should never be the same object.

## HARD LESSON 6 — apply the risk rules to EVERY leg (from 005, 2026-09-01)
005 had two entry types. The **follow** leg got a properly structural stop (far side of the box). The
**fade** leg's stop sat a few ticks beyond the breakout bar's extreme — inside the noise, the exact
mistake HARD LESSON 5 exists to prevent. I had applied the lesson to the leg I designed first and not
to the leg I designed second. Because thin-volume bars are far more common than 2x-volume bars, the
badly-stopped leg probably dominated the sample.

**Rule:** before running any multi-leg design, write an explicit audit — one line per leg, one line
per hard lesson — and confirm each cell. The leg you design second inherits none of your thinking.

## A recurring diagnostic worth naming
`avgBarsLosing` far below `avgBarsWinning` has now flagged the same defect twice (004: 12.3 vs 27.1;
005: 31.7 vs 75.6). **Losers dying roughly twice as fast as winners means the stop is inside the
noise.** Check this ratio on every result before interpreting anything else.

## Frequency-estimate scorecard (HARD LESSON 4 in practice)
| Cycle | Estimated | Actual | Miss |
|---|---|---|---|
| 003 | 150–400 | 1,532 | 4–10x HIGH |
| 004 | 500–1,500 | 844 | inside range |
| 005 | 200–600 | 93 | ~2x LOW |
| 006 | 300–800 | 44 / 77 | 4–7x LOW |
| 007 | 400–1,200 | 564 | **inside range** |

Estimates are improving but still unreliable in both directions. Keep pre-registering them, keep
scoring them, and treat any commission-gate argument built on one as provisional.

## HARD LESSON 7 — rung C is the rung that matters (from 006, 2026-09-02)
006 became the first strategy to clear rung A: PF 1.04 on 15m. It was noise. +0.5% across 4.7 years
and 44 trades is statistically indistinguishable from zero, and the 5m run settled it for one credit
— **PF 0.36, −20.2%, both legs losing.**

**A single-timeframe pass is not evidence.** The same rules on a different timeframe is the cheapest
out-of-sample test available, and it should be treated as the real gate. Rung A only decides whether
a strategy is worth one more credit.

**Objective C paid for itself on first contact.** The blended 1.04 hid a 4-trade long leg carrying
all the profit and a 40-trade short leg losing money. Without the leg split this would have been
recorded as "marginally profitable" instead of "one leg untested, the other broken".

**Frequency scorecard update:** estimated 300–800, actual 44 (15m) and 77 (5m) — missed LOW by 4–7x.
Three cycles, three misses, in both directions (003 high, 005 low, 006 low). The estimate remains a
hypothesis to score, never a fact to build on.

## Platform constraints — trader.dev engine
- Pine **//@version=6**, allowlist of 65 `ta.*` indicators.
- **FORBIDDEN:** `request.security` (no cross-symbol), arrays/maps, `strategy.cancel`,
  `strategy.order`, pyramiding > 1, martingale, custom var-trail (`if low <= trail → close`).
- Exits via `strategy.exit(stop=, limit=, trail_*, qty_percent=)` and `strategy.close`.
- Symbol universe: **Bybit USDT linear perpetuals only** (639 instruments).
- Each backtest costs **1 credit**. Weekly grant 1000. At 96 cycles/day, do not backtest every cycle.
- Always call `plan_backtest_window` first — it clamps dates and reveals symbol remaps.
- **Coverage differs by timeframe:** 15m reaches back to 2020-08, but **5m only starts 2024-06-08** and
  **1m only covers 2025-12-16 → 2026-05-03**. A 5m or 1m run is a shorter window than a 15m one, so
  never compare their returns without saying so.

## ARCHIVED — why the index universe was abandoned (2026-09-01)
`plan_backtest_window` verification of the original US30/NAS100/YM/NQ universe:

| Symbol | Result |
|---|---|
| `US30` | hard error — not in the Bybit catalog |
| `NAS100` | hard error — not in the Bybit catalog |
| `NQ` | **silently remapped to `IONQUSDT`** (crypto perp) |
| `YM` | **silently remapped to `DYMUSDT`** (crypto perp) |

The silent remaps were the real danger: a backtest would have returned **genuine metrics for the
wrong instrument**. Strategy 001 remains on file as an external-backtest-only spec should an index
data path ever be added.
