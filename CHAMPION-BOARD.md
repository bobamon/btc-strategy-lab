# BTC Lab — Champion Board

The lab's mandate changed on **2026-09-02**. Read this before the ledger.

> Research specifications for backtesting. Not trade recommendations.

## Why the mandate changed
Seven discovery cycles produced seven rejections:

| # | Strategy | PF |
|---|---|---|
| 002 | Variance-Ratio Regime Switch | 0.60 |
| 003 | Liquidation Cascade Reclaim | 0.69 |
| 004 | Moving-Average Retest Fade | 0.65 |
| 005 | Compression Release Volume Verdict | 0.52 |
| 006 | Volatility Term-Structure Regime | 1.04 → 0.36 on 5m |
| 007 | VWAP Value Migration | 0.89 |

Meanwhile the only thing in this project that has ever worked is the **War Formation v6** — PF 1.69 —
and it is **not a single mechanism**. It is five stacked filters, and the ablation proved the stack
*is* the edge: strip the cascade and PF collapses 1.40 → 0.68.

**The old mandate — "one genuinely new mechanism per cycle" — structurally cannot produce what
actually worked**, because a cascade is several mechanisms combined. So it is retired.

## THE NEW MANDATE — stack, measure, keep what earns its place
Each cycle takes the current **base** and changes **exactly one thing**: add a filter, remove a
filter, or alter one parameter. Then it runs the ladder and decides on evidence.

**A change is KEPT only if it improves profit factor AND does not worsen max drawdown.**

> **OPEN RULE QUESTION (raised by Attack 3, 2026-09-02).** Attack 3 improved PF 0.9121→0.9405 — the
> largest gain of any attack — but worsened drawdown by **0.064 percentage points**, so a strict
> reading reverted it. A tolerance band (allow DD to worsen by up to ~0.5pp when PF improves by more
> than 0.02) would have kept it. Changing the ratchet is a decision for the user, not for a cycle to
> make on its own. Until then the strict rule stands.
Anything else is reverted and recorded as tried. This is the ratchet that makes the lab get better
instead of merely different.

Every cycle must still satisfy the standing objectives (both directions built separately, an explicit
regime-flip response, legs reported separately) and every hard lesson in `STRATEGY-LEDGER.md`.

## CURRENT CHAMPION
**None yet.** Nothing has cleared the ladder (PF >= 0.95 on 15m, then 5m, then sensitivity).
The board is open.

## RATCHET PROGRESS
| Cycle | Base PF | Base DD | New PF | New DD | Verdict |
|---|---|---|---|---|---|
| Attack 1 — EMA200 trend filter | 0.89 | 35.0% | **0.91** | **28.8%** | **KEPT** |
| Attack 2 — shallow pullback | 0.91 | 28.8% | 0.85 | 32.6% | **REVERTED** |
| Attack 3 — witching-hour ban | 0.9121 | 28.780% | **0.9405** | 28.844% | **REVERTED** — borderline, see note |
| Attack 4 — R floor 0.8% → 1.2% | 0.9121 | 28.8% | 0.8845 | 36.6% | **REVERTED** |
| Attack 5 — volume confirmation | 0.9121 | 28.8% | 0.8392 | **26.9%** | **REVERTED** — PF is the binding term |
| Attack 7 — target 2R → 3R | 0.9121 | 28.8% | 0.9100 | 33.0% | **REVERTED** — PF flat, DD worse |
| **Regime split — high-vol only** | 0.9121 | 28.8% | **0.9321** | **23.4%** | **KEPT** — both terms improved |
| Regime split — low-vol complement | 0.9121 | 28.8% | 0.8751 | 23.1% | measurement only, not a candidate |
| **Attack 3 re-test — witching ban on high-vol base** | 0.9321 | 23.43% | **0.9640** | **22.61%** | **KEPT** — both terms strictly improved |
| **Move the base to 5m (scaled)** | 0.9615 | 21.33% | **1.0202** | **16.68%** | **KEPT** — like-for-like, both terms improved |
| Move the base to 1m (scaled x15) | 0.8753 | 6.63% | 0.7521 | 6.73% | **REVERTED** — worse than 5m on identical data |

## CURRENT BASE — what cycle 008 starts from
**007's LONG leg.** It has the best raw hit rate of anything tested in this lab: **38.3%** across 457
trades before costs, against a break-even of ~36% at its 1.76:1 payoff. It failed on *cost drag*
(18% of gross profit), not on signal quality — 564 trades was too many for the edge it had.

That makes it the right raw material: a signal that is nearly good enough, failing for a reason we
know how to attack.

**Base definition (updated after the high-volatility regime split, 2026-09-02):** VWAP with 2σ bands. Long only for now. Price stretched
to +2σ within the last 50 bars, then pulls back to within 0.5σ of VWAP and closes back above it,
while VWAP is rising over 50 bars, **close is above the 200-period EMA, and ATR14/close is above its own 200-bar average
(the high-volatility regime), and the bar is NOT inside the 1-4am ET witching window**. Stop at the 20-bar
swing low − 0.25×ATR14, floored at 0.8% of price, target 2R, both fixed at entry. Flip signal: close
crossing VWAP, stand down 20 bars.

**Current base numbers:** PF 0.9640 · max DD 22.61% · 271 trades · win rate 39.11% · net −6.5%
(updated after attack 3 was re-tested and kept). Previous: PF 0.9321 · DD 23.43% · 279 trades · net −12.7%. Older still:
(BTCUSDT 15m, 2022-01-01 → 2026-09-01). Previous base was PF 0.9121 / DD 28.78% / 433 trades.

## ⚠️ THE FEE-DRAG THESIS IS FALSIFIED (2026-09-02, after Attack 5)
This list was built on one diagnosis: *the base loses to fee drag, so cut trade count without cutting
edge.* **Five attacks in, the evidence says that diagnosis is wrong.** Sort them by how many trades
they removed:

| Attack | Trades removed | PF effect |
|---|---|---|
| 3 — witching ban | 13 (3%) | **0.9121 → 0.9405 (best gain)** |
| 1 — EMA200 | 35 (7%) | **0.89 → 0.91 (kept)** |
| 4 — wider R floor | 20 (5%), but enlarged every loss | 0.912 → 0.885 |
| 2 — shallow pullback | 91 (21%) | 0.91 → 0.85 |
| 5 — volume confirmation | 192 (44%) | 0.912 → 0.839 |

**The relationship is monotonic and it runs the wrong way.** Small, targeted cuts help; large cuts
hurt, in proportion to their size. Attack 5 is the decisive case: it delivered precisely the fee
saving the thesis called for — commission halved, $3,954 → $2,078 — and net return still fell from
−23.0% to −25.4%. You cannot save your way to an edge here.

**What that means.** The base is **signal-limited, not cost-limited.** Every broad filter prunes
winners and losers at roughly the same rate (win rate held at ~38% through all five attacks, moving
less than a point), so it removes gross profit as fast as it removes cost. Fee drag is real, but it
is a symptom of a signal that is only marginally profitable before costs, not the disease.

**Revised mandate for the next cycles:** stop pruning. The remaining moves must either (a) raise the
payoff ratio on the trades already taken — the exit, not the entry, since `avgWin/avgLoss` 1.50 is
what actually carries this system — or (b) add a genuinely uncorrelated second source of return,
which is what the short rebuild is. Any further proposal whose mechanism is "take fewer trades"
should be rejected without spending a credit on it.

## THE ATTACK — ranked, one per cycle
*(Items 1–5 were written under the now-falsified fee-drag thesis. Kept for the record.)*

1. ~~Add a trend filter (EMA200)~~ — **DONE, KEPT.** PF 0.89→0.91, DD 35.0%→28.8%. Now part of the base.
2. ~~Require the pullback to be shallow~~ — **DONE, REVERTED.** PF 0.91→0.85, DD 28.8%→32.6%.
   The deep retrace is where the edge lives; excluding it removed good trades.
3. ~~Add the time-of-day filter (1–4am ET witching ban)~~ — **DONE, REVERTED on a technicality.**
   PF 0.9121→0.9405 (best gain yet) but DD 28.780%→28.844%, a 0.064pp worsening. Worth re-running
   if the user approves a drawdown tolerance band.
4. ~~Raise the R floor from 0.8% to 1.2%~~ — **DONE, REVERTED.** PF 0.912→0.885, DD 28.8%→36.6%.
   Fee drag fell and win rate rose, but every loss got bigger and that dominated. 0.8% is nearer the
   optimum than 1.2%.
5. ~~Require volume confirmation on the pullback hold~~ — **DONE, REVERTED.** PF 0.9121→0.8392,
   DD 28.8%→26.9%. Cut trades 433→241 and halved commission $3,954→$2,078, and net return still got
   *worse*. The low-volume reclaims were the better trades.
6. **NOW THE TOP ITEM — rebuild a short leg** (promoted by the falsification above: it adds a return
   source rather than pruning one) on whatever survives, judged on its own profit factor
   (the mistake in 005 and E9 was bolting on a second leg before the first was sound).

## TRIED AND REVERTED
*(nothing yet — this table is the memory that stops a reverted change being retried)*

| Cycle | Change to the base | Result | Kept? |
|---|---|---|---|
| Attack 22 | `coolBars` 60 → 30 | PF 1.1525→1.0034, DD 16.54%→22.52%, trades 166→231 | **REVERTED** — half the stand-down is almost exactly break-even |
| Attack 23 | `coolBars` 60 → 120 | PF 1.1525→**1.3038**, DD 16.54%→**8.12%**, trades 166→77 | **KEPT — the new base.** Largest ratchet pass in this lab |
| Attack 24 | `coolBars` 120 → 240 | PF 2.3023, DD 2.00%, **7 trades** | **REJECTED as uninterpretable** — not as worse |
| Attack 1 | Require close above EMA200 | PF 0.89→0.91, DD 35.0%→28.8%, trades 468→433 | **KEPT** |
| Attack 2 | Require shallow pullback (low holds above VWAP) | PF 0.91→0.85, DD 28.8%→32.6%, trades 433→342 | **REVERTED** — worse on both terms |
| Attack 3 | Ban entries in the 1–4am ET witching window | PF 0.9121→0.9405, DD 28.780%→28.844%, trades 433→420 | **REVERTED** — PF up, DD worse by 0.064pp |
| Attack 4 | Raise R floor 0.8% → 1.2% | PF 0.912→0.885, DD 28.8%→36.6%, win rate 38.3%→40.2% | **REVERTED** — wider stops mean bigger losses |
| Attack 5 | Require volume above the 50-bar average on the reclaim | PF 0.912→0.839, DD 28.8%→26.9%, trades 433→241, commission $3,954→$2,078 | **REVERTED** — fee saving realised, edge lost with it |
| Attack 7 | Raise the target 2R → 3R | PF 0.9121→0.9100, DD 28.8%→33.0%, payoff 1.498→1.787, win rate 38.3%→33.7% | **REVERTED** — payoff gain exactly cancelled by win-rate loss |
| Attack 8 | Short leg 5m → 15m, every bar parameter /3 | PF 0.7413→0.5995, DD 34.40%→50.60%, trades 273→270 | **REVERTED** — the short's timeframe curve runs the OTHER way |
| Attack 9 | Remove the EMA200 filter, measured in H2 alone | PF 0.65656→0.66177, DD 12.66%→16.06%, trades 61→64 | **REVERTED** — but the filter is nearly INERT in H2 |
| Attack 10 | Remove the highVol split, measured in H2 alone | PF 0.65656→**0.76511**, DD 12.66%→19.59%, trades 61→103 | **REVERTED** on drawdown — but the gate is COSTING profit factor |
| Attack 11 | Remove the witching ban, measured in H2 alone | PF 0.65656→0.62814, DD 12.66%→16.54%, trades 61→62 | **REVERTED** — and this one genuinely EARNS its place |
| Attack 12 | Remove highVol, **full sample** (ratchet test of Attack 10) | PF 1.02025→0.91514, DD 16.68%→23.51%, trades 128→207 | **REVERTED** — the gate is regime-dependent, not harmful |
| Attack 13 | Remove EMA200, **full sample** (ratchet test of Attack 9) | PF 1.02025→1.01094, DD 16.68%→17.47%, trades 128→134 | **REVERTED** — genuinely inert, removes 6 trades in 2.2 years |
| Attack 14 | Remove the witching ban, **full sample** | PF 1.02025→0.96113, DD 16.68%→17.92%, trades 128→130 | **REVERTED** — earns its place, and HARD LESSON 12 called it in advance |
| **Attack 15** | **Remove `reachedUpper`, the +2σ stretch — a SIGNAL term, not a gate** | **PF 1.02025→1.15253, DD 16.68%→16.54%, trades 128→166** | ✅ **KEPT — the first change this ratchet has ever accepted** |

7. ~~Attack the EXIT, not the entry~~ — **DONE, REVERTED.** See the frontier note below.
8. **Attack the EXIT, original text:** Every attack so far has been an entry filter. The system lives
   on `avgWin/avgLoss` = 1.50 at a 38% win rate, which needs ~40% to break even. Nothing has yet
   tried to move the payoff ratio on the trades already being taken — a wider target, a partial at
   1R, a time-based exit tuned to the 49-bar average hold. This is the untouched half of the system.


## ⚠️ THE SIGNAL SITS ON AN ISO-PF FRONTIER (2026-09-02, after Attack 7)
Attack 7 raised the target from 2R to 3R. It worked, mechanically and precisely:

| | Base (2R) | 3R target |
|---|---|---|
| avgWin / avgLoss | 1.498 | **1.787** (+19%) |
| Win rate | 38.3% | 33.7% (−4.6pp) |
| Profit factor | 0.9121 | 0.9100 |
| Net return | −23.0% | −23.02% |

**The payoff gain and the win-rate loss cancelled to two decimal places.** The 2R and 3R points lie
on the same iso-profit-factor curve, so moving along the risk-reward axis is *neutral* for this
signal — there is no target setting that rescues it.

**Put this beside the Attack 5 falsification and the picture closes.** Entry selection has been
attacked five times and exit sizing once, and the profit factor has never left the 0.84–0.94 band.
The two halves of a trade are the only two things a parameter can touch. **PF ≈ 0.91 is a property
of the VWAP-reclaim signal itself, not of how it is filtered or harvested.**

**Therefore: stop tuning this base.** No further parameter change on the VWM long leg should be
funded. What remains genuinely untried is a *different source of return*:
- the **short leg**, rebuilt from its own geometry (adds a return stream rather than reshaping one);
- **regime conditioning** — the same signal may have PF well above 1 in one market state and well
  below in another, which the 4.7-year aggregate would hide. That is a measurement, not a filter,
  and it is the one question the lab has never asked of this base.


## THE REGIME SPLIT — THE FIRST THING TO WORK SINCE ATTACK 1 (2026-09-02)
Restricting the base to bars where ATR14/close is above its own 200-bar average:

| | Base | High-vol only |
|---|---|---|
| Profit factor | 0.9121 | **0.9321** |
| Max drawdown | 28.78% | **23.43%** |
| Trades | 433 | 279 |
| Win rate | 38.3% | 38.7% |
| Net return | −23.0% | **−12.7%** |

**KEPT — both ratchet terms improved, no tolerance needed.** Only the second change ever kept.

**Why this is not the pruning that killed attacks 2 and 5.** Those cut trades and the profit factor
fell in proportion. This cut 36% of trades and the profit factor *rose* while the win rate held.
The difference is the kind of thing being removed: a bar-level filter prunes individual signals out
of a population that is uniformly marginal, whereas a regime split separates two populations that
were never the same to begin with. **The 0.9121 aggregate was hiding a mix.**

By construction the low-volatility complement must then be materially worse than 0.9121. It runs
next cycle to close the decomposition and put a number on it.

**Honest limit:** 0.9321 is still below 1.0. This is a better description of *where* the signal
lives, not yet a profitable system. It does, however, reopen a question the falsification had
closed: the earlier attacks were all measured against a base that mixed two regimes, so a filter
that failed on the mixture is not necessarily a filter that fails inside the high-vol regime. The
reverted list stands, but **re-testing the single best of them against the new base is legitimate**
once the decomposition is complete.


## THE DECOMPOSITION IS COMPLETE — AND IT SIZES THE EFFECT HONESTLY (2026-09-02)

| | High-vol (kept) | Low-vol | Old mixed base |
|---|---|---|---|
| Profit factor | **0.9321** | 0.8751 | 0.9121 |
| Win rate | 38.71% | 38.70% | 38.3% |
| avgWin / avgLoss | 1.476 | 1.386 | 1.498 |
| Trades | 279 | 230 | 433 |
| Net return | −12.7% | −15.5% | −23.0% |

**The regime effect is real but modest, and it does not rescue the signal.** A 0.057 gap in profit
factor, with **both halves still below 1.0**. The hypothesis was worth the two credits it cost — it
produced the only KEPT change since attack 1 — but it does not overturn the frontier conclusion.

**The sharpest detail is the win rate: 38.70% vs 38.71%, identical to two decimal places.** Volatility
does not change how *often* this signal is right. The entire difference lives in the payoff ratio,
1.476 vs 1.386 — how far price travels before the fixed 2R target or the 96-bar time stop resolves
the trade. That is consistent with everything else this lab has measured: **the hit rate of the
VWAP-reclaim signal is a hard ~38% that nothing has moved**, through five entry filters, one exit
change and now a regime split.

**Caveat on the arithmetic, stated plainly:** the two halves total 509 trades against the mixed
base's 433. They are not a strict partition — each half runs independently and can take signals the
mixed run was already in a position for. The comparison is sound directionally; the trade counts do
not add up and should not be presented as though they do.

### Where this leaves the lab
Every lever that acts on *this signal* has now been tried: entry filtering (×5), exit sizing (×1),
and regime conditioning (×1). The profit factor has never left 0.84–0.94 and the win rate has never
left ~38%. **The remaining move is the one that adds a different return stream rather than reshaping
this one — the short leg, rebuilt from its own geometry.** It is now unambiguously the top item, and
the standing objective that it must never be mirrored off the long leg still binds: that failure has
been recorded three times in the War Formation lab and once here.


## THE OPEN TOLERANCE QUESTION IS CLOSED — BY BEING MADE UNNECESSARY (2026-09-02)
Attack 3 (ban entries 1–4am ET) was reverted earlier in this sprint against the old MIXED base: it
posted the best PF gain on record, 0.9121 → 0.9405, but worsened drawdown by 0.064 percentage points
and a strict ratchet killed it. That prompted a standing question to the user about adopting a
drawdown tolerance band.

**Re-tested against the high-volatility base, it improves BOTH terms strictly:**

| | High-vol base | + witching ban |
|---|---|---|
| Profit factor | 0.9321 | **0.9640** |
| Max drawdown | 23.43% | **22.61%** |
| Win rate | 38.71% | **39.11%** |
| avgWin / avgLoss | 1.476 | **1.501** |
| Trades | 279 | 271 |

**No tolerance is needed. The strict ratchet keeps it on its own terms.**

The lesson is about sequencing, not about thresholds. The witching ban and the volatility split are
**complementary**: against a base that mixed two regimes, banning the witching window shifted the
drawdown profile enough to trip the ratchet; against a base already restricted to high volatility,
the same eight trades were unambiguously bad. **A change that fails against the wrong base is not a
failed change.** That is the argument for re-testing the reverted list as the base evolves — but only
the reverted list, and only when the base has genuinely changed, never as a way to relitigate a
result on the same base.

**This is the first configuration to clear PF 0.95, so 5m and parameter sensitivity are owed next
cycle.** It remains below 1.0 and is not a profitable system.


## ⚠️ THE 5m CONFIRMATION FAILED — AND THE TEST WAS CONFOUNDED (2026-09-02)
The base cleared PF 0.95 on 15m, so a second timeframe was owed. Identical code on 5m:

| | 15m base | 5m |
|---|---|---|
| Profit factor | 0.9640 | 0.7066 |
| Max drawdown | 22.61% | 41.00% |
| Win rate | 39.11% | 38.76% |
| avgWin / avgLoss | 1.501 | 1.116 |
| Trades | 271 | 356 |

**Read the two middle rows together.** The win rate is unchanged; the payoff ratio collapses. That is
the signature of trades running out of *time*, not out of edge.

**And that points straight at a confound I should have caught before running.** Every bar-denominated
parameter means three times less wall-clock on 5m: `maxBars` 96 is **8 hours** here against 24 on 15m,
and `sdLen`, `slopeLen`, `pushLook`, `coolBars`, `swgLen`, `trendLen` and `volLen` are all compressed
the same way. **This was not a clean timeframe-transfer test**, and the result cannot carry the weight
a clean one would.

**Honest status: inconclusive, leaning negative.** A properly scaled re-run — `maxBars` 288 and every
lookback tripled — is owed before the 15m result is either trusted or discarded. Until then the
15m base stands but should be regarded as unconfirmed on a second timeframe.

**Rule for this lab going forward:** when changing timeframe, scale every bar-denominated parameter
by the timeframe ratio, or the test measures the parameters rather than the signal.


# ★ THE BASE MOVES TO 5m — AND CLEARS 1.0 FOR THE FIRST TIME (2026-09-02)

**New base: the same signal on 5m, every bar-denominated parameter scaled x3.**
`sdLen 300 · slopeLen 150 · pushLook 150 · coolBars 60 · swgLen 60 · maxBars 288 · trendLen 600 ·
volLen 600 · ATR 42`. Price-denominated inputs unchanged. **Nothing was reoptimised** — this is the
15m base translated, not a new fit.

**PF 1.0202 · max DD 16.68% · 128 trades · win 41.41% · net +1.60%** (BTCUSDT 5m, 2024-06-08 → 2026-09-01).

### Why this is believable rather than a lucky window
Three runs, and the control is the one that matters:

| | PF | Max DD | Trades | Window |
|---|---|---|---|---|
| 5m, unscaled | 0.7066 | 41.00% | 356 | 2024-06 → 2026-09 |
| **5m, scaled** | **1.0202** | **16.68%** | 128 | 2024-06 → 2026-09 |
| 15m base, same window | 0.9615 | 21.33% | 113 | 2024-06 → 2026-09 |
| 15m base, full window | 0.9640 | 22.61% | 271 | 2022-01 → 2026-09 |

- **5m beats 15m on identical data**, on both ratchet terms. Not a period artefact.
- **The 15m signal is stable across periods** (0.9640 vs 0.9615), so the recent window is not unusually kind.
- **Scaling was the entire difference** on 5m: 0.7066 → 1.0202. The confound diagnosis was right, and
  the unscaled run really was measuring the parameters instead of the signal.

### What it does NOT mean
**PF 1.02 on 128 trades is break-even plus noise, and +1.60% over 2.2 years is not an economically
meaningful return.** This is the first evidence that the signal has a real edge at all — it is not a
tradeable system, and no champion is being declared on it. Naming a champion is the user's call and
should require more than clearing 1.0 by two points.

### What this opens
The timeframe axis was never on the attack list, and it turned out to matter more than any of the
seven filters that were. **1m should be tested next**, scaled the same way (x15 from the 15m base), to
find out whether this is a trend or a 5m coincidence. Only the War Formation lab has used 1m so far,
and its coverage limit (2025-12-16 onward) applies here too, so that run will be sample-limited.

Then the short leg, still unattempted and still never to be mirrored.


## THE TIMEFRAME CURVE HAS AN INTERIOR OPTIMUM AT 5m (2026-09-02)
Faster is not monotonically better. Each comparison below is like-for-like — the same window, only
the timeframe differing — because the raw numbers across different windows are not comparable.

| Comparison (identical window) | Slower | Faster | Winner |
|---|---|---|---|
| 15m vs 5m, Jun 2024 – Sep 2026 | 0.9615 | **1.0202** | 5m |
| 5m vs 1m, Dec 2025 – May 2026 | **0.8753** | 0.7521 | 5m |

**5m wins both comparisons, so the curve turns over and the base stays at 5m.** 1m is REVERTED.

The mechanism is plausible and matches the War Formation result from the other direction: this signal
needs price to *travel* to a fixed 2R target within a bounded time. Coarser bars than 5m give fewer,
lower-quality pullback entries; finer bars than 5m add noise to the entry without adding distance.
War Formation, whose edge depends on catching a reclaim precisely at a level, prefers 1m for exactly
the opposite reason. **Timeframe preference is a property of the mechanism, not of the market.**

## ⚠️ AND THE CONTROL SURFACED SOMETHING UNCOMFORTABLE ABOUT THE 5m BASE
The 5m base scores **1.0202 over its full 2.2 years but only 0.8753 over Dec 2025 – May 2026.**

The recent window is materially harder than the 5m average, which means **the headline 1.02 is not a
stable property of the signal across time.** That is the same shape as the War Formation lab's
unexplained edge concentration, now appearing here too.

**Consequence: the 1.02 should be quoted with its window attached, never on its own.** Before this
base is trusted any further, the next diagnostic worth running is a period decomposition of the 5m
base — split its 2.2 years into halves or quarters and see whether the edge is spread or concentrated.
That is a measurement, and it should come before any further attack on the entry or exit.


# ⚠️ THE PERIOD DECOMPOSITION IS IN, AND IT TEMPERS EVERYTHING ABOVE (2026-09-02)

| Window | PF | Win rate | Trades | Net |
|---|---|---|---|---|
| Jun 2024 – Jul 2025 | **1.3552** | 52.24% | 67 | **+14.64%** |
| Full, Jun 2024 – Sep 2026 | 1.0202 | 41.41% | 128 | +1.60% |
| Dec 2025 – May 2026 | 0.8753 | 41.18% | 17 | −1.08% |

**The edge is heavily front-loaded.** The first half carries essentially all of it; the remaining
~61 trades must be break-even or worse to drag 1.36 down to 1.02.

**So the headline PF 1.02 is not a stable property of this signal — it is an average over a good
period and a poor one.** That is a materially weaker claim than "the first profit factor above 1.0",
and the board should read that way from here on.

### The cross-lab observation is now hard to dismiss
Two unrelated strategies degrade in the same recent window:

| Lab | Mechanism | Early period | Recent period |
|---|---|---|---|
| BTC | 5m VWAP mean-reversion, long only | PF 1.36 (Jun 24 – Jul 25) | PF 0.88 (Dec 25 – May 26) |
| War Formation | 1m momentum cascade, long only | PF 3.80 (Dec – Feb) | PF 0.89 (Feb – May) |

Different timeframes, different mechanisms, different entry logic — same shape. **This looks like
edge decay in the current regime rather than a flaw in either strategy**, and it explains why every
filter aimed at the War Formation concentration has failed: filters select on a proxy, and no proxy
matches a market-wide change.

### What this changes about priorities
1. **Do not tune against the recent window.** Anything optimised on Dec 2025 – May 2026 is being
   fitted to the weakest data in the sample.
2. **Walk-forward is now the honest test**, not another attack. Fit on the first half, measure on the
   second, and quote both.
3. The short leg remains genuinely untried and is the only route to a return stream that does not
   depend on this long signal's decaying edge.


# ■ THE DECOMPOSITION IS COMPLETE, AND THE BASE FAILS OUT OF SAMPLE (2026-09-02)

| Window | PF | Win rate | Trades | Net |
|---|---|---|---|---|
| Jun 2024 – Jul 2025 | 1.3552 | 52.24% | 67 | +14.64% |
| **Jul 2025 – Sep 2026** | **0.6566** | 29.51% | 61 | **−11.36%** |
| Full, Jun 2024 – Sep 2026 | 1.0202 | 41.41% | 128 | +1.60% |

**The split is exact — 67 + 61 = 128 — so this is a clean partition, not an approximation.**

## What this means, stated without hedging
**The 5m base does not have a persistent edge.** The full-sample PF of 1.0202 is an average of one
good year and one bad one, and the more recent year is decisively negative. Either the edge decayed
or the first half was luck; on 67 and 61 trades this data cannot separate those two. What it does
settle is that **PF 1.02 must never again be quoted as a property of this signal.**

Earlier this session it was described as "the first profit factor above 1.0 in this lab." That was
accurate as a full-sample number and misleading as a claim about the strategy. The correction stands
on the record.

## What this invalidates
Both changes KEPT this session — the **high-volatility regime split** and the **witching-hour ban** —
were measured on the full mixed sample. They cleared the ratchet against a benchmark that we now know
averages a good period with a bad one, so **neither is validated on the recent half.** They stay in
the base because reverting them is not justified either, but they are now marked unvalidated rather
than proven.

## What survives
- The **timeframe finding** (5m beats 15m and 1m) was measured with like-for-like controls on
  identical windows, so it survives as a statement about relative ordering.
- The **method** survives, and produced this result: measure, control, decompose. The period
  decomposition cost two credits and overturned the session's headline claim. That is the machinery
  working, not failing.

## Where the lab goes next
1. **Stop improving this long signal.** Seven filters, one exit change, three timeframes and two
   regime conditions have been tried; the honest verdict is that the underlying VWAP-reclaim edge is
   not durable on BTCUSDT.
2. **The short leg is now the only unexplored return source** and must be built from its own
   geometry, never mirrored.
3. **Any future candidate must pass a period split before being called an edge.** Full-sample metrics
   have now misled this lab once; make the split mandatory, not optional.


## THE SHORT LEG, AND A REAL FINDING ABOUT EXITS (2026-09-02)
The own-geometry short was built and then tested for exit fit, both runs from exact source:

| | 2R target | 1R target |
|---|---|---|
| Profit factor | 0.5506 | **0.5816** |
| Win rate | 17.65% | **29.41%** |
| Trades | 17 | 17 |

**Identical trade counts prove the entry was untouched** — this is the single-variable test the new
source-recovery rule is meant to produce.

**The fade hypothesis is directionally confirmed:** a target sized for a trend continuation is too far
for a trade that fades an extreme. The leg is still not viable at PF 0.58 on 17 trades, but the
principle is now evidence rather than intuition.

**And it does not generalise.** The identical change on the War Formation lab's short made it WORSE
(0.749 to 0.692). That is the third finding this session that failed to cross labs, after the
volatility filter and the timeframe translation. **Exit convention follows the mechanism.**

### Standing position of this lab
- The long signal is exhausted: seven filters, one exit change, three timeframes, two regime
  conditions, and a period split showing PF 1.36 early against 0.66 late.
- The short leg exists, is honestly built, and does not work: PF 0.58 on 17 trades.
- **No champion, and nothing close to one.** The dashboard holds 27 recorded runs and not one of them
  is a system worth trading.


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


# ██ THE MIRROR BEATS THE OWN-GEOMETRY SHORT — A RULE CORRECTED (2026-09-02)

| BTC short construction | PF | Trades | Win rate | Payoff |
|---|---|---|---|---|
| Own-geometry fade — rally into the upper band that fails | 0.5506 | 17 | 17.65% | 2.57 |
| **Mirrored mechanism — stretch to −2σ, retrace, lose VWAP** | **0.7413** | **273** | 17.58% | 3.47 |

**Better profit factor and sixteen times the sample.** The no-mirror doctrine sent this lab to a
17-trade fade when a 273-trade symmetric leg was available and better. That doctrine was inherited
from the War Formation lab's E9/E9b failures and applied here without ever being tested on this
mechanism — which is precisely the cross-lab inheritance error this session has now recorded four
times.

**What the rule should say, corrected:** a mirror is a legitimate first construction. What fails is a
mirror that ignores LOCATION — E9b's short entered after price had already fallen, and adding a
cycle-position gate lifted it from 0.68 to 0.75. Test the symmetric mechanism first, then fix
location; do not assume the short must be a different animal.

**Still not viable.** PF 0.74 with a 34.4% drawdown is not tradeable, and the leg is recorded as
`testing` because it is the best short on record and the basis for a bidirectional build, not because
it works.

### The two sides have genuinely different trade shapes
| | Long | Short |
|---|---|---|
| Win rate | 38–41% | 17.6% |
| Payoff ratio | ~1.5 | ~3.5 |

**The same mechanism does not produce the same trade shape on each side.** The short takes many small
losses and a few large wins; the long is far more balanced. That matters before running them
together — position sizing and expectancy behave differently, and a combined equity curve will be
driven by the short's tail rather than its hit rate.

### Standing position after this cycle
- Long: PF 1.02 full sample, but 1.36 early against 0.66 late. No persistent edge.
- Short: PF 0.74 on a real 273-trade sample. Best yet, still losing.
- **Neither side works. The lab has an honest map of the mechanism and no tradeable system.**


# ██ THE BOTH-DIRECTIONS REQUIREMENT: STRUCTURE BUILT, SUBSTANCE MISSING (2026-09-02)

Both labs now have a bidirectional build. **Both are worse than their long-only versions, and for the
same reason: the short leg has no edge in either.**

| Lab | Long leg | Short leg | Combined | vs long-only |
|---|---|---|---|---|
| BTC 5m | 128 trades, +$374 | **294 trades, −$2,416** | PF 0.888, DD 37.3% | worse than 1.020 |
| War Formation 1m | 32 trades, +$786 | **10 trades, 1 win, −$329** | PF 1.303, DD 5.02% | worse than 1.686 |

**What has been established, and it is not nothing:**
- The structure works. A single strategy that reads the regime and takes either side is built, running
  and measured in both labs, with a mechanical flip rule on each.
- The legs barely interact. BTC's long count is identical (128) whether the short is present or not,
  so `pyramiding=1` blocking is not the problem.
- **Raising short frequency does not help.** War Formation's shorts went 6 → 10 and the loss grew five
  times while wins stayed at one. Sampling a negative expectancy more often just costs more.

**What is NOT established: any short leg with an edge.** Across two labs and eight distinct short
constructions — mirrored, own-geometry fade, near-touch rejection, sweep-and-reject, with and without
a cycle-position gate, at 1R, 1.5R and 2R targets — **not one has reached a profit factor of 1.0.**
The best is E13's 0.749.

**The honest position on the requirement:** the labs can produce a bidirectional *structure* on demand.
Neither can yet produce a bidirectional *edge*, because no short leg works. Adding a losing leg to a
break-even leg makes the system worse, not more complete — so shipping a bidirectional build now would
be worse than shipping nothing.

**The right next work is on the short side alone**, judged on its own profit factor, until one clears
1.0. Everything else is premature.


## ██ ATTACK 8 — THE TIMEFRAME AXIS DOES NOT GENERALISE ACROSS LEGS (2026-09-02)

The timeframe axis is the only thing that has ever moved this system: seven entry and exit filters
left the long at PF 0.91, and going 15m -> 5m with every bar parameter scaled took it to 1.02. **The
short had never been tested on that axis** — every short construction ran at 5m because that is
where the long had landed.

| Short leg | 5m (base) | 15m, params /3 |
|---|---|---|
| Profit factor | **0.74125302** | 0.59953518 |
| Max drawdown | 34.40% | **50.60%** |
| Trades | 273 | 270 |
| Win rate | 17.6% | 14.8% |
| Payoff ratio | ~3.5 | 3.447 |

**REVERTED — worse on both ratchet terms.**

**The trade count is the informative number: 273 versus 270.** Slowing the timeframe by 3x barely
changed how often the signal fires, so this is not a sampling artifact. The *same* signal, on the
*same* period, is simply worse when read slower — the payoff ratio held at ~3.4 while the win rate
fell 2.8pp, and the drawdown got half again as deep.

**What this settles and what it does not.** It settles that the two legs do not share a timeframe
optimum in the way I assumed when scaling both to 5m. The long has an interior optimum at 5m; the
short degrades as far as it has been measured, so **both legs point faster, not toward each other.**
It does NOT establish where the short's optimum is — 1m is the untested direction, and that is
sample-limited to Dec 2025 onward.

**More importantly, it is the tenth negative short result across this lab and War Formation.** The
axis that rescued the long did nothing for the short, exactly as the seven filters did nothing for
the long. **Each leg has now had one axis that moves it and a long list that does not, and the
short's has not been found.**


## ██ ATTACK 9 — A KEPT FILTER THAT DOES NOTHING IN THE HALF THAT MATTERS (2026-09-02)

Every KEPT change on this board was accepted on the **full** sample. The decomposition then showed
that sample is not homogeneous — PF 1.3552 early against 0.6566 late — which means a change could
have been kept for removing trades that were only bad in the half where the system already worked.
Nobody had checked. Attack 9 checks the biggest one: Attack 1, the EMA200 trend filter.

| H2 only (2025-07-20 → 2026-09-01) | With EMA200 (control) | Without |
|---|---|---|
| Profit factor | 0.65655726 | 0.66176879 |
| Max drawdown | **12.66%** | 16.06% |
| Trades | 61 | 64 |

**Profit factor moved by 0.005.** That is noise, not a filter working.

**The trade count is the real finding: the gate removes THREE trades out of 64.** On the 15m full
sample Attack 1 cut 35 trades from 468 and was credited with lifting PF 0.89 → 0.91. In H2 it barely
binds at all — price is above the 600-bar EMA almost whenever the other seven conditions align, so
the term is very nearly a tautology here.

**REVERTED — the filter stays**, because removing it worsens drawdown by 3.4pp and the ratchet
forbids that. But it stays as ballast, not as an edge: **it is not contributing to profit factor in
the regime where this system is losing money.**

**This is E17 generalised — check whether a constraint BINDS, not just whether the metric moved.** A
gate credited on a mixed sample can be inert in one half and load-bearing in the other, and the
aggregate number cannot tell the difference. The other KEPT changes (the high-volatility regime
split, the witching ban) are still unvalidated on this axis and should be checked the same way before
any of them is treated as established.


## ██ ATTACK 10 — THE SECOND GATE HAS THE OPPOSITE DISEASE (2026-09-02)

Attack 9 found the EMA200 filter nearly inert in H2 — three trades removed out of 64. Attack 10 ran
the same test on the other unvalidated gate, `highVol`, the volatility regime split.

| H2 only (2025-07-20 → 2026-09-01) | With highVol (control) | Without |
|---|---|---|
| Profit factor | 0.65655726 | **0.76510562** |
| Win rate | 29.69% | 33.98% |
| Max drawdown | **12.66%** | 19.59% |
| Trades | 61 | 103 |

**This gate is the opposite of inert. It removes 42 of 103 trades — and the trades it removes are
disproportionately WINNERS.** Taking it out lifts profit factor by 0.109 and the win rate by 4.3pp.

**REVERTED, strictly by the ratchet** — profit factor improved but drawdown worsened by 6.9pp, and
the rule is *both* terms or nothing. That is the right call and I am not going to argue with it, but
the finding underneath deserves to be stated plainly: **the volatility split is paying for its
drawdown reduction with profit factor, in the half of the sample where this system loses money.**

### TWO KEPT GATES, TWO DIFFERENT DISEASES
| Gate | Trades removed in H2 | Effect on PF |
|---|---|---|
| EMA200 trend filter | 3 of 64 | none (0.005) — **inert** |
| highVol regime split | 42 of 103 | −0.109 — **actively harmful** |

Neither is doing what its KEPT verdict claimed. One barely binds; the other binds hard and costs.
**Both verdicts were artifacts of measuring on a sample that turned out not to be homogeneous** —
they were credited for behaviour in H1 and neither was ever checked in H2.

**What this means for the board.** The 5m base is not "the mechanism plus two validated
improvements". It is the mechanism plus one gate that does nothing and one that suppresses winners
to flatter the drawdown. **The PF 1.0202 headline on the full sample is now doubly qualified**: it
was measured on a mixed sample, and two of its components fail re-validation on the failing half.
The remaining unvalidated term is the witching ban, and it should be checked the same way.


## ██ THE RE-VALIDATION SWEEP IS COMPLETE — ONE GATE OF THREE SURVIVES (2026-09-02)

Every KEPT change on this board was accepted on the full sample, and the decomposition showed that
sample is not homogeneous. Three cycles have now re-tested all three surviving gates in H2 alone, the
half where the system loses money, each against the same control (PF 0.65655726, DD 12.66%, 61 trades).

| Gate | Trades removed in H2 | Effect on PF when removed | Verdict |
|---|---|---|---|
| EMA200 trend filter | 3 of 64 | +0.005 — noise | **INERT** |
| highVol regime split | 42 of 103 | **+0.109 — removing it HELPS** | **HARMFUL** |
| Witching ban (1–4am ET) | 1 of 62 | −0.028, and drawdown worsens too | **EARNS ITS PLACE** |

**Only the witching ban passes.** It is also the one that was REVERTED on the 15m base back in Attack
3 and entered the 5m base without separate justification — so the gate with the weakest paper trail
is the only one that holds up, and the two that were credited with lifting the system either do
nothing or actively cost profit factor.

### A MECHANICAL POINT WORTH KEEPING
The witching ban admits **one** extra trade and profit factor falls 0.028. That looks contradictory
until you remember the sizing: at `percent_of_equity` 100, **a single early loss rescales every
subsequent position**, so one bad trade propagates through the entire curve. **Small trade-count
differences in this lab are not automatically noise** — that assumption should not be made again
without checking where in the sequence the difference falls.

### WHAT THE BOARD NOW SAYS ABOUT THE BASE
The 5m base is not "the mechanism plus three validated improvements". It is **the mechanism, plus one
gate that does nothing, one that suppresses winners to flatter drawdown, and one that works.** The
PF 1.0202 headline was measured on a mixed sample with two of its three components failing
re-validation. **The honest description of this lab's state is that it has a well-mapped mechanism
with no demonstrated edge**, and the next cycle should stop attacking gates and say so on the board.


## ██ ATTACK 12 — A CORRECTION TO WHAT I WROTE AFTER ATTACK 10 (2026-09-02)

Attack 10 removed `highVol` in H2 and profit factor rose 0.65656 → 0.76511. I wrote on this board
that the base "carries a gate that suppresses winners to flatter the drawdown." **That conclusion was
drawn from a half-sample diagnostic and it does not survive the full-sample test.**

| Full 5m sample, 2024-06-08 → 2026-09-01 | Base (with highVol) | Without |
|---|---|---|
| Profit factor | **1.02024675** | 0.91514233 |
| Max drawdown | **16.68%** | 23.51% |
| Trades | 128 | 207 |
| Win rate | — | 39.13% |

**Worse on both terms. REVERTED, and the gate keeps its place properly this time.**

**What is actually true:** removing highVol admits **79 extra trades**, and across the whole sample
those trades are net negative — even though in H2 alone the same gate was cutting winners. **The
filter is regime-dependent, not bad.** It earns its keep in the first half and costs in the second,
and the aggregate is what the ratchet judges.

### THE METHOD LESSON, AND IT APPLIES TO THE WHOLE SWEEP
**A half-sample diagnostic tells you where a gate behaves differently. It does not tell you whether
to keep it.** I ran three of these (Attacks 9, 10, 11) and let the H2 verdicts stand as statements
about the gates themselves. Only Attack 12 asked the question the ratchet actually answers.

**So the sweep's conclusions are now correctly scoped:**
| Gate | H2 behaviour | Full-sample verdict |
|---|---|---|
| EMA200 trend | inert (3 of 64 trades) | untested on the full sample |
| highVol split | harmful (removing adds 0.109) | **KEEPS its place — removing costs 0.105** |
| Witching ban | earns its place | untested on the full sample |

**Two of the three still lack a full-sample test**, and until they have one the honest description is
that their H2 behaviour is *interesting*, not that they are inert or harmful. The base remains
PF 1.0202 on 128 trades — break-even plus noise, and no champion.


## ██ ATTACK 13 — THE SWEEP, PROPERLY SCOPED AT LAST (2026-09-02)

Two cycles ago I ran three H2 diagnostics and let their verdicts stand as statements about the gates.
Attack 12 showed that was wrong for `highVol`. Attack 13 now closes the second gate on the full
sample — and the answer is the *opposite* of Attack 12's, which is the interesting part.

| Gate | H2 verdict | Full-sample verdict | Trades it removes (full) |
|---|---|---|---|
| EMA200 trend | inert (3 of 64) | **inert — confirmed** | **6 of 134** |
| highVol split | harmful (removing adds 0.109) | **load-bearing — reversed** | 79 of 207 |
| Witching ban | earns its place | still untested | 1 of 62 (H2) |

Removing EMA200 on the full sample: PF **1.02025 → 1.01094**, DD **16.68% → 17.47%**, trades 128 →
134. Both terms marginally worse, so it stays — but it stays as **ballast, not as an edge.** Six
trades in 2.2 years is a gate that is very nearly a tautology: price sits above a 600-bar EMA almost
whenever the other six conditions have already aligned.

### THE SHARPER VERSION OF THE LESSON
After Attack 12 I wrote that a half-sample diagnostic cannot tell you whether to keep a gate. **That
was too strong.** trendOk's H2 verdict generalised perfectly; highVol's inverted. The difference is
not the method, it is **how hard the gate binds**:

> **A half-sample verdict is reliable in proportion to how little the gate binds.** A gate that
> removes 3 of 64 trades has almost no room to behave differently elsewhere. A gate that removes 42
> of 103 is re-selecting the sample, and its effect is a property of the regime, not of the gate.

**Check the trade count first, and let it tell you how far the verdict travels.** That is a cheaper
and better rule than "always re-test on the full sample", and it is now the standing guidance here.

### THE BASE, DESCRIBED HONESTLY
PF 1.0202 on 128 trades, long-only, no champion. Of its three accepted gates: **one is inert, one is
regime-dependent and load-bearing, one is untested on the full sample.** Nothing has ever been KEPT
by this ratchet. The mechanism is thoroughly mapped and has no demonstrated edge.


## ██ THE SWEEP IS COMPLETE, AND HARD LESSON 12 IS 3 FOR 3 (2026-09-02)

All three accepted gates have now been tested in H2 and on the full sample.

| Gate | Trades removed (full) | H2 verdict | Full-sample verdict | Travelled? |
|---|---|---|---|---|
| Witching ban | **2 of 130** | earns its place | **earns its place** | ✅ |
| EMA200 trend | **6 of 134** | inert | **inert** | ✅ |
| highVol split | **79 of 207** | harmful | **load-bearing** | ❌ inverted |

**HARD LESSON 12 made a forward prediction and it held.** The lesson says a half-sample verdict
travels only as far as the gate fails to bind. The witching ban removes **two trades in 2.2 years** —
the least binding gate in the base — so its H2 verdict should have generalised, and it did:
PF 1.02025 → 0.96113 without it, worse on both terms, exactly as H2 said.

**Three for three.** The two gates that barely bind both generalised; the one that re-selects a third
of the sample inverted. The rule is not a post-hoc accommodation of two results — it now has
predictive content.

### THE COMPOUNDING POINT, AGAIN
**Two extra trades move profit factor by 0.059.** At `percent_of_equity` 100 a single early loss
rescales every later position, so a change of two trades near the start of the curve is not a small
change. This has now shown up three times (Attacks 11, 13, 14) and it is why trade-count deltas in
this lab must never be dismissed as noise without checking *where* they fall.

### THE BASE, FINAL DESCRIPTION AFTER THE SWEEP
**PF 1.0202, DD 16.68%, 128 trades, long-only, no champion.** Of its three gates: one is inert
ballast, one is load-bearing but regime-dependent, one earns its place on two trades. **Nothing has
ever been KEPT by this ratchet in fourteen attacks.** The mechanism is now more thoroughly documented
than it is profitable, and the board should stop funding gate work: the honest remaining questions
are about the *signal*, not its filters.


# ██ ATTACK 15 — THE FIRST CHANGE EVER KEPT, AND THE STRATEGY IS NOT WHAT IT SAYS IT IS

Fourteen attacks had been reverted. Seven entry filters, three exit changes, two timeframe ports,
three gate re-validations. **Attack 15 is the first to pass the ratchet on both terms.**

| | Base | **Attack 15 (new base)** |
|---|---|---|
| Profit factor | 1.02024675 | **1.15252596** |
| Max drawdown | 16.68% | **16.54214281%** |
| Trades | 128 | **166** |
| Win rate | 39.13% | **44.57831325%** |
| Net return | +2.0% | **+16.10%** |

**The one change: `reachedUpper` removed** — the requirement that price reached +2σ within the last
150 bars. **The term the strategy is named for.**

## WHY THIS WORKED, AND WHY IT MATTERS MORE THAN THE NUMBER
The stretch requirement was **removing 38 trades that were net positive.** It was not selective; it
was harmful. And the reason the sweep never found this is that **every one of the fifteen attacks
before it targeted a FILTER.** The signal's own terms were treated as the thing being filtered, and
therefore never questioned.

**So this system is not a VWAP mean-reversion-from-extension strategy and never was.** It is a **VWAP
pullback-continuation** strategy — VWAP rising, price above trend, pull back toward VWAP, resume —
with a sigma-band costume bolted on that cost money for fifteen cycles. **Every description of this
strategy on this board before today was wrong**, including the ones I wrote.

## THE METHOD LESSON
HARD LESSON 12 said to read the trade count to learn how much a term binds. That was developed on
gates. **Applied to a signal term it found the only improvement this lab has ever produced.** The
generalisation: *the binding test belongs on every term in a conjunction, not only the ones you think
of as filters.* A strategy's name is a hypothesis about which term carries it, and it should be
tested like any other.

## WHAT THIS IS NOT
**It is not a champion, and PF 1.15 on 166 trades is not a validated edge.** The old base looked like
1.0202 right up until it decomposed into **1.3552 early / 0.6566 late**. The new base has never been
split, and until it is, 1.15 is a full-sample average of unknown composition.

## THE QUEUE, RESET
1. **DECOMPOSE THE NEW BASE.** H1/H2 split of Attack 15, same halves used before. This is the only
   thing that turns 1.15 into a claim.
2. **Test the remaining unexamined SIGNAL terms the same way** — `pulledBack`, `vwUp`, `coolingOff`,
   `close > open`. One found a +0.13; the others have never been asked.
3. **Re-test the three gates against the NEW base.** Their verdicts were earned against a base whose
   signal has now changed, and the ratchet's own rule says re-testing a reverted change against a
   genuinely changed base is allowed and must be labelled as such. `highVol` in particular was
   load-bearing on a signal that no longer exists in the same form.


## ██ ATTACK 16 — THE NEW BASE IS BETTER IN BOTH REGIMES AND STILL A BLEND (2026-09-02)

When Attack 15 was kept I wrote that PF 1.15252596 is "a full-sample average of unknown composition"
and refused to call it a champion. The decomposition confirms that caution.

| Identical windows | OLD base | **NEW base (Attack 15)** | Change |
|---|---|---|---|
| H1 · 2024-06-08 → 2025-07-20 | 1.3552 | **1.55157635** | **+0.196** |
| H2 · 2025-07-20 → 2026-09-01 | 0.6566 | **0.77846786** | **+0.122** |
| **Spread** | 0.699 | **0.773** | **wider** |

**Two things are true at once and both matter.**

**Removing the stretch genuinely improved the mechanism in both regimes** — +0.196 in the good half
and +0.122 in the bad one. That is not an artifact of averaging: the change helped everywhere, which
is the strongest form of evidence a single change can produce.

**And it did not fix the real problem.** The spread got *wider*, H2 still loses money at 0.778 with a
33.75% win rate, and the full-sample 1.15 remains a blend of a profitable period and an unprofitable
one. H1 alone would look like a strategy — PF 1.55, 54.65% win, Sharpe 1.83, 8.92% drawdown. H2 is a
different animal.

### WHAT THIS MEANS FOR THE BOARD
**Still no champion, and the reason is now precise rather than cautious.** The system does not have a
modest edge everywhere; it has a real edge in one regime and none in the other, and Attack 15 shifted
both up without changing that shape.

**So the productive question is no longer "which term to remove".** It is: **what distinguishes H1
from H2?** That is the same question the War Formation lab has been carrying as its biggest open item,
and neither lab has answered it. What is known here: it is not volatility (`highVol` is load-bearing
in aggregate but did not close the gap), not the trend filter (inert), not the clock (2 trades). The
untested candidates are market-structure descriptors that no build has ever computed — realised
trend persistence, autocorrelation of returns, or the ratio of directional to ranging bars.

### QUEUE
1. **Characterise H1 versus H2 directly** with a counter build, not another entry filter. Measure a
   structural property of each window and see whether it separates them.
2. **The remaining signal terms** — `pulledBack`, `vwUp`, `coolingOff`, `close > open` — still
   untested for binding. Attack 15 found +0.13 in that family.
3. **Re-test the three gates against the new base.** Their verdicts were earned against a signal that
   has changed.


## ██ ATTACK 17 — THE FIRST REGIME DESCRIPTOR THAT ACTUALLY SEPARATES H1 FROM H2 (2026-09-02)

The board's top question after Attack 16: what distinguishes the good half from the bad? Volatility,
trend and clock had all been tested **as filters** and none explained it. Attack 17 stopped filtering
and **characterised** the two windows instead.

**The measure: VWAP flip frequency** — every crossover or crossunder of VWAP. It is the right
descriptor for *this* system specifically, because Attack 15 established the base is a **VWAP
pullback-continuation** strategy, which should profit when price holds one side of VWAP and suffer
when it oscillates across it.

| | H1 (good half) | H2 (bad half) |
|---|---|---|
| VWAP flips | 4,905 | **5,609** |
| Bars | 117,254 | 117,997 |
| **Flips per bar** | **0.04183** | **0.04754** |
| Base profit factor | **1.55157635** | 0.77846786 |

**H2 has 13.6% more flips per bar — and the prediction was stated before the run.**

### WHY THIS MATTERS MORE THAN THE SIZE OF THE EFFECT
13.6% is modest, and that is worth saying plainly rather than dressing up. But **it is the first
structural property this lab has measured that moves in the right direction between the two windows**,
after three filter-based attempts found nothing. It is also mechanistically coherent: a
pullback-continuation system needs price to *stay* on one side of its reference, and H2 gives it less
of that.

### WHAT IT DOES AND DOES NOT LICENCE
**It does not licence a chop filter.** That would repeat the error the gate sweep exposed — the board
has fourteen reverted attacks that were all filters, and HARD LESSON 12 says a hard-binding gate
re-selects the sample rather than improving it. A flip-rate gate would bind hard by construction.

**What it licences is a better question.** If flip rate separates the regimes, the productive test is
whether the base's profit factor is *monotone* in flip rate — measurable by splitting the sample on
the descriptor rather than on the calendar. That is a decomposition, not a filter, and it is the next
BTC cycle.

### THE BASE, UNCHANGED
**PF 1.15252596, DD 16.54%, 166 trades, long-only. No champion.** Attacks 17a and 17b were counters;
they changed nothing and were never candidates.


## ██ ATTACK 18 — THE PULLBACK IS THE EDGE, AND THE RENAMING WAS THE REAL RESULT (2026-09-02)

Attack 15 deleted `reachedUpper`, the +2σ stretch, and produced this lab's only KEPT change. It also
forced a renaming: without the stretch this is not mean-reversion-from-extension, it is **VWAP
pullback-continuation**. HARD LESSON 15 says a strategy's name is a hypothesis — so the *corrected*
name deserved the same test the original one failed.

| | Base (Attack 15) | Without `pulledBack` |
|---|---|---|
| Profit factor | **1.15252596** | 0.87379592 |
| Max drawdown | **16.54214281%** | 42.82737208% |
| Trades | 166 | **290** |
| Win rate | 44.58% | 41.03% |

**REVERTED.** Removing the pullback admits **124 extra trades** that are heavily net negative and
**nearly triples the drawdown**.

### WHAT THIS RESOLVES
| Term | Role in the name | Verdict |
|---|---|---|
| `reachedUpper` — the +2σ stretch | the ORIGINAL name | **decoration, and costly** |
| `pulledBack` — the pullback to VWAP | the CORRECTED name | **the edge** |

**Attack 15 did not merely improve the base — it renamed the strategy correctly.** The old name
pointed at a term that was costing money; the new name points at the term that carries it. That is a
stronger result than the +0.13 profit factor, because it means the board's description of this system
is now load-bearing rather than decorative.

### AND IT SHARPENS HARD LESSON 15
The lesson said a name is a hypothesis. Attacks 15 and 18 together show the useful version:
**test the name, and if it fails, the term that survives tells you what to rename it to — then test
the new name too.** Two of three labs found their named term was decoration; here the *replacement*
name has now been confirmed load-bearing, which is what closes the loop.

**Base unchanged: PF 1.15252596, DD 16.54214281%, 166 trades, long-only. Still no champion** — the
H1/H2 spread of 0.773 is the open problem, not the entry terms.


## ██ ATTACK 19 — A DUPLICATED TREND REQUIREMENT, AND IT EXPLAINS ATTACK 13 (2026-09-02)

| | Base (Attack 15) | Without `vwUp` |
|---|---|---|
| Profit factor | **1.15252596** | 1.12540646 |
| Max drawdown | 16.54214281% | **15.17443126%** |
| Trades | 166 | **176** |
| Win rate | 44.58% | 43.75% |

**REVERTED** — the ratchet requires profit factor to improve, and it fell 0.027. Drawdown improved
1.37pp, which is not enough on its own.

### THE TRADE COUNT IS THE FINDING, NOT THE PROFIT FACTOR
**Removing `vwUp` admits only TEN extra trades out of 176.** A 150-bar VWAP slope requirement that
excludes ten candidates across 2.2 years is barely binding — and that **explains Attack 13 exactly.**

Attack 13 found `trendOk` (the 600-bar EMA) nearly inert: 6 trades of 134. The reason is now clear:
**`vwUp` had already excluded almost everything `trendOk` would have.** The base carries a
**duplicated trend requirement** — two instruments encoding one piece of information, each appearing
inert *because the other is doing the work*.

**Neither can be judged alone.** The E14 redundancy check flagged this pair as the only real overlap
in the conjunction before the run, and the result confirms it.

### THE OPEN QUESTION THIS CREATES
**Is the trend requirement load-bearing at all?** Both terms individually look near-inert, but that is
exactly what a redundant pair looks like. The test is to **remove BOTH together** — the only way to
measure information that two terms share. If the count explodes and profit factor collapses, trend
matters and one term is free to delete for simplicity. If the count barely moves, this system has no
meaningful trend requirement and two of its seven terms are decoration.

**That is the next BTC cycle**, and it is a case where removing two terms is the single coherent
change rather than a violation of the one-thing rule — they are one requirement expressed twice.

**Base unchanged: PF 1.15252596, DD 16.54214281%, 166 trades, long-only. No champion.**


## ██ ATTACK 20 — THE TREND REQUIREMENT IS REAL, AND TWO EARLIER VERDICTS WERE ARTIFACTS (2026-09-02)

Both trend terms removed together, because Attack 19 showed they are one requirement expressed twice
and shared information is not attributable to either alone.

| | Base (Attack 15) | Neither trend term |
|---|---|---|
| Profit factor | **1.15252596** | 1.04432441 |
| Max drawdown | 16.54214281% | **15.91706953%** |
| Trades | 166 | **208** |
| Win rate | 44.58% | 41.83% |

**REVERTED** — the ratchet needs profit factor to improve and it fell 0.108. Drawdown improved
0.63pp, which is not enough alone.

### THE ARITHMETIC IS THE FINDING
| Removed | Trades admitted | PF cost |
|---|---|---|
| `vwUp` alone (Attack 19) | +10 | −0.027 |
| **both together (Attack 20)** | **+42** | **−0.108** |

**The pair excludes four times as many trades together as `vwUp` does alone, and costs four times as
much profit factor.** That is the quantitative signature of shared information: each term looks small
because the other is covering for it, and the true size of the requirement only appears when both go.

### TWO CORRECTIONS TO THE BOARD
1. **Attack 13's "inert" verdict on `trendOk` must be re-scoped.** It measured *trendOk given vwUp*,
   not the trend requirement. The term is not inert; it is redundant with a term that was doing the
   same job.
2. **The suspicion that the base carried decoration here was wrong.** Neither trend term is free to
   delete. The trend requirement carries roughly 0.11 of profit factor, and the base needs it.

### AND A SHARPENING OF HARD LESSON 12
The lesson said a half-sample verdict travels only as far as the gate fails to bind, and that the
**trade count** tells you how far. Attack 20 adds the failure mode that count alone misses:
**a gate can appear not to bind because a REDUNDANT PARTNER is binding in its place.** A low removal
count is therefore ambiguous — it means either the term does nothing, or something else is already
doing it. Distinguishing them requires removing the candidate partners together, and until that is
done a "does not bind" reading is provisional.

**Base unchanged: PF 1.15252596, DD 16.54214281%, 166 trades, long-only. No champion.**


## ██ ATTACK 21 — coolingOff IS THE CHOP DEFENCE, AND IT GUARDS DRAWDOWN NOT PROFIT FACTOR (2026-09-02)

| | Base (Attack 15) | Without `coolingOff` |
|---|---|---|
| Profit factor | **1.15252596** | 1.07714686 |
| Max drawdown | **16.54214281%** | 28.17240888% |
| Trades | 166 | **413** |
| Win rate | 44.58% | 43.58% |

**REVERTED.** Profit factor fell 0.075 and **drawdown nearly doubled**.

### THE BINDING TABLE — coolingOff DWARFS EVERYTHING ELSE
| Term | Candidates it excludes |
|---|---|
| **`coolingOff`** | **247 of 413 — 60%** |
| `pulledBack` | 124 of 290 — 43% |
| `highVol` | 79 of 207 — 38% |
| trend pair together | 42 of 208 — 20% |
| `reachedUpper` (removed, was costly) | 38 of 166 — 23% |
| `witching` | 2 of 130 — 2% |

**Six of every ten would-be entries are blocked by a single term nobody had tested.**

### THE PRECISE READING, BECAUSE THE TWO COSTS ARE VERY DIFFERENT
Profit factor falls only 0.075 while drawdown rises 11.6 percentage points. **So `coolingOff` is a
RISK control, not an edge term.** The trades it blocks are not much worse *on average* — they are
worse *in sequence*. It stops the strategy re-entering repeatedly through the same VWAP oscillation,
which is exactly how a drawdown gets built without the average trade looking bad.

This is a distinction the ratchet's two terms are built to catch and a single-metric view would miss.

### IT ALSO GIVES THE H1/H2 PROBLEM ITS FIRST CONCRETE LEVER
Attack 17 found the only property separating the regimes: **H2 has 13.6% more VWAP flips per bar** and
is where the base fails. **`coolingOff` is the only term in the strategy that responds to flip
frequency** — and it turns out to be the most binding term in the base.

**So the response to the regime gap is to tune `coolBars`, not to bolt on the chop filter the board
warned against.** That is a parameter the strategy already has, aimed at the mechanism actually
identified, rather than a fifteenth filter.

### QUEUE
1. **`coolBars` neighbourhood: 30 and 120 against the current 60** (HARD LESSON 16 — and with 60%
   binding, this is the highest-leverage parameter in the base). Run both sides together; one side
   cannot distinguish a plateau from a spike.
2. **Then `close > open`** — the last untested signal term.
3. Note in passing: **PF 1.077 on 413 trades is the largest positive-profit-factor sample this lab
   has produced.** Not a candidate (the ratchet rejected it), but worth remembering that the
   wider-population version is not far below break-even-plus.

**Base unchanged: PF 1.15252596, DD 16.54214281%, 166 trades, long-only. No champion.**


---

## ██ ATTACKS 22–24 — THE CHOP DEFENCE HAS A DIRECTION, AND THE NEW BASE IS coolBars 120 (2026-09-02)

Attack 21 left `coolingOff` as the hardest-binding term in the base — **60% of candidates**, more than
double any other term — and the only term that responds to VWAP flip frequency, the single structural
property Attack 17 found separating H1 from H2. Its threshold had never been varied. Three runs this
cycle, because HARD LESSON 16 says a parameter is not measured until both sides of it are.

| coolBars | Profit factor | Max drawdown | Trades | Win rate | Net return |
|---|---|---|---|---|---|
| 30 (Attack 22) | 1.00338859 | 22.51971852% | 231 | 42.86% | +0.52% |
| 60 (old base) | 1.15252596 | 16.54214281% | 166 | 44.58% | — |
| **120 (Attack 23)** | **1.30380521** | **8.12167991%** | **77** | **48.05%** | **+12.68%** |
| 240 (Attack 24) | 2.30230986 | 1.99887631% | **7** | 71.43% | +2.40% |

### ATTACK 23 IS KEPT — THE SECOND CHANGE EVER, AND BY FAR THE LARGEST
Profit factor **+0.151** and drawdown **halved** (−8.42pp). For scale, Attack 15 — until now the only
change ever kept — moved PF +0.13 and drawdown −0.14 percentage points.

**And it is not merely "fewer trades".** Win rate rose 3.47pp and the payoff ratio rose with it. The
plainest statement of the result: **77 trades returned +12.68%, while 231 trades at `coolBars` 30
returned +0.52%.** Trading a third as often made more money in absolute terms, not just better ratios.

### THE CHOP-DEFENCE HYPOTHESIS IS CONFIRMED, AND IT NOW HAS A DIRECTION
The chain took five cycles to assemble and closed here:
- **Attack 16** — the base scores 1.552 in H1 and 0.778 in H2. The spread is the standing problem.
- **Attack 17** — the only structural property separating them is flip frequency: **H2 has 13.6% more
  VWAP flips per bar.** Volatility, trend and clock all failed to explain it.
- **Attack 21** — `coolingOff` is the only term that responds to flip frequency, it is the most binding
  term in the base, and its cost profile is drawdown-shaped rather than profit-factor-shaped — the
  signature of a risk control.
- **Attacks 22/23** — every measured quantity improves monotonically as the stand-down lengthens.

**The response to the regime gap was a parameter the strategy already had, not a fifteenth filter.**
That matters against this lab's record: fourteen filter attacks were reverted before this.

### ATTACK 24 IS REJECTED AS UNINTERPRETABLE, NOT AS WORSE — AND THE DISTINCTION IS THE FINDING
PF 2.30 and a 2.00% drawdown are the best numbers this lab has printed. They rest on **seven trades**,
spanning 2024-09-26 to 2025-07-04 — **nothing at all in the final fourteen months.** I registered
before the run that below roughly 30 trades I would report the count and not the ratio, and I am.

**The collapse is the informative part, and it was faster than I predicted.** I wrote that 240 would
land near 40. It landed at 7. The decay runs **231 / 166 / 77 / 7** — −28%, −54%, then **−91%**.
A super-exponential fall means the median gap between VWAP flips sits well below 240 bars, so at 240
the rule stops filtering chop and starts **requiring a rare 20-hour flip-free stretch** — a different
and much rarer condition, not more of the same one.

### THE HONEST WEAKNESS IN THIS PROMOTION, STATED RATHER THAN BURIED
Two things qualify the new base and neither should be lost:

1. **77 trades is thin.** PF 1.30 on 77 trades carries wide error bars. The old base had 166.
2. **120 is bounded above by DEGENERACY, not by a measured worse value.** That is a weaker bound than
   the sister lab achieved for the $2,000 shield in E40/E41, where both neighbours came back
   *measurably* worse and drew an actual curve. Here the upper neighbour simply ran out of data.

So `coolBars` 120 is promoted **because it strictly passes the ratchet with both neighbours measured**,
and it is recorded with those two caveats attached, not despite them.

### THE PREDICTION THAT WOULD VALIDATE THIS — REGISTERED NOW, BEFORE THE TEST
If `coolBars` 120 genuinely fixes chop, then **the H1/H2 spread should narrow**, because H2 is the
choppier half and the chop is what the longer stand-down removes. Attack 16 measured that spread on
the old base: **H1 1.552, H2 0.778, gap 0.773.**

**If the gap does not narrow, the promotion is a whole-sample coincidence and I will say so.** This is
the strongest available falsification and it is cheap — two runs on the halves.

### QUEUE
1. **Re-run the H1/H2 split on the NEW base** (the registered prediction above). Two runs, together.
2. **Then `close > open`** — still the last untested signal term, now against the new base.
3. **Then re-test `coolBars` 90 and 150** if the sample thinness becomes the binding objection — a
   finer grid around 120 would tell us whether the peak is broad, which the 60/120/240 grid cannot.

**NEW BASE: PF 1.30380521, DD 8.12167991%, 77 trades, 48.05% win, long-only, `coolBars` 120.**
**Still no champion** — a champion needs a validated result, and a 77-trade profit factor is a
direction.


---

## ██ ATTACK 25 — THE REGISTERED FALSIFICATION HELD. THE REGIME GAP IS GONE. (2026-09-02)

Last cycle promoted `coolBars` 120 and registered this test **before** running it, as HARD LESSON 17
requires: *if the promotion is really a chop fix, the H1/H2 spread should narrow — and if it does not,
the promotion is a whole-sample coincidence and I will say so.*

| Half | Old base (`coolBars` 60) | **New base (`coolBars` 120)** | Change |
|---|---|---|---|
| H1 · 2024-06-08 → 2025-07-20 | 1.55157635 | 1.30542369 | **−0.246** |
| H2 · 2025-07-20 → 2026-09-01 | 0.77846786 | 1.30384915 | **+0.525** |
| **Spread** | **0.773** | **0.0016** | **−99.8%** |

**The gap did not merely narrow. It effectively closed** — the two halves now sit within 0.0016 of
each other, and they moved in exactly the predicted direction: the choppier half rose the most.
45 + 32 = 77 reconciles against the whole-sample run.

**This is the first regime-stable result this project has produced**, across all three labs. Every
prior candidate here was a blend of a good period and a bad one — Attack 16 said so explicitly, and
Attack 15 *widened* the spread while improving both halves.

### WHAT THIS COSTS, SAID PLAINLY
**It was a trade, not a free gain.** H1 — the half that already worked — gave up 0.246 of profit
factor. The whole-sample number still improved (1.153 → 1.304), so the trade paid, but a strategy that
is uniformly mediocre is not automatically better than one that is excellent half the time; **it is
better only because the bad half was losing money and now is not.** That is the actual argument, and
it should not be dressed up as a pure improvement.

### THE QUALIFICATION THAT KEEPS THIS HONEST
**The halves reach the same profit factor by different routes.**

| Half | Profit factor | Win rate | Payoff ratio |
|---|---|---|---|
| H1 | 1.30542369 | 51.11% | 1.24866614 |
| H2 | 1.30384915 | 43.75% | 1.67637748 |

Near-identical PF, **7.4pp apart on win rate.** H1 wins more often and smaller; H2 wins less often and
bigger. So the equality is real at the level of profit factor and **not** at the level of behaviour —
the strategy is not doing the same thing in both regimes, it is arriving at the same score two ways.
A single number agreeing this precisely on 45 and 32 trades also deserves suspicion on its own terms.

### SAMPLE FLOOR HONOURED
45 and 32 trades are below the floor enforced on Attack 24, when a 7-trade PF of 2.30 was refused.
**The DIRECTION of the spread is what is read here; neither half is quoted as a standalone result.**

### QUEUE
1. **`close > open`** — still the last untested signal term, now against the new base.
2. **`coolBars` 90 and 150** — a finer grid. The 60/120/240 grid cannot tell a broad peak from a
   narrow one, and Attack 24's upper bound was degeneracy rather than a measured worse value
   (HARD LESSON 19).
3. **The thin-sample problem is now the binding constraint on this lab**, not the profit factor.
   77 trades is the cost of the fix that worked.

**BASE: PF 1.30380521, DD 8.12167991%, 77 trades, `coolBars` 120, long-only. Still no champion** —
but for the first time the obstacle is sample size rather than a broken half.
