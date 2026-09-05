# INDEX SWEEP — the original mandate, reopened 2026-09-05

> Research specifications for backtesting. Not trade recommendations.

**This is a fourth workstream and it is separate.** It does not share a base, a board or a ratchet
history with the invented BTC lab (`CHAMPION-BOARD.md`), War Formation (`war-formation/`) or 3M Elite
(`three-m-elite/`). Nothing here may be merged into those, and no construction from those was imported
here. The strategies used in this file are deliberately **neutral built-ins**, never Attack builds,
so that a result here can never be mistaken for a result about the BTC lab.

**Engine:** `backtest-lab` MCP (backtester24). Indices route to Yahoo, so `source="yahoo"` — the
`source="perp"` convention used elsewhere in this project is a Binance crypto archive and cannot serve
indices. Explicit `start`/`end` on every call; every cell recorded below reported `pinned: true`.

---

## WHY THIS WAS REOPENED

The original mandate (2026-09-01) was **one strategy that works across US30, NAS100, YM and NQ**. It
was abandoned the same day, and `STRATEGY-LEDGER.md`'s archived note records exactly why: on the old
trader.dev engine `US30` and `NAS100` were hard errors, and `NQ` and `YM` were **silently remapped to
`IONQUSDT` and `DYMUSDT`** — crypto perps. A backtest would have returned genuine metrics for the
wrong instrument. The universe was narrowed to BTCUSDT-only and stayed there for four days.

**That failure mode is fixed on the new engine, and it was verified before anything was run.**
`list_pairs(source="yahoo")` returns NAS100, US30 and SPX500 as first-class symbols with the mapping
stated openly (`NAS100 -> ^NDX`). No silent remap. The reason for the abandonment no longer holds.

## DATA LIMITS, MEASURED NOT ASSUMED

Yahoo caps intraday history, and the cap is real: a 1h request spanning 2024-09-05 → 2026-09-01
**errored outright** on all three symbols. What actually resolves:

| Timeframe | Window that works | Bars |
|---|---|---|
| 1h | 2025-09-05 → 2026-09-01 | 1,730 |
| 1d | 2022-01-01 → 2026-09-01 | 1,169 |

15m is not usable for this work — Yahoo caps 5m–30m at ~60 days, which cannot produce a sample worth
quoting. **The BTC lab's 15m convention does not transfer to indices.**

---

## SWEEP 1 — `donchian_breakout`, untuned defaults (entry 20 / exit 10)

Chosen because it is a classic, parameter-untouched trend follower: the point of a first sweep is to
read the universe, not to fit anything. Long and short both enabled (the engine's default for
indices), fee 5bps, no stop, no target.

### 1h — 2025-09-05 → 2026-09-01, 1,730 bars each, all `pinned: true`

| Symbol | PF | Trades | Win rate | Net | Buy & hold | Max DD |
|---|---|---|---|---|---|---|
| **NAS100** | **1.32603** | 48 | 37.5% | +11.610506% | +24.678064% | -19.147514% |
| SPX500 | 0.635257 | 57 | 31.578947% | -11.596804% | +18.661585% | -19.568481% |
| US30 | 0.533099 | 56 | 28.571429% | -12.361333% | +17.173812% | -12.721466% |

### 1d — 2022-01-01 → 2026-09-01, 1,169 bars each, all `pinned: true`

| Symbol | PF | Trades | Win rate | Net | Buy & hold | Max DD |
|---|---|---|---|---|---|---|
| **NAS100** | **1.194034** | 35 | 40.0% | +15.505107% | +78.507951% | -16.929431% |
| SPX500 | 1.004401 | 38 | 39.473684% | +0.246708% | +60.242758% | -17.982764% |
| US30 | 0.767016 | 39 | 38.461538% | -13.424086% | +45.37601% | -24.632748% |

Every cell clears RATCHET v2 clause 3 (≥30 trades): the counts run 35–57. Sample is not the problem
with any number above.

---

## THE FINDINGS

### 1. The mandate's own question has an answer, and it is no.

One strategy does **not** work across all three. On both timeframes NAS100 is profitable and US30 is
outright negative, with the same untuned construction on the same dates. The spread is not marginal —
PF 1.326 against 0.533 on the 1h window. **A single strategy generalising across these indices is not
supported by this evidence.**

### 2. The instrument ranking reproduced across two independent windows — and that is the trap.

NAS100 > SPX500 > US30, in that exact order, on **both** sweeps. The two sweeps use different
timeframes and barely-overlapping windows (1h covers one year; 1d covers four and a half), so a
reproduced ordering looks like a real property of the instruments.

**It is not, or at least it is not shown to be.** The buy & hold column ranks the three instruments in
the *identical* order in both sweeps:

- 1d B&H: NAS100 +78.51% > SPX500 +60.24% > US30 +45.38% — strategy PF: 1.194 > 1.004 > 0.767
- 1h B&H: NAS100 +24.68% > SPX500 +18.66% > US30 +17.17% — strategy PF: 1.326 > 0.635 > 0.533

The strategy's ranking of the instruments is perfectly rank-correlated with how much each instrument
simply went up. A long-biased trend follower ordering instruments by their trend is not a finding
about the strategy; it is the strategy restating its own bias. See HARD LESSON 54.

### 3. Every single cell loses to buy & hold. Including the winner.

The best cell on the board is NAS100 1d at PF 1.194 — which returned **+15.51% against buy & hold's
+78.51%** over the same window. NAS100 1h returned +11.61% against +24.68%. **There is no cell here
where the strategy beat holding the index**, so nothing in this sweep is yet a reason to trade a
strategy on an index rather than hold it.

This is the first time this project has had a buy & hold baseline at all — the old engine did not
report one, and no record in `CHAMPION-BOARD.md` contains one. It earned its keep immediately.

---

## WHAT THIS DOES NOT SAY

- It does not say index trading is dead. It says **one untuned Donchian breakout** does not
  generalise across three indices, and does not beat holding them, in these two windows.
- It does not say NAS100 is tradable. NAS100's advantage is not separated from its trend.
- **Neither sweep has been split-tested.** Per HARD LESSON 22 an in-sample number is not a finding,
  and nothing here has been validated outside the window it was read on. Nothing above should be
  built on until it is.
- No parameter was tuned, so nothing here is curve-fitted — but equally, nothing here is optimised,
  and a negative result on defaults is weaker evidence than a negative result after a fair search.

## QUEUE

1. **The next index tick must control for the buy & hold confound**, not repeat the sweep. The
   informative comparison is a strategy whose bias is not long-only-trend — a mean-reverter, or the
   same Donchian with shorts disabled versus enabled — so the ranking has a chance to disagree with
   B&H. If the ranking still tracks B&H exactly, that is itself the answer.
2. **Split-test the one cell that is above 1.0 on both timeframes (NAS100)** before treating it as
   anything. `split_test` exists on this engine and costs nothing.
3. **Do not sweep Donchian's `entry`/`exit` parameters** to rescue US30 or SPX500. Per HARD LESSON
   4/45 that is fitting a threshold to a diagnosed failure.
4. Consider whether the mandate's original YM/NQ are worth adding. They are the futures contracts for
   US30/NAS100 rather than separate instruments, so they likely add correlation, not coverage — check
   before spending a cell on them.

---

# SWEEP 2 — `bollinger_reversion`, untuned defaults (20 / 2.0). THE BUY & HOLD CONTROL, AND IT PASSES.

Executes this file's queue item 1. HARD LESSON 54 said the informative test is a strategy whose bias
is **not** long-only-trend, so that its instrument ranking has a chance to disagree with buy & hold.
A mean-reverter is that strategy. Same symbols, same windows, same fee, untuned defaults, both
directions enabled — only the mechanism changed.

### 1h — 2025-09-05 → 2026-09-01, 1,730 bars each, all `pinned: true`

| Symbol | PF | Trades | Win rate | Net | Buy & hold | Max DD |
|---|---|---|---|---|---|---|
| **US30** | **1.29779** | 64 | 60.9375% | +4.31124% | +17.173812% | **-4.570215%** |
| SPX500 | 0.827093 | 53 | 58.490566% | -4.243359% | +18.661585% | -15.583121% |
| NAS100 | 0.687711 | 57 | 57.894737% | -12.728016% | +24.678064% | -24.845305% |

### 1d — 2022-01-01 → 2026-09-01, 1,169 bars each, all `pinned: true`

| Symbol | PF | Trades | Win rate | Net | Buy & hold | Max DD |
|---|---|---|---|---|---|---|
| **SPX500** | **1.246588** | 43 | 72.093023% | +11.372664% | +60.242758% | -14.627893% |
| NAS100 | 0.689639 | 36 | 58.333333% | -19.329436% | +78.507951% | -31.245528% |
| US30 | 0.644028 | 43 | 51.162791% | -16.513792% | +45.37601% | -23.466576% |

All six cells clear the ≥30 sample floor (36–64 trades).

---

## FINDING 4 — THE CONTROL PASSES. THIS RANKING DOES **NOT** TRACK BUY & HOLD.

Buy & hold ranks the instruments **NAS100 > SPX500 > US30** on both timeframes. Sweep 1's trend
follower reproduced that order exactly, twice, which is what made it uninformative.

**The mean-reverter does not:**

| | 1st | 2nd | 3rd |
|---|---|---|---|
| Buy & hold (both TFs) | NAS100 | SPX500 | US30 |
| Sweep 1, trend follower, 1h | NAS100 | SPX500 | US30 |
| **Sweep 2, mean-reverter, 1h** | **US30** | SPX500 | **NAS100** |
| **Sweep 2, mean-reverter, 1d** | **SPX500** | **NAS100** | US30 |

On 1h the mean-reverter puts the **worst** buy & hold instrument first and the **best** one last. That
is the residual HARD LESSON 54 said to look for: a ranking that survives after drift is accounted for.
The lesson's test was proposed one cycle ago on a single confounded sweep, and on its first real
application it cleanly separated an informative result from an uninformative one.

## FINDING 5 — ON 1h THE TWO SWEEPS ARE AN EXACT INVERSION, AND THAT IS MECHANISTICALLY COHERENT

| Symbol | trend follower PF (1h) | mean-reverter PF (1h) |
|---|---|---|
| NAS100 | **1.32603** | 0.687711 |
| SPX500 | 0.635257 | 0.827093 |
| US30 | 0.533099 | **1.29779** |

The order reverses exactly. **The instrument the breakout system did best on is the one the reversion
system did worst on, and vice versa** — which is what you would expect if the three indices differ in
how much they trend versus range, and if these two untuned mechanisms are reading that same property
from opposite sides. US30 is the most range-bound of the three over this window and NAS100 the most
trending; each mechanism found the market that suits it.

**US30 1h is the single best risk cell either sweep has produced**: PF 1.29779 on 64 trades at a
**4.57% max drawdown**, the lowest in twelve cells by a wide margin.

## FINDING 5b — THE INVERSION DOES **NOT** HOLD ON 1d, AND THAT LIMIT IS STATED

On 1d the mean-reverter ranks SPX500 > NAS100 > US30, which is neither the buy & hold order nor an
inversion of the 1d trend-follower order (NAS100 > SPX500 > US30). US30 is last on both 1d sweeps.
So the clean trend-versus-range story is a **1h phenomenon in this data, not a general one**, and the
1d cells do not support it. One timeframe agreeing is not two.

## FINDING 6 — TWELVE CELLS, ZERO BEAT BUY & HOLD ON RETURN

Adding sweep 2, the count is now **12 cells across two mechanisms, two timeframes and three
instruments, and not one has beaten buy & hold on return.** The best of sweep 2 is US30 1h at +4.31%
against +17.17%. The strategy-versus-holding gap is not a property of the trend follower; it is so far
a property of this whole exercise.

---

# SPLIT TEST — NAS100 1d, `donchian_breakout` (queue item 2)

The only cell above PF 1.0 on both timeframes in sweep 1. Split at 2024-04-30.

| | in-sample | out-of-sample | full |
|---|---|---|---|
| Window | 2022-01-03 → 2024-04-30 | 2024-05-01 → 2026-08-31 | 2022-01-03 → 2026-08-31 |
| Bars | 584 | 585 | 1,169 |
| Profit factor | 1.241028 | **1.143209** | 1.194034 |
| Net | +9.174315% | **+5.239724%** | +15.505107% |
| Buy & hold | **+5.689814%** | **+70.08912%** | +78.507951% |
| Trades | 18 | **17** | 35 |
| Win rate | 50.0% | 35.294118% | 40.0% |
| Max DD | -15.259% | -16.929431% | -16.929431% |

Engine verdict: **"holds"** — "+9.17% in-sample, +5.24% out of sample. That is what a real edge looks
like — unexciting and consistent."

## THE VERDICT IS NOT QUOTABLE, AND THE REASON IS THIS LAB'S OWN RULE

**17 out-of-sample trades is below RATCHET v2 clause 3's floor of 30.** By the project's own standing
practice a ratio under ~30 trades is not quoted as a result, and that predates and survives the
ratchet. The engine's "holds" verdict is computed without reference to that floor. **So this split is
recorded as suggestive and explicitly not banked.** The full-window 35 trades clears the floor; each
half does not, which is the structural problem with splitting an already-small daily sample.

Two further warnings the engine raised, both material:

1. **One-legged.** The full window is carried by the long leg (+23.10%) while the short leg loses
   (-17.86%). Per the ledger's standing both-directions requirement the legs must be reported
   separately, and reported separately this is a long-only result with a loss-making short attached.
2. **Trails buy & hold by 64.85%** out of sample.

## THE ONE GENUINELY INTERESTING NUMBER IN THE SPLIT

**In-sample, this is the first index cell in this file to beat buy & hold: +9.174315% against
+5.689814%.** And the split window explains why. The in-sample half was a nearly flat market (B&H
+5.69% over 2.3 years); the out-of-sample half was a violent rally (B&H +70.09%). The strategy beat a
flat market and was left far behind by a rising one.

That is consistent with FINDING 4/5 rather than a separate result: **these mechanisms add value
relative to holding when drift is small, and are dominated by holding when drift is large.** It is
also the same shape as the War Formation benchmark result from the same day — `e58a` beat a *falling*
BTC market by 16 points. Two labs, two instruments, same direction of effect. That is not yet a
finding; it is a pattern worth naming and testing deliberately.

## QUEUE

1. **Test the low-drift hypothesis directly** rather than inferring it from splits: run the same two
   mechanisms on the flattest window each instrument has, and on the steepest, and compare. This is
   the natural next index tick and it costs nothing.
2. **Do not tune anything toward beating buy & hold on a measured window** — HARD LESSON 49.
3. **Report legs separately on every future index cell.** The `one_legged` warning showed the totals
   were hiding a losing short leg; that is exactly what the standing both-directions requirement
   exists to prevent.
4. **Do not bank the NAS100 split.** 17 out-of-sample trades is below the floor. If it is revisited,
   it needs either a longer daily history or a lower timeframe with more trades — and Yahoo's caps
   mean the second is not available.
5. Queue items 3 and 4 from sweep 1 (do not sweep Donchian's parameters; check whether YM/NQ add
   coverage over US30/NAS100) remain open and untouched.
