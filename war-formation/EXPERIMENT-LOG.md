# War Formation — Experiment Log

The memory for the mastery loop. **Read this before every cycle.** Never repeat a finished
experiment; take the next open question, run it, record the real result, move it to Done.

> Research specification for backtesting. Not a trade recommendation.

## Current champion
**v6 — HA cascade, LONG ONLY.** BTCUSDT 1m, 2025-12-16 → 2026-05-03.
*(Config updated 2026-09-02 after E17: `minRpct` is now 0.80%, not 0.15%. Behaviour is unchanged to
nine significant figures — the floor never bound — but the code now states its true risk floor.)*
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
| E17 | Raise the R floor 0.15% -> 0.80% (HARD LESSON 3 compliance) | **IDENTICAL RESULTS.** PF 1.68623784, DD 3.10289714%, 32 trades, 56.25% -- the floor never bound. 0.80% adopted as the documented config · [report](https://mcp-api.trader.dev/backtest/01M1GQYHZ94F1QPS3HFR8641NB) |
| E18 | Cross-lab transfer: restrict the champion to the high-volatility regime | **REVERTED.** PF 1.69->1.10, trades 32->7. The edge concentration is NOT a volatility regime · [report](https://mcp-api.trader.dev/backtest/01M1GR7Q2PD409YCKNDDQJ2J86) |
| E19 | SENSITIVITY: greenBull 4 -> 3 | **Degrades gracefully.** PF 1.686->1.282, win 56.25%->47.62%, trades 32->42, DD 3.10%->4.79%. Still clearly profitable -- not a knife-edge fit · [report](https://mcp-api.trader.dev/backtest/01M1GRHCBX2GY7QQ7NK1N173VB) |
| E20 | Timeframe translation to 5m, parameters scaled x5 | **REVERTED.** PF 1.621, DD 2.73%, but trades 32->5 · [report](https://mcp-api.trader.dev/backtest/01M1GTNK25PJC0J19WKQ6GKQXK) |
| E20b | CONTROL: same, but the coil keeps its 1:10 RATIO instead of wall-clock | **REVERTED.** Trades 5->9, so the coil was part of it -- but PF fell to 0.951 and 9 is still far below 32 · [report](https://mcp-api.trader.dev/backtest/01M1GTQ6BGVNPYGKX1AQAHQA39) |
| E21 | Macro trend filter: close above a 14400-bar EMA (~10 days) | **REVERTED.** PF 1.686->1.043, win 56.25%->38.89%, trades 32->18. Macro trend does NOT explain the concentration · [report](https://mcp-api.trader.dev/backtest/01M1GV425K3361APZQJ6BR9K24) |
| E22 | SENSITIVITY: coilK 0.85 -> 0.95 | **Degrades gracefully.** PF 1.686->1.300, win 56.25%->48.78%, trades 32->41, DD 3.10%->4.72%. Second parameter, second graceful result · [report](https://mcp-api.trader.dev/backtest/01M1GVATYA8Z4TR2VB58V9XHTT) |
| E23 | SENSITIVITY: velK 0.8 -> 0.6 | **Degrades gracefully, best of the three.** PF 1.686->1.458, win 56.25%->50.00%, trades 32->46, Sharpe 2.07 · [report](https://mcp-api.trader.dev/backtest/01M1GVMZZQ8JPNCPD7XV07WNYC) |
| E24 | velK 0.6 variant measured on the WEAK half only | **No rescue.** PF 0.8745 on 25 trades against the champion's own 0.8930 on 15. Loosening buys trades, not edge · [report](https://mcp-api.trader.dev/backtest/01M1GVTAJEFTNTP0EHED3XMF1N) |
| E25 | Rejection short + cycle gate, target 1R instead of 2R | **PF 0.489, 24 trades. COMPARISON CONFOUNDED** -- E13 made 39 trades, so the entry differs; E13 was rebuilt from prose, not source · [report](https://mcp-api.trader.dev/backtest/01M1GW8GZXNDHCXCAED1G87A17) |
| E26 | E13's EXACT source, one input changed: rr 1.5 -> 1.0 | **REVERTED.** PF 0.7490->0.6922, win 23.08%->27.03%, trades 39->37. Nearer target HURTS this short · [report](https://mcp-api.trader.dev/backtest/01M1GWGDZ6NDSF9H66YF7S7HZP) |
| E27 | Sweep-and-reject short: genuine BREAK above the 15m high, then close back below | **REVERTED.** PF 0.2531, win 10.53%, 19 trades, against E13's 0.7490 on 39. The sweep is WORSE than the near-touch · [report](https://mcp-api.trader.dev/backtest/01M1GWQ2NSQ5SBP1PDP4ZDC739) |

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


## E17 LESSON — CHECK WHETHER A CONSTRAINT *BINDS* BEFORE CALLING IT A DEVIATION
Every pre-run audit in this lab carried the same warning: the champion runs a 0.15% risk floor
against HARD LESSON 3's 0.8%. Raising it produced results **identical to nine significant figures** —
PF 1.68623784, net +7.8388076%, DD 3.10289714%, 32 trades, 56.25% win rate.

**The floor never bound.** The structural stop — the distance to the current 15m low plus a 0.25×ATR30
buffer — is always at least 0.80% of price on this timeframe. The champion was Lesson 3 compliant in
behaviour the whole time; only the *input* looked non-compliant.

Two things follow, and the second matters more than the first:
1. The 0.80% value is adopted as the documented config. Zero cost, and the code now states its real
   risk floor instead of a number that never applied.
2. **The audit habit needed fixing.** Reporting a parameter as a deviation without checking whether
   it ever engages is reporting on the source code rather than on the strategy. Cheap to check —
   plot the raw versus applied value — and it would have retired this warning several cycles ago.


## E18 LESSON — WHAT WORKED IN THE BTC LAB DOES NOT TRANSFER HERE
The BTC lab's only KEPT change this sprint was restricting entries to high volatility. Applied to
this champion it cut PF from 1.69 to 1.10 and kept only 7 of 32 trades.

**So the standing open problem is still open.** The edge concentration — PF 3.80 from December to
February against 0.89 from February to May — is **not** a volatility regime. High volatility does not
select the good period.

**Why the transfer failed is the useful part.** The BTC signal is a VWAP mean-reversion with a fixed
2R target: it needs price to *travel*, so volatility is exactly the variable that decides whether the
target is reached before the time stop. This one is a multi-timeframe momentum cascade whose entries
are already gated on a volatility *contraction* (the 3m coil). Asking for high ambient volatility and
a local coil at the same time is close to the redundancy trap of E14 — and the trade count collapse
from 32 to 7 is what that looks like.

**Record this so a later cycle does not assume a cross-lab result should carry.** Two strategies that
both trade BTCUSDT can still have opposite relationships to the same variable.


## E19 — THE FIRST GOOD NEWS ABOUT THE CHAMPION'S ROBUSTNESS
A 32-trade champion is only as trustworthy as its behaviour at neighbouring parameter values.
Loosening the 6h regime by one candle:

| | greenBull 4 (champion) | greenBull 3 |
|---|---|---|
| Profit factor | 1.686 | 1.282 |
| Win rate | 56.25% | 47.62% |
| Max drawdown | 3.10% | 4.79% |
| Trades | 32 | 42 |

**It degrades; it does not collapse.** PF stays well above 1.0 on a 31% larger sample. A fitted
artefact would have fallen below break-even at the adjacent value — this did not.

The champion keeps `greenBull = 4` because it is better on both ratchet terms, but **confidence in
the 32-trade result is materially higher than it was**, and that is worth more than another failed
filter. Sensitivity in the other direction (`greenBull = 5`) is still owed, as is `coilK`.


## E20/E20b LESSON — THIS STRATEGY NEEDS 1m ENTRY PRECISION, AND THE BTC RESULT DOES NOT TRANSFER

The BTC lab had just found that moving a strategy to a faster timeframe mattered more than any entry
filter. The reverse question here — would this champion do better SLOWER — is answered no, and the
control says why.

| | Champion (1m) | E20 (5m, wall-clock coil) | E20b (5m, ratio coil) |
|---|---|---|---|
| Profit factor | **1.686** | 1.621 | 0.951 |
| Max drawdown | 3.10% | 2.73% | 3.57% |
| Trades | **32** | 5 | 9 |

**The control did its job and split the cause.** Fixing the coil approximation raised trades from 5 to
9, so that parameter genuinely was suppressing frequency — naming it in the Pine header before the run
was correct. But 9 against 32 means **roughly three quarters of the loss is the timeframe itself.**

**The mechanism is the entry trigger.** The champion enters on `ta.crossover(close, p15l)` — a reclaim
of the previous 15m low. On a 1m chart there are fifteen opportunities per 15m candle to catch that
crossover; on 5m there are three. The cascade *identifies* the level on higher timeframes, but the
*entry* needs 1m granularity to catch the reclaim of it.

**Two strategies on the same instrument, opposite relationships to the same variable.** The BTC signal
is a mean-reversion needing price to travel to a fixed target, so coarser bars and longer horizons
help it. This one needs precision at a level, so coarser bars destroy it. **A cross-lab finding is a
hypothesis, never an inheritance** — the same caution E18 established, now confirmed from the other
direction.

**Consequence for the lab's biggest problem:** the sample-size constraint is NOT solvable by changing
timeframe. 1m coverage starting 2025-12-16 is a hard limit, and 32 trades is what this champion gets
until the engine's history extends. Robustness must therefore come from parameter sensitivity (E19's
approach) rather than from a bigger sample.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


## E21 — HYPOTHESIS TWO ELIMINATED, AND THE MYSTERY GETS MORE INTERESTING
The champion has no long-horizon trend filter, so a ten-day EMA was genuinely new information rather
than a redundancy trap. If the edge concentration were a macro uptrend, that filter should have kept
the December-to-February trades and dropped the February-to-May ones.

It did the opposite: PF 1.686 -> 1.043, win rate 56.25% -> 38.89%, trades 32 -> 18. Nearly half the
trades removed and the survivors markedly worse — the anti-selective signature of E14 and E16.

**Both hypotheses are now dead:**
| Hypothesis | Experiment | Verdict |
|---|---|---|
| Volatility regime | E18 | Ruled out — PF 1.69 → 1.10, kept only 7 of 32 |
| Macro trend | E21 | Ruled out — PF 1.69 → 1.04, kept 18 of 32 |

### THE IMPORTANT NEW OBSERVATION — IT MAY NOT BE THIS STRATEGY AT ALL
The BTC lab measured the same window this hour, on a completely different mechanism, and found the
same shape: its 5m base scores **1.0202 over 2.2 years but 0.8753 over this identical Dec-May
window.**

**Two unrelated strategies, one long-only 1m momentum cascade and one 5m VWAP mean-reversion, both
degrade in the same months.** That points at something in the market during that period rather than
at a property of either strategy — and it means the question has been framed wrongly. The right next
probe is a **calendar decomposition** of the champion (month by month, and both labs side by side),
which is a measurement, not another filter. Every filter tried so far has failed for the same reason:
filters select on a *proxy*, and no proxy has matched whatever the calendar is actually marking.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


## E22 — THE CHAMPION HAS NOW SURVIVED TWO INDEPENDENT PERTURBATIONS

| Parameter | Champion | Perturbed | PF | Trades |
|---|---|---|---|---|
| greenBull (E19) | 4 | 3 | 1.686 → 1.282 | 32 → 42 |
| coilK (E22) | 0.85 | 0.95 | 1.686 → 1.300 | 32 → 41 |

Both degrade gracefully and both stay clearly above 1.0 on larger samples. **coilK matters more than
greenBull did**, because 0.85 was *chosen* rather than derived — it is the most arbitrary number in
the build, and a fitted artefact would have been most fragile exactly there.

This is the strongest evidence the champion has, and it is the right kind: with the sample fixed at
32 trades by the 1m coverage limit (E20 proved the timeframe cannot be changed to fix that),
**robustness under perturbation is the only defence available.** `velK` is the remaining untested
parameter.

**The concentration question, meanwhile, has moved out of this lab.** The BTC lab's period
decomposition this hour found its own base runs PF 1.36 in Jun 2024 – Jul 2025 against 0.88 in
Dec 2025 – May 2026. Two unrelated mechanisms decaying in the same window points at the market, not
at either strategy — which is why E18's volatility filter and E21's trend filter both failed. Stop
looking for a filter that explains it.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


## THE SENSITIVITY SUITE IS COMPLETE — AND THE CHAMPION PASSES ALL THREE

| Parameter | Champion | Perturbed | PF | Trades | Sample change |
|---|---|---|---|---|---|
| greenBull (E19) | 4 | 3 | 1.686 → 1.282 | 32 → 42 | +31% |
| coilK (E22) | 0.85 | 0.95 | 1.686 → 1.300 | 32 → 41 | +28% |
| velK (E23) | 0.8 | 0.6 | 1.686 → **1.458** | 32 → 46 | +44% |

**Every parameter perturbation stays clearly above 1.0 while enlarging the sample by 28–44%.** That is
what a real edge looks like under perturbation; a curve fit collapses at its neighbours, and this
does not. It is also the only evidence available — the sample is fixed at 32 trades by 1m coverage,
and E20 proved the timeframe cannot be changed to grow it.

**Put this beside what just happened in the BTC lab.** Its base scored PF 1.36 in the first half of
its sample and **0.66 in the second**, so its full-sample 1.02 was an average of a good year and a
bad one. That is exactly the failure mode this champion has NOT been tested against, because 1m
coverage is only 4.6 months and cannot be split meaningfully.

**So the honest position on the champion is:** robust to parameter perturbation, unproven across
time, and untestable across time with the data available. Those are three different statements and
the log should keep them apart.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


## CORRECTION — THE CHAMPION IS NOT "UNTESTABLE ACROSS TIME". IT WAS ALREADY TESTED, AND IT SHOWS THE SAME DECAY.
The previous entry described the champion as robust to perturbation but *untestable* across time.
**That was wrong, and the data was already in this repo.** `results/backtests.json` holds
`war-formation-v6-half1` and `war-formation-v6-half2`:

| Half | PF | Win rate | Trades |
|---|---|---|---|
| Dec 16 – Feb 23 | **3.797** | 70.59% | 17 |
| Feb 23 – May 3 | **0.893** | 40.00% | 15 |
| Full | 1.686 | 56.25% | 32 |

**The champion's 1.686 is an average of a very strong period and a break-even one — precisely the
structure the BTC base was just condemned for.** The two labs are in the same position, and this log
should have said so a cycle earlier.

## E24 — AND LOOSENING DOES NOT RECOVER THE WEAK HALF
E23's velK 0.6 variant carried 46 trades against 32 on the full sample and had the best profit factor
of the three perturbations, so it was the natural candidate to test where it matters:

| Weak half, Feb 23 – May 3 | PF | Trades |
|---|---|---|
| Champion (velK 0.8) | 0.8930 | 15 |
| velK 0.6 variant | 0.8745 | 25 |

**Indistinguishable, and both just under break-even.** 67% more trades in that window, none of them
better. The weakness is in the signal, not the threshold.

### Where this leaves the champion, stated in three separate parts
1. **Robust to parameter perturbation** on the full sample — E19, E22, E23 all degrade gracefully.
2. **NOT robust across time** — 3.80 then 0.89, and E24 shows no parameter setting recovers the second half.
3. **The full-sample 1.686 should not be quoted alone**, for the same reason the BTC lab's 1.02 should not be.

The sensitivity line of enquiry is now closed. What remains genuinely unexplored is the **short leg**,
built from its own geometry with the E13 cycle-position gate — the only route to a return stream that
does not depend on this decaying long signal.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


## E25 — A CONFOUNDED TEST, AND A RULE THAT SHOULD HAVE PREVENTED IT
The run was designed as a single-variable change from E13: target 2R to 1R, everything else identical.
**It was not.** E13 made 39 trades; this made 24. An exit change cannot move the entry count by 38%,
so the entry logic differs — **E13 was rebuilt from its written description rather than from its Pine
source.**

**The rr hypothesis is therefore untested.** PF 0.4894 is a real number for what was actually run, and
nothing more. It says nothing about whether a fade wants a nearer target.

**This exact error was caught and avoided earlier the same session.** When the BTC lab needed its 007
base for a single-variable attack, the exact Pine was recovered with `get_strategy` precisely because
reconstructing from prose risked a two-variable change. The tool existed, the precedent existed, and
it was not applied here.

**STANDING RULE, both labs:** when a run claims to be a single-variable change from an earlier
experiment, recover that experiment's **SOURCE**, never its description. A trade-count mismatch
between the two is the tell that the claim is false — check it before interpreting anything.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


## E26 — THE SOURCE-RECOVERY RULE PAID FOR ITSELF IMMEDIATELY
Recovering E13's Pine with `get_strategy` instead of rebuilding it caught **two** errors in E25 that
had gone unnoticed:

1. **E13 used `rr = 1.5`, not 2.0.** E25's write-up asserted 2.0, so even its stated baseline was wrong.
2. **E25's reconstructed entry made 24 trades against E13's 39.** The entry was never the same.

**The trade-count check is the discriminator, and it works.** E26 returns 37 against E13's 39 — close,
with the small gap explained by a 1R trade closing at a different moment and blocking or unblocking a
few later signals. That is what a genuine exit-only change looks like. A 38% count collapse is not.

### The result itself
| | E13 (rr 1.5) | E26 (rr 1.0) |
|---|---|---|
| Profit factor | **0.7490** | 0.6922 |
| Win rate | 23.08% | 27.03% |
| Trades | 39 | 37 |

More winners, smaller ones, net worse. **The nearer target hurts this short**, and E13's 1.5 stays the
best short configuration this lab has.

### THIRD CROSS-LAB NON-TRANSFER
The identical change — target 2R/1.5R down to 1R — **improved** the BTC lab's short leg (0.5506 to
0.5816, win rate 17.65% to 29.41%) and **worsened** this one. Added to E18's volatility filter and
E20's timeframe translation, that is three for three: **nothing has ever transferred between these
labs.** Exit convention follows the mechanism, and a finding from one strategy is a hypothesis for
another, never an inheritance.

**Champion unchanged: v6, long-only, PF 1.68623784, DD 3.10289714%, 32 trades.**


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


## E27 — A REAL ASYMMETRY BETWEEN THE TWO SIDES
The long's whole edge is the failure of a GENUINE breakdown: price takes out the previous 15m low,
then reclaims it. Applying that same mechanism at a high produced the worst short yet.

| Short construction | PF | Win rate | Trades |
|---|---|---|---|
| E13 — near-touch of resistance, then reject | **0.7490** | 23.08% | 39 |
| E27 — genuine break above, then reject | 0.2531 | 10.53% | 19 |

**Requiring price to actually clear resistance makes shorts markedly worse; requiring it merely to
approach makes them better.** A plausible reading: in a downtrend, price clearing resistance is more
often continuation than exhaustion, while failing to reach it is the mark of a weak rally. Whatever
the cause, the two sides are not symmetric in this respect, and E13's near-touch stands.

## ██ DESIGN CLARIFICATION FROM THE USER — WAR FORMATION IS ONE BIDIRECTIONAL STRATEGY
**"It all depends on the higher time frames. That's what makes the entries longs or shorts."**

The 6h/1h cascade decides the SIDE; the 15m/3m/1m mechanics execute in that direction. **The v6
champion is long-only and is therefore an INCOMPLETE implementation, not a finished strategy** — the
log will describe it that way from now on.

Every short experiment so far treated the short as a separate system to design. Under this framing
that was the wrong approach. The reconciliation with the no-mirror rule is recorded in
ORACLE-RULES.md: the rule is downgraded from *never symmetric* to **never symmetric without solving
location for the short side**, because E13 showed the cycle-position gate is exactly what the short
needs and the long gets for free.

**Next build: ONE strategy, long when the 6h is bullish, short when it is bearish, cycle-position gate
on the short side, both legs reported separately.**
