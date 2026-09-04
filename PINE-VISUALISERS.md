# CHART VISUALISERS — see what each strategy is actually doing

These are **`indicator()` scripts, not the backtest scripts.** Paste one into TradingView and it
draws every zone, level, gate and trade the real strategy reasons about. The decision logic inside
each is copied **line-for-line** from the `strategy()` file that produced the recorded numbers —
only drawing is added, so what you see is what was measured.

The backtested `strategy()` files are left byte-identical on purpose, so their recorded metrics stay
reproducible (LESSON 25).

| visualiser | paste on | shows |
|---|---|---|
| `three-m-elite/pine/VISUAL-3m-elite-v37.pine` | **BTCUSDT.P, 15m** | 4H demand/supply zones, zone age + touch count, entries, stop, 2R target |
| `war-formation/pine/VISUAL-war-formation-e72-e71.pine` | **BTCUSDT.P, 1m** | the full 6h→1h→15m→1m cascade, whole-number band, shield and target, both legs |

---

## 3M ELITE v37 — `VISUAL-3m-elite-v37.pine`
Champion: **PF 1.25172059 / DD 8.72815312% / 155 trades.**

| on the chart | what it is |
|---|---|
| **green box** | a live **demand zone**. Top = the bull-engulfing 4H candle's **open**, bottom = its **low** |
| **grey box** | that zone after it died — 2 body closes inside it, or aged past 6 |
| **orange box** | a **supply zone** from a bear engulf. Drawn for reference; v37 does **not** trade it |
| **green triangle** | an entry: price tapped a zone that was still fresh and unused |
| **red line** | the stop — the zone's bottom. Fixed at entry, never trails |
| **blue line** | the 2R target. Fixed at entry |
| **label on the zone** | its **age** (in 4H candles) and **touch count** — the two numbers that decide whether the next tap is taken |
| **grey / orange ✗** | a tap that was **skipped**, and which rule skipped it: zone too old, or R under the 0.80% floor |

**Why supply zones are drawn but not traded.** The source says the bearish model is the same thing
upside down, and we built exactly that (v53). It returned **0.70512830**, and trade-level forensics
showed it is **gross-negative at −$895.26 before a cent of commission** — it shorts supply straight
through the 2023–2025 bull advance. The boxes let you see the zones that mirror was taking.

---

## WAR FORMATION — `VISUAL-war-formation-e72-e71.pine`
**Long (E72) PF 1.26239697 · Short (E71) PF 0.97315988** — both at 25% of equity, same window.

| cascade step | on the chart |
|---|---|
| **6H direction** | background tint — **green** = bull regime, **red** = bear regime |
| **1H agreement** | the **yellow** step-line is the current 1H **open**. Longs need price above it, shorts below |
| **15m structure** | the **white** step-line is the prior 15m extreme — the level that must break, then reclaim |
| **1m trigger** | the entry arrow — fires only if the reclaim exceeds **0.8 × ATR30** |
| **whole-number band** | dark red strip (x400–x600). Entries **banned** inside it |
| **witching** | grey shading, 1–4am ET. Longs banned |
| **✗ / ○ / ▫** | near-misses, marking **which gate blocked** a setup: the band, too slow, or the 6H block edge |

### The A.L.C.M. exit — the part most people get wrong
**War Formation has no stop loss.** The red line is not a stop, it is the **shield**: a fixed
**$1,000 dollar gap to liquidation**, adjusted with the Bitunix Pencil. The blue line is the fixed 2R
target. The position ends at one or the other. Nothing trails, nothing is added to a loser.

### One thing the chart cannot show you, and it decides the result
Both recorded runs use **25% of equity, not 100%** — a **declared deviation**. At 100% the margin call
fires at roughly **0.35% adverse**, long before a $1,000 shield is reached, so on the short side the
shield never got to act at all. Proven at trade level:

| | at 100% equity | **at 25% equity** |
|---|---|---|
| where losers exited | 0.013% – 0.585% adverse, inconsistent | **exactly the $1,000 shield, all 21** |
| where winners exited | exactly the $2,000 target | exactly the $2,000 target |
| win rate | 6.98% | **36.36%** |
| profit factor | 0.45442725 | **0.97315988** |

**Same entry logic, byte for byte.** If you trade this, position size is not a detail — it is the
whole result.

---

### Honest status of both
**Neither is a champion.** v37 carries a known bull-market component in its headline, and its H2 is
weak (1.12058245). War Formation has **no** champion: 36 and 33 trades sit at the floor of what can
be quoted, and its 1m data is 4.5 months of a **single regime** that cannot support a split test.
