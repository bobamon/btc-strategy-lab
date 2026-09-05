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
