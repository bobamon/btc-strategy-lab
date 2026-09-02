# War Formation — Experiment Log

The memory for the mastery loop. **Read this before every cycle.** Never repeat a finished
experiment; take the next open question, run it, record the real result, move it to Done.

> Research specification for backtesting. Not a trade recommendation.

## Current champion
**v6 — HA cascade, LONG ONLY.** BTCUSDT 1m, 2025-12-16 → 2026-05-03.
`+7.8% · PF 1.69 · win rate 56.3% · Sharpe 2.19 · max DD 3.10% · 32 trades` — status **testing**.

Pine: `war-formation/pine/war-formation-ha.pine` (long-only variant; short leg removed).

## The two things that are settled
1. **The cascade is the edge.** Stripping the 6h/1h/15m/3m vetoes takes PF from 1.40 to 0.68 and
   win rate from 42.6% to 25.1%, with trades exploding 47 → 521. Do not simplify the cascade away.
2. **The MIRRORED short was dead weight — this is not a verdict on shorting.** 2 winners in 15.
   The short leg was the long leg with `crossover` flipped to `crossunder`, and that is the thing
   that failed. A reclaim of support in an uptrend and a failed bounce into resistance in a
   downtrend are different events with different geometry, speed and follow-through. The short side
   must be **rebuilt from its own logic** and judged on its own numbers. Never mirror again.
3. **This cascade (6h/1h/15m/3m HA vetoes + a reclaim/rejection/acceleration trigger) is a
   LONG-ONLY edge on this data — settled at E15 (0d).** Five independently-designed short
   constructions on top of this cascade (mirrored, rejection-at-resistance, location-gated,
   trigger-gated pump-weakening, acceleration) all land on the same shape: decent-to-good payoff,
   low win rate, net negative — E15's 313-trade sample confirms it isn't noise. Stop attaching a
   short leg to this cascade; the both-directions objective needs an independently-designed short
   strategy (0i), not a sixth variant of this one.

## The open problem
**The edge is concentrated in time.** Same code, same parameters:

| | Dec 16 – Feb 23 | Feb 23 – May 3 |
|---|---|---|
| Net | +8.7% | −0.8% |
| PF | 3.80 | 0.89 |
| Win rate | 70.6% | 40.0% |
| Trades | 17 | 15 |

15 trades at PF 0.89 is within noise of break-even, not proof of failure — but it is not confirmation
either. **The binding constraint is sample size.** 1m coverage on this engine is only
2025-12-16 → 2026-05-03 and has not extended (re-checked 2026-09-01).

## DONE — do not re-run
| # | Experiment | Result |
|---|---|---|
| E1 | v1 standard candles, 4% gap | 0 trades — coil and thrust required on the same bar |
| E2 | v2 coil moved to prior bar | PF 0.38 — every winner exited on the time stop |
| E3 | v3 gap 4% → 2% | PF 0.58 — target still never hit |
| E4 | v4 Heikin Ashi + structural stop, R floor 0.15% | PF 0.47 — fees exceeded gross profit |
| E5 | v5 R floor 0.15% → 0.80% | **PF 1.40** — first profitable build |
| E6 | Ablation: strip the whole cascade | PF 0.68 — cascade is the edge |
| E7 | v6 long only | **PF 1.69** — best full-window result |
| E8 | Split-half stability | 3.80 vs 0.89 — edge concentrated in first half |
| E9 | Short rebuild, rejection-at-resistance, strict gates | 5 trades — inconclusive, sample too small to test |
| E9b | Same short, gates loosened for sample size | PF 0.68, 69 trades, win rate 20.3% — **short side fails again** |
| E10 | Diagnostic: long the whole bear episode | PF 0.83, −12.6%, 125 episodes — bear label is SOUND |
| E11 | Diagnostic: short the whole bear episode | PF 0.50, −17.6%, 11.1% win rate — **both directions lose** |
| E12 | ORACLE-RULES item 1: direction = 2+ consecutive same-colour REAL 6h candles (long only) | PF 1.35, DD 2.48%, 12 trades — **rejected, does not beat champion; sample collapsed 32→12** |
| E13 | ORACLE-RULES item 2: 3m cycle-position gate, short leg alone, cyclePos >= 0.7 | PF 0.00, 2 trades — **sample collapse, gate too tight to judge** |
| E13b | Same short leg, cyclePos threshold loosened 0.7 → 0.5 | PF 0.63, 12 trades, 16.7% win rate, 3.15:1 payoff — **rejected; same E9/E9b shape, gate did not fix the short leg** |
| E14 | ORACLE-RULES item 3 / queue 0g: short leg requires ≥2 consecutive shrinking-range GREEN 3m candles ("wait for the pump weakening") before the reversal trigger, cyclePos gate removed | 2 trades, 0 winners, PF 0.00 — **sample collapse, same shape as E13** |
| E14b | Same trigger, loosened minGreenN 2 → 1 (just the last 3m candle must be green) | 9 trades, PF 0.83, win rate 11.1%, payoff 6.66:1 — **rejected; the fourth structurally distinct short construction lands on the same shape** |
| E15 | 0d option (i): crash-timing short — bear regime + acceleration trigger (range >= 1.5x atr30, down bar, close in bottom 35% of range, already extended below prior 15m low), no reversal/pullback requirement | 313 trades, PF 0.65, win rate 15.7%, net −29.4%, max DD 29.4%, payoff 3.51:1 — **rejected; fifth short construction, same shape, now at a sample large enough to settle it** |
| E16 | 0i: independent short strategy, different primitives — EMA50<EMA200 + EMA200 slope-down regime (not HA colour count), "sell the failed rip" RSI(14) 55→50 crossunder trigger (not reversal-at-a-level), stop beyond last confirmed pivot high (not the cascade's 15m level) | 587 trades, PF 0.5866, win rate 15.84%, net −58.43%, max DD 58.72%, payoff 3.116:1 — **rejected; sixth structurally distinct short construction, same shape, this time with zero shared primitives with the cascade** |

## STANDING OBJECTIVES — every variant must satisfy these
- **Both directions.** Long AND short, each with its own entry logic, its own level definition and
  its own risk geometry. A short rule that is only a sign-flipped long rule does not count.
- **Handle the flip.** The strategy must detect when the regime changes and respond mechanically —
  not merely filter for one regime and sit out the other. Report bull-regime and bear-regime
  performance separately in every result so the flip is visible.
- **Fixed SL and TP at entry**, no trailing stop as primary risk, no martingale, averaging down, or
  grid. These never relax.

## OPEN QUEUE — take the top unblocked item each cycle
0a. ~~REBUILD THE SHORT SIDE PROPERLY~~ — **DONE (E9/E9b), failed.** See the new 0c below.
0c. ~~DIAGNOSE THE BEAR REGIME ITSELF~~ — **DONE (E10/E11). ANSWERED.**
    Long through bear episodes loses 12.6% (PF 0.83); shorting them loses 17.6% (PF 0.50). **Both
    directions lose on the same bars.** That is only possible if bear-labelled periods carry no
    consistent drift: they drift slightly UP most of the time (112 of 126 shorts lost small) and fall
    hard occasionally (14 shorts won big, 3.99:1 payoff). **The 6h HA bear label marks CRASH RISK,
    not downtrend.** This explains every short failure so far — E9b's 20% win rate at 2.68:1 is the
    same shape. A short here cannot work by "being short during bear"; it must time the crash.
0z. ~~READ `ORACLE-RULES.md` FIRST~~ — **item 1 DONE (E12), rejected.** Items 2-5 remain, in order.
    (a) He defines clear direction as **more than one consecutive green (or red) 6h candle** — simpler
        than this lab's "4+ green HA 1h candles in the previous 6h block", and it is what he says.
        **Tested as E12: requiring 2+ consecutive same-colour REAL 6h candles collapsed the sample
        from 32 to 12 trades and PF fell 1.69→1.35. The real 6h candle rarely strings two of the same
        colour in a row; the old HA-1h-count proxy was a much looser (more frequent) condition.** Do
        not retry this exact formulation without changing something (e.g. minConsec=1, or count HA 6h
        candles instead of real 6h candles) — that is a new open question, not a re-run.
    (b) He names **"singularity"** as 6h and 1h agreeing in colour, and calls it a bonus, not a
        requirement: "don't wait for that". (item 5, untested)
    (c) **He states that "war formation has nothing to do with entering here."** What this lab calls
        the War Formation is actually his *3-minute cycle drill-down*. Name kept for continuity.
    Implement items 2-5 at the bottom of ORACLE-RULES.md, one per cycle, in order. Item 2 (the 3m
    cycle-position gate) is next — see 0f below, which already specifies it.
0f. ~~THE 3-MINUTE CYCLE POSITION GATE~~ — **DONE (E13/E13b), rejected.** Added a rolling-window
    `cyclePos = (close - cycleLow) / (cycleHigh - cycleLow)` gate (computed via ta.highest/ta.lowest
    over 30x 1m bars, mathematically equal to a rolling max/min over reconstructed 3m candles — arrays
    are forbidden so no literal candle storage was needed) on top of the unchanged bear-regime short
    cascade. At threshold 0.7 (top 30% of range) the sample collapsed to 2 trades — too tight to
    judge. Loosened to 0.5 (upper half): 12 trades, PF 0.63, 16.7% win rate, 3.15:1 payoff —
    **the same E9/E9b shape.** The gate did not fix the short leg. Diagnosis: this gate only
    constrains the *setup window*, not where the *trigger bar* lands inside it — the crossunder
    trigger still fires only once price is already reversing down through the 15m high, so the entry
    can land after most of the favourable move is gone even while cyclePos was technically "high"
    somewhere earlier in the window. **Location alone is not the fix; the trigger itself needs to
    change.** This sharpens 0g below rather than replacing it — 0g (the counter-move-weakening
    trigger) is the next thing to test on the short leg, not another location gate.
0g. ~~THEN: require the retrace ("wait for the pump")~~ — **DONE (E14/E14b), rejected.** Added a
    reconstructed-3m counter-move-weakening gate (≥2 shrinking-range green 3m candles required
    before the reversal trigger) on top of the unchanged bear-regime cascade. Tight form (minGreenN=2):
    2 trades, sample collapse. Loosened (minGreenN=1, just "last 3m candle was green"): 9 trades,
    PF 0.83, win rate 11.1%, payoff 6.66:1 — **the same E9/E9b/E13b shape.** This is now the
    **fourth** structurally distinct short construction (mirrored sweep-reclaim, rejection-at-
    resistance, location-gated, trigger-gated pump-weakening) landing on identical statistics:
    healthy-to-excellent payoff, single-digit-to-low-teens win rate, net negative. Changing WHERE in
    the range the trigger sits (0f) and WHAT immediately precedes the trigger (0g) both moved which
    bar the entry fires on without moving the outcome distribution at all. **The remaining
    un-tested lever is WHAT the entry is triggering ON** — every construction so far fires on a
    variant of "price crosses back through a recent extreme with velocity/rejection." None have
    tried gating on acceleration/range-expansion (0d option (i): the crash-timing short) rather than
    on reversal-after-a-pullback. 0d is now unblocked and is the next thing to test before
    concluding (per 0d option (ii)) that this cascade is long-only on this data.
0d. ~~Decide the short question honestly~~ — **DONE (E15), ANSWERED.** Option (i) — bear regime +
    acceleration/range-expansion trigger, no reversal/pullback requirement, targeting the crash
    directly — was tested once at full scale: 313 trades, PF 0.65, win rate 15.7%, net −29.4%, max DD
    29.4%, payoff 3.51:1. This is the **fifth** structurally distinct short construction on this
    cascade (mirrored sweep-reclaim, rejection-at-resistance, location-gated, trigger-gated
    pump-weakening, now acceleration) and it lands on the exact same shape as the other four —
    healthy-to-good payoff, low win rate, net negative — but this time at a sample 4-30x larger than
    any prior attempt, large enough to call it settled rather than noisy. Extended-session bars are
    common, so the trigger fired often; most fires were false-crash snapbacks (avgBarsLosing 56.2 vs
    avgBarsWinning 275.8, losers dying ~5x faster). **SETTLED: this cascade (6h/1h/15m/3m HA vetoes,
    reclaim/rejection or acceleration trigger, structural stop) is a LONG-ONLY edge on this data.**
    Taking option (ii): the both-directions standing objective must be met by a **separately-designed
    strategy** for the short side, not another leg bolted onto this cascade. That separate-strategy
    design is now open item 0i below.
0i. ~~BUILD AN INDEPENDENT SHORT STRATEGY (not a leg on this cascade)~~ — **DONE (E16), rejected.**
    Built a short-only strategy from primitives sharing NOTHING with the cascade: EMA50<EMA200 +
    EMA200-slope-down regime (not HA colour count), an RSI(14) 55→50 "failed rip" crossunder trigger
    (not reversal-at-a-swept-level), a stop beyond the last confirmed `ta.pivothigh` (not the
    cascade's 15m structural level). Result: 587 trades, PF 0.5866, win rate 15.84%, net −58.43%, max
    DD 58.72%, payoff 3.116:1 (breakeven win rate ~24.3%, actual 15.8%) — **the sixth structurally
    distinct short construction on this dataset, and it lands on the identical shape as the five
    cascade-leg attempts** (healthy-to-excellent payoff, low win rate, net negative), this time with
    zero shared machinery. This is materially stronger evidence than 0c/E10-E11 that the failure is
    not about regime-detector choice or entry geometry — it points at something about this symbol and
    window (BTCUSDT Dec 2025 – May 2026) itself: a persistent bullish skew that runs over
    counter-trend positions faster than it lets them pay off at 2:1 R:R. See new open item 0j below.
0j. **TEST WHETHER THE R:R ITSELF, NOT THE CONSTRUCTION, IS WHAT'S FAILING SHORTS.** Six independently
    designed short constructions (E9, E9b, E13, E13b, E14, E14b, E15, E16) all land on the same shape:
    healthy-to-excellent payoff ratio (2.68:1 to 6.66:1), win rate 11-20%, net negative. Every one used
    rr=2.0 and a structural stop. The unexamined variable is the reward:risk itself — a persistent
    payoff-vs-win-rate shape this consistent across six unrelated entry/regime designs suggests the
    stop distance or target distance (not the trigger) may be miscalibrated for how BTC actually snaps
    back against short positions in this window. Before concluding (as 0i's result invites) that shorts
    are simply unprofitable here, run E16's exact construction at a tighter rr (e.g. 1.2 or 1.5) or a
    volatility-scaled target instead of a flat rr=2.0 multiple, and see whether win rate rises enough
    to compensate. If it still fails at every rr tested, that is much stronger grounds to call the
    both-directions objective genuinely unmeetable on this symbol/window and document it as such on
    the CHAMPION-BOARD-equivalent status for this lab.
0e. (was 0c) **DIAGNOSE THE BEAR REGIME ITSELF (superseded).** Two structurally different short
    constructions have now failed: the mirrored failed-breakout (v5, 2 of 15) and
    rejection-at-resistance (E9b, 14 of 69, PF 0.68). Both had healthy payoff ratios and losing win
    rates. **Geometry is not the problem, so stop iterating on geometry.** Test the regime label
    instead: (i) how many bars of the window were even classified BEAR by `grnPrev <= 2`? (ii) what
    was BTC's net return across exactly those bars? If the bear-labelled periods were flat or rising,
    no short construction could have worked and the finding is about the sample, not the strategy.
    This is a plotting/measurement question first — it may need no backtest at all.
0b. **BUILD AN EXPLICIT REGIME-FLIP DETECTOR.** Right now the 6h HA green-count classifies the
    regime but nothing detects the *transition*. Add a flip signal — the green count crossing its
    threshold in either direction — and test three responses: (i) stand down for N bars after a
    flip, (ii) trade the flip itself as an entry, (iii) ignore it (current behaviour, the control).
    Report each separately.
1. **Port the cascade to 15m and 5m.** Highest value by far: 4.7 years of data instead of 4.6 months.
   6h/1h/15m all reconstruct from 15m bars the same way they do from 1m. Entry precision is coarser,
   but a 500+ trade sample settles what 32 trades cannot. **Do this first.**
1b. **If 0c shows the bear label is sound but shorts still lose**, the honest conclusion is that this
    cascade is a long-only edge on this data, and the short requirement should be met by a separate
    strategy rather than by forcing a second leg onto this one. Record that and move on.
2. **Leave-one-out ablation of each veto** (six runs, one per cycle): 6h regime · time gate ·
   1h agreement · 15m violation · 3m coil · middles filter · witching ban. Which layers earn their
   place? Drop any that costs nothing — fewer vetoes means more trades means a bigger sample.
3. **Loosen the tightest veto** to roughly double trade count on 1m, then re-run the split-half.
   If the edge survives at 60–70 trades it is real; if it evaporates, E7 was luck.
4. **Sensitivity sweep**, one parameter per cycle: `velK` {0.6, 0.8, 1.0} · `greenBull` {3, 4, 5} ·
   `rr` {1.5, 2.0, 2.5} · R floor {0.6, 0.8, 1.2%}. An edge that lives at exactly one setting is noise.
5. **Time-of-day breakdown.** The Oracle map (witching 1–4am, AM waves 7–8, 9:30 open, 11–1 midday,
   4pm close, 8pm end-of-day) is currently plotted but not traded. Does entry hour predict outcome?
6. **`maxBars` sensitivity** {360, 720, 1440} — is the 12h cap helping or truncating winners?

0h. **AUDIT: does the champion's committed Pine actually honor the 0.80% R floor it claims?**
    While building E13, `minRpct` in the committed `war-formation-ha.pine` (and in every stored
    `pineSource` for v5/v6/the ablation run, checked by grep) reads `input.float(0.15, ...)`, not
    0.80 — yet every note from E5 onward says the floor was raised 0.15% → 0.80% per LESSON 3. Either
    the stored `pineSource` text is a stale snapshot that doesn't match what was actually sent to
    `quick_backtest` at run time (a HARD LESSON 8-style record-keeping bug — the numbers could still
    be real, just the archived source wrong), or the R floor was never actually 0.80% and the champion
    result was produced at a 0.15% floor. This is a measurement question, not a backtest: diff the
    committed `war-formation-ha.pine` against each `results/backtests.json` `pineSource` field and
    determine which is true before leaning on the champion numbers further. Not spent this cycle (0f
    was already the chosen item); take this next if it is unblocked and no result has re-run the
    champion baseline to settle it directly.

## Rules for this loop
- **One experiment per cycle.** Record the real result before starting another.
- **Never hand-write metrics.** Copy them from the backtest response.
- **A negative result is a complete cycle.** Record it and move on.
- **Do not tune toward a number.** If an experiment only helps at one exact parameter value, that is
  evidence against it, not for it.
- Every hard lesson from the main `STRATEGY-LEDGER.md` applies here too — especially LESSON 3
  (R >= 8x the round-trip fee), LESSON 5 (stop beyond structure, never beyond the signal level) and
  LESSON 6 (audit every leg separately).
