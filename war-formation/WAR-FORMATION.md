# THE WAR FORMATION
BTCUSDT · base chart **1m** · cascade 6h → 1h → 15m → 3m → 1m
Separate test, separate ledger, separate dashboard.

> Research specification for backtesting. Not a trade recommendation.

---

## The idea
A single trade has to survive five layers of agreement before it is allowed to exist. The 6-hour
block sets which side of the war you are on. The 1-hour must not be fighting it. The 15-minute gives
the level worth defending. The 3-minute has to coil — the pullback must run out of energy. Only then
does the 1-minute fire, and only if the reclaim comes back with **velocity**. Every layer is a veto.
Most of the time nothing is allowed to trade, which is the point.

Once filled, the trade gets a **protective gap** and is left alone. No trailing, no management, no
reacting to the first move — roughly 40% of good trades start negative, and interfering during that
phase is how winners get closed early.

## Why this shape can survive costs
Strategy 002 died because it fired ~5,000 times at a ~0% edge and commission ate it (HARD LESSON 1
in the main ledger). The War Formation is built the opposite way: five stacked vetoes crush trade
frequency, and the protective gap makes each trade large relative to the 0.05% fee. A wide stop with
few trades is structurally the right answer to a commission problem.

---

## Timeframe reconstruction (important)
The engine has **no 3m data and no 6h timeframe**, and Pine here **cannot use `request.security`**.
So every higher timeframe is rebuilt from 1m bars using timestamp arithmetic:

> **VERIFIED 2026-09-05 (cycle check #37).** This claim had stood since v1 without ever being checked.
> It is **TRUE**: `plan_backtest_window(BTCUSDT, 3m, ...)` and `(BTCUSDT, 6h, ...)` both return a hard
> `404 no_bars`, as does `2m`. The engine's BTCUSDT timeframe set is **{1m, 5m, 15m, 30m, 1h, 4h}** —
> so the 3m of the Oracle's own drill-down and the 6h "God of direction" must both be synthesised, and
> the timestamp arithmetic below is not a convenience, it is the only available route. Full coverage
> table in `EXPERIMENT-LOG.md` cycle check #37.

```
bucket6h  = floor(time / 21600000)     // 360 x 1m
bucket1h  = floor(time /  3600000)     //  60 x 1m
bucket15m = floor(time /   900000)     //  15 x 1m
bucket3m  = floor(time /   180000)     //   3 x 1m
```
A bucket index changing between bars marks a new higher-timeframe candle. This is exact, not an
approximation — a 6h candle *is* 360 consecutive 1m bars.

---

## LAYER 1 — the 6-hour war (direction)
Direction for the current 6h block is set by the **previous completed 6h block**, counted in 1-hour
candles. Six 1h candles make one 6h block.

| Green 1h candles in the last 6h block | Regime |
|---|---|
| >= 4 | **BULL** — longs only |
| <= 2 | **BEAR** — shorts only |
| 3 | **NEUTRAL** — no trades |

Using the *previous* block means direction is defined and fixed for the whole current block, rather
than drifting as the block fills in.

## LAYER 2 — the time gate
**No trading in the first hour or the last hour of the 6h block.** Tradeable window is minutes
60–300 of the 360-minute block. The open is noise and the close is repositioning.

## LAYER 3 — the 1-hour must agree
The current 1h candle must be pointing the same way as the regime:
- BULL requires `close > open_of_current_1h`
- BEAR requires `close < open_of_current_1h`

If the 1h is fighting the 6h, stand down.

## LAYER 4 — the 15-minute level
The level is the **previous completed 15m candle's extreme**:
- BULL: `level = previous 15m low` (support to be defended)
- BEAR: `level = previous 15m high` (resistance to be rejected)

Price must first violate the level — dip below it in BULL, poke above it in BEAR — so that the
reclaim has something to reclaim.

## LAYER 5 — the 3-minute coil
The pullback must lose energy before the entry. Measured as volatility compression:
```
coiled = ta.atr(3) < ta.atr(30) * coilK        (coilK default 0.85)
```
On a 1m chart `ta.atr(3)` is the last 3 minutes — the 3m candle's energy — against the last half
hour. A pullback still accelerating is not an entry.

## THE TRIGGER — 1 minute, with velocity
- **LONG:** `ta.crossover(close, level)` — 1m closes back above the reclaimed 15m low
  **AND** `close - level >= velMin` (the reclaim has velocity, not a limp touch)
- **SHORT:** `ta.crossunder(close, level)` **AND** `level - close >= velMin`

`velMin` default $120. This is the **velocity** lesson: a level retaken hard tends to run; a level
barely touched tends to fail back through.

---

## THE ORACLE OVERLAYS
These are context filters, not signals. They veto; they never trigger.

### Whole-number middles — the dead zone
`sub = close mod 1000`. **No entries when `400 <= sub <= 600`.** The middles are the most dangerous
place to trade — no structure, no memory, nothing to lean on.

### The witching hour
`1:00–4:00 a.m. ET` is the overnight dump window. **No longs during it.** Shorts are permitted —
that is the direction the window is known for. (Exchange time is UTC; ET offset is an input,
default −4.)

### Time-of-day map (logged, not traded)
The known pump/dump windows — AM waves 7–8, the 9:30 open, the 11–1 midday bus pump, the 4pm close
pump, the 8pm end-of-day pump — are recorded as a plot for later analysis but do **not** gate entries
in v1. They are "usually right, not always on time", so they earn their way in only if the data
supports it.

---

## RISK — the protective gap. Fixed at entry. Walk away.
| | |
|---|---|
| **Stop loss** | `entry * (1 -/+ gapPct)` — `gapPct` default **4.0%** (the $4,000 gap at ~$100k BTC) |
| **Take profit** | `entry * (1 +/- gapPct * rr)` — `rr` default **1.5** → 6.0% |
| **Time stop** | flat after `maxBars` = **1440** 1m bars (24h) if neither level is hit |

Both levels are set at the moment of entry and never moved. **No trailing stop.** No averaging down,
no grid, no martingale, no adding to a loser. One position at a time, `pyramiding = 1`.

Worst case per trade is one gap. The whole design intent is that you set it, protect it, and leave.

---

## Data limitation — state this with every result
1m coverage on this engine is **2025-12-16 → 2026-05-03**, about **4.6 months** (199,802 bars).
That is a single market era, not a multi-regime sample. With five stacked vetoes the trade count
will be low, and a low trade count over one era is **suggestive, never conclusive**. Any result here
is a screening result. Treat a good number as "worth testing further", not as validation.

Also note the engine forces `commission 0.05%`, `percent_of_equity 100`, `margin 100/100` — so the
backtest tests the *signal*, not the position sizing written above (main ledger, HARD LESSON 2).

## Falsifiable claim
Requiring all five layers produces a materially higher win rate and profit factor than the 1m
reclaim trigger alone. If stripping the 6h/1h/15m/3m vetoes leaves performance unchanged, the
cascade is decoration and only the velocity trigger matters.


---

# v4/v5 — HEIKIN ASHI EDITION (2026-09-01)

The strategy is read on **Heikin Ashi**, and the protective-gap framing is dropped.

## Heikin Ashi policy — read this before trusting any number
HA is computed from real OHLC in-script (pure arithmetic, no higher-timeframe fetch):
```
haClose = (open + high + low + close) / 4
haOpen  = (previous haOpen + previous haClose) / 2
```
**HA is used for direction and colour only:**
- the 6h regime counts green **HA** 1h candles,
- the live 1h must agree on **HA**,
- the 1m trigger bar must be the right **HA** colour.

**All levels, entries, stops and targets use REAL prices.** HA prices are synthetic — an order cannot
fill at one. A backtest that enters and exits at HA prices reports fills that cannot happen, and it
always looks spectacular. This is the single most common way an HA strategy fools its author.

## Risk (replaces the protective gap)
Stop sits **beyond the level that was just swept** — the current 15m extreme, plus a 0.25×ATR(30)
buffer — clamped between a floor and ceiling expressed as a % of price. Target at **2R**. Both fixed
at entry, never moved. Time stop at 720 bars as a backstop only.

## HARD LESSON 3 — commission sets a FLOOR on stop distance
The 0.05% fee is charged twice per round trip: **0.10% of notional**. That cost is fixed, so its
damage depends entirely on how wide the stop is:

| Risk (R) as % of price | Fee as % of R | Effect on a nominal 2:1 |
|---|---|---|
| 0.15% | ~66% | destroyed — actual 0.89:1 (v4, PF 0.47) |
| 0.50% | ~20% | badly degraded |
| **0.80%+** | **~12%** | **survivable — actual 1.89:1 (v5, PF 1.40)** |

v4 and v5 are the SAME strategy. The only change is the risk floor: 0.15% → 0.80%. That one number
moved it from PF 0.47 to PF 1.40. Nothing about the signal changed.

**Rule: R must be at least ~8x the round-trip fee.** At 0.10% round trip, that means R >= 0.8%.
This is the mirror image of HARD LESSON 1 in the main ledger — there, too many trades killed it;
here, too tight a stop killed it. Both are the same fee arithmetic seen from different sides.

## Results
| Version | Change | Trades | Net | PF | Max DD | Status |
|---|---|---|---|---|---|---|
| v1 | standard candles, 4% gap | **0** | — | — | — | design bug: coil and thrust required on the same bar |
| v2 | coil moved to prior bar | 32 | −11.6% | 0.38 | 14.9% | rejected — every winner exited on the time stop |
| v3 | gap 4% → 2% | 36 | −5.5% | 0.58 | 7.0% | rejected — target still never hit |
| v4 | **Heikin Ashi** + structural stop, R floor 0.15% | 52 | −4.6% | 0.47 | 4.9% | rejected — fees > gross profit |
| **v5** | **R floor 0.15% → 0.80%** | 47 | **+6.5%** | **1.40** | 4.7% | **testing** |

v5 detail: Sharpe 1.70, win rate 42.6%, avgWin/avgLoss 1.89.
**Longs 18 of 32 (+$784). Shorts 2 of 15 (−$139).**

## Why v5 is TESTING and not PASSED
1. **47 trades over 4.6 months in one market era.** That is a screening sample, not validation.
2. **The edge is entirely long-side.** Shorts are 2 for 15. Either the bear-side level logic is wrong
   or the sample period simply rose — this data cannot separate those.
3. **No out-of-sample period and no parameter sensitivity run.** 1m coverage is all there is
   (2025-12-16 → 2026-05-03), so a true holdout is not available on this engine.
4. The engine forces 100%-of-equity sizing, so this tests the signal, not position sizing.

## Next tests, in order of value
1. **Strip the cascade.** Run the 1m velocity trigger alone. If it matches v5, the 6h/1h/15m/3m
   vetoes are decoration and only velocity and the risk floor matter.
2. **Long-only.** Shorts lost money; removing them should raise PF. If it does, that is a finding
   about the short logic, not a curve-fit.
3. **Sensitivity sweep** on the risk floor (0.6 / 0.8 / 1.0 / 1.2%) and rr (1.5 / 2.0 / 2.5).
   If the edge only exists at exactly 0.80%, it is noise.
4. **Split the window** in half and compare first vs second half.
