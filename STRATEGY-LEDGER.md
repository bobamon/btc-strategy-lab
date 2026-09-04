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


---

## ██ HARD LESSON 29 — THE OCCUPANCY CONFOUND IS NOT SPECIFIC TO `maxBars`. IT APPLIES TO ANY PARAMETER
## THAT CHANGES HOW LONG A TRADE STAYS OPEN (WAR FORMATION, 2026-09-03)

E56 and E57 both diagnosed book-occupancy shifting the admitted trade set when `maxBars` changed — a
trade's exit bar moves, so the flat-book window every downstream signal depends on moves with it (HARD
LESSON 24). Both treated this as a property of the CAP specifically. **E58a/E58b show it is not.**

Sweeping `shieldUsd` DOWN from the $2,000 anchor to $1,000/$1,500 (with `maxBars` scaled
proportionally, the one direction this axis had never been tested), the three points came back
non-monotonic: PF 1.240 (36 trades) / 0.860 (28 trades) / 1.219 (21 trades, the e50b anchor) as the
shield rises. Neither a degrade-with-width trend nor a plateau — the exact anti-pattern HARD LESSON
28 flagged as the tell for a confound rather than a real reading.

`get_trades` confirmed it directly: e58a's and e58b's trade 1 is identical (same entry bar, same
price — the entry signal does not depend on `shieldUsd`), but its EXIT differs, because a wider
shield means both a wider stop and (at fixed `rr`) a wider target, so it takes longer to resolve
either way. That shifted exit re-opens the book at a different bar, so trade 2 onward diverge
immediately: **e58b's trade 2 is exactly e58a's trade 3, shifted by one**, because e58a's book was
flat again in time to catch an entry e58b's still-open trade 1 was occupying through.

**Why this generalizes past `maxBars`:** in a `pyramiding=1`, single-position construction, ANY
parameter that changes a trade's resolution time — the cap, the stop distance, the target distance,
the reward:risk ratio — changes which bars the book is flat on, which changes which of the strategy's
own entry signals get admitted at all. The entry LOGIC can be byte-identical across two runs and the
admitted TRADE SET can still be entirely different past the first divergence. `shieldUsd` moves both
the stop and (via `rr`) the target simultaneously, so it was never going to be exempt.

**How to apply:**
- **Before reading a sweep across ANY parameter in this family as "same trades, different R" (or
  different cap, or different anything), check `get_trades` for where the admitted entries first
  diverge.** If they diverge before the last trade, the comparison is confounded and the ratchet
  cannot be applied trade-for-trade — only the aggregate PF/DD/count can be compared, and only as
  "this construction, this setting" versus "this construction, that setting," never as an isolated
  read of the swept variable's own effect.
- **A single-leg, single-position (`pyramiding=1`) construction cannot cleanly A/B any exit-timing
  parameter on a fixed historical window.** There is no way to hold "which trades get taken" constant
  while varying how long they take to resolve — the two are mechanically the same lever. This is a
  structural property of the construction, not a bug in any one experiment, and no amount of careful
  pre-registration removes it.
- **Individually, an unconfounded-looking number can still be a real reading of "this exact
  configuration on this exact window."** E58a's PF 1.240 on 36 trades (this family's largest sample
  and lowest drawdown) is not thereby worthless — it is a genuine result for that specific
  construction, just not evidence that narrower shields beat wider ones, because the comparison that
  would show that cannot be run here.

## ██ HARD LESSON 30 — A RESET CONDITION BUILT ON "AN ENTIRE CYCLE FREE OF A PERSISTENT LATCH" CAN BE
## FUNCTIONALLY PERMANENT, NOT MERELY RARE (3M ELITE, 2026-09-03)

3M Elite's v48/v49 built VOCABULARY.md's fully-decoded 5-state stage/cluster machine for the first
time and measured it before gating the champion with it (this lab's own HARD LESSON 10/12
discipline). v48's occupancy counter stopped firing entirely 10 months into a 4.7-year window; v49,
isolating LATE STAGE 2 specifically, showed occupancy of that one blocked state continuing almost to
the end of the same window. **The machine falls into its one no-entry state early and functionally
never leaves.**

**This is HARD LESSON 9's shape (a persistent condition with no realistic expiry becomes a lock once
mechanised) but with a different mechanism worth naming on its own.** HARD LESSON 9's lock came from a
monotone guard (`pL < dzBot`) that could only ever get harder to satisfy. This lock comes from
something structurally different: an *exit* condition defined as "a full cycle containing ZERO
occurrences of event X," where X is itself gated by a LATCH that stays true for as long as any
qualifying object (here, a demand zone) remains live. Because the latch (`dzTapped`) is true across
most of the time some zone is alive and already touched, and zones are created frequently, most
break-up events co-occur with the latch — so a cycle containing *none* of them is the rare case, not
the common one. **A condition that is individually plausible ("eventually there will be a clean
cycle") can still have a probability low enough, given how the underlying latch actually behaves, that
"eventually" does not arrive inside any window this lab tests.** Mathematically possible is not
practically different from impossible when the base rate is measured in years.

**How to apply:**
- **Before trusting a RESET, TIMEOUT, or "eventually clears" condition anywhere in a state machine,
  ask what it is a conjunction OF, and whether any of those terms is itself a persistent latch.** A
  condition requiring "zero occurrences of X across an entire cycle" is only as loose as X is rare —
  if X's own gating condition is a latch that stays true for long stretches, the reset is much
  stricter than its English description ("just needs a clean cycle") suggests.
- **Measure occupancy of the blocked state directly, the way v49 did, rather than inferring it from a
  collapsed aggregate trade count.** v48 alone (a stopped counter) was consistent with several
  different causes; only isolating the specific state distinguished "stuck in the no-entry branch"
  from "the eligible-state exit condition itself broke."
- **A structurally sound decode of source language is not the same claim as a structurally sound
  MECHANISATION of it.** Every individual rule in this lab's stage/cluster decode (VOCABULARY.md) was
  read faithfully from the transcripts; the lock-up is a property of how those individually-correct
  rules compose, not a mistranslation of any one of them. Composition needs its own check even when
  every component checks out alone.

**UPDATE (v57, 2026-09-04) — THE PREDICTED FIX WAS TESTED AND DID NOT WORK EITHER.** RESET condition 1
("the model turns bearish, then bullish again") was named here as one of two live paths out of the
lock, blocked at the time on a missing bias/model definition. That definition was later built (v54/v55)
for an unrelated reason (the source's own bias gate) and then used here to finally implement RESET 1.
Result: late-stage-2 occupancy fell only 5.1% (3,737 → 3,546 one-bar-exit counts) and the last occupancy
bar moved from 2026-08-30 to 2026-07-31 — one month, on a 4.7-year window. **Both of this lesson's named
live paths are now closed with real answers**: a looser RESET condition 2 (checked at v50) does not
exist in the captured source; a working RESET condition 1 (built at v57) barely moves the lock. The
lesson's core claim stands strengthened, not weakened — this is a second, independent confirmation that
a reset gated by a persistent latch can be "eventually true" in principle and still not fire inside any
window a project actually tests.


---

## ██ HARD LESSON 31 — IF A CHANGE CAN ONLY MOVE THE WINNER SIDE, AN UNCHANGED DRAWDOWN LOCATES THE
## PROBLEM ON THE LOSER SIDE, TO THE CENT (BTC ATTACK 35, 2026-09-03)

Attack 34 (weekly break-and-hold) was flagged as disqualified by its **drawdown** (46.88% / 32.25%),
not its profit factor. Attack 35 changed exactly one thing — reward:risk 2.0 → 1.5 — with entry and
stop byte-identical to Attack 34. The change was reverted (profit factor fell on both halves), but
one number in the reverted run was worth more than the revert itself: **the recent half's max
drawdown came back at 32.24854336% — identical, to the cent, to Attack 34's own recent-half
drawdown.**

**Why that is diagnostic and not a coincidence.** A target-multiple change can only alter where a
*winning* trade closes — it cannot move a stop-loss exit at all. If the worst peak-to-trough point in
the equity curve had been set by a trade that used to run further before hitting 2R, cutting the
target to 1.5R would have closed that trade earlier, at a smaller gain, and the drawdown number
would have shifted. **It did not shift, at all, to eight significant figures.** The only
configuration consistent with that is that the trade setting the drawdown floor never reached its
target in either version — it was stopped out, and the stop is untouched by this change. So the
drawdown in this mechanism is a property of the **stop side**, not the **target side**, and that was
established from one exact-match number rather than inspected trade-by-trade.

**How to apply:**
- **Before proposing a fix to a metric, ask which side of the trade the proposed change can actually
  reach.** A target-side change cannot explain or repair a loss-side problem, and the reverse. Attack
  34's own header had already speculated the drawdown came from unbounded R on the stop side; this
  cycle turned that into a checked fact rather than leaving it a plausible-sounding guess.
- **An unchanged output after a change that could only touch one branch of the logic is itself a
  result.** Read it, don't discard it because the headline ratchet verdict was REVERTED — HARD LESSON
  11's point (a declared limitation must be measured, not reasoned about) applies here in reverse: an
  *unmeasured null result* is still a result if the match is exact enough to rule out coincidence.
- **This also retires a search direction cheaply.** One pair of runs (2 credits) now rules out the
  entire "target multiple" axis for Attack 34's successors, rather than requiring a second or third
  guess at the right multiple.


---

# ██████ THE RATCHET — v2. USER DECISION, 2026-09-03. THIS SUPERSEDES ALL EARLIER STATEMENTS.

The three rule questions raised by Attack 3, Attack 27 and Attack 29 were put to the user and
**answered on 2026-09-03**. They are CLOSED. This section is now the canonical definition of the
ratchet for **all three labs** and outranks any statement of it in a scheduled prompt, a board, a log,
or an older ledger entry.

## THE RULE

A change is **KEPT** only if **all three** hold:

1. **Profit factor improves.**
2. **Max drawdown does not worsen** — *except* it may worsen by up to **0.50 percentage points** when
   profit factor improves by **more than 0.02**.
3. **The resulting trade count is at least 30.**

And two obligations attach to every KEPT change:

4. **A change that cuts the trade count by more than 50% must pass a split test before it can be
   kept.** Not after. The split is the price of a large sample cut.
5. **The H1/H2 regime spread must be measured and reported.** It does NOT veto. But a KEPT change
   whose spread was never measured is not properly recorded, and the record is incomplete until it is.

Anything failing 1–3 is **REVERTED** and added to that lab's tried-and-reverted table.

## WHY EACH CLAUSE EXISTS — THE EVIDENCE, NOT THE PREFERENCE

**Clause 2, the 0.50pp band.** Attack 3 produced the largest profit-factor gain that lab ever
recorded and was reverted because drawdown worsened by **0.064 percentage points** — comfortably
inside noise on a ~100-trade sample. A strict rule that discards the best result over a rounding-scale
difference is measuring precision it does not have. The band is deliberately narrow: it takes a real
PF gain (>0.02) to buy a small DD cost, and everything outside it still reverts.

**Clause 3, the floor of 30.** `coolBars` was measured at six points — 231, 166, 145, 85, 56, 7
trades — with profit factor rising monotonically the whole way and **every step passing the old
two-term rule against the step below it.** A rule with no sample floor does not converge; it walks a
selectivity parameter toward degeneracy and calls each step an improvement.

**Clause 4, the split on a >50% cut, and why the floor alone was not enough.** 3M's v32 cut the sample
**78%** — from 734 trades to 165 — and that cut was *legitimate*: it enforced LESSON 3's R floor,
excluding entries whose stop was under 0.8% of price. It went on to clear a real out-of-sample split
(H1 1.34562489, H2 1.05357727) and became the first champion in this project. **A blunt percentage
veto would have blocked it.** So a large cut is not forbidden — it is made expensive. It must be
split-tested before it counts.

**Clause 5, report the spread but do not veto it.** Attack 26 passed both old terms while widening the
H1/H2 spread from 0.0016 to 0.2566 — the rule was blind to it because both its terms are whole-sample
aggregates (HARD LESSON 20). But a hard third veto would block changes that trade a little uniformity
for a lot of edge, and **the split test — now mandatory on every kept change — already catches the
fatal version**. Measuring the spread every time makes the blind spot visible without adding a term
that can reject a good simplification.

## WHAT THIS DOES NOT CHANGE
- **A ratio below ~30 trades is still not quoted as a result.** That practice predates this rule and
  survives it; clause 3 makes it a keep/revert condition as well as a reporting one.
- **Every KEPT change still needs its source on disk** (HARD LESSON 21) and a cold re-run that
  reproduces to the cent before anything is built on it (HARD LESSON 25).
- **An in-sample number is still not a finding** (HARD LESSON 22). The ratchet decides what is kept;
  the split test decides what is believed. They are different gates and both apply.

## THE HONEST LIMIT OF THIS RULE
Every clause here was derived from failures inside this project, on one instrument, over four and a
half years of data. **A rule tuned on its own history is subject to the same objection as a strategy
tuned on its own history.** The thresholds — 0.50pp, 0.02, 30 trades, 50% — are judgement calls
anchored to observed failures, not measured optima, and none of them has a neighbourhood test behind
it. They are better than the two-term rule they replace because they close failures that actually
occurred; they are not proven, and a future cycle that finds one of them binding in a stupid place
should say so rather than route around it.


---

# ██████ MANDATE CORRECTION — USER DIRECTIVE, 2026-09-03. THIS OUTRANKS EVERY QUEUE ITEM.

The user restated the mandate, and it corrects a drift that had crept into two labs.

## THE THREE LABS ARE NOT THE SAME KIND OF PROJECT

**WAR FORMATION and 3M ELITE are the USER'S strategies.** They came from source material the user
supplied — the Oracle rules and the A.L.C.M. infographic for War Formation, the SPENNYFX videos, PDFs
and transcripts for 3M. The job in those two labs is to **MASTER what is written there and make SMALL
TWEAKS that perfect the strategy on its own terms.** Not to replace the mechanism, not to re-engineer
its frame, not to decide a leg does not exist.

**THE BTC LAB IS THE INVENTED ONE.** There is no source material. The job there is to build a strategy
that works and keep improving it, indefinitely.

**All three get worked every cycle.** None is ever "done", "paused", or "closed".

## WHERE THIS CORRECTS WAR FORMATION
**E63 moved the entry from 1m to 5m.** It was justified on the grounds that the A.L.C.M. constrains the
EXIT, so the entry timeframe was free. **That was wrong.** The cascade the user supplied is
6h → 1h → 15m → 3m → 1m, and the **1m entry is part of the specification**, not an incidental choice
inherited from the data.

- **E63 stands as a DIAGNOSTIC and is not withdrawn.** It established something real: at 5m the hold
  cap stops binding, and the 1m results from E35 onward look like thin-sample readings rather than a
  microstructure edge. That is worth knowing and stays on the record.
- **But 5m is NOT the new home timeframe, and E63 is NOT the new base.** Work returns to the 1m
  cascade as specified.
- **The 20–30 trade ceiling is therefore back**, and it is a property of the user's strategy on the
  available data — not a defect to engineer away. Results are reported with the count stated, and the
  ratio is not quoted below ~20 trades. That constraint is lived with, not removed.

## WHERE THIS CORRECTS 3M ELITE
**The short leg was marked "paused, not queued" after six failed constructions. That was overreach.**
The source material describes a two-sided system — supply zones and demand zones — so the short side
is part of the user's strategy, not an optional extra this lab gets to retire.

- **The short leg is REOPENED.** It stays on the queue and keeps receiving small, source-faithful
  tweaks.
- The six failures remain on the record as evidence about which constructions do not work
  (v34's fade into the zone, v51's failed reclaim, and four earlier mirrored attempts). They are not
  evidence that the strategy has no short side.
- **Go back to the source before the next attempt.** VOCABULARY.md decodes terms from the transcripts;
  if the source says something specific about short entries that is not yet implemented, implementing
  it outranks inventing a seventh geometry.

## WHAT DOES NOT CHANGE
- **RATCHET v2 still governs what is KEPT** in all three labs (user decision, same day).
- **Never fabricate a metric, always record real provenance, always save the Pine** (HARD LESSONS 21
  and 25).
- **Split-test before believing a number** (HARD LESSON 22) — though in War Formation the 1m window
  cannot support a split, and that limitation is stated rather than engineered around.
- **Never mirror one leg off the other** (LESSON 6). Reopening the 3M short does not license mirroring.

## THE PRACTICAL RULE FOR EVERY FUTURE CYCLE
Before proposing a change in War Formation or 3M Elite, ask: **is this a small tweak that perfects the
strategy the user gave me, or am I rebuilding it into something else?** If the second, it does not
belong in that lab. Ideas of that kind belong in the BTC lab, which exists precisely to be invented.


---

# ██████ USER DIRECTIVE, 2026-09-03 (second of the day) — BOTH LABS, BOTH DIRECTIONS

> "my 3M and War Formation should work in both directions not just longs or shorts. 6Hr is the
> direction for War formation so if red we look for shorts but also depends on the information that
> I provided, and same for 3M — they should work on both long and shorting, just look over the
> information I provided for that also."

**This is not a new requirement, it is an unmet one.** The standing requirement of 2026-09-02 already
said both directions, all regimes. What this directive adds is the instruction to **stop inventing
short geometries and read what the user already supplied**, plus one concrete rule: in War Formation
the **6H candle is the direction**, and red means shorts.

**Acted on the same cycle.** Both labs went back to the source, and in both the source turned out to
have already answered the question — and in both the lab had been ignoring the answer.

## ██ HARD LESSON 31 — WHEN A LAB CANNOT BUILD A LEG, CHECK WHETHER THE SOURCE ALREADY DEFINED IT
## BEFORE INVENTING A SEVENTEENTH GEOMETRY (BOTH USER LABS, 2026-09-03)

Between them, War Formation and 3M Elite had failed **sixteen** short constructions. Every one was
designed by this project: where to short, what confirms it, what invalidates it. The two labs then
generalised those failures into a rule — *never mirror the short off the long* (LESSON 6) — and, in
3M's case, into a decision that the short leg could be shelved.

**Both labs had source material that specified the short, and neither had implemented it.**

- **War Formation.** `ORACLE-RULES.md` L204-216 records the author's own rule — *"The six hour is the
  God of direction... Clear direction is either more than one green bar on the six hour"*, and
  explicitly **"Mirrored for short."** The file even flags, in its own words, that this is *"simpler
  and better specified than the current build's 4+ green HA 1h candles"*. The lab had written that
  down and kept running the proxy anyway. L179-180 goes further and prescribes the exact build:
  *"a single strategy that takes longs when the 6h is bullish and shorts when it is bearish...
  reported with both legs split out."* **That build had never been run.**
- **3M Elite.** `transcripts/2026-08-09 04-18-22.txt` [06:19]: *"all these advance models are the same
  thing on the bearish side just upside down."* The source states the mirror as the design. Worse,
  `bearEngulf` **was already computed in the v37 champion and wired to nothing** — the champion had
  been carrying half of its own short leg, unused, the whole time.

**The lesson is about the direction of inference.** Sixteen failed constructions felt like strong
evidence that the short side was hard. It was actually strong evidence that **this project keeps
guessing at a thing the source states plainly.** A rule earned from failed inventions (LESSON 6) is a
rule about inventions — it says nothing about a specification, and it must not be used to override
one. **LESSON 6 is hereby scoped: it governs geometries this project invents. It does not govern a
mirror the user's own source material prescribes.**

**And the corollary, which cost real credits today:** neither source-faithful build worked. E64a
returned 0.454 and v53 returned 0.705. **That does not weaken the lesson, it sharpens it** — because
for the first time the failures are attributable. A failed invention tells you nothing except that
one guess was wrong. A failed *specification* tells you exactly which stated rule does not survive
contact with the data, and both runs pointed at the same missing piece (below).

## ██ HARD LESSON 32 — THE THING BOTH USER LABS ARE MISSING IS THE BIAS GATE, AND THE LONG LEG HID IT

Three runs this cycle, three failures, **one shared cause.**

| | mechanism | PF | trades | what it shorted into |
|---|---|---|---|---|
| WF E64a | 6h-red direction, mirrored sweep | 0.45442725 | 43 | one 4.5-month window |
| 3M v53 | supply zone, exact source mirror | 0.70512830 | 255 | the 2023-2025 bull advance |
| BTC 35a | narrow-day expansion (long) | 0.83969095 | 118 | n/a — control |

**3M v53 is the clean case.** It shorted supply zones straight through 4.7 years that were mostly a
bull market, and returned a 13.73% win rate against an rr of 2.0 that needs 33% to break even. The
source forbids exactly this — *"the model is just going to be the same thing that the hard time frame
is"* [05:12], and the whole of 04-18-22 turns on whether a break is read in a bullish or bearish
context. **v37, the project's only split-tested champion, implements NO bias gate on either leg.**

**The long leg concealed the omission for months.** A long-only strategy in a rising market does not
need a bias gate to avoid its worst trades — the market supplies the filter. The moment the same
geometry is pointed the other way, the missing gate is the whole result.

**So the shared finding is: the short leg is not the problem. The absence of a regime gate is, and it
has been a latent defect in the LONG leg the entire time.** The next work in both user labs is the
same and it is a small, source-faithful tweak rather than a new mechanism:

1. **3M** — implement the bias gate the source keeps insisting on (12H/24H model direction), then
   re-run BOTH legs against it. If the long leg's numbers move at all, v37's headline was partly the
   bull market, and that is worth knowing before anything is promoted.
2. **War Formation** — E64b showed the source's literal 6h-colour rule (0.959) is WORSE than the
   lab's own 4-green-1h proxy (1.240). Build the short on the **proxy** rather than the raw colour,
   which isolates the leg against a direction rule that demonstrably works.

## ██ OPEN TECHNICAL FLAG — THE CASCADE SIGNATURE, SECOND SIGHTING

3M v53 returned `cascadeRatio` **1.4655** — 255 rows from 174 unique entries, max depth 4. v51 showed
the same signature at 1.419. **Both are short builds.** The one-entry-per-zone latch is not holding on
the short side, which means the headline is computed over more rows than there were entries.
**No short number from this lab should be believed until this is understood** — including v53's own
0.705, which is recorded with that caveat attached rather than as a clean reading.

**RESOLVED, 2026-09-04 (3M v54/v55).** Pulled the full per-trade list for v53's job via `get_trades`
(255 rows) and had it examined for what separates the 174 "unique" entries from the extra 81 rows.
**Every cascade group shares an identical `entryBar`/`entryTime`/`entryPrice` and differs only in
`qty`, exit bar/price, and P&L.** Concrete example: one entry at bar 20139 (entryPrice 20915.5) is
reported as four rows — qty 0.004 exiting at bar 20140, qty 0.004 at bar 20142, qty 0.008 at bar 20143,
and the remaining qty 0.466 at bar 20148, each a distinct exit price and P&L. **This is the parity
engine reporting each partial-exit fill of a single bracket order as its own trade-list row** — not a
re-entry storm and not the `dzTraded`/`szTraded` one-entry-per-zone latch failing. The latch IS holding;
174 (and 62 on v55, ratio 1.4516, the same signature a third time) is the real count of zone decisions,
not 255 or 90.

**What this changes and does not change.** `profitFactor` and `netProfitPct` are dollar sums over all
rows and are invariant to how the engine splits one position's exits — every PF this lab has reported,
short builds included, stands as measured and does not need re-reading. `totalTrades`, `winRatePct` and
the `avgBars*` fields ARE computed at row level and can be inflated or distorted by this artefact, so on
any build (this lab's or a sibling's) where `get_backtest_result`'s `cascade` block shows a ratio above
1.0, those specific fields should be read alongside `uniqueEntries`, not instead of it. **Open and
low-priority: why the artefact appears on short builds (v51, v53, v55) and not the long ones (v37, v52,
v54, all ratio 1.0) is unexplained** — worth a look if it recurs on a fourth build, not before.

---

## ██ HARD LESSON 33 — AN AUTOMATED CYCLE THAT ENDS IN A PERMISSION PROMPT DOES ALL THE WORK AND
## SAVES NONE OF IT (ALL THREE LABS, 2026-09-03/04)

**Overnight, roughly nine consecutive hourly cloud runs across the three labs each did a complete,
correct research cycle — and threw every bit of it away.**

The stored prompts ended with: *"...build the dashboard, republish it with url=..., update the log,
commit, pull --rebase, push."* The publish step came **before** the commit. A cloud run cannot approve
its own `Artifact` publish permission prompt, so every run reached that call and **hung there
permanently** — `worker_status: requires_action` — and never reached `git commit`, let alone `push`.

**The cost, measured not estimated.** Credits went 690 → 623 across the window, **67 spent**, against
**three** surviving commits. The runs pulled the repo, read the docs, wrote correct Pine, spent a
credit on a real backtest, recorded it with provenance, updated the log and built the dashboard — all
of it inside a sandbox that was then discarded.

### WHY THIS WAS INVISIBLE FOR HOURS
Nothing failed. There was no error, no red status, no alert. `git log` simply showed no new commits,
which is indistinguishable from "the routines had nothing to do." **The failure mode of a blocked
permission prompt is silence**, and silence is exactly what a healthy idle loop looks like. It was
found only by checking `last_fired_at` on the routine against the newest commit timestamp and noticing
a fifteen-hour gap — then by reading a run log and seeing it end mid-sentence on a permission prompt.

### THE RULE
1. **In an unattended run, ORDER THE STEPS BY DURABILITY.** Persist first — commit and push — then do
   anything that could block. The push is what makes work real; everything after it is decoration.
2. **Never put a tool that can raise a permission prompt in the tail of an automated cycle.** For
   these labs the fix is absolute: cloud routines do not call `Artifact` at all. The dashboard HTML is
   committed to git, and a local session with a human present republishes it.
3. **A silent loop is not a healthy loop.** Verify an automated cycle by comparing the routine's
   `last_fired_at` against the newest artefact it should have produced — a commit, a row, a file. "No
   news" from an unattended agent is a claim to be checked, not a state to be trusted.

### THE GENERAL FORM, WHICH IS BIGGER THAN THIS BUG
**Capability granted to an unattended process must be checked against what that process can actually
approve.** Handing a cloud routine a tool that requires interactive consent is not a partial
capability — it is a **trap**, because the routine will reach for it, block, and lose everything it
did beforehand. The right question when designing an automated loop is not "can it do this step" but
**"what happens to the work already done if this step never returns."**


---

## ██ HARD LESSON 34 — THE SHORT LEG WAS NEVER TESTED. THE ENGINE LIQUIDATES IT BEFORE THE STOP CAN
## FIRE, AND FIFTEEN EXPERIMENTS MEASURED THE HARNESS INSTEAD OF THE STRATEGY (WAR FORMATION, 2026-09-04)

**Across this project, short constructions have failed with win rates of 4-7% against reward:risk
ratios that need 33% to break even.** Fifteen of them in War Formation, six in 3M, several in BTC.
The labs treated that as a fact about the market and kept redesigning the entries.

**It was a fact about the test harness.**

### WHAT THE TRADE LOGS SHOW — FOUND FREE, NO CREDITS SPENT
Comparing `e58a` (long, PF 1.24015239 / 36 trades) with `E64a` (short, PF 0.45442725 / 43 trades) —
same shield, same cap, same window, mirrored code:

| | LONG e58a | SHORT E64a |
|---|---|---|
| Loser exit price | **exactly −$1,000**, all 36 | +$8.20, +$11.40, +$23.50 … +$503.10 |
| Winner exit price | exactly +$2,000 | exactly −$2,000 ✓ |
| Loss vs the trade's own max adverse excursion | −$113 vs $138.99 — **stop cut it early** | −$14.3376 vs $14.3376 — **identical, every trade** |

**Every losing short exits at precisely its worst point.** A stop exits at a level you chose; a
liquidation exits at the moment margin runs out, which is by definition the worst point reached. The
winners prove the code is not simply broken: shorts *do* hit the −$2,000 target exactly, because when
price falls a short's notional shrinks and margin pressure eases. **Only the adverse direction is
truncated.**

### THE CONFIRMING TEST (E67), REGISTERED BEFORE RUNNING
Multiply the shield 5×, $1,000 → $5,000, change nothing else. Pre-registered: *losers unchanged means
the shield is inert; losers growing toward −$5,000 means the reading is wrong and it is withdrawn.*

**Average loser went from −$35.80 to −$33.43. Largest loss from −$72.80 to −$76.46.** A five-fold
wider stop produced statistically identical losses. **Confirmed.**

### THE ARITHMETIC THAT CLOSES IT
The engine forces `percent_of_equity = 100` and `margin_short = 100`. A short so sized has **zero
excess margin**, and unlike a long its **notional grows as price moves against it** while equity
simultaneously falls — both sides of the margin ratio move the wrong way at once.

Liquidation lands at roughly **−$33 on $10,000 — about 0.33% of price.**
**HARD LESSON 3's commission floor requires a stop of at least 0.8%.**

**So there is no shield width that is both wide enough to be valid and tight enough to bind. On this
engine, at this sizing, a short strategy with a legitimate stop CANNOT BE TESTED AT ALL.**

### WHAT THIS INVALIDATES, AND WHAT IT DOES NOT
- **INVALIDATES:** every War Formation short — E9, E9b, E13, E25, E26, E27, E64a, E66 and the rest.
  They never ran the A.L.C.M. exit model. Their win rates are an artefact.
- **DOES NOT INVALIDATE:** every LONG result. e58a, e50a/e50b and alcm-reference all exit exactly on
  the shield, verified trade by trade. The long lineage stands untouched.
- **NOT YET DECIDED:** 3M's shorts (v53 0.70512830, v55 0.72183885) and the BTC lab's short attempts
  use **structural** stops rather than a dollar shield. The same arithmetic may or may not apply —
  their stop distances must be measured against the ~0.33% liquidation threshold before any of those
  numbers is trusted. **That check is free via `get_trades` and is the next task in both labs.**

### THE METHOD LESSON, WHICH IS THE PART THAT GENERALISES
**An asymmetry between two legs of the same code is a claim about the harness until proven otherwise.**
This lab spent fifteen experiments and many credits redesigning short *entries* because it read a
persistent long/short performance gap as a market fact. The gap was mechanical, it was visible in
free trade-log data the whole time, and no backtest was needed to find it — only a comparison of exit
prices against the levels the code actually set.

**Before explaining a persistent asymmetry, verify that both sides are running the model you wrote.**
Check exits against the levels you set, and check whether a loss equals the trade's own maximum
adverse excursion — if it does, the position was closed *for* you, and you are not measuring what you
think you are measuring.


---

## ██ HARD LESSON 34 — CROSS-LAB CONFIRMATION (3M ELITE + BTC, 2026-09-04). THE ~0.35% SHORT CEILING
## IS UNIVERSAL, AND IT IS PARTIAL IN 3M RATHER THAN TOTAL

E68 established in War Formation that the A.L.C.M. dollar shield never fires on a short position. Its
queue item 1 was to check the other two labs, **free, via `get_trades`**, because 3M and BTC use
*structural* stops rather than a dollar shield and the arithmetic might not carry over. It does — but
not identically, and the difference matters.

### THE SAME-STRATEGY, SAME-WINDOW, MIRRORED-CODE COMPARISON

| Lab | build | LONG avg loss | build | SHORT avg loss |
|---|---|---|---|---|
| 3M Elite | v54 (gated long) | **−$123.85 ≈ 1.24%** | v55 (gated short) | **−$36.36 ≈ 0.36%** |
| War Formation | E64b | −$143.20 ≈ 1.43% | E64a | −$35.80 ≈ 0.36% |
| War Formation | e58a | −$1,000 exactly | E68 ($5,000 shield) | −$33.43 ≈ 0.33% |

**Shorts cap out at roughly 0.35% of equity in both labs, on two completely different stop models.**
Longs lose three to four times more and clear HARD LESSON 3's 0.8% floor properly. The ceiling is a
property of the engine's short-side margin handling, not of any strategy.

### BUT IN 3M IT IS PARTIAL, NOT TOTAL — AND THAT DISTINCTION IS THE HONEST READING
`get_trades` on v53 (255 trades, 220 losers) measured directly:

- **162 of 220 losing shorts (74%) exit at LESS than 0.8% adverse** — they cannot have reached their
  structural stop, which the R floor guarantees is at least 0.8% away.
- **58 of 220 (26%) DO exceed 0.8%** — those are genuine stop-outs.
- Median loser adverse move **0.454%**, max **2.096%**.
- Only **27.3%** exit at exactly their max adverse excursion, against **100%** in War Formation's
  E64a. The most likely reason is bar granularity: on 1m bars a close sits essentially at the bar
  extreme, so exit and max-excursion coincide; on 15m bars wicks are wide enough that a close-based
  forced exit often lands short of the wick low. **That is an inference, not a measurement.**

**So 3M's short exit model is partially active. War Formation's was entirely inactive.**

### WHICH WAY THE DISTORTION RUNS — STATED, BECAUSE IT IS NOT THE OBVIOUS DIRECTION
Truncated losses make gross loss **smaller**, which pushes profit factor **UP**. So **v53's 0.705 and
v55's 0.722 are OPTIMISTIC readings, not pessimistic ones** — a correctly-stopped short would very
likely score worse, not better. Truncation also closes positions before they can recover, which
suppresses the winner count, and a 13.73% win rate against a 2R target needing 33% is consistent with
that. The two effects push profit factor in opposite directions, so **the net bias is not cleanly
signed and no corrected figure should be quoted.** What can be said is that neither number measures
the strategy as specified.

### WHAT THIS DOES AND DOES NOT TOUCH
- **3M's short results (v53 0.70512830, v55 0.72183885, and v55's split H1 0.630 / H2 1.437) are
  DISTORTED and provisional.** Not withdrawn outright as War Formation's were, because a quarter of
  their stops genuinely fired — but not trustworthy as measurements of the specified system.
- **3M's LONG champion v37 is UNAFFECTED.** Its losses run 1.24% and clear the floor, so its stops
  fire as designed. v37 stands, with its existing caveats unchanged.
- **THE BTC LAB IS UNAFFECTED.** Attacks 34, 36 and 37 are all `shortTrades: 0` — every recent
  discovery mechanism is long-only, so nothing there passes through the short-side margin path. No
  BTC result needs revisiting on this account.

### THE STANDING RULE THIS CREATES
**Before trusting any SHORT result from any lab on this engine, check the average losing trade against
~0.35% of equity.** If it sits at or below that, the stop did not fire and the number is not measuring
the strategy. This check is free, takes one `get_trades` call, and would have saved sixteen
constructions across two labs.


---

## ██ HARD LESSON 35 — THE CASCADE SIGNATURE IS THE LIQUIDATION, SEEN FROM THE TRADE LOG. IT INFLATES
## TRADE COUNT AND CRUSHES WIN RATE, BUT LEAVES PROFIT FACTOR ALONE (3M ELITE, 2026-09-04)

Three short builds carried an unexplained `cascadeRatio` — v51 at 1.419, v53 at 1.4655 (255 rows from
174 unique entries, max depth 4), v55 at 90 rows from 62 entries. The standing instruction was that
**no short number from that lab should be believed until it was understood.** It is now understood,
and it is the same defect as HARD LESSON 34 viewed from a different angle.

### WHAT THE ROWS ACTUALLY ARE
One v53 entry at 20915.50 produces **four rows**, all with the same `entryTime` and `entryPrice`:

| seq | qty | exit | P&L |
|---|---|---|---|
| 51 | 0.004 | 20956.0 | −$0.25 |
| 52 | 0.004 | 21050.0 | −$0.62 |
| 53 | 0.008 | 21141.5 | −$1.98 |
| 54 | **0.466** | 21189.0 | **−$137.26** |

That is not four trades. It is **one position of 0.482 BTC unwound in tranches at progressively worse
prices** — the engine closing a sliver, re-checking margin, closing more, and finally dumping 97% of
the position at the worst price. **The cascade signature is the margin unwind.**

### WHICH METRICS IT BREAKS, MEASURED RATHER THAN ASSUMED
Recomputing v53 by aggregating tranches back into positions:

| | rows (as reported) | positions (true) |
|---|---|---|
| Count | 255 | **174** |
| Winners | 35 | **35 — identical** |
| Win rate | 13.73% | **20.11%** |
| Profit factor | 0.70512830 | **0.70360999** |
| Net P&L | −$2,480.312467 | −$2,480.312467 |

**Only losers are ever tranched** — the winner count does not move, which is exactly what a forced
unwind on the adverse side predicts and is independent confirmation of HARD LESSON 34. **77 of 255
rows (30.2%) are sub-$5 nibbles, and all 77 are losers.**

### THE PRACTICAL RULES THIS CREATES
1. **PROFIT FACTOR IS SAFE.** It is dollar-weighted, so splitting one loss into four changes it by
   0.0015. Every PF quoted from a cascaded run stands as a PF.
2. **WIN RATE IS NOT.** 13.73% was really 20.11% — a 6.4-point error, and always in the pessimistic
   direction. Any win rate from a run with `cascadeRatio > 1` is wrong and must be recomputed.
3. **TRADE COUNT IS NOT, AND THIS ONE MATTERS FOR THE RULES.** RATCHET v2 clause 3 requires at least
   30 trades. On short builds the reported count has been inflated by ~46% (255 vs 174; v55's 90 vs
   62). **A short build reported at 40 "trades" may hold only 27 real positions and should never have
   passed clause 3.** Every short result near the floor needs its count re-derived before its keep
   decision is trusted.
4. **`cascadeRatio` in the result is the tell, and it is free.** Any value above 1.0 means rows exceed
   positions. Read it on every run; recompute count and win rate whenever it is not 1.

### WHAT THIS RETIRES AND WHAT IT LEAVES STANDING
The blanket instruction *"no short number from this lab should be believed"* is now **too broad and is
narrowed**: profit factors survive, win rates and counts do not. What still stands against those
shorts is HARD LESSON 34 — 74% of their losses were truncated before the stop — and that remains the
reason v53 and v55 are not measurements of the specified system.


---

## ██ HARD LESSON 36 — A NET PROFIT FACTOR NEAR 1.0 ON A HIGH-FREQUENCY MECHANISM HIDES WHETHER THE
## EDGE IS WEAK OR MERELY EXPENSIVE, AND THOSE NEED OPPOSITE FIXES (BTC, 2026-09-04)

Attack 37 sat at PF 1.02423271 / 1.01155847 across 322 and 196 trades and was read, for four cycles,
as a **thin edge** that a filter might sharpen. Three filter terms were built and all three failed —
two of them by helping H1 and breaking H2, the same signature that killed the VWAP family.

**The trade log, read for free, says the edge was never thin.**

| Attack 37a | |
|---|---|
| Gross P&L | $3,405.88 |
| Commission | $2,845.60 — **83.5% of the gross edge** |
| **PF before commission** | **1.15945508** |
| PF after commission | 1.02423271 |

**A raw 1.159 is a healthy mechanism** — the same band as 3M's verified champion and War Formation's
reference build. It was not weak. It was **expensive**.

### WHY THIS MATTERS BEYOND ONE ATTACK
**A weak edge and an expensive edge look identical in the net number and need opposite treatments.**
- A weak edge needs a **conditioning filter** — find when the mechanism is right.
- An expensive edge needs **fewer trades** — keep the same logic, pay for it less often.

Selecting filters on net profit factor when cost dominates optimises the wrong quantity, which is
exactly what Attacks 38, 39 and 40 did. Each was a sensible price-action idea judged against a number
that was mostly a commission artifact.

### THE RULE
**On any mechanism above ~100 trades, decompose gross P&L and commission BEFORE designing a filter.**
`get_trades` gives both and costs nothing. If commission is a large share of gross, the design target
is trade count, not signal quality — and no amount of filtering on the net number will find that out.

### THE COROLLARY ON SIZING, ALSO MEASURED
Recomputing the same trade sequence at 100 / 50 / 25 / 10 percent of equity gives return-to-drawdown
ratios of 0.178 / 0.246 / 0.274 / **0.289**. Sizing down helps, because 100%-equity compounding
amplifies drawdowns superlinearly — but it **asymptotes**, and returns fall with it. **A bad
return-to-drawdown ratio is scale-invariant in the way that matters: you cannot size your way out of
it.** The drawdown here came from a **14-trade losing streak costing 21.42% of equity** at an average
loss of 1.312% — a streak problem, not a bet-size problem.


---

## ██ HARD LESSON 37 — GROSS EDGE PER TRADE IS THE SCREEN. EVERY MECHANISM IN THIS PROJECT IS
## STRONGER THAN ITS RECORDED NUMBER, AND ONE IS FAR WEAKER THAN IT LOOKS (ALL THREE LABS, 2026-09-04)

HARD LESSON 36 established that a net profit factor hides whether an edge is weak or merely expensive.
This applies that lens to every build the project currently rests on. **All three decompositions came
free from `get_trades`. No credits were spent.**

| build | trades | **gross PF** | net PF | commission as % of gross | **gross edge / trade** | commission / trade |
|---|---|---|---|---|---|---|
| **3M v37** (champion) | 155 | **1.44026949** | 1.25172059 | 37.4% | **$30.69** | $11.49 |
| **WF e58a** (reference) | 36 | **1.38769869** | 1.24015239 | 33.4% | **$31.17** | $10.40 |
| **BTC Attack 37a** | 322 | 1.15945508 | 1.02423271 | **83.5%** | **$10.58** | $8.84 |

*(e58a's decomposition was checksummed against its recorded net PF and reproduces 1.24015239 exactly.)*

### THE FIRST FINDING: THE TWO WORKING MECHANISMS ARE BETTER THAN RECORDED
**3M's champion has a raw edge of 1.44, not 1.25. War Formation's reference build is 1.39, not 1.24.**
Roughly a third of each is paid away in commission. Neither number is wrong — the net figure is the
one you would actually earn — but the project has been judging *mechanisms* by a number that
conflates mechanism quality with trading cost.

### THE SECOND FINDING, WHICH IS THE GENERAL ONE
The variable that separates these builds is **not** trade count, and **not** profit factor. It is
**GROSS EDGE PER TRADE MEASURED AGAINST A ROUGHLY FIXED PER-TRADE COST.**

At the forced parity profile — 100% of equity, 0.05% per side — **commission is about 0.1% of equity
per round trip, roughly $10 on $10,000, no matter what the trade does.** So:

- **e58a earns $31.17 of gross edge per trade and pays $10.40.** It keeps two-thirds.
- **v37 earns $30.69 and pays $11.49.** It keeps nearly two-thirds.
- **Attack 37 earns $10.58 and pays $8.84.** It keeps a sixth.

**Attack 37's per-trade edge is three times smaller than the two mechanisms that work.** That single
number explains its 83.5% cost share, its thin net profit factor, and why three price-action filters
selected on net PF all failed — they were tuning a quantity dominated by a cost the mechanism could
never outrun.

### THE SCREEN THIS CREATES, USABLE BEFORE ANY CREDIT IS SPENT
**A mechanism needs gross edge per trade at least ~3x the per-trade commission to be worth building
on.** Both working builds sit near 3x. Attack 37 sits at 1.2x.

And the estimate can be made **from the design alone**, before a single backtest: expected gross move
per trade is approximately `winRate x (rr x R) - (1 - winRate) x R`, with R the stop distance as a
percentage of price. Against a fixed ~0.1% cost, a mechanism whose R is ~1% and whose win rate barely
clears break-even has almost nothing left. **Estimate that ratio when the mechanism is proposed, not
after four cycles of filters.**

### WHAT THIS DOES NOT SAY
It does not say Attack 37 has no edge — 1.159 gross on 322 trades is real. It says the edge is too
small **relative to the cost of harvesting it at this frequency**, which is a different and more
fixable problem: the same mechanism at a fraction of the frequency, or on a timeframe where each
signal carries a larger move, could clear the screen. That is why the BTC queue now tests a cooldown
rather than a fourth filter.


---

## ██ HARD LESSON 38 — RAISING GROSS EDGE PER TRADE ONLY HELPS IF IT DOES NOT LENGTHEN HOLDS INTO THE
## CAP. A QUALIFIER ON HARD LESSON 37, MEASURED IN TWO LABS ON THE SAME DAY (2026-09-04)

HARD LESSON 37 established that **gross edge per trade against a fixed per-trade fee** is the screen
that separates workable mechanisms from expensive ones. Two experiments then tested the obvious
corollary — *raise gross edge per trade* — and **both failed, for the same reason.**

| | BTC Attack 41 | WF e50b vs e58a |
|---|---|---|
| The change | rr 2.0 → 3.0 | shield $1,000 → $2,000 |
| Gross edge per trade | $10.58 → **$6.00** | $31.17 → **$41.56** ✅ |
| Commission share of gross | — | 33.4% → **24.0%** ✅ |
| **Profit factor** | 1.024 → **0.973** | gross 1.388 → **1.300** |
| Hold length | avgBarsWinning 49 → **78** (cap 192) | **3 of 21 trades hit the cap exactly** |

**In War Formation the cost axis behaved exactly as predicted — and the build still got worse.**

### THE MECHANISM
Widening R (a wider target, a wider stop, or both) makes each trade **take longer to resolve**. Longer
holds do two damaging things at once:

1. **Trades time out at the hold cap** instead of resolving at stop or target, converting clean ±R
   outcomes into small arbitrary ones. e50b's three capped trades returned −$5.85, +$43.71 and +$68.94
   of gross where a resolution would have returned roughly ±$280.
2. **Open positions block later entries** under `pyramiding = 1`, shrinking the sample — which in War
   Formation's case (21 trades) drops it below the ratchet's own 30-trade floor.

### THE QUALIFIED RULE
**Gross edge per trade is still the right screen. But it is a RATIO of two things that move together:
edge per trade rises with R, and so does time-to-resolution.** A change that raises R without
lengthening holds is a genuine improvement; one that raises R by holding longer trades the cost ratio
for the win/loss ratio, and the second usually wins.

**BEFORE any change that widens a target, a stop, or a hold: measure what fraction of the existing
trades already sit at `maxBars`.** It is free from `get_trades`. e58a's **0 of 36** was headroom;
e50b's **3 of 21** was the cap already biting; Attack 37's winners at 78 of 192 bars had less room than
they looked.

### WHAT THIS RETIRES
Two "obvious next levers" are now closed by measurement rather than by opinion — **rr on BTC Attack 37**
and **shield width in War Formation**. Both were queued by me on HARD LESSON 37's logic, and both were
wrong for the same unaccounted reason. **The lesson is stronger for having been falsified in its first
two applications than it would have been if they had worked.**


---

## ██ HARD LESSON 39 — THE ACHIEVED WIN/LOSS RATIO AGAINST THE NOMINAL TARGET IS THE ONE NUMBER THAT
## SEPARATES A WORKING MECHANISM FROM A FAILING ONE, AND IT IS FREE (ALL LABS, 2026-09-04)

HARD LESSON 37 proposed gross edge per trade as the screen. HARD LESSON 38 qualified it: raising R
only helps if holds do not lengthen into the cap. Attack 42 then showed the screen **cannot rule a
design in**, because its `rr` term must be the ACHIEVED win/loss ratio and that is unknown before
running. **This lesson names the number to read afterwards, and it is decisive.**

| build | nominal target | **achieved gross win/loss** | shortfall | verdict |
|---|---|---|---|---|
| **3M v37** (champion) | 2.0 | **1.9422** | **3%** | works — net 1.252 |
| BTC Attack 42 | 2.0 | **1.4452** | **28%** | fails — net 1.013, discarded |
| BTC Attack 41 (rr 3.0) | 3.0 | — (win rate collapsed 38%→31%) | — | fails — net 0.973 |
| WF e50b ($2,000 shield) | 2.0 | — (3 of 21 trades capped) | — | worse gross PF than e58a |

**A mechanism whose achieved ratio tracks its nominal target is resolving as designed. One whose
achieved ratio falls well short is being truncated — by the hold cap, by slow resolution, or by
reversals before the target — and no amount of filtering or R-widening fixes that.**

### WHY THIS IS THE RIGHT NUMBER
It collapses three separate failure modes into one observable:
- **Cap truncation** — winners time out (Attack 42: winners at 49% of cap, 13.5% capped).
- **Slow resolution** — the target is simply too far for the timeframe (Attack 41).
- **Occupancy loss** — long holds block entries and shrink the sample (e50b).

All three show up as **achieved < nominal**, and the gap size is proportional to the damage.

### THE PRACTICAL RULE, AND IT COSTS NOTHING
**On every result, compute `avgWinningTrade / |avgLosingTrade|` on GROSS figures and compare it to the
nominal reward:risk.** Both are in the backtest response; the gross split needs one free `get_trades`
call. **Within ~5% of nominal means the exit model is working. Below ~85% of nominal means the design
is being truncated and the profit factor is measuring the truncation, not the idea.**

### AND IT REFRAMES WHAT v37 IS GOOD AT
The project has been reading v37's advantage as a better entry. **Its measured advantage is a cleaner
EXIT**: 1.9422 achieved against 2.0 nominal, the best ratio anywhere in three labs. Every BTC-lab
mechanism that failed did so with a truncated exit, not obviously a worse entry. **That is where the
invented lab should be looking.**

---

## HARD LESSON 40 — TIME-TO-TARGET IS NOT A BAR-COUNT PROPERTY. GEOMETRY EXPRESSED IN BARS DOES NOT TRANSFER ACROSS TIMEFRAMES.

**Attack 43 falsified this directly, on both of its specific predictions.**

I took Attack 37's geometry, held **every parameter in bar units** (lookback 20 bars, maxBars 192
bars, rr 2.0, minRpct 0.80), and changed **only the bar size**, 15m to 1h. The argument was that a
bar-expressed geometry sees the same *shape* on any timeframe, so the achieved/nominal win-loss
ratio would be preserved while R rose. Both halves of that argument were wrong:

| prediction | result |
|---|---|
| achieved/nominal preserved | **1.507 vs 2.0 — still 25% short**, essentially Attack 42's 1.445 |
| frequency falls ~4x with 4x fewer bars | **315 trades vs 322**, on 21,640 bars vs 85,655 |

**Two things this establishes:**

1. **The target does not get proportionally easier on a bigger bar.** A 2R move where R is set by a
   larger bar's range is a larger *percentage* move, and percentage moves do not complete in a fixed
   number of bars. Bar-count and price-distance are separate budgets, and rescaling one does not
   rescale the other.
2. **The signal itself is not scale-invariant.** A 20-bar swing low was swept roughly **four times
   more often per bar** on 1h. So "the same rule on a different timeframe" is not a controlled
   comparison in either direction — it admits a different population *and* a different edge.

**HOW TO USE THIS:** a timeframe change is a **new mechanism**, not a rescaling of an old one, and
must be justified and screened as one. Never argue that a result should transfer because the
parameters are written in bars.

**READING CORRECTION worth keeping:** `avgWinningTrade` and `avgLosingTrade` are in **dollars off a
moving equity base**. Attack 43's −$92.37 average loss looks *smaller* than Attack 37's −$116.19, but
equity fell 47.81% during the run, so later trades sized off a much smaller base. **Compare
percentage fields across runs with different equity paths, never dollar averages.** Ratios like
`ratioAvgWinLoss` are safe because the base cancels.


---

## HARD LESSON 41 - A TARGET DEFINED AS A MULTIPLE OF THE STOP IS A DISTANCE THE MARKET HAS NO REASON TO TRAVEL. TARGET A LEVEL INSTEAD.

**HARD LESSON 39 said the achieved-vs-nominal ratio is the number that separates working from failing,
and five builds confirmed it. Attack 44 found the CAUSE, and it is fixable.**

Every one of those five set its target as `rr x R`:

| build | achieved ratio |
|---|---|
| Attack 41 (rr 3.0) | win rate collapsed |
| Attack 42 (daily anchor, 2R) | 1.4452 |
| Attack 43 (1h, 2R) | 1.5071 |
| WF e50b (wider shield) | capped |
| **Attack 44 (prior 20-bar HIGH)** | **2.41021229** |

**Twice the stop distance corresponds to nothing.** Price is not aiming at it, so it is reached only
when a move happens to be large enough - which is why the achieved ratio kept landing 25-28% short no
matter what was done to R, to the anchor, or to the bar size. **A level price traded at an hour ago is
something price demonstrably returns to.**

**HOW TO USE THIS:** prefer an exit at a STRUCTURAL LEVEL over an exit at a multiple of risk. Then let
reward:risk be an OUTPUT of the geometry and merely DECLINE setups whose geometry is poor, rather than
making rr an input and imposing it on every trade.

**AND THE CONSTRAINT MOVES RATHER THAN DISAPPEARING.** Fixing the exit did not produce a winner - it
relocated the binding constraint to the ENTRY. Attack 44's ratio is excellent and its win rate (27.95%)
is 1.39pp under the 29.33% break-even that ratio implies, with gross edge per trade of $3.31 against an
$8.24 fee. **Exit geometry and entry quality are separate problems and fixing one exposes the other.**

**ENGINE FIELD CORRECTION, worth keeping:** the returned `grossProfit` / `grossLoss` are sums of *net*
trade P&L - their quotient reproduces the reported `profitFactor` exactly. **True pre-commission gross
must be computed as `netProfit + commissionPaid`.** Do not read those two fields as pre-cost figures.


---

## HARD LESSON 42 - THE SHORT-SIDE MARGIN CEILING IS A PROPERTY OF THE MARGIN FORMULA, AND IT HAS BEEN SILENTLY FAKING SHORT RESULTS IN BOTH USER LABS.

HARD LESSON 34 observed that shorts at 100% equity are force-closed at ~0.35% adverse. **Trade-level
forensics in two labs on the same day now show the mechanism, the signature, and the reason it is
asymmetric -- and confirm that every short number this project has produced measured the harness.**

**THE MECHANISM.** For a SHORT, an adverse move increases the loss AND increases the notional, so
required margin rises while equity falls and at `percent_of_equity 100` with `margin_short=100` the two
cross almost immediately. For a LONG, an adverse move SHRINKS the notional, so required margin falls
alongside equity and they never cross. **Longs are safe and shorts are not, by arithmetic.**

**TWO DISTINCT SIGNATURES, and they look nothing alike:**

| | 3M v53 | WF e64a |
|---|---|---|
| signature | `cascadeRatio` 1.4655 | `cascadeRatio` **1** |
| what happens | position sheds ~2% slivers to meet margin, remainder closes later | position is closed outright |
| how to spot it | first row of a group is under 10% of size, always short | **losers exit at wildly inconsistent tiny adverse distances (0.013%-0.585%) while winners exit exactly on target** |

**The second signature is the dangerous one, because `cascadeRatio 1` looks clean.** The tell is not the
cascade ratio -- it is that a build with a FIXED exit distance produces losses at INCONSISTENT
distances. A fixed shield or a fixed stop must produce a consistent loss size. **If it does not, the
strategy's exit is not the thing closing the trade.**

**HOW TO USE THIS:**
1. **On any short build, check loss-distance consistency before believing the win rate.** Read
   `get_trades` -- it is free -- and compare the adverse distance across losers.
2. **Never diagnose a low short win rate as an entry-timing problem until this is ruled out.** Both labs
   did exactly that and both were wrong; War Formation spent three experiments on it.
3. **The only fix is reduced position size (~25-50% of equity), and it is a DECLARED DEVIATION** from
   the forced parity profile. Label it on every run, and never compare such a run against a
   100%-equity long without saying so.


---

## HARD LESSON 43 - HARD LESSON 42's FIX WORKS, AND THE SIZE OF THE CORRECTION IS THE WARNING.

E71 cut War Formation's short from 100% to 25% of equity and **changed nothing else**. Byte-identical
entry logic, same window, same direction rule.

| | 100% equity | **25% equity** |
|---|---|---|
| profit factor | 0.45442725 | **0.97315988** |
| win rate | 6.98% | **36.36363636%** |
| loser exit distances | 0.013% - 0.585%, inconsistent | **exactly +1000.0 points, all 21** |

**A fivefold win-rate change from a sizing parameter.** Verified free with `get_trades`: every loser
exits at exactly the shield and every winner at exactly the target, with zero liquidations.

**THE WARNING IS THE MAGNITUDE.** A harness artifact did not shade this result, it INVERTED it - a
gross-positive mechanism with a win rate above its own break-even was reading as a 0.45 profit factor
and a 6.98% win rate. Three experiments were spent theorising about entry geometry on top of it.

**HOW TO USE THIS:**
1. **On any short build, verify loss-distance consistency BEFORE interpreting anything else.** It is
   free. A build with a fixed exit distance must produce a consistent loss size.
2. **Reduced size is a DECLARED DEVIATION.** Label it on every run and never place such a run beside a
   100%-equity run as though they were comparable. Every long number in the War Formation lab is a
   100%-equity number and none of them can currently be set beside E71.
3. **Report the POINT ratio, not just the dollar ratio, for fixed-gap builds.** E71's exits are exactly
   1000 and 2000 points, an exact 2.0, yet `ratioAvgWinLoss` reads 1.70302978 because qty varies with
   price and commission is subtracted from both sides. The dollar ratio understates a fixed-gap design.

---

## HARD LESSON 44 — AN IDENTICAL TRADE COUNT PLUS AN IDENTICAL WIN/LOSS SPLIT IS THE STRONGEST "NOTHING CHANGED" EVIDENCE THERE IS. IT BEATS A MATCHING PROFIT FACTOR.

E72 re-ran War Formation's long at 25% of equity against e58a's 100%. The profit factor moved from
1.24015239 to 1.26239697 — close, but on its own that proves little; two different trade populations
can land on similar ratios by luck.

**What actually settled it: 36 trades both times, and 15W/21L both times.**

An identical count means the size change admitted **the same population**. An identical win/loss split
means it resolved **every one of them the same way**. Together they say the mechanism was untouched,
which no aggregate ratio can establish on its own.

**This mattered because the alternative was expensive.** Had the long moved materially, HARD LESSON
42's account of the margin asymmetry would have been incomplete and **every 100%-equity number in the
War Formation lab would have needed re-running.** The control cost one credit and closed that off.

**HOW TO USE THIS:**
1. **When testing whether a change is inert, read count and win/loss split before the ratio.** They
   are the population-level evidence; the ratio is a summary that can coincide.
2. **A parameter proven inert on one leg is not proven inert on the other.** Sizing destroyed the
   short (0.45442725 → 0.97315988) and left the long alone — the same change, opposite verdicts, for a
   reason that is arithmetic and was predictable in advance.
3. **Reproducing a result at a DIFFERENT setting, with an identical trade population, is stronger
   evidence than repeating it at the same setting** (LESSON 25). e58a now clears that higher bar.

---

## HARD LESSON 45 — WHEN EVERY VERSION OF A FILTER COSTS THREE QUARTERS OF THE SAMPLE, THE BINDING CONSTRAINT IS THE DATA, NOT THE FILTER.

3M tried two bias gates on the same mechanism:

| gate | source | count | profit factor |
|---|---|---|---|
| v54 — consecutive higher/lower closes, 12H **and** 24H | **the lab's own invention** | 155 → 48 (−69%) | 1.25172059 → 1.15861551 |
| v56 — 20/50/200 SMA stack on 15m | **the source's own rule**, verified in the transcripts | 155 → 37 (**−76%**) | 1.25172059 → **1.62137752** |

v56 improves profit factor by 0.37 **and** improves drawdown — it passes RATCHET v2 clauses 1–3
outright. **Clause 4 kills it:** a >50% cut needs a split test, and splitting 37 trades at 2024-06-08
gives **27 and 10**. Both under the sample floor, so the split can never clear **no matter how it
lands**.

**Two gates, opposite provenance, opposite PF directions — same fatal count collapse.** That points at
the data, not at either gate. The mechanism fires ~155 times in 4.7 years; **any** condition that is
true less than a quarter of the time takes it under the floor.

**HOW TO USE THIS:**
1. **Before building a filter, estimate what fraction of bars it will be true on, and multiply.** If
   the projected count lands near the floor, the run cannot promote whatever it returns — so run it
   only as a measurement, and say so up front.
2. **Compute the split feasibility from the FREE trade log before spending credits on halves.** Two
   credits were saved here by reading entry timestamps rather than running H1 and H2 that could not
   have counted.
3. **A result can be genuinely good and still unpromotable.** v56's halves land at roughly 1.60 and
   1.67 — strikingly consistent — and that is *still* not evidence, because 10 trades cannot carry a
   ratio. Consistency is not a substitute for sample size.

**AND A CORRECTION TO MY OWN REASONING, which is the reason this lesson exists.** I registered the
prediction that "a stack ordering is a COMMON state" and would therefore cut mildly. It cut *harder*
than the gate I was criticising. A 200-SMA on 15m spans ~50 hours, and demand-zone taps happen during
pullbacks — exactly when the fast averages are dipping toward the slow one. **The gate and the entry
were competing for the same moments**, which is the redundancy the E14 audit line names but which I
did not weigh heavily enough when predicting the count.
