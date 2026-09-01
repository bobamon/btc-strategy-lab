# 002 — VRS-1 "Variance-Ratio Regime Switch"
Universe: US30, NAS100, YM, NQ · Timeframes: 15m and 5m · Session: NY RTH
Status: SPEC — not yet backtested (see Platform note)
Family consumed: `autocorrelation-sign regime`

## Idea in one paragraph
Lo & MacKinlay's variance ratio asks a single question: does variance scale linearly with holding
period? Under a random walk, `VR(q) = 1`. Above 1, returns are positively autocorrelated and the
market is trending; below 1, they are negatively autocorrelated and the market is mean-reverting.
That one number is a *measured* statement about which regime the tape is currently in — not a
guess from a moving-average slope. So: compute VR on a rolling window, trade breakouts when VR
says trending, fade band extremes when VR says reverting, and stand aside in the middle where the
tape is a coin flip. The regime flip is the strategy, and it is arithmetic rather than opinion.

Unlike 001, every input comes from the traded symbol's own OHLCV — no partner series — so this is
expressible in Pine and backtestable wherever index data exists.

## Definitions
Working timeframe TF ∈ {15m, 5m}. All times US/Eastern.
- `q = 5` — aggregation horizon (bars)
- `L = 120` on 15m, `L = 240` on 5m — variance estimation lookback
- `r1 = close - close[1]` (1-bar change)
- `rq = close - close[q]` (q-bar change)
- **Variance ratio:** `VR = ta.variance(rq, L) / (q * ta.variance(r1, L))`
- `A = ta.atr(14)`
- Bollinger: `[bbMid, bbUpper, bbLower] = ta.bb(close, 20, 2.0)`
- Donchian: `hh = ta.highest(high, 20)[1]`, `ll = ta.lowest(low, 20)[1]`

## Regime classification (evaluated every bar close)
| Condition | Regime | Behaviour |
|---|---|---|
| `VR >= 1.15` | **TREND** | trade breakouts with the move |
| `VR <= 0.85` | **REVERT** | fade band extremes |
| `0.85 < VR < 1.15` | **NEUTRAL** | no new entries |

Thresholds are symmetric around 1.0 and deliberately wide — the dead zone is where the random-walk
null cannot be rejected, and taking trades there is the main way this family bleeds.

## Entry — bar close only, window 10:00–15:00
**TREND regime**
- **Long:** `ta.crossover(close, hh)`
- **Short:** `ta.crossunder(close, ll)`

**REVERT regime**
- **Long:** `ta.crossover(close, bbLower)`  (price closing back up through the lower band)
- **Short:** `ta.crossunder(close, bbUpper)`

All four are edge-triggered crossovers, never level tests — this avoids re-firing on every bar that
happens to sit beyond a level. Entry at next bar open, market.

## Risk — SL and TP both fixed at entry. No trailing stop.
| Regime | Stop loss | Take profit | R:R |
|---|---|---|---|
| TREND | entry ∓ `1.2 * A` | entry ± `2.4 * A` | 2.0 |
| REVERT | entry ∓ `1.0 * A` | entry ± `1.2 * A` | 1.2 |

The asymmetry is deliberate: trend trades are paid by the tail, reversion trades by hit rate.

**Position exit** — whichever comes first:
1. Stop loss, or
2. Take profit, or
3. **Time stop:** flat at the close of the last bar ending at or before 15:55.

**If the regime flips while a position is open, hold to one of the three exits above.** Do not close
on regime change and do not reverse — the stop and target were set on the thesis at entry, and
churning on a flipping statistic is how this family gets chopped up.

## Position sizing and portfolio rules
- Risk **0.50%** of equity per trade. `size = (0.005 * equity) / (stop_distance * point_value)`.
- One position per symbol. **Max 3 entries per symbol per session.**
- **Correlation cap:** at most one symbol per complex concurrently (US30/YM are one bet; NAS100/NQ
  are one bet). Max concurrent risk 1.0%.
- No new entries within 10 minutes of a scheduled high-impact US release.

## Why this has defined downside
Fixed stop and fixed target set at entry, hard time stop, capped entries per session, fixed
fractional sizing, no position ever added to. No martingale, averaging down, or grid. Worst case per
symbol per session is 3 × 0.50% = 1.5%.

## Backtest instructions for the coding agent
- Pine v6 is viable: `ta.variance`, `ta.atr`, `ta.bb`, `ta.highest`, `ta.lowest`, `ta.crossover`,
  `ta.crossunder` are all on the engine allowlist. No `request.security`, no arrays needed.
- Header: `pyramiding=1`, `process_orders_on_close=true`, percent-of-equity sizing.
- Exits via `strategy.exit(stop=..., limit=...)` with absolute ATR-derived prices; `strategy.close`
  only for the 15:55 time stop.
- Run 4 symbols × 2 TFs = 8 runs, then a portfolio run honouring the correlation cap.
- **Report TREND trades and REVERT trades separately.** The whole claim is that the VR sign selects
  the right behaviour; if both legs are only profitable together, the regime switch is doing nothing
  and the result is an artifact of the ATR exits.
- Sensitivity: sweep `q ∈ {3,5,10}`, thresholds `{1.10/0.90, 1.15/0.85, 1.25/0.75}`, `L ∈ {60,120,240}`.
  A real effect should survive the neighbourhood, not live at one point.

## Falsifiable claim
Breakout trades taken when `VR >= 1.15` outperform breakout trades taken when `VR <= 0.85`, and
band-fade trades show the reverse ordering. If the two legs perform the same regardless of VR, the
variance ratio carries no intraday regime information at these horizons and the family is dead.

## Platform note (2026-09-01)
**Not backtestable on trader.dev — the symbols do not exist there.** Verified via
`plan_backtest_window`: the engine covers Bybit USDT linear perpetuals only (639 instruments).
`US30` and `NAS100` return a hard "not in catalog" error. `NQ` and `YM` are worse — they *silently
fuzzy-match* to `IONQUSDT` and `DYMUSDT`, unrelated crypto perps, and would return real-looking
metrics for the wrong instrument entirely.

Route to TradingView's own Strategy Tester (which has the index data) or a Python backtest.
The Pine source is portable to TradingView unchanged.
