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

## HARD LESSON 8 — a spec without saved Pine source is not a base (from cycle 008/009, 2026-09-02)
The CHAMPION-BOARD "current base" was described only in prose (007's markdown spec, then an EMA200
filter described in the board itself) with no Pine source ever committed to `strategies/pine/`. Two
concurrent sessions running this same mandate each reconstructed "the base" independently from that
prose and got different code: 433 trades / PF 0.912 / DD 28.8% in one, 649 trades / PF 0.9555 / DD
47.7% in the other (the second added a risk cap the first lacked). Same idea in English, different
strategy in Pine.

**Rule:** every base on the CHAMPION-BOARD must have committed Pine source in `strategies/pine/`
before the next cycle attacks it. If a source is missing, reconstructing it and re-running it in
isolation IS the cycle's mandatory first step, and the reconstruction's real numbers — not the old
spec's numbers, and not a rival session's uncommitted numbers — become the baseline the ratchet
compares against. Record the reconstruction as its own `results/backtests.json` entry so any
discrepancy is visible, not silently absorbed. When two committed reconstructions disagree, the one
with real source wins over the one without; between two real sources, prefer the one that follows
established lab convention (here: capping R like every sibling leg already does).

**Corollary, learned the same cycle:** a base that clears rung A deserves the SAME rung-C scrutiny as
any attack candidate (HARD LESSON 7) before the next several cycles lean on it. `008-vwm-base.pine`
passed 15m at PF 0.9555 but failed 5m at PF 0.7992 — the pass was noise, exactly as it was for 006.
Check generalization on the base itself, not just on cycles that individually clear rung A.

## HARD LESSON 9 — a 15m-only fix does not touch 5m fee drag (from cycle 010, 2026-09-02)
The ET witching-hour filter (ban longs 1:00–4:00am ET) improved the 15m base cleanly — PF
0.9555→0.9614, max DD 47.65%→45.78% — clearing the ratchet and rung A. Its 5m run came back
PF 0.7883, DD 52.22%: not just still-failing, but marginally *worse* than 008's own unfiltered 5m
result (PF 0.7992, DD 51.36%).

A time-of-day gate removes a slice of bars roughly proportional to its width regardless of
timeframe, so it *should* transfer if the edge it's cutting is real. That it didn't move 5m at all
means the 5m loss isn't concentrated in that window — it's fee drag from trade frequency and R
sizing, the mechanism HARD LESSON 3 names directly. **Rule:** a candidate change should be judged by
whether it plausibly touches the failure mode rung C already diagnosed (fee drag on 5m), not just
by whether it improves the 15m number. Selectivity filters (time-of-day, shallow pullback) prune
bars; they don't change the R-vs-fee ratio. The R floor (attack list item 1 as of cycle 011) is the
first change on this base that hits the actual mechanism.

## HARD LESSON 10 — a flat % R floor binds harder on the tighter timeframe (from cycle 011, 2026-09-02)
Cycle 011 raised the min-risk floor from 0.8% to 1.2% of price, reasoning from HARD LESSON 3/9 that a
wider floor dilutes the fixed 0.10% round-trip fee and should help *both* timeframes. It helped 15m
cleanly — PF 0.9614→1.0211, max DD 45.78%→40.67%, the first time this base line has cleared PF 1.0 —
but 5m came back *worse* than the pre-change base on both metrics: PF 0.7883→0.7769, max DD
52.22%→57.02%. Not flat, like the time-of-day filter in cycle 010 — actively worse.

The likely mechanism: `rawR` (distance from close to the structural swing low) is naturally smaller
on 5m than 15m, because 5m swings are tighter. That means the min-R floor binds — i.e. `rawR` gets
overridden by `minR` — on a larger share of 5m trades than 15m trades. Raising the floor therefore
inflates nominal per-trade risk *more* on 5m than on 15m, which widens 5m's losses and drawdown
instead of just diluting its fee drag.

**Rule:** a fee-economics argument ("wider R dilutes the fixed fee") is necessary but not sufficient
— it ignores how a *flat percentage* floor interacts with a timeframe's typical structural stop
distance. Before trusting a stop-sizing change to transfer across timeframes, check what fraction of
trades are floor-bound on each timeframe; if that fraction differs a lot, the change's effect will
differ a lot too, in a direction that isn't obvious from the fee math alone. A volatility-relative
floor (e.g. a multiple of ATR%, not a flat % of price) is the natural fix and is now on the attack
list.

## HARD LESSON 11 — a selectivity filter can shrink the loss without fixing the edge (from cycle 012, 2026-09-02)
Cycle 012 added a volume-confirmation gate (current volume >= its 20-bar SMA) to the pullback-hold
bar, predicting per HARD LESSON 9 that pruning bars (rather than resizing risk, as 011's R-floor did)
would avoid 011's 5m regression. It delivered the best 15m result this base line has ever posted — PF
1.0211→1.0237, max DD 40.67%→21.95%, a ~19pp drawdown improvement — and did shrink 5m's damage: max DD
57.02%→47.78%, net loss −49.83%→−41.82%, trades 622→466.

But 5m profit factor did **not** clear 0.95, and it did not even fully recover to pre-011 levels:
0.7769 (011's 5m) → 0.7544 (012's 5m). avgTradePct got slightly worse (−0.0801%→−0.0897%). The filter
removed low-conviction bars roughly proportionally across both win and loss buckets — smaller book,
similar edge quality — rather than disproportionately removing losers.

**Rule:** a change that measurably improves drawdown and shrinks total loss is not the same as a
change that fixes the underlying edge. Judge rung C strictly on PF crossing 0.95, not on "moved in
the right direction." The 5m failure mode (HARD LESSON 3/9: fee drag interacting with how R is sized
relative to structural stop distance) has now survived two different attack types — a risk-resizing
change (011) and a bar-pruning selectivity change (012) — without being fixed. The next candidate
should target the R-sizing mechanism directly (a volatility-relative floor, attack list item 1) rather
than another selectivity filter, since selectivity alone has now been tried and holds the loss steady
without moving PF.

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

## ██ HARD LESSON 22 — A LAB CAN ONLY VALIDATE OUTSIDE THE WINDOW IT TUNED ON, AND UNTIL IT DOES, IT HASN'T

**Earned:** BTC Attack 31, 2026-09-03.

The BTC 5m base was tuned across 29 attacks — seven filters, a signal-term sweep, a six-point
`coolBars` curve, four KEPT changes — entirely within 2024-06-08 → 2026-09-01, because that is the
first bar 5m coverage has. There was no second window to check against until Attack 30 ported the
same code to 15m, which reaches back to 2022. Attack 31 split that 15m run at the coverage boundary:

| | Never tuned (2022–2024) | The tuned window (2024–2026) |
|---|---|---|
| Profit factor | **0.79859252** | 2.07724976 |
| Trades | 77 | 64 |

**The only period this mechanism has never been shaped by is a loser, on a bigger sample than the
current base's own headline number.** Attack 30 had called the blended full-window result (PF 1.232)
evidence the edge "survives out of period." It does not generalize — the tuned half was strong enough
(PF 2.08) to carry the untuned half's loss and still average above 1.0. Averaging a win with a loss
is not the same claim as a win.

**Why this is a different failure from HARD LESSON 20 (the aggregate ratchet can't see a distributional
change).** That lesson was about two halves of the SAME tuned window. This is about tuned versus
never-tuned, and the gap (0.80 vs 2.08) is roughly ten times wider than anything the within-window
splits ever found. A lab whose only data source starts where its tuning starts has never actually
been out-of-sample tested, no matter how many gates, filters, or coolBars values it has swept — it has
only ever cross-validated against itself.

**How to apply:**
- **Before treating any full-sample or blended number as evidence of a durable edge, ask what window
  the tuning was DONE on, not just what window the final number was MEASURED on.** If they're the
  same window, no amount of internal sweeping substitutes for external data.
- **When a mechanism's tuning coverage and its data coverage start at the same date, that coincidence
  is not a green light — it is the reason no genuine out-of-sample test has happened yet.** Actively
  look for a longer-history proxy (a coarser timeframe, as here) specifically to break that
  coincidence, and do it before crediting any KEPT change with generality.
- **A positive blended average across a tuned and an untuned period is compatible with the untuned
  period being a clear loser.** Report the two halves separately before quoting the blend, every time
  a boundary like this exists — do not wait for a queue item to force it, since the blend actively
  hides the failure it should reveal.
- **This generalises to the other two labs.** War Formation and 3M Elite have both tuned exclusively
  within whatever window their own working data covers; neither has run this same test. Until they
  do, their KEPT/champion claims carry the identical caveat this one just earned.


---

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


---

## ██ HARD LESSON 14 — TRADERS SEE ACCURATELY AND PRESCRIBE BADLY. MINE THE OBSERVATIONS.

**Earned:** two independent sources, nine measured items, 2026-09-02.

| Source | Items tested | Descriptive claims | Prescriptive claims |
|---|---|---|---|
| The Oracle (video material) | 5 | 1 of 1 helped — the diagnostic item | 0 of 4 helped |
| The 950 Rule (user-supplied) | 4 | **2 of 2 TRUE** | **0 of 2 TRUE** |

**The 950 Rule split perfectly along that seam.** Its descriptive claims measured out: reaching x950
does mean the whole number gets taken (95.0%), and break velocity is a real, balanced distinction
(48/52 on 4,864 events). Its prescriptive claims both failed: strong breaks do not continue
(PF 0.605) and weak breaks do not fade profitably (PF 0.732).

**Why this happens.** A trader's observations are compressed experience of what a chart actually
does, and they survive mechanisation because they are statements about the market. Their rules are
compressed experience of *how that person trades* — including discretion, position sizing, sizing
down, waiting, and skipping setups that "look wrong" — and none of that survives mechanisation,
because the parts that were doing the work were never written down.

**How to apply:** when new trading material arrives, **split it into what it SEES and what it TELLS
YOU TO DO before spending a credit.** Measure the observations first — they are cheap counters and
they usually hold. Treat every instruction as an untested hypothesis with a poor prior. Do not
abandon a source when its rules fail; the observation that survives is often the useful part, as the
Oracle's cycle-position diagnostic was.

**Corollary:** a source whose observations FAIL is a different matter, and should be dropped quickly.
Neither of these two has failed that test.


---

## ██ HARD LESSON 15 — THE BINDING TEST BELONGS ON THE SIGNAL, NOT ONLY ON THE FILTERS

**Earned:** BTC Attack 15, 2026-09-02 — the first change ever KEPT by that lab's ratchet.

Fifteen attacks. Seven entry filters, three exit changes, two timeframe ports, three gate
re-validations — **all reverted.** Attack 15 removed `reachedUpper`, the +2σ excursion requirement
**the strategy is named for**, and both ratchet terms improved: PF **1.02025 → 1.15253**, drawdown
**16.68% → 16.54%**, trades 128 → 166, win rate 39.13% → 44.58%.

**The stretch requirement was deleting 38 net-positive trades.** It was not selective; it was
harmful.

**Why fifteen cycles missed it:** every attack targeted something classified as a *filter*. The
signal's own terms were treated as the thing being filtered and were therefore never questioned. The
strategy's name functioned as an unexamined assumption about which term carried the edge.

**How to apply:**
- **A strategy's name is a hypothesis, not a description.** Test it like any other term.
- Enumerate every term in the entry conjunction and apply the E17 binding test to **all** of them —
  signal terms included — reading the trade count to see how much each one does (HARD LESSON 12).
- When a lab has reverted many changes in a row, the fault is more likely in what it has declined to
  question than in the changes it keeps trying.
- **After a signal term changes, previously settled filter verdicts are no longer valid.** They were
  measured against a different signal, and the ratchet's own rule permits re-testing a reverted change
  against a genuinely changed base.


---

# ██ LEVERAGE: WHAT EVERY BACKTEST IN THIS PROJECT ASSUMED (user note, 2026-09-02)

The user raised that War Formation is traded **leveraged, around 86x**. That was never stated before
and it changes how these numbers must be read. Recording it properly because it affects all three
labs.

## WHAT THE ENGINE ACTUALLY RAN
Every run in this project carries the same forced parity profile, visible in each result's
`parityAdjustments`:

```
margin_long = 100, margin_short = 100      -> 100% margin = 1x. NO LEVERAGE.
default_qty_type = percent_of_equity, 100  -> position notional = 100% of equity
```

**The engine OVERRIDES whatever the Pine asks for** — the adjustment is logged as
`mcp_parity_profile_margin_100` on every single backtest. So leverage cannot be set here, and every
result in all three labs is **1x**. That is a constraint of the tool, not a choice I made, and it
cannot be worked around by editing the strategy declaration.

## WHAT LEVERAGE DOES AND DOES NOT CHANGE

**UNCHANGED — these are ratios, so they are leverage-invariant:**
- **Profit factor.** Gross profit / gross loss. Multiply every trade's P&L by 86 and the ratio is
  identical. **Every edge conclusion in this project therefore still stands at any leverage.**
- **Win rate, payoff ratio, trade count, the ranking of one config against another.**

**SCALES ROUGHLY LINEARLY:**
- **Return and drawdown.** Both are multiplied by the leverage factor.

**So the ratchet's verdicts are all still valid.** A configuration with PF 0.61 does not become
profitable at 86x — **it loses money 86 times faster.** Leverage is a magnifier, never a source of
edge, and nothing in this project's conclusions changes because of it.

## THE ARITHMETIC THAT DOES MATTER, AT 86x

Liquidation occurs at roughly a **1/86 = 1.163%** adverse move against the position, before fees and
maintenance margin — so in practice sooner.

| Champion v6 parameter | Value at 1x | At 86x, sized 100% of equity |
|---|---|---|
| Min stop distance (`minRpct`) | 0.15% of price | **12.9% of equity per loss** |
| Max stop distance (`maxRpct`) | 1.50% of price | **129% of equity — liquidated** |
| Max drawdown | 3.10289714% | **~267% — account gone** |

**The champion's own maximum stop distance exceeds the liquidation threshold.** At 86x with
full-equity sizing, a single trade that runs to its widest permitted stop wipes the account before
the stop is ever reached. And the observed 3.10% drawdown — which is genuinely excellent at 1x —
becomes an impossible ~267%.

## WHAT THIS MEANS PRACTICALLY

**Leverage and position size are the same dial, and only one of them can be at maximum.** The
backtests size at 100% of equity because that is what the parity profile forces. At 86x, the position
*fraction* has to come down by the same order for the risk per trade to stay survivable — 86x on 1%
of equity is the same risk as 1x on 86%. Used that way, leverage is a capital-efficiency choice
(less margin tied up for the same exposure), not a returns multiplier.

**How to read every number in this project from now on:**
- **Profit factor, win rate, payoff — take at face value.** Leverage-invariant.
- **Return and drawdown percentages — these are 1x figures.** Multiply by the leverage actually used,
  and check the result against 100% before treating any configuration as tradeable.
- **A drawdown that looks small may not be.** v6's 3.10% is the best in the project at 1x and is
  fatal at 86x with this sizing.

**This is arithmetic about the backtests, not advice about what to trade.** The sizing decision is
the user's; what this lab can say is what the numbers mean at each leverage.


---

## ██ HARD LESSON 16 — A LOAD-BEARING TERM WITH A NARROW OPTIMUM IS A CURVE-FIT WARNING

**Earned:** War Formation E32 + E33, 2026-09-02.

E32 showed the 3m coil is the term that carries the champion: remove it and PF goes 1.686 → 0.611.
E33 then varied its threshold for the first time: coilK 0.85 → 0.75 gives **0.749**.

| coilK | Profit factor | Trades |
|---|---|---|
| removed | 0.611 | 67 |
| 0.75 | 0.749 | 23 |
| **0.85** | **1.686** | **32** |

**Steep falloff on both sides of one setting, on a 32-trade sample.**

**Why this pairing is the diagnostic, not either result alone.** A term that barely binds can sit on
a narrow optimum harmlessly — it is not doing much either way. A term that carries the strategy AND
sits on a narrow optimum means the strategy's entire result depends on one number being exactly
right, which is what curve-fitting produces.

**How to apply:**
1. **After establishing a term is load-bearing, immediately test its threshold in both directions.**
   The two tests are a pair and neither is complete alone.
2. **Graceful degradation is the evidence you want.** War Formation E19 found greenBull 4 → 3 held at
   PF 1.28 — that is what a robust parameter looks like, and it is why E19 was the champion's best
   evidence until now.
3. **Report the sensitivity profile alongside the headline number**, not in a footnote. A profit
   factor without its parameter neighbourhood is an unqualified claim.
4. **One intermediate point resolves it.** Testing the other side of the peak distinguishes a plateau
   edge from a spike, and it is cheaper than any new construction.


---

## ██ HARD LESSON 17 — STATE THE DEMOTION CRITERION BEFORE THE RUN, THEN HONOUR IT

**Earned:** War Formation E33 → E34, 2026-09-02, when the project's only "champion" was demoted.

E33 found the champion's load-bearing parameter collapsed when tightened. Before running E34 — the
loose side — the log recorded both outcomes in advance:

> *PF holds near 1.686 → 0.85 sits on a plateau and the champion is defensible.*
> *PF collapses → the peak is one point wide, the champion should be demoted to "best fitted result",
> and the honest position is that this lab has no validated strategy.*

**It collapsed: 0.41366124, the worst of the four points tested.** So v6 was demoted, and the board
now says this lab has no validated strategy.

**Why writing it down first mattered.** After a result arrives there is always a way to soften it —
different threshold, sample-size caveat, "the trend is still favourable". Fixing the criterion in
advance removes that latitude. It is the same discipline as the counter builds (HARD LESSON 10) and
the forward predictions on trade count: **the value comes from committing before the data, not from
interpreting after it.**

**How to apply:**
1. **Before a decisive run, write down what each outcome will mean** — including the outcome that
   destroys the result you like. Put it in the Pine comment and the notes field, where it is
   timestamped by the run itself.
2. **When the unfavourable outcome lands, report it in the same terms.** No new caveats invented
   afterwards.
3. **Separate what is damaged from what survives.** E34 destroyed the claim that v6 has an edge; it
   did NOT destroy E32's finding that the coil is load-bearing, which holds at every threshold. Being
   precise about the boundary is what keeps a negative result useful.


---

## ██ HARD LESSON 18 — A TERM CAN LOOK INERT BECAUSE A REDUNDANT PARTNER IS COVERING FOR IT

**Earned:** BTC Attacks 13, 19 and 20, 2026-09-02.

| Removed from the base | Trades admitted | PF cost |
|---|---|---|
| `trendOk` alone (Attack 13) | +6 | −0.009 |
| `vwUp` alone (Attack 19) | +10 | −0.027 |
| **both together (Attack 20)** | **+42** | **−0.108** |

Two separate tests each concluded a term "barely binds". Removing both showed the requirement they
share is worth **0.108 of profit factor** — four times what either measured alone.

**Why:** when two terms encode the same information through different instruments, removing one
leaves the other to exclude nearly everything the first would have. The measured effect of each is
then not the term's contribution but the *residual* not already covered by its partner.

**How to apply:**
- **HARD LESSON 12 needs this qualifier.** A low removal count means one of two things — the term
  does nothing, **or** something else is already doing it. The count cannot distinguish them.
- **Before concluding a term is inert, ask what else in the conjunction encodes the same idea.** Two
  trend measures, two volatility measures, two location measures. If a candidate partner exists, the
  "inert" reading is provisional until they are removed together.
- **Removing a redundant SET is one change, not several.** The attributable question is about the
  requirement, not the individual terms, and testing them separately is what produced the two wrong
  verdicts in the first place.
- **The reverse also holds:** a term that looks load-bearing may only be so because it is standing in
  for a partner that was deleted earlier. Re-check surviving terms after any removal.


---

## ██ HARD LESSON 19 — "BOUNDED BY A WORSE VALUE" AND "BOUNDED BY DEGENERACY" ARE DIFFERENT BOUNDS

*(BTC Attacks 22–24, 2026-09-02, against War Formation E40/E41)*

HARD LESSON 16 says a parameter is not measured until both of its neighbours are. Attacks 22–24 show
that satisfying it **literally** can still leave a weak result, because there are two ways a
neighbour can fail and only one of them is evidence about the parameter.

`coolBars` 30 / 60 / 120 / 240 gave PF 1.003 / 1.153 / 1.304 / 2.302 on 231 / 166 / 77 / **7** trades.
The 240 case has the best ratios in the lab and tells us nothing: seven trades, none in the final
fourteen months of the window.

**Why:** a neighbour that comes back *measurably worse* is a reading of the response curve — it says
the parameter has an interior optimum. A neighbour that comes back *degenerate* says only that the
condition stopped occurring. The first bounds the peak; the second bounds the DATA. Quoting an
interior optimum on the strength of the second overstates what was measured.

The sister lab's shield sweep is the contrast: $1,000 through $4,000 all produced 19–27 trades, so
every point was a real reading and $2,000 sat on an actual curve. Here the upper side ran out.

**How to apply:**
- **Record which kind of bound you have.** "Both neighbours measured" is not sufficient detail; say
  whether each neighbour was worse or was degenerate.
- **Watch the trade count's SECOND difference, not just its level.** Decay of −28%, −54%, −91% is not
  a filter tightening smoothly — a super-exponential fall means the condition has moved into the tail
  of its own distribution and has become a *different, rarer* condition rather than more of the same.
- **Set the interpretability floor BEFORE the run and honour it.** The floor is what stops a
  seven-trade PF of 2.30 from being read as the best result ever produced.
- **A degenerate upper bound is a queue item, not a closed question.** The fix is a finer grid on the
  measurable side (90, 150), which can still distinguish a broad peak from a narrow one.


---

## ██ HARD LESSON 20 — AN AGGREGATE RATCHET CANNOT SEE A DISTRIBUTIONAL CHANGE

*(BTC Attacks 25–27, 2026-09-02)*

The ratchet keeps a change if whole-sample profit factor improves and whole-sample drawdown does not
worsen. Attack 26 satisfied both — PF 1.3038 → 1.3499, DD 8.12% → 7.14% — and in doing so **widened
the H1/H2 spread from 0.0016 to 0.2566**, undoing the single most valuable property the strategy had.

**Why:** both ratchet terms are aggregates over the whole sample. A change that adds five good trades
to the strong regime and three bad ones to the weak regime improves both aggregates while making the
strategy *less* uniform. The rule cannot express the difference, so it silently prefers the version
that is better on average over the version that is better everywhere.

**How to apply:**
- **A metric measured on a base is void when the base changes.** Attack 25's spread was quoted for two
  cycles after the configuration it described had been replaced. Re-measure headline claims after any
  KEPT change, not only after ones that look relevant — Attack 26 deleted the LEAST binding term in
  the strategy and still moved the spread by 0.25.
- **HARD LESSON 12 extends to regimes:** an aggregate count says nothing about distribution. Attack
  26's 8 trades split 5/3, almost proportionally, while their effect split +0.151/−0.105.
- **A suspiciously exact agreement is evidence of noise, not of structure.** The 0.0016 was recorded
  with that suspicion already attached, and the suspicion proved correct. Write the doubt down at the
  time; it is worth far more than restating it afterwards.
- **When a rule fails to capture something that matters, surface it as a rule question rather than
  quietly applying a better rule.** Changing the ratchet mid-experiment would make every prior KEPT
  and REVERTED verdict incomparable.


---

## ██ HARD LESSON 21 — A RESULT WITHOUT ITS SOURCE ON DISK IS NOT A RESULT

*(War Formation E44, 2026-09-02)*

E38 was this lab's best configuration for six experiments. E44 attempted a byte-identical re-run to
read a number that had not been recorded, and got **PF 0.346 on 28 trades against E38's 1.502 on 21**.
The source had never been written to `pine/`. The log held the metrics and an English description of
the build; that was not enough to rebuild it.

**Why:** a prose description of a strategy is lossy in ways that are invisible until reproduction is
attempted. Every parameter can be listed correctly and the program still differ — in a gate that went
unmentioned because it seemed obvious, an ordering, a default. **The metrics are a hash of the code,
and without the code they cannot be checked, extended, or compared against.**

**The compounding cost is the real damage.** E42 and E43 were both measured against E38's number.
Neither verdict survives, because neither was comparing what it claimed to compare. **Two full cycles
of work were spent producing deltas against an unanchored baseline.**

**How to apply:**
- **Write the Pine to `pine/` (or `strategies/pine/`) in the SAME action that records the metrics.**
  Not afterwards, not when the build looks promising — a run that is worth recording is worth saving.
- **Re-derive a baseline before comparing against it** whenever the source is not on disk. One
  reproduction run is far cheaper than two cycles of void conclusions.
- **Record the composition, not only the aggregate.** E38's leg split was the trigger here; had it
  been captured at the time, the defect would have surfaced six experiments earlier.
- **A failed reproduction is a finding worth publishing**, not an embarrassment to quietly re-run. It
  reclassifies every result that depended on the unreproducible one.
- **This generalises past the ALCM:** E36–E41 have the same defect, so the $2,000 shield optimum rests
  on the same unverifiable ground as E38.


---

## ██ SOURCE AUDIT, 2026-09-02 — HARD LESSON 21 WAS NEVER A WAR FORMATION PROBLEM

E44 found that War Formation's E38 could not be reproduced because its source had never been saved.
An audit of all three labs immediately afterwards found the same defect everywhere:

| Lab | Base at audit time | What was actually on disk |
|---|---|---|
| BTC | Attack 29 (`coolBars` 150) | `002`–`006` — the discovery strategies REJECTED before the mandate changed |
| War Formation | none (2x2 closed) | `alcm-reference.pine`, created an hour earlier by the E44 failure |
| 3M Elite | v30 (zone freshness) | `3m-elite-v1.pine` only |

**Not one of Attacks 1–30 had been written to disk. Neither had any 3M version after v1.** Three labs,
roughly a hundred recorded backtests, and the working history existed as metrics plus prose — the
exact form that proved insufficient to rebuild E38.

### WHAT WAS DONE
- **BTC: fixed.** `strategies/pine/vwm-base-current.pine` now holds the exact program behind Attack 29,
  with its result URL, the four KEPT changes that produced it, the full six-point `coolBars` curve,
  and Attack 30's out-of-period figure in the header.
- **War Formation: already fixed** by E44's fallout.
- **3M Elite: NOT fixed, and deliberately not faked.** v30's source is gone. Reconstructing it from
  SYSTEM.md prose and running v31 against the reconstruction is precisely the error that voided two
  War Formation cycles today, so no 3M experiment should run until the base is rebuilt and saved.

### THE GENERAL POINT
**A lab's real state is what is on disk, not what is in its log.** Every lab here believed it had a
base; two of the three could not have produced one on demand. The defect is invisible until something
forces a reproduction, and by then the comparisons built on it are already void.

**Audit the sources whenever a base is promoted, not only when a reproduction fails.**


---

## ██ HARD LESSON 22 — AN AGGREGATE THAT SPANS TUNED AND UNTUNED DATA REPORTS THE TUNED PART

*(BTC Attacks 30–31, 2026-09-02)*

Attack 30 ran the base over 4.7 years of 15m data and returned **PF 1.232 on 141 trades**. It was
recorded as the first evidence the edge survives out of period. Attack 31 split that same window at
the date the tuning data begins:

| | Profit factor | Trades |
|---|---|---|
| Never-seen half | **0.799** | 77 |
| Tuning-era half | **2.077** | 64 |

**The aggregate was a blend of a losing strategy and a fitted one, and it read as mildly positive.**

**Why:** a profit factor pools gross profit and gross loss across the whole span. A strongly fitted
segment can carry a losing one to a number above 1.0 while hiding that half the record is negative.
The pooled figure is not a compromise between the halves — it is dominated by whichever half has the
larger gross flows, and the fitted half usually does.

**How to apply:**
- **Split before you claim.** "Survives out of period" is a statement about the halves, and only a
  split can support it. An aggregate that merely INCLUDES unseen data proves nothing about it.
- **Find the date the tuning data begins and treat it as the split.** Here it was 2024-06-08, the
  first bar of 5m coverage — an infrastructure detail that silently defined the in-sample window for
  thirty-one experiments.
- **Compare the drawdowns, not only the profit factors.** The combined run's max drawdown equalled
  the losing half's to eight decimals, which alone revealed where all the risk lived.
- **A monotone parameter with no interior optimum is a fitting signature.** `coolBars` improved the
  score at every step as it grew more selective. That is what fitting a window looks like from the
  inside, and HARD LESSON 20's ratchet blindness was a symptom of it.
- **Withdraw the claim in the same words it was made in.** It was written as "the edge survives out of
  period"; it has to be unwritten that plainly, in the same document, not softened into a caveat.


---

## ██ HARD LESSON 23 - LEVERAGE IS NOT RISK, AND A REPEATED CAVEAT IS NOT A CHECKED ONE

*(War Formation position-sizing review, 2026-09-02)*

For most of this lab's life the log, the cycle prompts and the session summaries all carried a
version of: "drawdown is a 1x figure and far past total loss at the ~50x the shield implies."

**It was never true.** The engine forces `percent_of_equity = 100` and `margin 100/100`, so notional
is one unit of equity and risk per trade is set by the SHIELD - a fixed dollar distance - not by
venue leverage. At BTC ~$100k a $2,000 shield on a 0.1 BTC position is $200, or **2% of equity**.
The recorded drawdowns were already correctly scaled.

**Why:** on a perp, leverage determines MARGIN POSTED, not position size. The same 0.1 BTC costs
$10,000 of margin at 1x or ~$172 at 58x; the trade, the shield and the loss are identical. Ruin
requires raising the POSITION, which the specification's own liquidation-gap logic forbids.

**How to apply:**
- **A caveat that is restated every cycle is not thereby verified.** This one survived dozens of
  write-ups because repeating it felt like diligence. Diligence would have been four lines of
  arithmetic.
- **Check the claims that make you look careful first.** An overstated risk warning attracts no
  scrutiny precisely because it sounds conservative - which is exactly why it can persist unchecked.
- **Separate the three quantities every time:** notional (position size), margin (leverage), and risk
  (stop distance x position). Only the third is risk, and only the third belongs in a drawdown
  discussion.
- **The engine's parity profile is part of the model.** `margin_long/short = 100` is not a limitation
  to apologise for in every summary; it fixes notional at 1x equity, which is what makes the recorded
  drawdowns readable in the first place.


---

## ██ HARD LESSON 24 — "ZERO TRADES ON THE OTHER LEG" IS AN OUTCOME, NOT A CONSTRUCTION, UNTIL THE
## CODE IS READ

*(War Formation E48, 2026-09-02)*

E45 and E46 both describe deleting the short leg from the entry conjunction. The saved source that
inherited their lineage, `e47-alcm-long-cap12960.pine`, still had the full short leg live in code —
`goShort`, its regime/coil/trigger terms, and its `strategy.entry` block, all present and reachable.
E47's 21 trades were genuinely all long, but not because the code excluded shorts: on a single-position
engine (`pyramiding=1`, one `flat` gate shared by both directions), a long leg whose trades happen to
occupy the book for long enough, often enough, can starve every short setup of a flat book across an
entire 4.5-month window without a single line of code saying so. Changing an unrelated exit parameter
(`maxBars`, 12960 → 8640 or → 25920) shortened those occupancies just enough to let the short leg back
in — 21 of 31 trades at one neighbour, 16 of 24 at the other — and PF collapsed from 1.22 to 0.43–0.60
purely because the dead-weight leg (which this lab had already shown wins about 2 of every 73 times it
fires) got the chance to trade again.

**Why this is not the same failure as a curve-fit spike (HARD LESSON 16).** A spike means the edge
itself is fragile to the parameter. This means the parameter change re-admits a leg the entry
conjunction never actually excluded — the "long-only" description was true of the OUTCOME at one
parameter value, never true of the CODE. Retuning the parameter that exposed it cannot fix this;
deleting the leg can.

**How this was caught.** Not by re-running anything — by reading the actual entry logic in the saved
Pine file before trusting a neighbourhood-sensitivity result built from it, and separately by pulling
the real trade-level `direction` field for the anchor result (`get_trades`, a free read of an already
completed backtest, not a new one) instead of trusting a trade-COUNT match to a different build as
proof of composition. HARD LESSON 21 already warned that a result without its source on disk is not a
result; this is the sharper form — **a result whose source IS on disk can still not say what its
description claims, and the only way to know is to read the entry conditions, leg by leg, against the
prose that describes them.**

**How to apply:**
- **"Leg X was removed" is a claim about the code, not about a trade count.** Before trusting it, open
  the saved source and confirm the leg's entry condition cannot fire — not that it happened not to.
- **On any single-position engine, a trade count of zero for one leg is consistent with two entirely
  different facts:** the leg was excluded, or the leg was merely never offered a flat book. These are
  distinguishable only by reading the code or by testing a parameter that changes occupancy (as this
  neighbourhood check did, by accident of what it was meant to test for something else).
- **Before running a sensitivity sweep on a build described as single-leg, verify the description
  against the code first.** A sweep run on a mislabelled build measures the mislabelling, not the
  parameter.
- **Prefer reading the trade list's own `direction`/`entryId` field over inferring composition from a
  trade-count match to a different run.** E46's "no shorts" claim rested on its count matching E43's
  long-only count — plausible, but a coincidence, not a verification; this cycle's actual check of
  E47 used the real per-trade field and only then could rule out one explanation from the other.

---

## ██ HARD LESSON 25 — A RESULT ON DISK CAN STOP REPRODUCING ITSELF. VERIFY BEFORE BUILDING ON IT, NOT
## JUST BEFORE COMPARING AGAINST IT

**Earned:** War Formation E50, 2026-09-03.

The consolidated queue's item 1 asked for a minimal, mechanical change: delete the short leg from
`pine/e47-alcm-long-cap12960.pine` and confirm the result still reproduces E47's documented 21
all-long trades. The deletion (e50a) came back with **10 trades** — impossible if E47's own "zero
shorts, occupancy accident" description were still true of the current file, since removing an inert
leg cannot change the surviving leg's count by more than book-occupancy noise, and 21 vs 10 is not
noise.

**That contradiction forced a check nothing in the queue had asked for: an exact, unmodified re-run of
`pine/e47-alcm-long-cap12960.pine` itself.** It returned **PF 0.58008733, 24 trades (9 long, 15
short)** — not the documented PF 1.21869905, 21 trades, all long. Same file, same code, same declared
window (2025-12-16 to 2026-05-03). **E47 does not currently reproduce E47.**

**Why this is a different failure from HARD LESSON 21/24.** Those were about source that was never
saved, or saved source that never matched its own prose description — both are defects fixed once,
at save time, and stable afterward. This is a result that had a real source on disk, verified once
against its own trade list (E49, via `get_trades`), and **stopped matching that verification on a
later, byte-identical re-run.** Nothing in this lab's process could have caught it earlier, because
nothing before E50 ever re-ran an already-anchored file just to check it still behaves the same way.

**The likely mechanism, not yet isolated:** the short leg's firing depends on exact book-occupancy
timing (HARD LESSON 24), which is sensitive to the precise bar-by-bar path — so either the underlying
1m data for this fixed historical window has been revised/re-ingested since E47 ran, or the backtest
engine itself changed (`engineVersion: tv_jul26_mc7` on both runs, so if it changed, the tag didn't
move), or there is genuine non-determinism in the engine across otherwise-identical calls. This cycle
did not have credit budget left to distinguish these after the two runs above; it is the top item for
whichever cycle picks this up next.

**How to apply:**
- **A construction check that comes back somewhere it structurally cannot be is itself a finding, not
  a bug to shrug off.** e50a's 10-vs-21 gap was the tell; treating it as "must be my diff" and moving
  on without the confirming re-run would have buried the real defect under a wrong explanation.
- **"Verified once" is not "verified."** E49's `get_trades` check on E47 was real and correct *at the
  time it ran*. It did not survive to E50. Anchors should be treated as perishable until this lab has
  evidence they are not — re-check a load-bearing anchor's own reproducibility before spending more
  cycles building on it, not only when a downstream number looks wrong.
- **Do not silently re-baseline.** E47 is reclassified here as "recorded but UNREPRODUCIBLE," the same
  status E38 carries. It is not deleted from the log and its old number is not quietly replaced by the
  new one — both are recorded, dated, and flagged, exactly as HARD LESSON 21 requires for the original
  case.
- **This is now the second- and third-best results this lab has ever produced (E38, then E47) that
  failed to reproduce.** Whatever the root cause turns out to be, the base rate for "this lab's best
  number survives a re-run" is currently 0 for 2. Treat every future headline PF as provisional until
  it has been re-run at least once, cold, before it is used as a comparison baseline for anything else.

## ██ HARD LESSON 26 — A STALE SCHEDULED PROMPT REPEATING AFTER A BOARD HALT IS A NOTIFY, NOT A NO-OP (BTC, 2026-09-03)

The BTC lab's scheduled cycle prompt is stored text that predates Attack 30. After Attack 31/32
retired the base, one cycle correctly found the prompt superseded, ran nothing, and recorded the
halt on the board. The *next* firing carried the identical unedited prompt and produced the
identical verdict — a second cycle burning a full read-the-board-and-conclude-nothing pass because
the thing that needed to change (the stored prompt, or the user's answer to the open questions) is
outside any single cycle's power to fix.

**How to apply:** a board halt that survives one full cycle unchanged is not still "in progress" —
it is stuck, and a second identical cycle check will not unstick it. The correct action on the
*second* consecutive no-op is not a third quiet board entry; it is flagging to the user, explicitly,
that the automated loop cannot proceed without them (a successor mechanism/instrument decision, or
an update/pause to the stored prompt itself). Recording the halt is necessary but not sufficient —
a halt nobody outside the repo will read is not a halt anyone will act on.

## ██ HARD LESSON 27 — A DIFFERENT CONSTRUCTION LANDING ON AN ORPHANED RESULT IS EVIDENCE ABOUT THAT RESULT'S TRUE SOURCE, NOT A COINCIDENCE TO WAVE AWAY (WAR FORMATION, 2026-09-03)

E50 established that `pine/e47-alcm-long-cap12960.pine` — coilPrev present, full short leg present —
no longer reproduces its own documented headline (PF 1.21869905, 21 trades, all long). That failure was
left as an open root cause: data revision, engine drift, or genuine non-determinism, in that order of
suspicion.

E53, run for an unrelated reason (testing whether `coilPrev` binds on the long leg alone, via a file —
`e50b` — that had never been run before), landed on **the exact same number**: PF 1.21869905, DD
17.44898097%, 21 trades, all long, to eight decimal places. e50b is not e47's file — it has the short
leg deleted from the code AND `coilPrev` removed, a strictly different construction. E54 confirmed E53
is itself stable under an immediate cold re-run, so this was not a fluke of that one call.

**A different, independently-built file reproducing an orphaned, unreproducible result exactly is not
noise — it is the strongest evidence yet of what actually generated that result.** The engine-drift and
data-revision hypotheses both predicted nearby files would drift together; E51/E52 already showed they
did not. This finding points somewhere more specific: the file saved on disk under the E47 name is
likely not the file that was actually run to produce the number recorded under that name — e50b's
construction is.

**How to apply:**
- **When an unrelated run reproduces a previously "unreproducible" number, treat that as a lead, not a
  curiosity.** The natural instinct is to log it as a nice coincidence and move on to the queue item the
  run was actually for. The coincidence IS the finding — chase it the same cycle, while the context for
  interpreting it (what changed, what didn't, what construction produced it) is still loaded.
- **"Source on disk" (HARD LESSON 21) can fail in a form neither HARD LESSON 21 nor 24 named yet: a file
  that was genuinely saved, genuinely readable, and STILL not the file that generated the result
  attached to it.** Verifying a result now has three tiers, not two: the source exists (21), the source's
  own construction matches its prose description (24), and the source reproduces the number recorded
  under its name (25) — a file can pass the first two and still fail the third, and this lesson shows a
  fourth check worth adding: does anything ELSE, run for a different reason, land on the same number?
  If so, that other file — not the named one — may be the real source.
- **Do not resolve this by editing the orphaned file's provenance after the fact.** e47's original
  entry in `backtests.json` is left exactly as it was recorded; the new understanding is recorded in the
  entries that discovered it (E50, now E53/E54), per HARD LESSON 21's own instruction not to
  silently re-baseline.

## ██ HARD LESSON 28 — CALIBRATING A COUPLED PARAMETER FROM ONE DATA POINT DOES NOT MEAN THE RELATIONSHIP IS LINEAR (WAR FORMATION, 2026-09-03)

E48 found the A.L.C.M. shield and `maxBars` are coupled: a wider shield needs a longer cap to resolve,
so sweeping shield width at a fixed cap just measures the cap. E48's own numbers looked like they
supported a linear fix — going from a $2,000 shield to $3,000 (1.5×) at the SAME fixed cap moved
avgBarsWinning from 56.5% to 84%, and a naive linear projection from the $2,000 anchor alone predicted
almost exactly that (~55.5% vs the actual — coincidentally close). That single point of agreement was
then used to scale `maxBars` linearly with shield width for a real sweep (E57): 1.5× shield → 1.5× cap,
2× shield → 2× cap.

**The linear projection failed on the very data it was supposed to unlock.** Both scaled runs came in
far above the targeted ~56% avgBarsWinning ratio (77% at $3,000, 97% at $4,000), and trade count
collapsed (21 → 13 → 8) because each trade's actual resolution time grew faster than the shield width
did — an occupancy effect (HARD LESSON 24), not a truncation effect (the cap itself barely bound: only
1-2 trades per run hit it, and always as forced wins, never as winners-turned-losses). **One point of
agreement between a linear model and a real measurement is not confirmation of linearity** — it is
consistent with linearity and with any number of other relationships that happen to agree near that one
point. The projection needed a second point to be trustworthy, and the sweep it was calibrating had no
budget left to get one before spending it.

**How to apply:**
- **A calibration built from a single data point is a guess with a number attached, not a verified
  relationship.** Before spending real credits on a projection's extrapolated range, ask what a SECOND
  point would look like if the model is wrong — here, that would have meant checking whether E48's
  84%-vs-projected-~55.5% agreement held at a nearby width too, before committing both of a cycle's
  credits to two extrapolated points at once.
- **A parameter that "just needs scaling" can still make the population unmeasurable.** Fixing the
  confound (cap truncating winners) does not guarantee the fix lands the result back above the
  interpretability floor — here it revealed a second, independent limit: total sample size shrinks
  mechanically as R widens, regardless of where the cap sits, because each trade occupies the book
  longer. Both limits have to be checked, not just the one the previous experiment named.
- **When a sweep can't be run cleanly on the data available, say so and stop, rather than reading the
  degenerate numbers as a verdict on the parameter.** E57's PF 0.60/0.69 at $3,000/$4,000 are NOT
  evidence wider shields hurt the edge — they are evidence this window's trade count cannot support the
  test at those widths. Conflating "unmeasurable" with "worse" would have closed off $3,000-$4,000
  shields on invalid grounds.
