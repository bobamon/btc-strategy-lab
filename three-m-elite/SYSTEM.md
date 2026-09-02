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

## EXPERIMENT LOG
| # | Change | Result |
|---|---|---|
| v1 | Full cascade, no validation gate | PF 0.91, 20 trades, longs 6 of 8 · [report](https://mcp-api.trader.dev/backtest/01M1GGX4RQ707R9HHX2KFP471E) |
| v2 | + Type 2 validation gate (engulfing 48m in bias, `valLife` 3) | **0 TRADES** · [report](https://mcp-api.trader.dev/backtest/01M1GNBA7TRRHRYK61KXZADD4F) |
| v3 | Same cascade ported to a 15m base (4H/12H/2D), 4.7 years | PF 0.64, 94 trades, longs 10/35, shorts 5/59 · [report](https://mcp-api.trader.dev/backtest/01M1GNPDBWJD63TBCV11SYY30H) |
| v4 | 0a re-test: Type 2 gate (engulfing 4H in bias, `valLife` 3) on the **v3 15m base** | **0 TRADES** · [report](https://mcp-api.trader.dev/backtest/01M1GP6D1N4V36G2M6T7CR6BQ4) |
| v5 | Latched tap + zone invalidation + Type 2 gate (0a+0b merged) | **2 trades**, both losses, PF 0 -- latch fixed, but validation is still an instant · [report](https://mcp-api.trader.dev/backtest/01M1GQ0RFWSXSK5XM54A3DSXT0) |
| v6 | Latch BOTH the tap and the Type 2 validation; both die on a 12H body close beyond the zone | **PF 1.77, +3.10%, 10 trades** (longs 5/2W +$298, shorts 5/1W +$12), DD 2.49% -- first positive result, but 10 trades is not a sample · [report](https://mcp-api.trader.dev/backtest/01M1GQ7S426QJBAXE07YRFW2VW) |
| v7 | Remove the four LAB-INVENTED gates, keep only the source's rules | **Still exactly 10 trades** (5 long, 5 short). PF 1.32. My gates were never binding · [report](https://mcp-api.trader.dev/backtest/01M1GQE5ZSFMXKVQK5NTYAVY8F) |

**v3 lesson — v1's PF 0.91 was noise.** The same cascade measured on 4.7 years instead of 4.6 months
gives PF 0.64 across 94 trades. The larger sample is the trustworthy one. This is the sample-size fix
working as intended: it did not improve the strategy, it revealed that the earlier number was never
evidence. **v3 is now the reference base** even though its profit factor is lower.

Queue order corrected again: adding gates to a 20-trade base was always going to produce empty runs
(v2 did exactly that, as did War Formation v1). Widen the base first, then filter. Gates should now
be tested against v3.

**v2 lesson — the gate needs a lifetime, not a timer.** v1 made only 20 trades in 4.6 months.
Requiring an engulfing 48m candle within 3 structure candles of entry removed every one of them.
`valLife = 3` was an arbitrary stand-in for logic that does not exist yet: in the source, a
validation stays live **until the zone invalidates**, not for a fixed number of candles.

> "If the next candle right after this just is a body closed down here, then that immediately
> invalidates it. And then we just need a new triple M or a new engulfing candle."

So the queue order was wrong. **Zone invalidation (0b) must be built before the validation gate (0a)**,
because invalidation is what gives validation its lifetime. Reordered below.

This result is NOT on the dashboard: `build_dashboard.py` correctly rejects any record with zero
trades ("a run with no trades is not a backtest"). It is recorded here instead.


## v4 LESSON — THE SETUP AND THE TRIGGER MUST BE SEQUENTIAL, NOT SIMULTANEOUS
v2 gave 0 trades on the 1m base and I attributed it to a 20-trade sample. **v4 ran the same gate on
the v3 15m base — 163,826 bars, 4.7 years, a 94-trade parent — and still returned 0 trades.** That
kills the sample-size explanation. The conjunction is structurally near-impossible, and here is why:

- `demandTap` requires price to be **at the previous 12H candle's low** — the bottom of the range.
- A bullish **engulfing 4H candle is a strong up-move** by definition.
- `valLife = 3` gives them a shared window of only 12 hours.

So the rule asks price to sit at the bottom of the range *at the same time as* having just surged
off it. Those two states barely coexist, which is why the intersection is empty rather than merely
rare.

**This is the identical defect that produced War Formation v1's 0 trades** (volatility coil AND
velocity thrust demanded on the same bar). Twice now, so it is a pattern and is promoted to
STRATEGY-LEDGER.md as HARD LESSON 8.

**The source describes a sequence, and I coded a coincidence.** In his words the zone is tapped
*first*, and only *then* do you wait for the validating candle:

> "...that immediately invalidates it. And then we just need a new triple M or a new engulfing candle."

"Then we just need a new" is sequential language. The correct build **latches the tap** — a tap sets
a live flag that persists until the zone invalidates — and entry fires on the engulf that arrives
*afterwards*. That merges 0b-FIRST and 0a into one coherent mechanism, which is what v5 will be.

## v5 LESSON — THE SAME BUG, ONE LEVEL DOWN
The latch worked. v2 and v4 produced zero trades; v5 produced trades, so requiring the tap as a
persistent STATE rather than a same-bar coincidence was the right fix. But only 2 trades in 4.7
years, which is not a sample and not evidence about the strategy -- it is evidence about the code.

**The validation is still an instant.** `validBull` is true for exactly one bar every four hours,
the moment a new 4H candle opens behind an engulfing one. Every other gate -- bias, zone, structure,
slope, extension, break counts -- has to happen to be true on precisely that bar. That is HARD
LESSON 8 again, one level down: I latched the setup and left the trigger as a coincidence.

**In the source a validation is a STATE, not an event.** It persists until the zone invalidates:

> "If the next candle right after this just is a body closed down here, then that immediately
> invalidates it. And then we just need a new triple M or a new engulfing candle."

**v6: latch BOTH.** A tap arms the zone; an engulfing candle arms the validation; both persist until
a 12H body close kills the zone; entry fires on the first bar where both are live and the
trend/extension gates permit. Then, and only then, is the mechanism a fair test of the system.

## v6 — THE MECHANISM IS NOW CORRECT. THE FREQUENCY IS NOT.
Latching both states finished the repair: **0 trades (v2, v4) -> 2 (v5) -> 10 (v6)**, and for the
first time the lab is in profit, PF 1.77 on +3.10%, with both legs positive (longs +$297.97 on 5,
shorts +$12.05 on 5).

**This is not yet evidence, and the lab has already been burned by exactly this shape.** v1 showed
PF 0.91 on 20 trades; the same cascade measured properly gave PF 0.64 on 94. Ten trades across 4.7
years is thinner still. **v3 remains the reference base.** v6 is marked `testing`, not `passed`, and
must not be promoted on these numbers.

**The real finding is the frequency.** Ten entries in 4.7 years means the gate stack is far too
restrictive to test the system at all. The next cycle is a MEASUREMENT, not a change: find which gate
is binding. Note which of the current gates actually come from the source and which are mine --
`maSpreadOk`, the break counters, the MA slope test and the Keltner extension check are all lab
additions, not the author's rules. Those are the candidates to relax first, and relaxing an invented
gate to reach a testable sample is not curve-fitting; it is removing something that was never in the
system being tested.

## v7 — THE MEASUREMENT ANSWERED, AND I WAS WRONG ABOUT THE CAUSE
I expected removing the MA-spread test, the break counters, the slope test and the Keltner check to
raise the trade count. **It stayed at exactly 10, still 5 long and 5 short.** Those four gates were
never binding. The frequency ceiling is produced by the SOURCE-derived conjunction itself: 2D bias,
12H zone and 4H structure all having to rise together while a tap and a validation are both live.

PF fell 1.77 -> 1.32 on the same ten-trade sample, which is noise in both directions and is not a
reason to reinstate the invented gates. They should stay out on principle: they were never part of
the system under test.

**So the next question is a SPECIFICATION question, not a tuning one.** Two candidates, and the
video material should decide between them rather than a backtest:
1. Requiring bias, zone AND structure to all be rising may be my reading of "direction". The author
   may treat the higher timeframe as establishing bias only, with the zone providing location -- in
   which case demanding all three agree is a triple-counting of one idea.
2. The 12H zone defined as the previous candle's high/low may be far too narrow. A zone in the
   source is a region drawn from a range, not a single prior extreme.

Do not spend another credit on this until one of those is settled from the transcripts.

## Open queue
0. ~~Get definitions for Type 1/Type 2~~ — **DONE 2026-09-02, see VOCABULARY.md.**
   Type 1 = a 3M candle; Type 2 = an engulfing candle in the direction of bias; both only on the
   STRUCTURE timeframe (48m for this variant), inside the tapped zone.
0-V5. ~~LATCHED TAP + VALIDATION~~ — **DONE (v5). Latch works; 2 trades. See the v5 lesson.**
0-V6. ~~LATCH THE VALIDATION TOO~~ — **DONE. PF 1.77 on 10 trades. Mechanism correct, sample far too small.**
0-V7. ~~MEASURE WHICH GATE IS BINDING~~ — **DONE. My gates were NOT binding; the source conjunction is.**
0-V8-NEXT. **SETTLE THE SPECIFICATION FROM THE TRANSCRIPTS, NOT FROM A BACKTEST.** Decide (1) whether
    bias/zone/structure must all agree or whether the higher timeframe sets bias alone, and (2) whether
    a zone is a prior candle extreme or a region drawn from a range. Original v7 text: Count how often each condition blocks an
    otherwise-complete setup, then relax the LAB-INVENTED gates (maSpreadOk, break counters, slope,
    Keltner extension) -- never the source's own rules -- until the trade count is large enough to
    judge. Original v6 text: Both the tap and the Type 2 validation become
    persistent states that die with the zone. Entry on the first bar both are live. Original v5 text:
    A zone tap sets `tapLive := true`. It stays live until the zone invalidates (a BODY close beyond
    the zone on the zone's own timeframe). While it is live, the FIRST engulfing 4H candle in the
    direction of bias fires the entry. Never test tap and engulf on the same bar again — see the v4
    lesson and HARD LESSON 8. Measure the latch hit-count before adding any further filter.
0b-FIRST. **IMPLEMENT ZONE INVALIDATION BEFORE THE GATE (folded into v5 above).** A candle BODY closing
    beyond the zone kills the zone, judged on the ZONE's own timeframe (3H here). A body close
    immediately after a validation voids that validation. Once this exists, a Type 2 validation can
    persist until invalidated rather than expiring on an arbitrary counter — which is what killed v2.
0a. ~~THEN RE-TEST THE VALIDATION GATE~~ — **TESTED (v4) AS A SIMULTANEOUS CONDITION. 0 TRADES.**
    Re-test only in the latched form described in 0-V5-NEXT.
    (original wording) **Re-test the validation gate with a proper lifetime.** The current Pine has NO validation gate at all.
    Add: after a zone tap, require an engulfing candle in the direction of bias on the 48m
    reconstruction before an entry is allowed (that is Type 2, fully specifiable). Type 1 needs the
    3M candle anatomy, which is still unknown — implement Type 2 alone first and label it as such.
0b. **IMPLEMENT ZONE INVALIDATION.** A candle BODY closing beyond the zone kills it, judged on the
    ZONE's own timeframe. Also: if the candle immediately after a validation body-closes beyond,
    the validation is void and a new one is required. Neither is in the current build.
0c. **IMPLEMENT THE PROTECTED LOW/HIGH.** After validating, mark the structure-timeframe low (for
    longs) as the protected level and stop beneath it. The current build stops at the 3H zone edge
    instead, which is not what the source does.
1. Port the cascade to a 15m base (scaling every layer up) to get 4.7 years of data instead of 4.6
   months. Loses 3m entry precision, buys a real sample.
2. Test the source's BE-at-2RR rule as a variant.
3. Test structural trailing (every second break, 50MA condition) as a variant.
4. Sensitivity on the break caps (6 / 4) and the Keltner width.
5. Rebuild the short leg separately once the long leg is sound — never mirror it.
