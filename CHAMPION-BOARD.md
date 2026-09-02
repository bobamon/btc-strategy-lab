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
| Attack 1 | Require close above EMA200 | PF 0.89→0.91, DD 35.0%→28.8%, trades 468→433 | **KEPT** |
| Attack 2 | Require shallow pullback (low holds above VWAP) | PF 0.91→0.85, DD 28.8%→32.6%, trades 433→342 | **REVERTED** — worse on both terms |
| Attack 3 | Ban entries in the 1–4am ET witching window | PF 0.9121→0.9405, DD 28.780%→28.844%, trades 433→420 | **REVERTED** — PF up, DD worse by 0.064pp |
| Attack 4 | Raise R floor 0.8% → 1.2% | PF 0.912→0.885, DD 28.8%→36.6%, win rate 38.3%→40.2% | **REVERTED** — wider stops mean bigger losses |
| Attack 5 | Require volume above the 50-bar average on the reclaim | PF 0.912→0.839, DD 28.8%→26.9%, trades 433→241, commission $3,954→$2,078 | **REVERTED** — fee saving realised, edge lost with it |
| Attack 7 | Raise the target 2R → 3R | PF 0.9121→0.9100, DD 28.8%→33.0%, payoff 1.498→1.787, win rate 38.3%→33.7% | **REVERTED** — payoff gain exactly cancelled by win-rate loss |

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
