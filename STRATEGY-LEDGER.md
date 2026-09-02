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

### HARD LESSON 8 — A setup and its trigger must be LATCHED IN SEQUENCE, never required on the same bar
Observed twice, in two different labs, both times as a run with **zero trades**:

- **War Formation v1** demanded a volatility coil (`atr(3) < atr(30)*0.85`) *and* a velocity thrust on
  the same bar. A coil is low volatility; a thrust is high volatility. Mutually exclusive → 0 trades.
- **3M Elite v2 and v4** demanded a zone tap (price at the previous 12H low) *and* a bullish engulfing
  4H candle inside a 12-hour window. A tap is the bottom of a range; an engulf is a surge off it.
  Near-mutually exclusive → 0 trades on a 163,826-bar, 4.7-year base.

**The tell is a zero-trade run on a base that trades normally without the new gate.** That is almost
never "too strict"; it is almost always two conditions that cannot be true at the same instant.

**The fix is always the same shape:** latch the setup into a state variable (`var bool tapLive`),
give it an explicit invalidation rule, and let the trigger fire on a *later* bar while the latch is
live. Setup and trigger occupy different points in time — code them that way.

**Corollary — how to avoid paying for this discovery.** ~~Before spending a credit on a run that adds
a gate, `plot()` the gate's own hit count.~~

**CORRECTED 2026-09-02 (3M Elite v16).** That corollary does not work on this engine: `plot()` values
are NOT returned by `quick_backtest`. The response carries trade statistics only, so a plotted gate
counter is invisible and the advice was unusable — it was written from TradingView habits, not from
this API's actual output. Three runs were designed around it before the gap was noticed.

**The technique that DOES work is the counter build, proven in v12 and v13:** make the gate itself the
entry condition and force a one-bar exit, so `totalTrades` becomes the gate's hit count and
`longTrades`/`shortTrades` split it by side. It costs a credit but returns a real number. Use it
whenever a gate's frequency is in question, and never trust a plot to answer it.


### HARD LESSON 8 — GENERALISED, 2026-09-02 (3M Elite v17)
The original lesson was that a setup and its trigger must be latched in sequence, never required on
the same bar. **A third zero-trade run showed the rule is narrower than the failure mode it describes.**

In 3M Elite v16 and v17 the sequencing was correct — the setup latched and the trigger came later —
and the build still made zero trades across 4.7 years. The cause was that **the same price action that
ARMED the setup also started the clock on its DEATH**: entering a zone armed it, and closing inside
that zone mitigated it, with mitigation evaluated first at every higher-timeframe boundary.

**The generalised rule: whenever a latch is introduced, ask what ELSE the arming event triggers.**
A latch is only useful if the state it creates can outlive the event that created it. Check the
invalidation path with the same care as the trigger path.

**And use the counter build to check it** — gate as entry, one-bar exit, `totalTrades` is the hit
count — because this engine returns no plot values.


# ██ STANDING REQUIREMENT — BOTH DIRECTIONS, ALL REGIMES (user directive, 2026-09-02)

**The user's words: every strategy must work in bull markets, bear markets, AND on market flips.
Both directions. This binds all three labs and overrides any convenience of building long-only.**

A build is only finished when all four hold:
1. **A LONG leg** that stands on its own profit factor.
2. **A SHORT leg** that stands on its own profit factor — built from its OWN geometry, never mirrored
   (that has failed four times across two labs and the rule is not negotiable).
3. **A mechanical FLIP response** — a defined rule for what happens when the regime changes, not an
   implicit one. Standing down is a valid response; having no rule is not.
4. **Evidence in BOTH regimes.** A period split that shows the system in a rising market and a falling
   one. A number averaged across both is not evidence for either.

**Long-only is now an INTERIM state, never a finished result.** Any cycle reporting a long-only
configuration must say explicitly that the short leg and the regime evidence are outstanding.

## HONEST STATUS AGAINST THIS REQUIREMENT — NONE OF THE THREE MEET IT TODAY

| Lab | Long | Short | Flip rule | Both regimes | Meets it? |
|---|---|---|---|---|---|
| BTC | yes, but PF 1.36 early / 0.66 late | built, PF 0.58, fails | yes — VWAP cross, stand down 60 bars | no — the base REQUIRES close above the 600 EMA, so it only trades bull conditions | **NO** |
| War Formation | yes, PF 1.69 full / 0.89 recent | four attempts, best PF 0.75 | yes — 6h regime recomputes each block | no — requires 4+ green HA 1h candles, so bull conditions only | **NO** |
| 3M Elite | broken | broken | yes — zone invalidation on a body close | symmetric BY DESIGN (demand and supply zones) but no working entry yet | **NO — but the only one built symmetric from the start** |

**The blunt version: two of the three labs are structurally bull-only.** The BTC base gates on price
above a long EMA and War Formation gates on green Heikin Ashi hourly candles — those are not filters
that happen to favour uptrends, they are conditions that make a downtrend un-tradeable by
construction. Meeting this requirement means changing the systems, not tuning them.

**3M Elite is the closest in structure**, because supply and demand zones are inherently two-sided —
its problem is that the entry does not work yet in either direction, not that it is one-sided.


### THE NO-MIRROR RULE, CORRECTED — 2026-09-02
The original rule, from War Formation E9/E9b: *never mirror the short off the long.*

**Tested directly in the BTC lab and found too strong.** The mirrored mechanism scored PF 0.7413 on
273 trades; the deliberately non-mirrored "own geometry" fade scored 0.5506 on 17. The rule steered
the lab away from the better construction.

**Corrected rule: BUILD THE MIRROR FIRST, THEN FIX LOCATION.**
A symmetric mechanism is a legitimate starting point and usually the higher-frequency one. What
actually failed in E9/E9b was a short that entered *after price had already fallen* — a location
error, not a symmetry error. E13 proved this by adding a cycle-position gate to a mirrored short and
lifting it from 0.68 to 0.75.

**And note how the error propagated:** the rule was earned in one lab and applied in another without
being tested there. That is the fourth cross-lab inheritance failure this session, after the
volatility filter, the timeframe translation and the exit-target hypothesis. **A finding from one
strategy is a hypothesis for another, never an inheritance — including this lab's own rules.**


# ██ THE BOTH-DIRECTIONS REQUIREMENT: STRUCTURE BUILT, SUBSTANCE MISSING (2026-09-02)

Both labs now have a bidirectional build. **Both are worse than their long-only versions, and for the
same reason: the short leg has no edge in either.**

| Lab | Long leg | Short leg | Combined | vs long-only |
|---|---|---|---|---|
| BTC 5m | 128 trades, +$374 | **294 trades, −$2,416** | PF 0.888, DD 37.3% | worse than 1.020 |
| War Formation 1m | 32 trades, +$786 | **10 trades, 1 win, −$329** | PF 1.303, DD 5.02% | worse than 1.686 |

**What has been established, and it is not nothing:**
- The structure works. A single strategy that reads the regime and takes either side is built, running
  and measured in both labs, with a mechanical flip rule on each.
- The legs barely interact. BTC's long count is identical (128) whether the short is present or not,
  so `pyramiding=1` blocking is not the problem.
- **Raising short frequency does not help.** War Formation's shorts went 6 → 10 and the loss grew five
  times while wins stayed at one. Sampling a negative expectancy more often just costs more.

**What is NOT established: any short leg with an edge.** Across two labs and eight distinct short
constructions — mirrored, own-geometry fade, near-touch rejection, sweep-and-reject, with and without
a cycle-position gate, at 1R, 1.5R and 2R targets — **not one has reached a profit factor of 1.0.**
The best is E13's 0.749.

**The honest position on the requirement:** the labs can produce a bidirectional *structure* on demand.
Neither can yet produce a bidirectional *edge*, because no short leg works. Adding a losing leg to a
break-even leg makes the system worse, not more complete — so shipping a bidirectional build now would
be worse than shipping nothing.

**The right next work is on the short side alone**, judged on its own profit factor, until one clears
1.0. Everything else is premature.


---

## ██ HARD LESSON 9 — A GATE IS ONLY GOOD RELATIVE TO THE ANATOMY OF ITS SETUP

**Earned:** War Formation E28, 2026-09-02, and confirmed against E14 which is its mirror image.

Nine short constructions into War Formation, recovering E13's source revealed that the **long has
required a volatility coil since v1 and no short had ever included it.** Adding it looked like
correcting an oversight. It cut 22 of 39 trades and dropped profit factor from **0.749 to 0.490** —
removing disproportionately the winners.

**Why:** a coil is stillness before a spring. The long is a *reclaim* — sweep a low, go quiet, snap
back — so stillness is part of that setup's anatomy. The short is a *rejection at resistance*, which
happens while the market is already moving. Demanding quiet first selects for rallies arriving
exhausted, which are exactly the ones that keep grinding instead of turning.

**E14 is the same lesson from the other side:** there a weakening-run gate removed good *longs*
because it duplicated the coil. Here the coil removes good *shorts* because it contradicts them.

**How to apply:** before porting a component between legs, systems or labs, ask what the setup is
*physically doing* and whether the gate describes a state that setup passes through. **Symmetry of
components is not symmetry of logic.** This is now the fifth cross-inheritance failure in these labs
— see the no-mirror rule, E18's volatility-filter transfer, and the BTC location rule.

---

## ██ HARD LESSON 10 — MEASURE THE TERMS BEFORE TESTING THE CONJUNCTION

**Earned:** 3M Elite v19/v20, 2026-09-02.

Four cycles were spent filtering a population whose size had never been measured. v16, v17 and v18
each fixed something genuinely wrong and each returned **0 trades**; v9, v10 and v11 each landed on
exactly **3**. The binding constraint was one clause in the engulf definition — `open < prevClose`, a
gap requirement — which is meaningful in equities and meaningless in a market that never closes.
Removing it took the population from **10 to 2,711** across 4.7 years.

**How to apply:** when an entry is a conjunction of N terms, **count each term alone before testing
them together** — a counter build with a one-bar exit, since this engine returns no plot values. And
when a definition is inherited from another market, check that its *preconditions* exist here. When
successive independent fixes produce the same trade count, stop fixing and start counting.


---

## ██ HARD LESSON 11 — DECLARING A CAVEAT IS NOT BOUNDING IT

**Earned:** War Formation 950-1 / 950-2 / 950-1b, 2026-09-02.

950-1 shipped with a stated defect: an armed level blocked re-arming until it resolved or expired. I
wrote that it "depresses both counts, so the ratio is the robust output" and published a 51.3% hit
rate. **The fix moved the take count from 1,589 to 4,864** — more than the original run had counted
as signals — and the true hit rate is **95.0%**. Two conclusions were published off a number that a
one-credit re-run would have corrected.

**Why:** stating a limitation feels like handling it. It is not. A declared defect with an assumed
direction and an unmeasured magnitude is still an unmeasured defect, and reasoning about its size is
exactly the kind of inference the lab exists to avoid.

**How to apply:** when a run has a known defect, **the next run fixes the defect** — it does not
build on the flawed output and it does not reason about the bias. If the defect is discovered after
publishing, withdraw the number explicitly rather than footnoting it. See also HARD LESSON 10:
measure the term, do not estimate it.

---

## ██ HARD LESSON 12 — A HALF-SAMPLE VERDICT TRAVELS ONLY AS FAR AS THE GATE FAILS TO BIND

**Earned:** BTC Attacks 9-13, 2026-09-02.

Three gates were tested on the failing half of the sample, then two were re-tested on the whole.

| Gate | H2 verdict | Full-sample verdict | Trades removed (full) |
|---|---|---|---|
| EMA200 trend | inert | **generalised** | 6 of 134 |
| highVol split | harmful | **inverted — load-bearing** | 79 of 207 |

After the first reversal I wrote that half-sample diagnostics cannot decide anything. **That was an
overcorrection.** The trendOk verdict generalised exactly.

**The rule that actually fits both results:** a gate that barely binds has almost no room to behave
differently in another regime, so its half-sample verdict travels. A gate that binds hard is
*re-selecting the sample*, so what you measured is a property of that regime, not of the gate.

**How to apply:** read the TRADE COUNT before deciding how far a partial-sample result generalises.
Few trades removed → the verdict is probably general. Many removed → assume it is regime-specific
until a full-sample run says otherwise. This is cheaper than re-running everything on the full sample
and it explains, rather than just accommodates, both outcomes.


---

## ██ HARD LESSON 13 — THE RISK-REWARD AXIS IS NEUTRAL AT BEST. STOP SPENDING CREDITS ON IT.

**Earned:** three independent mechanisms, 2026-09-02.

| Lab | Mechanism | Target change | Result |
|---|---|---|---|
| BTC | VWAP mean-reversion | 2R → 3R | PF 0.9121 → 0.9100 — neutral |
| War Formation | HA cascade reclaim | 1.5R → 1R | PF 0.7490 → 0.6922 — negative |
| 3M Elite | Supply/demand zones | 2R → 2.5R | PF 0.8945 → 0.8804 — negative |

**Why:** moving a fixed target trades payoff against win rate at close to par. A further target
raises `avgWin/avgLoss` and lowers the hit rate by an offsetting amount; a nearer one does the
reverse. The two effects cancel to within noise, and what does not cancel is **commission**, which is
paid on every trade regardless. So the axis is neutral in principle and slightly negative in
practice.

**How to apply:** treat the risk-reward multiple as **already set** unless there is a specific,
stated reason to think a given system is off its own frontier — for example a target that is
physically unreachable, which is what v14 found and v15 fixed. That is a different failure (a broken
parameter) from tuning along a frontier (a neutral one). **Do not spend a credit moving R:R by 25%
and hoping.**

**Corollary, from 3M v25-v27:** the same logic applies to time stops once an interior optimum is
found in both directions. When up and down are both worse, the parameter is done — record it and
move to a different kind of question.
