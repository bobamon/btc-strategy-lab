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

## Mechanism families already consumed
- `cross-complex-OR-confirmation` (001, archived)
- `autocorrelation-sign regime` (002) — variance-ratio form, **rejected on real data**

## Families still open for future cycles
volume/participation profile · volatility-term-structure (5m vs 15m realized vol ratio)
· time-of-day seasonality (Asia/London/US overlap) · order-flow imbalance proxies
· range-compression expansion · session-VWAP band mechanics · funding-rate / basis effects
· liquidation-cascade signatures · autocorrelation regime via other estimators (Hurst, ACF sign)
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

## Platform constraints — trader.dev engine
- Pine **//@version=6**, allowlist of 65 `ta.*` indicators.
- **FORBIDDEN:** `request.security` (no cross-symbol), arrays/maps, `strategy.cancel`,
  `strategy.order`, pyramiding > 1, martingale, custom var-trail (`if low <= trail → close`).
- Exits via `strategy.exit(stop=, limit=, trail_*, qty_percent=)` and `strategy.close`.
- Symbol universe: **Bybit USDT linear perpetuals only** (639 instruments).
- Each backtest costs **1 credit**. Weekly grant 1000. At 96 cycles/day, do not backtest every cycle.
- Always call `plan_backtest_window` first — it clamps dates and reveals symbol remaps.

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
