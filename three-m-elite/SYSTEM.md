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

## ⚠️ v8 — THE SPECIFICATION IS SETTLED, AND THE MODEL WAS INVERTED
The v7 queue item said to settle the specification from the transcripts rather than buy another
backtest. **Done, and the answer is decisive: an engulfing candle CREATES a zone; it does not
validate one.** Full quotes and the corrected model are in VOCABULARY.md.

This explains the entire failure history of this lab in one stroke:

| Build | Trades | Cause, understood now |
|---|---|---|
| v2, v4 | 0 | engulf and 12H tap required on the same bar -- two unrelated events |
| v5 | 2 | tap latched, but engulf still had to coincide with everything else |
| v6, v7 | 10 | both latched, but the zone was still the wrong object entirely |
| v9 | THE CORRECTED MODEL: engulfing 4H candle CREATES the zone; One Candle Rule mitigation | **3 trades** (2 long, 1 short). Model right, single-slot approximation wrong · [report](https://mcp-api.trader.dev/backtest/01M1GR0M5GXEY4BAP7P9R13SZS) |
| v10 | Keep the DEEPEST unmitigated zone instead of the most recent | **IDENTICAL TO v9** in every figure. The selection rule never fires -- zones die before the next engulf arrives · [report](https://mcp-api.trader.dev/backtest/01M1GRCBFT1PRT556PPKAJ1Q1X) |
| v11 | Zone = the BASE ([low, open] demand / [open, high] supply), not the whole candle | **Still 3 trades** (1 long, 2 short). Real change, wrong constraint · [report](https://mcp-api.trader.dev/backtest/01M1GRHZGJY679F1V9P4P5NPZD) |

**The scarcity was never the system. It was my definition of a zone.** A zone defined as the previous
12H candle's extreme is one level per 12 hours that price rarely revisits under all the other
conditions. A zone defined as *every engulfing candle's range* is a continuously replenished
population of levels, each with a mitigated/unmitigated state.

**No backtest this cycle** -- v7's queue entry explicitly said not to spend a credit until this was
settled, and the right move now is to rebuild on the corrected model rather than tune the wrong one.

## v9 — THE MODEL IS RIGHT, THE SLOT LIMIT IS WRONG (and it was flagged before running)
3 trades, down from v6's 10. The cause is exactly the deviation declared in the Pine header: arrays
are forbidden, so **one zone per side is tracked and every new engulfing candle overwrites the
previous one.** In a trending market engulfing candles arrive every few 4H bars, so a zone is almost
never still alive when price finally returns to it.

The source presupposes several zones being tracked at once -- that is what **"deepest unmitigated
zone"** means. Tracking the most RECENT zone is the opposite of tracking the deepest.

**v10 is a one-line fix that follows the source directly:** replace the tracked zone only when the new
one is DEEPER -- a lower bottom for demand, a higher top for supply -- or when the current one is
already dead. That keeps a zone alive across the many shallower engulfs that currently destroy it.

Do not read PF 0.64 on 3 trades as information about the model. It is information about the slot.

## v10 — AN IDENTICAL RESULT IS A DIAGNOSIS, AND IT POINTS AT THE ZONE GEOMETRY
PF 0.64013804, 3 trades, same net, same everything as v9. **If overwriting had been the cause of v9's
scarcity, requiring the replacement zone to be deeper would have changed something.** It changed
nothing — which proves the guard clause never fires. By the time the next engulfing candle arrives,
the tracked zone is already dead, so `not dzLive` is true and the replacement happens exactly as before.

**The real defect is the zone geometry, and it was mine, not the source's.**

I defined a demand zone as the engulfing candle's whole range, low to high. That makes the zone TOP
equal to the impulse HIGH — so price is sitting inside its own zone the instant the candle closes.
The mitigation counter then trips within two candles, every time, and no zone ever survives long
enough to be returned to.

**In supply and demand a zone is the BASE the impulse left behind, not the impulse itself.** For a
demand zone that is the region from the candle's low up to its OPEN (the body's lower edge) — the
small area price accelerated away from — not the full extent of the move.

**v11: fix the geometry first.** Demand zone = [low, open] of the engulfing candle; supply zone =
[open, high]. Only once a zone can survive its own creation does any selection rule, mitigation count
or validation gate mean anything. The last three cycles have all been downstream of this one error.

## v11 — THREE STRUCTURAL FIXES, THREE TIMES THE SAME ANSWER. STOP GUESSING.
The geometry fix was real: the trade composition changed from 2 long / 1 short to 1 long / 2 short,
so the code genuinely behaves differently. **But the count stayed at 3.**

| Build | Fix applied | Trades |
|---|---|---|
| v9 | latched tap, engulf creates the zone | 3 |
| v10 | keep the deepest zone, not the most recent | 3 |
| v11 | zone is the base, not the whole candle | 3 |
| v12 | DIAGNOSTIC: entry stripped to "zone live and price inside it", 1-bar exits, to COUNT opportunities | **15 opportunities in 4.7 years** (6 long, 9 short). Ignore the P&L -- it is an instrument · [report](https://mcp-api.trader.dev/backtest/01M1GTWJTF7K07205ZD8P4EM5Y) |
| v13 | Mitigation judged on the BODY (a 4H close inside the zone) instead of a wick, counter form | **Opportunities 15 -> 40** (13 long, 27 short). The fix works · [report](https://mcp-api.trader.dev/backtest/01M1GV4JAZ169SE54YC2AZAVVT) |
| v14 | Repaired lifecycle, NO filters, REAL fixed exits -- does the zone population have an edge? | **PF 0.29, win rate 4.17%, 24 trades** (5 long 0W, 19 short 1W). The TAKE PROFIT IS UNREACHABLE -- no trade ever hit it · [report](https://mcp-api.trader.dev/backtest/01M1GVG1713A1BXSDAF6551N29) |
| v15 | Unreachable ATR target replaced with a fixed 2R, still no filters | **PF 0.363, win rate 8.33%, 24 trades** (5 long 1W, 19 short 1W). Target fix confirmed; entries are worse than chance · [report](https://mcp-api.trader.dev/backtest/01M1GVV0F20WJY72GZSQWM2VJX) |
| v16 | Type 2 validation restored, latched setup + later trigger | **0 TRADES.** Sequencing was correct; the four-way conjunction at firing is what kills it · [report](https://mcp-api.trader.dev/backtest/01M1GW1PWQ2YY4ZX0AFCMBCCYM) |
| v17 | Counter build for the validation gate, 2D bias DROPPED | **0 TRADES.** The bias was not the binding term -- arming and mitigation race, and mitigation wins · [report](https://mcp-api.trader.dev/backtest/01M1GW9BZV25S3MC76DK784RBE) |

**When three independent corrections land on the same trade count, the binding constraint is upstream
of all of them.** I have now spent three cycles fixing things that were genuinely wrong and none of
them was the thing limiting the strategy.

**v12 MUST BE A DIAGNOSTIC, NOT A FIX.** Strip the entry to the single condition *a zone is live and
price is inside it* — no 2D bias, no direction, no candle-colour requirement — purely to count how
many opportunities exist at all. If that returns a handful, the zone lifecycle is still broken. If it
returns hundreds, the bias and direction gates are doing the killing and the lifecycle was fine.

**The general error is worth naming: I have been filtering a population without ever measuring its
size.** That is what produced v9, v10 and v11.

## v12 — THE MEASUREMENT IS IN, AND THE FILTERS WERE NEVER THE PROBLEM
**15 opportunities in 4.7 years.** With every gate removed — no bias, no direction, no candle colour —
price enters a live zone only fifteen times. With all gates on it was 3.

So the bias and direction conditions do cut 15 down to 3, but **15 was never enough to begin with.**
The zone lifecycle is the binding constraint, which is exactly what this diagnostic was built to
determine, and it settles three cycles of guessing.

**Prime suspect, and it is specific: the mitigation test counts WICKS.**
`dzTouch` increments whenever a completed 4H candle's LOW dips below the zone top. A single wick
therefore counts as a touch, and two wicks kill the zone — typically within eight hours of creation.
Almost no zone survives long enough for price to return to it.

**The source does not work that way.** Invalidation is judged on the BODY (a candle closing beyond the
zone), and the One Candle Rule is about candles closing back INTO it:

> "this one candle does not mitigate the zone yet ... the second one is what makes the zone mitigated"

A candle that merely wicks through is not a candle that has mitigated anything.

**v13: require a BODY inside the zone to count as mitigation** — for demand, `close <= dzTop`, not
`low <= dzTop`. Re-run the v12 counter afterwards to confirm the opportunity population actually grew
before putting any filter back on.

## v13 — THE LIFECYCLE IS REPAIRED. OPPORTUNITIES 15 -> 40.
Judging mitigation on the BODY instead of the wick nearly tripled the opportunity population over the
same 4.7 years: **15 -> 40**, 13 long and 27 short. The diagnosis from v12 was correct — zones were
being killed by candles that dipped a wick into them without ever closing inside, which the source
never treats as mitigation.

**This is now the settled rule:** a zone is mitigated when a completed candle on the zone's timeframe
CLOSES inside it, and the One Candle Rule applies to those closes — the first does not mitigate, the
second does. Recorded in VOCABULARY.md.

**Do not read v13's profit factor.** Exits are forced after one bar; it is a counter, and its P&L is
an artefact of the instrument exactly as in v12.

**v14: restore the filters ONE AT A TIME, measuring what each costs.** v9/v10/v11 cut 15 down to 3 by
switching bias, direction and colour on together, and that ratio applied to 40 would leave about 8 —
still too few. Turning them on one at a time is the only way to learn which one is expensive. The
order should be cheapest-information-first: 4H structure, then 12H zone direction, then 2D bias, then
the candle-colour condition.

## v14 — THE TAKE PROFIT HAS BEEN UNREACHABLE SINCE v1
The run asked whether the repaired zone population is profitable before any filter. **It could not
answer, because the exit is broken — and the trade distribution says so unambiguously.**

| | Value | What it means |
|---|---|---|
| Win rate | 4.17% (1W / 23L) | Almost nothing resolves in profit |
| avgWin / avgLoss | 306.97 / 45.99 = 6.67 | The single win was enormous |
| avgBarsWinning | **96** | Exactly `maxBars` — it exited at the TIME CAP |
| avgBarsLosing | 18.5 | Losers hit the stop quickly |

**The one winner never reached the target either — it timed out.** So in 4.7 years, across every
build, **no trade has ever hit the take profit.** `tpATR = 12 x ATR14` on 15m is an unreachable
distance, and it has been carried unexamined since v1. The system has been structurally
stop-or-timeout the entire time, with the reward leg never paying.

**Do NOT read this as "the zones are unpredictive."** That question remains open and this run could
not address it. What has been established is that the *exit* has been silently broken beneath every
result this lab has produced, including v3's PF 0.64 reference base.

**This is the same error class as the zone-geometry bug: a parameter carried from v1 that was never
examined because attention was always on the layer above it.** The lab has now found three of these —
the inverted zone model, the wick-based mitigation, and now the unreachable target.

**v15: replace the ATR target with a fixed multiple of R (2R, as both other labs use) and re-ask the
v14 question.** Only then do filters go back on, one at a time.

Note also the leg split: 5 long against 19 short. Once the exit is fixed, that skew needs explaining —
the zone logic is meant to be symmetric.

## v15 — THE TARGET FIX IS CONFIRMED, AND THE ENTRIES ARE WORSE THAN CHANCE

| | v14 (12 x ATR14) | v15 (2R) |
|---|---|---|
| Profit factor | 0.290 | 0.363 |
| Win rate | 4.17% | 8.33% |
| avgBarsWinning | 96 (= maxBars) | 43.5 |

v14's diagnosis holds: the target really was unreachable, and with a 2R target trades now resolve at
the target rather than only at the time cap.

**But the comparison that matters is against chance.** A coin flip with a 2R target and a 1R stop
wins about **33%** of the time. These entries win **8.33%** — a quarter of that. They are not merely
unpredictive; they are **systematically badly timed**. Price is far more likely to continue through a
zone than to reverse off it.

**The right reading is NOT that the system fails.** It is that **entering on the first touch of a zone
is premature, and the source never says to do that.** It requires a VALIDATION inside the zone — a 3M
candle (Type 1) or an engulfing candle (Type 2) — before an entry is allowed. This diagnostic
deliberately removed that step to measure the raw population.

**Being worse than chance without the validation is evidence that the validation is LOAD-BEARING, not
optional.** That is a genuinely useful result: it tells us which part of the system carries the work.

**v16: restore the Type 2 validation on the corrected lifecycle** — an engulfing candle in the
direction of bias occurring INSIDE a live zone, latched per HARD LESSON 8, with the 2R target. That is
the first build in this lab where the lifecycle, the geometry, the mitigation rule and the exit are
all correct at the same time.

## v16 — ZERO TRADES, BUT NOT THE OLD BUG. AND A METHOD FAILURE WORTH MORE THAN THE RUN.
This is not v2/v4/v5 repeating. **The sequencing was right this time:** price entering a live zone
arms it as a latched setup, and the engulfing candle fires on a later bar. HARD LESSON 8 was obeyed.

What kills it is the **four-way conjunction at the moment of firing** — the zone must still be live,
still armed, the 2D bias must agree, and a bullish engulf must land on that exact 4H boundary. Each
condition is individually reasonable; together they never co-occur in 4.7 years.

### The method failure matters more than the result
I designed this run around plotting the gate counters, which HARD LESSON 8's corollary explicitly
recommends. **But `quick_backtest` does not return plot values — only trade statistics.** Those plots
were invisible, so the corollary was unusable, and I had been writing it into run after run without
noticing it could never pay off. It was carried over from TradingView habits rather than derived from
this API's actual output.

**The ledger corollary is now corrected.** The technique that genuinely works is the **counter build**
already proven in v12 and v13: make the gate itself the entry condition and force a one-bar exit, so
`totalTrades` IS the hit count and the long/short split comes free.

**This result is not on the dashboard.** `build_dashboard.py` rejected it — "a run with no trades is
not a backtest" — which is the provenance gate working exactly as intended.

**v17: count the armed-plus-engulf occurrences with a counter build before attempting any entry
logic.** If the count is near zero, the 2D bias is the binding term and should be dropped or widened;
if it is healthy, the fault is in the entry plumbing.

## v17 — THE COUNTER BUILD WORKED, AND IT FOUND A STRUCTURAL CONFLICT
Dropping the 2D bias changed nothing: still zero. **So the bias was never the binding term**, and the
counter technique earned its credit by ruling that out cleanly instead of leaving it to guesswork.

**The real conflict: ARMING AND MITIGATION ARE DRIVEN BY THE SAME PRICE ACTION.**

- A zone **arms** when price enters it.
- A zone is **mitigated** when a 4H candle CLOSES inside it — and the One Candle Rule kills it on the
  second such close.
- The mitigation check runs at each 4H boundary **before** the fire check.

So the very act of entering a zone begins killing it, and the zone dies within two 4H candles of
arming — before any later engulfing candle can fire the entry. The two states can essentially never
coexist.

**This is HARD LESSON 8 in a new disguise.** Not setup-and-trigger required on the same bar, but a
**setup and a death condition driven by the same event.** The lesson should be generalised: whenever a
latch is introduced, check what ELSE that same price action triggers.

**v18: the arming candle must not count toward mitigation.** The candle that first brings price into
the zone is the setup, not a mitigation of it; only closes inside on SUBSEQUENT candles should count.
That is also closer to the source, which treats mitigation as what happens when price comes back
*again*, not when it first arrives.

**Not on the dashboard** — a zero-trade run is not a backtest, and `build_dashboard.py` refuses it.

## Open queue
0. ~~Get definitions for Type 1/Type 2~~ — **DONE 2026-09-02, see VOCABULARY.md.**
   Type 1 = a 3M candle; Type 2 = an engulfing candle in the direction of bias; both only on the
   STRUCTURE timeframe (48m for this variant), inside the tapped zone.
0-V5. ~~LATCHED TAP + VALIDATION~~ — **DONE (v5). Latch works; 2 trades. See the v5 lesson.**
0-V6. ~~LATCH THE VALIDATION TOO~~ — **DONE. PF 1.77 on 10 trades. Mechanism correct, sample far too small.**
0-V7. ~~MEASURE WHICH GATE IS BINDING~~ — **DONE. My gates were NOT binding; the source conjunction is.**
0-V8. ~~SETTLE THE SPECIFICATION~~ — **DONE 2026-09-02. The engulfing candle CREATES the zone.**
0-V9. ~~REBUILD ON THE CORRECTED MODEL~~ — **DONE. Model correct, 3 trades, single-slot is the limit.**
0-V10. ~~KEEP THE DEEPEST ZONE~~ — **DONE. Identical to v9; the rule never fires. See the v10 lesson.**
0-V11. ~~FIX THE ZONE GEOMETRY~~ — **DONE. Real change, still 3 trades. Not the binding constraint.**
0-V12. ~~DIAGNOSTIC RUN~~ — **DONE. 15 opportunities in 4.7 years. The zone lifecycle is the constraint.**
0-V13. ~~MITIGATION ON THE BODY~~ — **DONE. Opportunities 15 -> 40. Settled rule.**
0-V14. ~~UNFILTERED EDGE TEST~~ — **RUN, BUT INCONCLUSIVE: the take profit is unreachable. See the v14 lesson.**
0-V15. ~~FIX THE TAKE PROFIT~~ — **DONE. Confirmed broken and fixed; entries are worse than chance without validation.**
0-V16. ~~RESTORE THE TYPE 2 VALIDATION~~ — **0 trades. Sequencing correct; the firing conjunction is too narrow.**
0-V17. ~~COUNTER-BUILD THE VALIDATION GATE~~ — **DONE. Bias exonerated; arming and mitigation conflict.**
0-V18-NEXT. **THE ARMING CANDLE MUST NOT COUNT TOWARD MITIGATION (top priority).** Only closes inside
    the zone on candles AFTER the one that first brought price into it should increment the touch
    counter. Re-run the v17 counter to confirm the gate can now fire. Superseded text: Entry = armed zone AND engulf, with
    a one-bar exit, so totalTrades is the hit count. Then relax the narrowest term. Do NOT rely on
    plot() -- this engine does not return plot values. Superseded text: An engulfing candle in the direction of
    bias, occurring INSIDE a live zone, latched in sequence with the zone tap. With the 2R target and
    the corrected lifecycle this is the first build where every layer is right at once. Superseded text: Replace
    `tpATR = 12 x ATR14` with a fixed 2R target, then re-run the unfiltered edge test. No filter goes
    back on until the exit can actually pay. Superseded text: Measure the
    cost of each gate separately -- 4H structure, then 12H zone direction, then 2D bias, then candle
    colour -- instead of switching them all on together. Superseded text: Change dzTouch /
    szTouch to increment on a CLOSE inside the zone rather than a low/high touching it. Then re-run
    the v12 counter to verify the population grew before restoring any filter. Superseded text: Entry = zone live AND price inside it.
    Nothing else. Count the opportunities before filtering them. Superseded text: A demand zone is the
    BASE beneath the impulse -- [low, open] of the engulfing candle -- not its whole range. Supply is
    [open, high]. With the top set at the impulse high, price is inside the zone at creation and the
    mitigation counter trips immediately, which is why v9 and v10 both made 3 trades. Superseded text: One-line change: a new
    engulf replaces the tracked zone only if it is deeper (lower bottom for demand, higher top for
    supply) or the tracked zone is dead. This is what "deepest unmitigated zone" means and it should
    restore frequency without adding anything the source does not contain. Superseded v9 text:
    (a) Detect engulfing candles on the structure timeframe; each one creates a zone spanning that
        candle plus one extra candle. Non-engulfing candles create nothing.
    (b) Track each zone as unmitigated until mitigated, applying the ONE CANDLE RULE: the first
        candle back into the zone does not mitigate it, the second does.
    (c) Target the DEEPEST UNMITIGATED zone.
    (d) Validation (Type 1 3M candle, or Type 2 engulfing) is a separate event occurring INSIDE a
        live zone -- not the thing that creates it.
    Pine has no arrays, so zones must be held in a fixed set of `var float` slots; start with the
    single deepest unmitigated zone per side, which is what the source says to trade anyway.
    Superseded original text: Decide (1) whether
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
