# LEGACY FOREX TRADER — FORWARD-TEST PROTOCOL

> Research specification. Not trade recommendations. Nothing here has been run.

**Written 2026-09-06.** Nineteen ticks established that this system cannot be backtested honestly on
any engine reachable from this project. This is the specification for the one route that remains, laid
out in advance so that when it is run the result means something — and so that it cannot be quietly
abandoned or reinterpreted halfway.

---

## WHY THIS IS THE ONLY ROUTE — ALL FOUR BLOCKERS ARE BACKTEST-SPECIFIC

| Blocker | Why forward testing dissolves it |
|---|---|
| **Instrument** — `NQ`/`YM` silently remap to crypto perps; `NAS100`/`US30` are cash proxies | You watch **actual NQ and YM**. No symbol resolution layer exists to get it wrong. |
| **Intra-bar resolution** — his trades resolve inside one 5m bar, so a backtester must *guess* whether stop or target came first | **Live fills have real sequence.** The ambiguity is an artefact of compressing time into OHLC; forward, time is not compressed. |
| **15m execution** — `run_backtest` errors on NAS100 15m | **No engine is involved.** |
| **Data quality** — Yahoo intraday is patchy and silently gapped | **Live feed.** No retention limit, no silent revision. |

**Every blocker in this workstream is a property of backtesting it, not of the method.** That is an
unusual and genuinely favourable position: the method is untestable *backwards* and perfectly testable
*forwards*.

The research adds one more advantage, which matters given how this project has been burned: forward
testing **eliminates forward bias entirely**, because *"you are trading live data that has not happened
yet."* Manual backtesting does not — *"when you're scrolling through a chart and can see what happens
next, your brain unconsciously skips trades that would lose"*, and after 50 trades even minor forward
bias can show *"a 60% win rate when the real number is 45%."*

---

## THE SAMPLE TARGETS, PRE-REGISTERED

Practitioner guidance is specific, and it is stricter than this project's own 30-trade floor:

> *"Ten trades tell you almost nothing."* · *"30 trades represents the bare minimum to start seeing
> patterns."* · **"A forward test is statistically valid when it reaches at least 100 trades with no
> rule changes."**

| Milestone | Trades | Status at that point |
|---|---|---|
| Checkpoint | **30** | Bare minimum. Report only. **No decision may be taken here.** |
| **Decision point** | **100** | The first point at which a verdict is permitted. |

**Combined with the expectancy literature already recorded** — *"below 50 trades, expectancy is
dominated by the randomness of a few outlier wins or losses"* — **100 is the number, not 30.**

### ⚠️ CORRECTED BY TICK #22, 2026-09-06 — 100 IS RETAINED, BUT IT BUYS FAR LESS THAN THIS SECTION CLAIMED

**The quoted "statistically valid at 100 trades" is practitioner folklore and this section inherited it
without checking.** Tick #22 computed what n=100 can actually decide (STATUS.md Findings 28–30, exact
binomial plus Monte Carlo, both reproducible; no source states this — it is this lab's own derivation):

| At his decoded 3R target | n=100 delivers |
|---|---|
| Smallest true PF detectable at 80% power, 5% level | **1.73** — a very large edge |
| Power against a true PF of 1.3 | **0.307** — misses a real edge ~69% of the time |
| Trades needed for 80% power vs true PF 1.3 | **460** ≈ 22 months at 1/day, **3.7 years** at 0.5/day |

**100 is kept as the decision point because the calendar alternative is multi-year** — but it is kept
with its limits stated, not as a validity threshold. **A pass at n=100 licenses "worth continuing",
never "validated"**, and a *failure* at n=100 rules out only large edges, not modest ones.

## THE TIMELINE, STATED HONESTLY UP FRONT

His rules cap trades at **2 per day**, and his no-trade rules (consolidation, no volume, *"you may miss
three days in a row"*) remove many sessions entirely.

| Realised rate | Sessions to 100 trades | Calendar |
|---|---|---|
| 1.0 / day | 100 | ~5 months |
| 0.5 / day | 200 | ~10 months |

The research says the same: *"forward testing requires weeks or months to accumulate just 20 to 30
trades."* **This is a multi-month commitment and should not be started under the impression it is
quick.** Recording that here is the point — the most common failure is starting one and abandoning it.

---

## THE STOPPING RULE, WHICH IS THE PART THAT USUALLY FAILS

> *"Many traders cut their forward test far too early after only five or ten trades based on a feeling
> rather than solid statistics, and a shortened forward test adds almost no extra guarantee over the
> backtest alone."*

**Binding rules, fixed before any signal is recorded:**

1. **No rule changes during the test.** Any change to the strategy, its parameters, the instruments or
   the session window **resets the trade count to zero.** A forward test with mid-flight edits measures
   nothing.
2. **No early verdict.** Results below 100 trades are *reported*, never *decided on*. A run stopped at
   30 because it looked good or bad produces no verdict at all — that is the recorded outcome.
3. **Abandonment is a result and gets written down.** If the test stops, `STATUS.md` records how many
   trades were reached and why. Silence is not permitted.

## THE DECISION CRITERIA, PRE-REGISTERED

At 100 trades, and not before, the method is judged on:

> **⚠️ THE FIRST ROW OF THIS TABLE WAS WITHDRAWN BY TICK #22 AND REPLACED BELOW.** `PF > 1.0` applied
> to a point estimate accepts a **zero-edge** system roughly **half the time**, at *every* sample size —
> 0.4465 at n=100 and 0.4880 at n=2000 for a 3R payoff, exact binomial, and 0.49–0.53 under Monte Carlo
> over his real ladder anatomy. **More trades does not fix it; the rate converges to 50%.** The
> superseded table is kept visible so the correction cannot be read as though it had always said this.

| Criterion | ~~Threshold~~ **WITHDRAWN** | Source |
|---|---|---|
| Profit factor | ~~> 1.0 net of costs~~ | RATCHET v2 clause 1 |
| Sample | ≥ 100 | this protocol, stricter than the project's 30 floor |
| **Cost hurdle** | must clear **~2% of capital per fortnight** at his trade cap | measured, tick #19 |
| Expectancy per trade | positive **gross of commission** | the gross-edge screen |
| Implied t | Sharpe × √years, reported | the board audit's standard |

### THE REPLACEMENT PROFIT-FACTOR RULE — PRE-REGISTERED, TICK #22

**The threshold depends on the payoff actually realised, so it is computed at judgement time, not
guessed now.** Let `b` = the mean R of winning trades and `n` = trades reached. Then:

1. **Compute the break-even win rate** `p₀ = 1/(1+b)`, and the critical win count `k` — the smallest
   `k` with `P(W ≥ k | n, p₀) ≤ 0.05` under the binomial. **Reject unless wins ≥ `k`.** For reference,
   at n=100 this is an observed PF of roughly **1.44 (b=1) / 1.45 (b=2) / 1.48 (b=3) / 1.56 (b=4)** —
   not 1.0.
2. **Report a bootstrap confidence interval on profit factor, never the point estimate alone**, and
   quote the **lower bound** as the conservative figure. BCa bootstrap on the realised R-multiples;
   this is standard practice, not an invention (PyBroker implements exactly this).
3. **State the power of the test actually run**, against a true PF of 1.3 and 1.5, alongside the
   verdict. A "fail" whose power was 0.31 is not evidence the method is worthless — say so in the
   same sentence as the verdict.
4. **The cost hurdle and the gross-expectancy screen are unchanged** and remain the criteria most
   likely to bind first.

**The asymmetry to hold onto:** a PF threshold at 1.0 used to **accept** is ~50% false-positive and is
therefore forbidden here. Used to **reject** — as this project's KILL RULE does — the same coin flip
falls in the conservative direction: it discards good systems rather than banking worthless ones. The
kill rule is untouched by this correction.

**The cost hurdle is the one most likely to bind.** Tick #19 measured that trading this instrument at
5m cost **4.3% of capital in sixteen days at 46 trades**; at his 2-trade cap that is roughly **2% per
fortnight**. Against 1:3–1:5 targets on ~25-point stops, cost is the dominant term, not a rounding
error.

---

## WHAT TO RECORD PER SIGNAL

`legacy-forex/pine/VISUAL-legacy-forex-complete.pine` fires two alerts — **`Legacy LONG`** and
**`Legacy SHORT`** — and exposes **57 data-window fields**. For each signal record:

| Field | Why |
|---|---|
| Timestamp, instrument (NQ or YM), direction | identity |
| Entry, stop, and each target rung actually reached | the ladder, not just a single target |
| Minutes from entry to each rung | tests tick #14's finding that trades resolve in 12–190 seconds |
| **`IntraBarAmbiguity` at entry** | whether a backtest of that bar *would* have had to guess — the direct measurement of the blocker |
| Structure state, volume state, trade number of the day | which gate was actually doing the work |
| Whether the day was a **no-trade day**, and why | his no-trade rule is a rule; skipped days are data |

**The `IntraBarAmbiguity` field is the one this project needs most.** It converts tick #17's abstract
blocker into a measured frequency: *what fraction of his real signals would a bar-data backtest have
had to guess?* No other workstream can produce that number.

## WHAT THIS PROTOCOL CANNOT FIX

- **Execution under real pressure.** *"With no real money on the line in paper trading, the
  psychological pressure is completely different."* A forward test validates mechanics, not the
  trader's ability to follow them.
- **The multiple-testing hurdle.** 100 forward trades is one clean test — but it is a test of a
  hypothesis fixed in advance, which is exactly why it carries no mining penalty. That is its main
  statistical advantage over everything else in this repository.
- **His prop-firm claims.** Out of scope, and never in it.

## STATUS

**NOT STARTED.** No signal has been recorded. This document is the specification only, and no number
will be written into it that did not come from an observed live signal.
