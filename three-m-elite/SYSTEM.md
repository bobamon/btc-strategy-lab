# 3M ELITE — system reading and build notes

Source: `3M SYSTEM CHECKLIST - 15SEC.pdf` and `- 30SEC.pdf` (both copied into this folder), plus
frames extracted from the ten screen recordings (see VIDEO EVIDENCE below). Audio is still not
readable — anything spoken and never shown on screen remains unavailable.

> Research specification for backtesting. Not a trade recommendation.

## The system's shape
The two checklists are the SAME system at two zoom levels, with consistent ratios:

| Variant | Entry | Structure | Zone | Bias | Top |
|---|---|---|---|---|---|
| 15sec | 15s | 4m (16x) | 15m (60x) | 1H & 2H | 6H |
| 30sec | 30s | 8m (16x) | 30m (60x) | 2H & 4H | 12H |
| **3m ELITE (derived)** | **3m** | **48m (16x)** | **3H (60x)** | **12H & 24H** | 3D |

The scaling is the authors' own, applied to a 3-minute entry. The top timeframe is optional in the
source ("check model ONLY if both bias timeframes are advanced"), so v1 omits it.

## The checklist, layer by layer
Gate order is strict — the source says do not progress until the previous layer passes.

**BIAS (12H & 24H)** · model/structural bias · max 6 breaks up/down
**ZONE (3H)** · model matches bias · max 6 breaks · supply/demand zone tap
**STRUCTURE (48m)** · model matches bias · max 6 breaks · zone tap · Type 1/Type 2 validation ·
swing rule not invalidated · not overextended from the 20MA (Keltner) · MAs not fully against bias ·
either 20MA or 50MA slope favours the trade
**ENTRY (3m)** · determine stage (most recent stage 1 / no stage) · not more than 4 breaks ·
20 & 50 MA not overextended from the 200 · MAs not fully against bias

## Risk rules (stated in the source)
- Move SL to break-even once price reaches **2RR**
- ATR take-profit method: full TP at **12x ATR**
- Max loss: 2 losses per session per instrument on 1min & 30sec; 3 on 15sec
- Trailing: move SL behind structural breaks only when the 50MA is beyond it; trail every **second**
  break, never the most recent

---

## WHAT I COULD DEFINE MECHANICALLY (implemented in v1)
| Term | Interpretation used | Confidence |
|---|---|---|
| Model / structural bias | Directional structure on the reconstructed TF: consecutive higher closes = bull, lower = bear | medium |
| Break | Close beyond the prior swing extreme on that TF (break of structure) | medium-high |
| 6 breaks max | Count of consecutive same-direction breaks; block entry above the cap (an overextension filter) | medium-high |
| Supply/demand zone tap | Price trades back into the prior completed candle's range on the zone TF — demand = prior low in bull, supply = prior high in bear | medium |
| Overextended from 20MA | Price outside a Keltner channel built on the 20MA — the 30SEC checklist names Keltner explicitly | high |
| MAs not fully against bias | 20/50/200 not all stacked opposite the bias | high |
| 20MA or 50MA slope favours trade | Either MA rising for longs, falling for shorts | high |

## VIDEO EVIDENCE (frames read 2026-09-02)
The videos are readable after all — not as video, but by extracting frames with OpenCV and reading
them as images. Method: `cv2.VideoCapture`, seek to a frame, resize to 1600x900, write JPEG, read it.
`imageio_ffmpeg` ships an ffmpeg binary and OpenCV 5.0 is installed, so no extra tooling is needed.

Confirmed from frames so far:
- **Author/brand: "SPENNYFX | 3M TRADING — PATIENCE | DISCIPLINE | EXECUTION".**
- Platform is **TradingView Replay** — these are replay-mode backtests, not live trades.
- Instruments seen: **NAS100, GBPUSD, BTCUSDT**. Watchlist also carries US30, SPX500, XAUUSD,
  XAGUSD, COPPER, NGAS, ETHUSD, SOLUSD. The system is **not BTC-specific**.
- Timeframe buttons in use: 30s · 1m · 8m · 15m · 30m · 1h · 2h · 4h · 8h · 12h · D — this matches
  the **30SEC checklist ladder** (8m structure, 30m zone, 2H/4H bias, 12H top).
- **Breaks are counted with numbered labels on the chart** — green numerals 1,2,3… for up-breaks and
  red numerals 1,2… for down-breaks, and **the count resets when direction flips.** That confirms the
  counter design used in v1 (`upCount` / `dnCount`, each resetting the other).
- **Supply/demand zones are drawn as rectangles** extending right from a base — grey and blue boxes.
- Three MAs on the chart plus **ATR displayed as a label** (e.g. "ATR: 18.82", "ATR: 0.00021"),
  consistent with the checklist's ATR take-profit method.
- One title card seen so far: **"One Candle Rule"** — a named rule not mentioned in either checklist.

### Still to extract from the videos
The three undefined terms below have not yet been located in the frames sampled. The 156-minute
video (`2026-08-09 04-42-54.mp4`) is by far the largest and is the most likely place they are taught.
A systematic pass over it is the top queue item.

## WHAT I COULD NOT DEFINE — these need the videos, or you
These are proprietary terms with no definition in the checklists. **v1 leaves them out**, and their
absence is the most likely reason a v1 result understates the real system.

1. **Type 1 / Type 2 Validation** — named as a required 48m gate. No definition anywhere in either PDF.
   Almost certainly the core entry-pattern classification.
2. **The swing rule** — "make sure swing rule has not invalidated". An invalidation condition on a
   swing point, but the condition itself is not stated.
3. **Stage (stage 1 / no stage)** — the entry-timeframe gate. "Look for most recent stage 1 / no
   stage" implies a numbered sequence of states, none of which are described.

**Until these three are supplied, 3M ELITE v1 is a partial implementation and should be read as a
lower bound on the system, not a verdict on it.**

## Data reality on this engine — read before interpreting any result
- **There is no 3m data.** The engine serves 1m, 5m, 15m, 1h, 4h only. 3m, 48m, 3H and 12H are all
  **reconstructed from 1m bars** by timestamp arithmetic, the same technique the War Formation uses.
  This is exact, not approximate: a 3m candle *is* 3 consecutive 1m bars.
- **1m coverage is only 2025-12-16 to 2026-05-03** (~4.6 months, 199,802 bars). With a four-layer
  cascade the trade count will be small, and a small sample over one market era is screening
  evidence, never validation.
- The engine forces `commission 0.05%`, `percent_of_equity 100`, `margin 100/100`. It tests the
  signal, not the position sizing.
- Sub-minute variants (15sec, 30sec) **cannot be tested here at all** — no data exists below 1m.

## Deviations from the source, and why
- **Fixed SL and TP at entry.** The source moves SL to BE at 2RR and trails behind structural breaks.
  The engine forbids the custom trailing pattern, and this project's rules require SL and TP fixed at
  open. v1 therefore uses a structural stop and the source's own **ATR take-profit method (12x ATR)**,
  which is fully specifiable. The BE-at-2RR and trailing variants are on the queue as later tests.
- **Max-loss-per-session rule not implemented** in v1 — it is a session-level risk control, not a
  signal, and it cannot change whether the signal has an edge.

## Open queue
0. ~~Get definitions for Type 1/Type 2~~ — **DONE 2026-09-02, see VOCABULARY.md.**
   Type 1 = a 3M candle; Type 2 = an engulfing candle in the direction of bias; both only on the
   STRUCTURE timeframe (48m for this variant), inside the tapped zone.
0a. ~~IMPLEMENT THE VALIDATION GATE~~ — **DONE 2026-09-02, REJECTED.** Built as `3m-elite-v2-validation.pine`:
    a zone tap arms a wait, a qualifying 48m engulfing candle (Type 2, computed independently for
    longs and shorts per HARD LESSON 6) validates it, a zone-bias flip clears it; entry requires the
    persistent `validLong`/`validShort` flag instead of v1's instant `demandTap`/`supplyTap` test.
    Result: PF 0.64 (v1: 0.91), maxDD 12.1% (v1: 3.47%), net -11.2%, 92 trades (v1: 20), WR 33.7%.
    Worse on both gates, so v1 stays the best-known config. Trade count rose ~4.6x — the persistent
    validated-state test turned out to pass MORE setups than v1's instant tap-and-go, not fewer, so
    this was not a pure filter on v1's trades. Both legs are now net losers (longs -$860.79/23 trades,
    shorts -$259.83/69 trades) versus v1 where longs alone carried the profit. avgBarsLosing/avgBarsWinning
    = 0.52, the HARD LESSON 5/6 diagnostic: losers still die roughly twice as fast as winners run,
    which points at the stop (unchanged 3H zone edge, not touched by this experiment), not the gate.
    Full record: `results/backtests.json` id `3m-elite-v2-type2-validation`.
0b. **IMPLEMENT ZONE INVALIDATION.** A candle BODY closing beyond the zone kills it, judged on the
    ZONE's own timeframe. Also: if the candle immediately after a validation body-closes beyond,
    the validation is void and a new one is required. Neither is in the current build.
0c. **IMPLEMENT THE PROTECTED LOW/HIGH (raised priority after 0a).** After validating, mark the
    structure-timeframe low (for longs) as the protected level and stop beneath it, replacing the
    3H-zone-edge stop both v1 and v2 use. 0a's result diagnostic (avgBarsLosing far below
    avgBarsWinning, the same defect HARD LESSONS 5 and 6 both flagged) points straight at this stop
    as the next thing to fix, ahead of 0b.
1. Port the cascade to a 15m base (scaling every layer up) to get 4.7 years of data instead of 4.6
   months. Loses 3m entry precision, buys a real sample.
2. Test the source's BE-at-2RR rule as a variant.
3. Test structural trailing (every second break, 50MA condition) as a variant.
4. Sensitivity on the break caps (6 / 4) and the Keltner width.
5. Rebuild the short leg separately once the long leg is sound — never mirror it.
