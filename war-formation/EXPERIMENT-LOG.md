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
| E12 | v7: Oracle's direction rule (2+ consecutive green HA 6h) | PF 1.14 vs champion 1.69, DD 4.19% vs 3.10% — **REVERTED** |
| E13 | Short + 3m cycle-position gate (Oracle item 2) | PF 0.68→**0.75**, WR 20.3%→23.1%, net −5.9%→−3.0% — **gate helps, still unprofitable** |
| E14 | Queue item 3: counter-move weakening trigger on the v6 long champion (>=2 red HA 3m candles with decreasing range, latched 5 candles) | **REVERTED.** PF 1.69->0.73, win 56.3%->45.0%, trades 32->20, DD 3.10%->1.36%. The gate removed disproportionately GOOD trades -- redundant with the 3m coil, which already measures a move losing force. [report](https://mcp-api.trader.dev/backtest/01M1GPMTPZ146ZY2KJVDVKQF8G) |
| E15 | Queue item 4: Oracle COLOUR-FLIP exit replacing the fixed 2R TP (stop still fixed) | **REVERTED.** PF 1.69->0.31, win 56.3%->20.0%, trades 32->35, hold 12.8 bars. Exits on the first red 3m HA candle, which inside an uptrend is noise. [report](https://mcp-api.trader.dev/backtest/01M1GQ6PQPVP1T3JNZ74JWZYT7) |
| E16 | Queue item 5: require the SINGULARITY (last completed 1h HA candle green too) | **REVERTED.** PF 1.69->0.52, win 56.3%->34.6%, trades 32->26. He said don't wait for it, and he was right · [report](https://mcp-api.trader.dev/backtest/01M1GQM0TYEWM41J1DPAYB0HT2) |

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
0z. **READ `ORACLE-RULES.md` FIRST — it now contains the author's COMPLETE rule set, quoted from his
    own audio, and it supersedes several of this lab's design choices.** Three corrections matter:
    (a) He defines clear direction as **more than one consecutive green (or red) 6h candle** — simpler
        than this lab's "4+ green HA 1h candles in the previous 6h block", and it is what he says.
    (b) He names **"singularity"** as 6h and 1h agreeing in colour, and calls it a bonus, not a
        requirement: "don't wait for that".
    (c) **He states that "war formation has nothing to do with entering here."** What this lab calls
        the War Formation is actually his *3-minute cycle drill-down*. Name kept for continuity.
    Implement items 1-5 at the bottom of ORACLE-RULES.md, one per cycle, in order.
0f. **THE 3-MINUTE CYCLE POSITION GATE.** Read `ORACLE-RULES.md` first; it is
    decoded from the author's own videos and it names the exact defect in every short built so far.
    His rule: direction comes from the 6h and 1h, but **direction alone does not permit an entry —
    position inside the 3-minute cycle does.** "Even if you had direction to short you can wreck an
    absolutely perfect trade... do you want to short down here?" Every short this project has built
    entered AFTER price had already fallen, i.e. at the bottom of the cycle, which is exactly what he
    says destroys the trade. That fits E9/E9b perfectly: healthy payoff, ~20% win rate.
    **Implement:** reconstruct the 3m cycle from 1m bars (3 x 1m, same technique already used for
    15m/1h/6h). Compute `cyclePos = (close - cycleLow) / (cycleHigh - cycleLow)` over a rolling
    window of 3m candles. Then gate: **shorts only when cyclePos is HIGH, longs only when cyclePos is
    LOW.** Test the short leg alone first, judged on its own profit factor.
0g. **THEN: require the retrace ("wait for the pump").** "All this is, is waiting." A short should
    additionally require a green push against the bear regime first — N consecutive green 3m candles,
    or a retrace of X% of the prior leg. Test as a separate change so it is attributable.
0d. **Decide the short question honestly (deferred until 0f/0g are tested).** Given 0c, there are two options and
    the data should pick, not preference: (i) build a short that targets the crash specifically —
    require the bear regime PLUS an acceleration trigger (range expansion, or a break with the
    session already extended), accepting a low win rate and a large payoff; or (ii) accept that this
    cascade is a LONG-ONLY edge on this data and meet the both-directions requirement with a separate
    strategy. Test (i) once; if it fails, take (ii) and record it as settled.
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

## Rules for this loop
- **One experiment per cycle.** Record the real result before starting another.
- **Never hand-write metrics.** Copy them from the backtest response.
- **A negative result is a complete cycle.** Record it and move on.
- **Do not tune toward a number.** If an experiment only helps at one exact parameter value, that is
  evidence against it, not for it.
- Every hard lesson from the main `STRATEGY-LEDGER.md` applies here too — especially LESSON 3
  (R >= 8x the round-trip fee), LESSON 5 (stop beyond structure, never beyond the signal level) and
  LESSON 6 (audit every leg separately).


## E14 LESSON — CHECK A NEW GATE FOR REDUNDANCY BEFORE PAYING FOR IT
The Oracle's weakening rule ("candles get smaller, the move gets weaker") is real, and it is
**already in this build under another name.** The 3m coil, `atr(3) < atr(30) * 0.85`, IS a
measurement of a move losing force. Adding an explicit shrinking-red-run requirement on top of it
double-counted the same information and selected a narrower, worse subset of the same signals.

The tell that separates this from an ordinary failed filter: **the survivors got worse.** A filter
that removes noise raises the win rate on what remains. This one dropped it 56.3% -> 45.0%, so it
was not removing noise, it was removing signal. Compare E13, where the cycle-position gate cut the
short leg from 69 trades to 39 and *improved* PF -- that is what a non-redundant filter looks like.

**Rule for future cycles:** before adding a gate, ask which existing condition already measures the
same property. If one does, the honest experiment is to REPLACE it, not stack on it. Also note the
drawdown trap here -- DD improved 3.10% -> 1.36% purely because there was less trading. A drawdown
improvement that arrives with a large drop in trade count is not a risk improvement.

**Queue item 3 is answered and closed. Do not re-run it as an additive gate.** The open variant, if
it is ever wanted, is weakening-run *instead of* the coil, judged head to head.


## E15 LESSON — THE FIXED TAKE-PROFIT IS LOAD-BEARING, AND HIS EXIT IS A JUDGEMENT
Replacing the 2R target with his colour-flip rule cut the profit factor from 1.69 to 0.31. The
diagnostic is in the hold times: **12.8 bars average, winners 24.7, losers 9.8.** The flip fires on
the first red 3m Heikin Ashi candle, and inside a 1m uptrend that is ordinary noise -- so winners get
closed after roughly twenty minutes at small profits while losers still run the full distance to the
stop. Thirty-five tiny trades paid $344 in commission.

**Both halves of the champion's exit turn out to matter.** The 2R target is not an arbitrary default:
it is what lets a winning trade run past the noise that the colour rule reacts to.

**This is queue item 1's lesson repeating.** His stated direction rule underperformed the lab's HA
count; his stated exit rule collapses when mechanised literally. In both cases the words describe how
a person READS a chart, with a human deciding whether a given flip means anything. Reading is not a
rule. What survived from his material was the part that was diagnostic rather than prescriptive --
the cycle-position insight in E13, which explained a failure the lab could not otherwise explain.

**Queue item 4 is answered and closed.** If it is ever revisited, the flip must be qualified (two
consecutive counter candles, or a close beyond the entry-side structure), and that is a different
experiment, not this one.


## E16 LESSON — THE ORACLE IMPLEMENTATION QUEUE IS NOW FULLY WORKED
Requiring the singularity cut PF from 1.69 to 0.52 and the win rate from 56.3% to 34.6%. Six trades
removed and the survivors much worse: the same anti-selective signature as E14.

**The satisfying part is that he predicted it.** His exact words: *"if you got it on the one, you got
double clarity, **but don't wait for that**."* The data agrees with his caveat, not his enthusiasm.
Waiting for the bonus costs more than the bonus is worth.

### Final scorecard on his five stated rules
| Item | His rule | Result |
|---|---|---|
| 1 | Direction = consecutive green 6h candles | REVERTED — the lab's HA 1h count beat it |
| 2 | 3m cycle position | **HELPED** — the only one that improved anything (E13) |
| 3 | Counter-move weakening | REVERTED — redundant with the 3m coil |
| 4 | Colour-flip exit | REVERTED — fires on noise; the fixed 2R target is load-bearing |
| 5 | The singularity | REVERTED — and he told us not to wait for it |

**One of five survived, and it was the DIAGNOSTIC one.** Item 2 was not a rule he gave for entry; it
was his explanation of *why* entries fail — "don't long the top or short the bottom", "entering the
enemy's camp." That explained the lab's every failed short when nothing else could. His prescriptive
rules consistently underperformed the lab's own mechanisations; his description of *why price moves*
was the valuable part. **That is the durable lesson for mining any trader's material.**

**Champion is unchanged and now stands on a fully explored queue: v6, long-only, PF 1.69, DD 3.10%,
32 trades.** The binding constraint remains sample size — 1m coverage is still only 2025-12-16 to
2026-05-03. Future cycles need a new source of questions, not more items from this list.
