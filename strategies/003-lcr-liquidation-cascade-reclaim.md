# 003 — LCR-1 "Liquidation Cascade Reclaim"
Universe: BTCUSDT (Bybit USDT linear perp) · Timeframes: 15m and 5m
Status: SPEC → see Results
Family consumed: `liquidation-cascade signatures`

## Idea in one paragraph
A liquidation cascade is not ordinary selling. One forced close pushes price into the next trader's
liquidation threshold, which forces another, and thin books turn that chain into a violent wick.
Minute-level work on the October 2025 crash documents volume surging ~22x baseline ahead of the
trough. The tradeable question is not "did a cascade happen" but **"is it finished?"** — and the bar
itself answers that. If the cascade bar closes back up off its low, the forced sellers are cleared and
the snapback is on. If it closes *on* its low, the chain is still running and the next move is down.
Same detection, opposite trade, selected mechanically by where the close sits in the bar.

## Why this shape can pay the fees
This is the deliberate opposite of 002. Cascades are rare, so trade count is low; cascade bars are
2.5x ATR, so the payoff per trade is large. HARD LESSON 1 says a mechanism needs ~0.10% average gross
per trade to survive the 0.05% commission; HARD LESSON 3 (from the War Formation) says the stop must
be at least ~8x the round-trip fee, i.e. R >= 0.8%. This design targets R >= 1.2% and rr 2.0.

**Pre-registered estimate (compare against the real result below):**
cascade bars ≈ 0.1–0.3% of bars → ~150–400 trades over 4.7 years.
At R = 1.2%, rr = 2.0, win rate 40%: EV = 0.4(2.0) − 0.6(1.0) = **0.2R ≈ 0.24% gross per trade**
versus a 0.10% round trip. Clears the gate with roughly 2.4x margin.

## Definitions
Working timeframe TF ∈ {15m, 5m}.
- `atrN = ta.atr(50)`
- `volAvg = ta.sma(volume, 50)`
- `rng = high - low`
- `closePos = (close - low) / rng` — where the close sits inside the bar, 0 = on the low, 1 = on the high
- **Cascade bar** = `rng > rangeK * atrN` **AND** `volume > volK * volAvg`
  (`rangeK` default 2.5, `volK` default 3.0)
- **Down cascade** = cascade bar **AND** `low <= ta.lowest(low, 50)[1]` (a new 50-bar low)
- **Up cascade** = cascade bar **AND** `high >= ta.highest(high, 50)[1]` (a new 50-bar high)

## The regime switch — where the close sits decides the side
| Cascade | closePos | Reading | Trade |
|---|---|---|---|
| Down | `>= 0.55` | flush rejected, forced sellers cleared | **LONG** (reversion) |
| Down | `<= 0.25` | closed on the low, chain still running | **SHORT** (continuation) |
| Up | `<= 0.45` | spike rejected, forced buyers cleared | **SHORT** (reversion) |
| Up | `>= 0.75` | closed on the high, squeeze still running | **LONG** (continuation) |

`0.25 < closePos < 0.55` on a down cascade (and `0.45 < closePos < 0.75` on an up cascade) is the
dead band — ambiguous, no trade. Entry at the open of the bar after the cascade bar closes.

## Risk — SL and TP both fixed at entry. No trailing stop.
Let `buf = 0.2 * atrN`.

| Trade | Raw risk R |
|---|---|
| Reversion LONG | `close - (low - buf)` — stop under the cascade wick |
| Continuation SHORT | `(high + buf) - close` — stop over the cascade high |
| Reversion SHORT | `(high + buf) - close` |
| Continuation LONG | `close - (low - buf)` |

`R` is then clamped to **[1.2%, 4.0%] of price** — the floor enforces HARD LESSON 3, the ceiling stops
one enormous bar from sizing the whole account into a single idea.

- **Stop loss:** entry ∓ R
- **Take profit:** entry ± `2.0 * R`
- **Time stop:** flat after `maxBars` (default 96 bars = 24h on 15m) if neither level is hit.

One position at a time, `pyramiding = 1`. No averaging down, no grid, no martingale, no adding to a
loser. Worst case per trade is one R.

## Backtest instructions
- Pine v6, all allowlisted: `ta.atr`, `ta.sma`, `ta.highest`, `ta.lowest`, `volume`.
- Header: `pyramiding=1`, `process_orders_on_close=true`, percent-of-equity sizing.
- Exits via `strategy.exit(stop=, limit=)` at absolute prices; `strategy.close_all` only for the time stop.
- Ladder: 15m first. PF < 0.95 → stop and record rejected. Otherwise 5m, then sensitivity on `volK`.
- **Report reversion trades and continuation trades separately.** The whole claim is that `closePos`
  selects the right side. If both legs behave identically, the switch is doing nothing and the result
  is just "trade big volatile bars".

## Falsifiable claim
On a cascade bar, `closePos` predicts the sign of the next move: closes in the upper part of a
down-cascade are followed by upward drift, closes on the low by further decline. If reversion and
continuation trades perform the same, `closePos` carries no information and the family is dead.

---

## RESULTS
See `results/backtests.json` and the dashboard. Filled in after the ladder ran.
