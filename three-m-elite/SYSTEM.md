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
| v18 | Arming candle exempted from mitigation | **0 TRADES.** Third consecutive zero on this gate · [report](https://mcp-api.trader.dev/backtest/01M1GWQMNTR2YC3YY3YFBWDM42) |
| v19 | Count 4H engulfing candles alone | **TEN in 4.7 years** (5 bull, 5 bear) out of ~9,800 candles. The engulf definition assumes GAPS · [report](https://mcp-api.trader.dev/backtest/01M1GX4DEVQGF6R39CE7FJWRC9) |
| v20 | The SAME counter with the gap clause removed — body containment only | **2,711 ENGULFS** (1,325 bull, 1,386 bear). 271x the old count, ~28% of all 4H candles · [report](https://mcp-api.trader.dev/backtest/01M1GXHFTDY20ZA3GP2HBDW7J6) |
| v21 | v15's source with the corrected engulf — the lifecycle's first real population | **PF 1.0239, DD 10.58%, 185 trades** (56 long 21W +$652 / 129 short 25W -$423). Best on record; 11-month trade gap disclosed · [report](https://mcp-api.trader.dev/backtest/01M1GXYHSEMAS3J7ABRE3V169G) |
| v22 | Count ZONE CREATION — the engulf AND the deepest-zone condition | **71 creations from 2,711 engulfs** (29 demand, 42 supply). Last creation 2025-10-07. The rule discards 97.4% then locks up · [report](https://mcp-api.trader.dev/backtest/01M1GYGFHTD06PZWQS0FQF8JQG) |
| v23 | Most-recent zone replaces deepest zone | **PF 0.7363, DD 89.27%, 1,792 trades** (749 long 275W / 1,043 short 184W), spanning the full window. The lock-up is fixed and the edge went with it · [report](https://mcp-api.trader.dev/backtest/01M1GYTGY7YZSNAP6QNCAMFP4A) |
| v24 | Long leg alone | **PF 0.8945, DD 42.50%, 833 trades**, win rate 36.61%, payoff 1.548. Best honest number this lab has produced, still under 1.0 · [report](https://mcp-api.trader.dev/backtest/01M1GZ8DM3Q20JQDX3AKSP1XQV) |
| v25 | Time stop 96 -> 192 bars (first exit test) | **REVERTED.** PF 0.8945->0.8578, DD 42.50%->53.38%, trades 833->797. The cap was cutting LOSERS, not winners · [report](https://mcp-api.trader.dev/backtest/01M1GZGBXAJB8SVFHF3Y41XVGN) |
| v26 | Time stop 96 -> 48 bars | **REVERTED.** PF 0.8945->0.8204, DD 42.50%->58.85%, trades 833->915. Win rate rose to 40.33% but payoff fell to 1.214 · [report](https://mcp-api.trader.dev/backtest/01M1GZPAKD9H3HC2R8BA4BNPX8) |
| v27 | Target 2R -> 2.5R | **REVERTED.** PF 0.8945->0.8804, DD 42.50%->45.88%, trades 833->803. Payoff +12.3%, win rate -3.0pp -- the iso-PF trade again · [report](https://mcp-api.trader.dev/backtest/01M1H00SH71Q3T0K3EBPF04E9S) |
| v28a | Walk-forward, FIRST half 2022-01 to 2024-05 | **PF 0.9220, DD 27.59%, 410 trades**, win 36.59% -- against the full sample's 0.8945 and 36.61%. Halves look consistent; H2 pending · [report](https://mcp-api.trader.dev/backtest/01M1H0CFPW1HKNYQT9HYDEDAD4) |
| v28b | Walk-forward, SECOND half 2024-05 to 2026-09 | **PF 0.8612, DD 36.26%, 423 trades**, win 36.64%. THE HALVES AGREE -- spread 0.061, win rates within 0.05pp · [report](https://mcp-api.trader.dev/backtest/01M1H0HYT2RJTJTEPVMMY6CTET) |

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

## v18 — THIRD ZERO IN A ROW, AND I SKIPPED THE MORE BASIC QUESTION THREE TIMES
v16, v17 and v18 have all returned zero trades on the validation gate. Each fixed a real defect —
sequencing, then the bias term, then the arming/mitigation conflict — and none of them changed the
outcome.

**The mistake is one this lab already named and then repeated.** Every one of those runs counted
`armed AND engulf`. **Not one of them counted `armed` on its own.** I have been measuring a
conjunction three times without ever confirming that its first term occurs at all — which is exactly
the "filtering a population without measuring its size" error that v12 was created to fix.

**v19: count ARMING EVENTS ALONE.** Entry = a zone is live and price has just entered it, one-bar
exit, nothing else. If arming is frequent, the fault is the engulf term or its timing. If arming is
rare or absent, the zone geometry still does not permit re-entry and everything downstream is moot.

Three credits have gone to this gate on the strength of an unverified assumption. That is the cost of
skipping the cheapest measurement.

**Not on the dashboard** — zero-trade runs are refused by the provenance gate.

## ██ v19 — THE ANSWER. THE ENGULF DEFINITION ASSUMES GAPS, AND CRYPTO HAS NONE.
**Ten engulfing candles in 4.7 years.** Five bullish, five bearish, out of roughly 9,800 four-hour
candles — 0.1%. Every zero-trade run from v16 onward is explained: the conjunction could never fire
because one of its terms essentially never occurs.

**The definition carried since v9:**
```
bullEng = close > prevOpen AND open < prevClose
```
**In a 24/7 market the open of one aggregated candle equals the close of the previous one almost
exactly.** So `open < prevClose` is decided by tick noise, not by structure, and is effectively never
true. That condition comes from equities, where overnight gaps make it meaningful. It was imported
without being questioned and has silently disabled the validation gate in every build that used it.

**v20 — the fix, and it is a definition change, not a tuning change:**
```
bullEng = prev candle bearish AND this candle bullish AND close > prevOpen
```
Body containment, no gap requirement. Then re-run the v19 counter to confirm the population is
sensible before restoring the gate.

### This is the FOURTH error carried from v1
| # | Error | Found in |
|---|---|---|
| 1 | The engulfing candle CREATES the zone, it does not validate one | v9 |
| 2 | Mitigation judged on the wick instead of the body | v13 |
| 3 | The take profit was unreachable at 12 x ATR14 | v14 |
| 4 | **The engulf definition requires a gap that cannot occur** | **v19** |

Every one was a parameter or definition inherited early and never examined, while attention stayed on
the layer above. **The pattern is now unmistakable and worth stating: in this lab, the failures have
never been in the thing being tested — they have been in the assumptions underneath it.**

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
0-V18. ~~ARMING CANDLE EXEMPT FROM MITIGATION~~ — **0 trades. Third consecutive zero. See the v18 lesson.**
0-V19. ~~COUNT THE MISSING TERM~~ — **DONE, and it was the ENGULF, not arming. Ten in 4.7 years.**
0-V20. ~~REDEFINE THE ENGULF WITHOUT A GAP REQUIREMENT~~ — **DONE. 10 became 2,711.** The clause was
    the whole problem. The population is real and balanced; the validation gate can now be tested.
0-V21. ~~CORRECT THE ENGULF IN THE LIFECYCLE ITSELF~~ — **DONE. PF 0.363 -> 1.024 on 185 trades.**
    v15 still carried the gap clause, so zone CREATION was the binding step, upstream of the gate.
0-V22. ~~EXPLAIN THE ELEVEN-MONTH TRADE GAP~~ — **DONE. CONFIRMED, and worse than predicted.**
    71 zone creations from 2,711 engulfs; last creation 2025-10-07. It is a lock-up, not a market.
0-V23. ~~REPLACE THE DEEPEST-ZONE RULE WITH MOST-RECENT~~ — **DONE. The lock-up is fixed; PF 1.024
    -> 0.736 on 1,792 trades. v21's edge WAS the lock-up.** v23 is the new reference base.
0-V24. ~~ISOLATE THE LONG LEG~~ — **DONE. PF 0.7363 combined -> 0.8945 long-only on 833 trades.**
    The short side is not underperforming; it is the entire deficit.
0-V25. ~~THE EXIT: WIDEN THE TIME STOP~~ — **REVERTED. PF 0.8945 -> 0.8578, DD 42.50% -> 53.38%.**
    The cap was cutting losers loose, not truncating winners. v24 stands.
0-V26. ~~TIGHTEN the time stop: 96 -> 48~~ — **REVERTED. PF 0.8945 -> 0.8204, DD 42.50% -> 58.85%.**
    Both directions on the time axis are worse, so 96 is an interior optimum and THE AXIS IS CLOSED.
0-V27. ~~THE TARGET: 2R -> 2.5R~~ — **REVERTED. PF 0.8945 -> 0.8804, DD 42.50% -> 45.88%.**
    THE EXIT AXIS IS FULLY CLOSED: time stop up, time stop down and target further are all worse.
0-V28a. ~~WALK-FORWARD, FIRST HALF~~ — **DONE. PF 0.92199683 on 410 trades, win rate 36.59%.**
    Encouraging but NOT a conclusion: one half cannot settle stability.
0-V28b. ~~WALK-FORWARD, SECOND HALF~~ — **DONE. PF 0.86121615 on 423 trades at 36.64% win.**
    THE HALVES AGREE. v24's 0.894 is a real, stable number and every v25-v27 conclusion stands.
0-V29. ~~THE ENTRY: BINDING TEST ON A SIGNAL TERM~~ — **DONE. Removing the zone TOUCH raised PF
    0.89445064 -> 0.97210749 on 833 -> 1,076 trades, but drawdown went 42.50% -> 61.45%. REVERTED on
    the ratchet. The touch is NOT what carries this system.**
0-V30-NEXT. **RECOVER v29's PROFIT FACTOR WITHOUT ITS DRAWDOWN (top priority).** v29 is the closest
    this lab has come to 1.0 and it failed on one term only. The drawdown came from 243 extra trades
    compounding at percent_of_equity 100, not from worse trades -- the win rate ROSE. Test v29 with
    the entry re-narrowed by a DIFFERENT term than the touch, so frequency comes down without
    reinstating the condition that was not working. First candidate: require the zone to be fresh
    (dzAge <= some bound), which is a recency condition rather than a location one.
0-V31. **Then the remaining signal terms**: close > dzBot, and dzAge >= 1 itself.
    Superseded text: THE ENTRY -- and take the BTC lab's Attack 15 lesson. That lab spent
    fifteen cycles attacking FILTERS and found its only improvement by removing a term from the
    SIGNAL ITSELF -- the one the strategy was named for, which turned out to be costing money. This
    lab has never applied the binding test to its own signal terms either. The v24 entry is a
    conjunction: dzLive, dzAge >= 1, dzTouch < 2, low <= dzTop, close > dzBot. Remove ONE and read
    the trade count. Start with `dzTouch < 2`, the One Candle Rule mitigation cap, because it is the
    term inherited most directly from the source material and never independently measured.
    Superseded text: WALK-FORWARD, SECOND HALF 2024-05-01 to 2026-09-01. Same byte-identical
    v24 source, only the window changes. This is the run that decides whether 0.894 is a real property
    or a blend. Do not draw the conclusion from H1 plus arithmetic -- HARD LESSON 11 says measure the
    term, do not estimate it, and an implied H2 is an estimate.
0-V29. **THEN the entry, and only then.** If the halves agree, the 2.6-point win-rate deficit is
    stable and worth attacking with entry selectivity chosen from trade-count evidence. If they
    diverge, the v24-v27 exit conclusions need re-scoping the way BTC's gate verdicts did.
    Superseded text: WALK-FORWARD SPLIT OF v24. PF 0.894 has never been split across time,
    and the BTC base looked like 1.02 until it decomposed into 1.36 early and 0.66 late. Two runs on
    the same source, halves of 2022-01-01 -> 2026-09-01, nothing else changed. If the halves agree,
    0.894 is a real number about the mechanism. If they diverge, this lab has been optimising an
    average of two different systems and the entry work has to be re-scoped.
0-V29. **ONLY AFTER v28: the entry.** Every exit parameter is exhausted and the long leg is 2.6
    points of win rate short. If the halves agree, the remaining lever is entry selectivity -- but
    pick the term from the trade-count evidence, not from another rule import.
    Superseded text: THE TARGET: 2R -> 2.5R. The last untouched
    exit parameter. Stated in advance: the BTC lab found 2R and 3R sit on the SAME iso-profit-factor
    curve, and War Formation's E26 found a nearer target actively hurt. If 2.5R also lands within
    noise of 0.894, the exit is exhausted and the lab should say so rather than keep poking it.
0-V28. **IF the exit is exhausted, the honest next move is a WALK-FORWARD split of v24** -- does
    PF 0.894 hold across 2022-2024 and 2024-2026 separately, or is it another mixed-sample average
    like the BTC base turned out to be? That question matters more than another parameter.
    Superseded text: TIGHTEN the time stop instead: 96 -> 48 bars. v25 established the
    direction of the gradient -- more time is worse -- so the untested question is whether less time
    is better. avgBarsLosing is 27.26 against avgBarsWinning 48.83, so a 48-bar cap cuts most losers
    while leaving the average winner room. Single variable, same base.
0-V27. **THEN the target**, 2R -> 2.5R, and only if v26 settles the time axis. Superseded text: THE EXIT, not the entry. The long leg wins 36.61% with a payoff of
    1.548, which needs ~39.2% to break even -- it is 2.6 percentage points short, and every cycle so
    far has attacked entries. Test ONE exit change against v24: the 2R target moved to 2.5R, or the
    96-bar time stop, chosen and run as a single variable. This is the untouched half of the system.
0-V26. **THE TYPE 2 GATE IS DEFERRED, NOT FORGOTTEN, AND HERE IS WHY.** It requires "an engulfing
    candle in the direction of BIAS", and VOCABULARY.md records that this bias is the
    model/structural bias computed by a closed-source TradingView indicator we do not have. Building
    it means inventing a definition and then testing MY invention while calling it SPENNYFX -- the
    E25 error exactly. It can only be run if the bias is first given a definition the user confirms.
    Superseded text: RESTORE THE TYPE 2 VALIDATION GATE, now on a working lifecycle. For
    the first time the gate can be tested against a strategy that is neither starved (v16-v18) nor
    blind (v21). One change from v23: entries require an engulf in the direction of the 2D bias
    inside the live zone, latched in sequence. If PF rises above 0.736 the gate is doing real work;
    if not, the SPENNYFX entry has no edge on this instrument and the lab should say so.
0-V25. **The short leg is the bleed: 1,043 trades, -$7,082 against the long's -$1,815.** After v24,
    test the long leg ALONE before anything else. Superseded text: REPLACE THE DEEPEST-ZONE RULE WITH A MOST-RECENT-ZONE RULE. One
    change: a new engulf always replaces the incumbent zone, dropping the `pL < dzBot` /
    `pH > szTop` clause entirely. The rule was invented to prefer the strongest zone; v22 shows it
    instead makes the strategy blind to everything after the first deep low. Re-run the v22 counter
    first to confirm creations track the engulf population, THEN re-run v21's full build.
0-V24. **THEN restore the Type 2 validation gate.** Superseded text: EXPLAIN THE ELEVEN-MONTH TRADE GAP. v21's last trade exits
    2025-10-06 on a window running to 2026-09-01. Suspected cause: the deepest-zone rule — a live
    demand zone can only be replaced by a DEEPER one, so in a rising market it persists untouched
    and blocks demand entries indefinitely. Counter-build it: fire on dzLive alone with a one-bar
    exit and read the trade distribution across time. Do NOT tune anything until this is measured; a
    result computed on two thirds of its window is not the result it appears to be.
0-V23. **THEN restore the Type 2 validation gate on the corrected engulf.** Superseded text: RESTORE THE TYPE 2 VALIDATION GATE ON THE CORRECTED ENGULF. This is
    v16's build with one term replaced: the engulf now uses body containment, no gap. v16 returned 0
    trades on a population of 10; the same conjunction now draws on 2,711. If it still returns a
    handful, the constraint is the zone lifecycle after all and the next counter measures LIVE ZONES.
    If it returns a workable number, the system finally has a testable entry. Keep the 2R target from
    v15 and the deepest-zone rule from v10. Superseded text: Bullish engulf = previous
    candle bearish, this candle bullish, close above the previous open. Body containment only. Re-run
    the counter to confirm frequency, THEN restore the validation gate. Superseded text: Entry = zone live AND price just entered it.
    Nothing else. Confirm the first term of the conjunction exists before testing the conjunction
    again. Superseded text: Only closes inside
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


---

## ██ v20 — TEN BECAME 2,711. THE DEFINITION WAS BROKEN, NOT SELECTIVE.

Removing one clause — `open < prevClose`, the gap requirement — multiplied the engulf population by
**271x**.

| | v19 (gap required) | v20 (body containment) |
|---|---|---|
| Engulfs in 4.7 years | 10 | **2,711** |
| Bullish | 5 | 1,325 |
| Bearish | 5 | 1,386 |
| Share of ~9,800 4H candles | 0.1% | **~28%** |

*(P&L on both runs is meaningless by construction — one-bar exits. Only the counts are evidence.)*

**The balance is the proof.** 1,325 versus 1,386 across a period containing a bull run, a bear leg
and several reversals is what an unbiased structural pattern looks like. The old count — five and
five — was not a rare pattern being found; it was tick noise deciding whether a 24/7 candle's open
sat a hair below the previous close.

**WHAT THIS RETIRES.** Every zero-trade run from v16 onward, and the three-trade plateau of v9, v10
and v11, was starved by this single clause. The structural corrections in those builds — the latched
engulf-created zone, the deepest-zone rule, the base geometry — were never disproven. **They were
never given a population to act on.** They go back on the table unmodified.

**THE METHOD LESSON, NOW EARNED TWICE IN THIS LAB.** v19 measured a term and found it empty; v20
measured the fix before building on it. Four cycles were spent filtering a population whose size had
never been checked. **Measure the terms of a conjunction before testing the conjunction** — and when
a definition is imported from another market, check that its preconditions exist here. A gap is an
equities concept. This market never closes.

~28% is a *permissive* term, not a selective one — so the engulf is no longer a candidate explanation
for a low trade count. Whatever binds next is elsewhere, and v21 will say where.


---

## ██ v21 — THE BEST RESULT THIS LAB HAS PRODUCED, AND THE ANOMALY THAT QUALIFIES IT

Recovering v15's source (never the description) showed it **still carried the gap-requiring engulf**.
So the correction v20 measured had never actually reached the strategy: every zone this lab has ever
created — v9, v10, v11, v15, and the **v3 reference base** — was built from the population of ten.

One change. Body containment, no gap. Everything else byte-identical to v15.

| | v3 (old reference) | v15 | **v21** |
|---|---|---|---|
| Profit factor | 0.64 | 0.36258373 | **1.02389497** |
| Trades | 94 | 24 | **185** |
| Max drawdown | — | 15.53% | **10.58%** |
| Win rate | — | 8.33% | 24.86% |

**Long 56 trades, 21 wins, +$652.14. Short 129 trades, 25 wins, -$423.19.** The long carries it and
the short loses — the same shape as both sister labs, from a completely different mechanism. That
consistency is itself a finding.

### THE ANOMALY, DISCLOSED RATHER THAN BURIED
**The last trade exits 2025-10-06. The window runs to 2026-09-01.** Roughly eleven months — about a
third of the sample — produced no entries at all.

The likely cause is structural, not market: the **deepest-zone rule** only replaces a live demand
zone with a *deeper* one. In a rising market every new engulf low is higher, so the incumbent zone is
never replaced, and if price never returns to close inside it, it never mitigates either. It simply
sits there forever, blocking demand entries.

**So v21 is recorded as `testing`, not promoted, and PF 1.0239 is break-even plus noise even at face
value.** A profit factor computed over two thirds of its window is not the number it appears to be,
and the same rule that produces the gap would also have distorted v15 and v3. Measuring it is v22.

**The method held, though, and that is worth stating:** v19 counted a term, v20 counted the fix, v21
applied it to the lifecycle — and the trade count went 24 -> 185 exactly as the counter predicted.
The number that had never been measured was the one that mattered.


---

## ██ v22 — THE DEEPEST-ZONE RULE IS THE BLOCKER. CONFIRMED, AND WORSE THAN PREDICTED.

v20 counted the engulf alone: **2,711**. v21 used it. Nobody had counted the conjunction that
actually gates creation — `bullEng AND (not dzLive OR pL < dzBot)`.

| | Count |
|---|---|
| Engulfing candles (v20) | **2,711** |
| Zone CREATIONS (v22) | **71** — 29 demand, 42 supply |
| Survival rate | **2.6%** |
| Last creation | **2025-10-07** |

**The deepest-zone rule discards 97.4% of zone creation, and then stops creating altogether.** The
last creation on 2025-10-07 matches v21's last trade on 2025-10-06 almost exactly, which closes the
question: v21's eleven-month gap is **not a market feature, it is a lock-up.**

**The mechanism of the lock-up.** An incumbent demand zone can only be replaced by a *deeper* one. In
a rising market every subsequent engulf low is higher, so replacement never happens; and if price
never returns to close inside the incumbent, mitigation never happens either. The zone becomes
immortal and blocks that side permanently. Supply has the mirror pathology in a falling market.

**What this retires.** v21's PF 1.0239 was computed on two thirds of its window, and **v15 and the v3
reference base carry the same defect** — every historical number in this lab was produced by a
strategy that had gone blind partway through. None of them mean what they appeared to mean.

**The rule was a reasonable idea.** Preferring the strongest, deepest zone is sound discretionary
practice. Mechanised as a monotone ratchet with no expiry, it converts "prefer the best zone" into
"ignore every zone after the first extreme one" — a distinction a human reading a chart would never
make, because a human silently retires stale zones. **That is now the fourth time in this lab a
sound-sounding rule has failed on the transition from judgement to mechanism.**

**Third diagnostic in a row that paid.** v19 counted a term and found it empty; v20 counted the fix;
v22 counted the term one level down and found the real blocker. The pattern is established: **when
the trade count is the symptom, count the terms, do not tune the strategy.**


---

## ██ v23 — THE LOCK-UP IS FIXED, AND THE EDGE WAS THE LOCK-UP

One change from v21: drop `pL < dzBot` / `pH > szTop`, so the freshest engulf always owns the zone.

| | v21 (deepest zone) | **v23 (most recent)** |
|---|---|---|
| Profit factor | 1.02389497 | **0.73626670** |
| Trades | 185 | **1,792** |
| Trades span | stops 2025-10-06 | **full window, to 2026-08** |
| Max drawdown | 10.58% | 89.27% |
| Long | 56 (21W) **+$652** | 749 (275W) **−$1,814.86** |
| Short | 129 (25W) −$423 | 1,043 (184W) **−$7,081.71** |

**The fix works exactly as v22 predicted** — the strategy now trades across the entire window instead
of going blind in October 2025. **And profit factor falls from 1.02 to 0.74.**

### WHAT v21's 1.02 ACTUALLY WAS
Not an edge. **An accidental filter.** A frozen demand zone sat in one favourable location while the
strategy was blind to every zone that formed afterwards. Being unable to trade turned out to be worth
more than the entry logic, which is a damning thing to discover about an entry.

**This retires the entire numeric history of this lab.** v21's 1.024, v15's 0.363, and the v3
reference base's 0.64 were all produced by builds carrying the lock-up. **v23 at 0.736 on 1,792
trades is the first undistorted measurement the SPENNYFX mechanism has ever received here**, and it
becomes the reference base on correctness grounds even though its headline number is worse. A real
0.736 is worth more than a fabricated 1.02.

**It is not tradeable and I am not going to dress it up:** −89% return, 89% drawdown, and the short
leg alone loses $7,082 against the long's $1,815. But it is finally an honest starting point, and the
next test — restoring the validation gate — is the first one in this lab that will be measured
against a lifecycle that is neither starved nor blind.

### THE PATTERN, FOUR FOR FOUR
v19 counted a term and found it empty. v20 counted the fix. v22 counted the term one level down and
found the blocker. v23 removed it and found the edge was the blocker all along. **Every diagnostic in
this sequence paid, and every one of them paid by deleting a belief rather than adding a feature.**


---

## ██ v24 — THE LONG LEG IS THE WHOLE SYSTEM

One change from v23: short entries removed, so the demand side is judged alone (LESSON 6).

| | v23 (both legs) | **v24 (long alone)** |
|---|---|---|
| Profit factor | 0.73626670 | **0.89445064** |
| Win rate | 25.61% | **36.61%** |
| Payoff ratio | 2.138 | 1.548 |
| Trades | 1,792 | 833 |
| Max drawdown | 89.27% | 42.50% |

**PF 0.894 is the best honest number this lab has produced on a real sample** — and it is still below
1.0, and a 42.5% drawdown is not tradeable. But the shape of the problem has changed: this is no
longer a broken mechanism, it is a mechanism that is **close** and losing on one side.

### A DETAIL THAT CONTRADICTS THE SISTER LAB
Trade count rose from **749 to 833** when the short leg was removed. The shorts were *blocking* demand
entries under `pyramiding=1` — so here the two legs are **not** independent. In the BTC lab the long
count was identical (128) with and without the short, and I generalised from that. **That
generalisation was wrong for this system**, and any future combined build here has to account for
84 demand entries that only exist when the short leg is absent.

### WHERE THE REMAINING GAP IS, PRECISELY
36.61% win rate at a 1.548 payoff needs **~39.2%** to break even. **The long leg is 2.6 percentage
points of win rate away from break-even** — and every cycle in this lab so far has attacked entries.
The exit has never been touched since v15 set the 2R target, which makes it the obvious next target
and the reason v25 is an exit test rather than another filter.


---

## ██ v25 — THE TIME STOP WAS CUTTING LOSERS, NOT WINNERS

The first exit test this lab has run. One change from v24: `maxBars` 96 → 192.

**The hypothesis was reasonable and wrong.** v24's winners averaged 48.83 bars against a 96-bar cap,
which looked like a truncated right tail. If that were true, widening the cap should let winners run.

| | v24 (96 bars) | v25 (192 bars) |
|---|---|---|
| Profit factor | **0.89445064** | 0.85781046 |
| Max drawdown | **42.50%** | 53.38% |
| Trades | **833** | 797 |
| avgBarsWinning | 48.83 | 53.64 |
| avgBarsLosing | 27.26 | **33.14** |

**REVERTED — worse on both terms.** And the reason is in the last two rows: doubling the cap moved
the average winner by **4.8 bars** and the average loser by **5.9**. The extra room went
disproportionately to trades that were going to lose anyway. **The cap was not truncating the right
tail; it was cutting losers loose**, which is the opposite of what its own statistics suggested.

### A COUPLING NOBODY IN THIS LAB HAD ACCOUNTED FOR
**Trade count FELL, 833 → 797.** A wider time stop means positions are held longer, and under
`pyramiding=1` a held position blocks every new entry that arrives while it is open. **The exit and
the entry frequency are coupled** — so an exit change is never purely an exit change here, and any
future exit test has to read the trade count as part of the result rather than as a side effect.

### WHAT IT BUYS
The gradient now has a direction: **more time is worse.** That makes the untested question whether
*less* time is better, and v24's own numbers make it plausible — losers average 27.26 bars against
winners' 48.83, so a 48-bar cap would cut most losers while leaving the average winner room. That is
v26, and it is a genuinely informed test rather than another guess.


---

## ██ v26 — THE TIME AXIS IS CLOSED. v24 SITS ON AN INTERIOR OPTIMUM.

| maxBars | Profit factor | Max drawdown | Trades | Win rate | Payoff |
|---|---|---|---|---|---|
| 48 (v26) | 0.82035131 | 58.85% | 915 | **40.33%** | 1.214 |
| **96 (v24)** | **0.89445064** | **42.50%** | 833 | 36.61% | **1.548** |
| 192 (v25) | 0.85781046 | 53.38% | 797 | — | — |

**Both directions are worse. 96 is a local maximum, and the time-stop axis is finished.**

### THE PREDICTION WAS HALF RIGHT, AND THE HALF THAT FAILED IS THE INTERESTING ONE
v26 was built on a specific claim: losers average 27.26 bars against winners' 48.83, so a 48-bar cap
should cut most losers while leaving a typical winner room. **The first half happened exactly as
predicted — win rate rose 36.61% → 40.33%.** The second half did not: **payoff collapsed 1.548 →
1.214**, because a 48-bar cap does not leave the average winner room, it closes a large share of
winners *before* they reach 2R.

Net effect: break-even moved from **39.2%** to **45.2%**, so the gap to profitability **widened from
2.6 points to 4.9** even though the win rate improved. **A better win rate bought at the price of
payoff is not an improvement**, and the averages that motivated this test could not have revealed
that — an average winner taking 48.83 bars says nothing about how many winners take 60 or 80.

### THE COUPLING, CONFIRMED BY PREDICTION
v25 discovered that exit length and entry frequency are coupled under `pyramiding=1`. v26 **predicted
in advance** that a tighter cap would raise the trade count, and it did: 833 → 915. That is the
coupling verified forward rather than explained backward, which is the stronger form.

### WHERE THIS LEAVES THE SYSTEM
The exit has one parameter left untested — the 2R target — and the prior is poor: the BTC lab found
2R and 3R on the same iso-profit-factor curve, and War Formation's E26 found a nearer target hurt.
**Two labs have now found the risk-reward axis to be neutral or negative**, so v27 is worth one credit
to close it, not more.

**After that the exit is exhausted, and the more valuable question is whether PF 0.894 is even a
stable number** — the BTC base looked like 1.02 until it was split into 1.36 and 0.66. v24 has never
been split. That is v28, and it matters more than any remaining parameter.


---

## ██ v27 — THE EXIT AXIS IS CLOSED. ALL THREE DIRECTIONS ARE WORSE.

| Change from v24 | Profit factor | Max drawdown | Trades |
|---|---|---|---|
| Time stop 96 → 192 (v25) | 0.85781046 | 53.38% | 797 |
| Time stop 96 → 48 (v26) | 0.82035131 | 58.85% | 915 |
| Target 2R → 2.5R (v27) | 0.88039828 | 45.88% | 803 |
| **v24, unchanged** | **0.89445064** | **42.50%** | **833** |

**Three exit parameters, three directions, all worse. v24 sits on a local optimum in exit space and
the axis is finished.**

### THE ISO-PF TRADE, FOR THE THIRD TIME IN THREE MECHANISMS
v27 did exactly what the risk-reward axis does: payoff rose **1.548 → 1.738 (+12.3%)** and win rate
fell **36.61% → 33.62% (−3.0pp)**. Break-even moved from 39.2% to 36.5%, and the actual win rate fell
further than that, so the gap to profitability widened from 2.6 points to **2.9**.

| Lab | Mechanism | Target change | Result |
|---|---|---|---|
| BTC | VWAP mean-reversion | 2R → 3R | PF 0.9121 → 0.9100 — **neutral** |
| War Formation | HA cascade reclaim | 1.5R → 1R | PF 0.7490 → 0.6922 — **negative** |
| 3M Elite | Supply/demand zones | 2R → 2.5R | PF 0.8945 → 0.8804 — **negative** |

**Three unrelated mechanisms, one regularity: moving the target buys payoff and sells win rate at
roughly par, and pays commission for the privilege.** This is now strong enough to be a standing
prior rather than a per-lab finding — it belongs in the ledger, and future cycles should not spend
credits on the risk-reward axis without a specific reason to think this system is different.

### BOTH FORWARD PREDICTIONS CONFIRMED
Stated before the run: (1) the axis would not help, and (2) trade count would **fall** because a
further target lengthens holds and held positions block entries under `pyramiding=1`. Trades went
833 → 803. **That is the exit/entry coupling predicted correctly for the second consecutive cycle**,
which is now the best-verified mechanical fact in this lab.

### WHERE THE SYSTEM ACTUALLY STANDS
v24: **PF 0.894, 833 trades, long-only, 42.5% drawdown, 2.6 points of win rate short of break-even.**
Entries have absorbed nine cycles and exits are now exhausted in every direction. **The next credit
should not buy another parameter — it should ask whether 0.894 is a real number at all**, because
the BTC base looked like 1.02 right up until it split into 1.36 and 0.66.


---

## ██ v28a — THE FIRST HALF. ENCOURAGING, AND NOT YET A CONCLUSION.

| | Full sample (v24) | **First half (v28a)** |
|---|---|---|
| Profit factor | 0.89445064 | **0.92199683** |
| Win rate | 36.61% | **36.59%** |
| Payoff ratio | 1.548 | 1.598 |
| Trades | 833 | 410 |
| Max drawdown | 42.50% | 27.59% |

**The win rates match to two decimal places — 36.61% against 36.59%.** That is the number that
matters most, because win rate is the term the whole system is short on, and it is the term most
likely to move if the mechanism only worked in one regime.

**The lower drawdown on the half is expected, not a finding:** a shorter window has less room to
compound a bad run, so half-sample drawdowns are structurally smaller and should not be compared
across window lengths.

### WHAT THIS WOULD MEAN IF IT HOLDS
The BTC base decomposed into **1.3552 early and 0.6566 late** — an average of a good period and a bad
one, which invalidated three gate verdicts earned on the blend. **If v24's halves come in close, this
system is the opposite case: a stable, genuinely measured 0.894**, and the remaining 2.6 points of
win rate is a real deficit worth attacking rather than an artifact of averaging.

### WHY I AM NOT CONCLUDING IT YET
H1 at 0.922 against a full sample of 0.894 *implies* H2 near 0.87. **That is arithmetic, not a
measurement**, and HARD LESSON 11 exists precisely because I once reasoned about a number instead of
running it. The implied value also ignores that profit factor does not decompose linearly across
sub-periods when position size compounds. **v28b runs the second half next cycle and the conclusion
waits for it.**

**Best config unchanged: v24, long-only, PF 0.894 on 833 trades.**


---

## ██ v28b — THE HALVES AGREE. v24 IS A REAL NUMBER.

| | H1 (2022-01 → 2024-05) | H2 (2024-05 → 2026-09) | Full sample |
|---|---|---|---|
| Profit factor | 0.92199683 | 0.86121615 | 0.89445064 |
| **Win rate** | **36.59%** | **36.64%** | **36.61%** |
| Trades | 410 | 423 | 833 |
| Max drawdown | 27.59% | 36.26% | 42.50% |

**Profit-factor spread: 0.061. Win-rate spread: 0.05 percentage points.**

### THE CONTRAST THAT MAKES THIS MEANINGFUL
| Lab | H1 | H2 | Spread |
|---|---|---|---|
| BTC base | 1.3552 | 0.6566 | **0.699** |
| **3M v24** | **0.9220** | **0.8612** | **0.061** |

The BTC base was an average of a good period and a bad one, and three gate verdicts earned on that
blend had to be re-scoped. **v24 is the opposite case.** H1 is a bear market and a recovery; H2 is a
sustained bull run. Two completely different markets, and the win rate — **the term this system is
short on** — matches to within 0.05 of a percentage point.

### WHAT THIS BUYS
1. **v24's 0.894 is a property of the mechanism**, not an artifact of averaging.
2. **The v25-v27 exit conclusions stand as measured.** The time-stop optimum at 96 bars and the
   closed risk-reward axis were established on a homogeneous sample, so they do not need re-scoping.
3. **The 2.6-point win-rate deficit is a real, stable target.** It is the same deficit in both halves,
   which means it is a property of the entry and not of any particular market.

That last point is what makes the next cycle worth spending: **there is a specific, stable thing to
fix**, which is more than this lab has had at any previous point. The BTC lab's Attack 15 just showed
where to look — not at the filters, but at the terms of the signal itself.


---

## ██ v29 — THE ZONE TOUCH IS NOT WHAT CARRIES THIS SYSTEM

| | v24 | **v29 (no touch)** |
|---|---|---|
| Profit factor | 0.89445064 | **0.97210749** |
| Win rate | 36.61% | **39.87%** |
| Trades | 833 | **1,076** |
| Max drawdown | **42.50%** | 61.45% |

**REVERTED strictly on drawdown** — the ratchet is both terms or nothing, and 42.50% → 61.45% fails
it. But **PF 0.972 is the closest to break-even this lab has ever been**, and the win rate rose while
the trade count grew by 243, which means the extra trades are *better* than the average of the ones
already there.

### WHAT IT ESTABLISHES
**The condition this system is named for — price trading back INTO the zone — is not what makes it
work.** Remove it and the strategy improves. What remains is "a demand zone is live and price is
above its base", which is much closer to a trend-participation condition than a zone condition.

### THREE LABS, ONE TEST, TWO ANSWERS
| Lab | Named term | Verdict |
|---|---|---|
| BTC | +2σ stretch | **decoration — removing it improved both halves** |
| **3M Elite** | **zone touch** | **decoration — removing it raised PF 0.089** |
| War Formation | 3m coil | **the edge — removing it cost 1.075 of PF** |

**Two of three named mechanisms are decoration.** HARD LESSON 15 is now measured three times, and the
split is what makes it valuable: the *test* is what transfers, never the answer.

### WHY THE DRAWDOWN BLEW UP, AND WHY THAT IS FIXABLE
The losing trades did not get worse — the win rate improved. **The drawdown grew because 30% more
trades compound at `percent_of_equity` 100**, so a bad run has more positions to work through at full
size. That is a frequency-and-sizing problem, not a signal problem, which is why v30 attacks
frequency with a *different* term rather than putting the touch back.

**Best config unchanged: v24, long-only, PF 0.894 on 833 trades.**
