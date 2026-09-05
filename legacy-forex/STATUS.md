# LEGACY FOREX TRADER — WORKSTREAM STATUS

**Created 2026-09-05, on the first rotation tick that ever actually reached this workstream.**

This workstream is one of the four the scheduled prompt rotates through. It has **never been worked
before this tick**, and the reason is recorded here rather than left as a silent gap.

---

## ██ FINDING 1 — THE SPEC THIS WORKSTREAM IS SUPPOSED TO RUN FROM DOES NOT EXIST

The scheduled prompt says:

> *(3) LEGACY FOREX TRADER - trades NQ and YM ONLY, 5m/15m only, New York session only. **Fully
> specified in legacy-forex/SYSTEM.md**.*

**There is no `legacy-forex/SYSTEM.md`, and there never has been.** Verified this tick, three ways:

| check | command | result |
|---|---|---|
| file present anywhere in the working tree | `ls -d legacy*` | nothing |
| file present in ANY commit on ANY ref | `git log --all -- 'legacy-forex/*' 'legacy*'` | **zero commits** |
| string mentioned anywhere in the repo | `grep -ril legacy` over `*.md`/`*.txt`/`*.json` | **zero hits** |

There are exactly two committed transcript sets — `war-formation/transcripts/` and
`three-m-elite/transcripts/` — and **neither contains NQ or YM material**. The only NQ/YM references
in the whole repo are in the archived index-era specs `strategies/001`/`002`, `results/SCHEMA.md`,
and the ledger's own ARCHIVED note.

So the prompt asserts a source of truth that is not in the repo. Per the standing rule that
transcripts committed here are the source of truth, and per the ABSOLUTE RULE, **the correct action
is to record the gap, not to invent a specification for a system I have never seen.** Writing a
plausible-looking NQ/YM rule set out of general trading knowledge would be exactly the fabrication
the mandate forbids, and it would then be inherited by every later tick as if it were the trader's
own words.

**Nothing about this workstream can advance until the spec (or the source video/transcript) is
committed to the repo by the user.**

---

## ██ FINDING 2 — NQ AND YM ARE STILL SILENTLY REMAPPED, AND THE REMAP IS INVISIBLE IN `parityAdjustments`

The ledger's ARCHIVED note (2026-09-01) recorded that `NQ` and `YM` silently remap on this engine.
**Re-verified today, 2026-09-05, with real `plan_backtest_window` calls** — and the re-check found the
hazard is *worse* than the original note described.

| requested | engine applied | coverage returned |
|---|---|---|
| `NQ`, 5m, 2024-01-01 → 2026-09-01 | **`BYBIT:IONQUSDT.P`** | 14,267 bars, first bar **2026-07-17** |
| `YM`, 5m, 2024-01-01 → 2026-09-01 | **`BYBIT:DYMUSDT.P`** | 235,343 bars, first bar **2024-06-09** |
| `US30`, 5m | hard error — *"not in the Bybit USDT perp catalog (639 instruments)"* | — |
| `NAS100`, 5m | hard error — same | — |
| `USTEC`, 5m | hard error — same | — |
| `US500`, 5m | hard error — same | — |

**The new part, and it matters.** The `plan_backtest_window` tool description tells callers to
*"ALWAYS call this (or trust `quick_backtest` `parityAdjustments`) so you do not invent unavailable
history."* On the NQ and YM calls, `parityAdjustments` contained **only a date clamp**
(`clamped_to_clickhouse_first_bar`). **No adjustment entry names the symbol substitution at all**, and
the response's own `requested.symbol` field comes back already rewritten to `IONQUSDT` / `DYMUSDT` —
so the echo that would normally let you catch a substitution has been overwritten by the substitution.

**Consequence: `parityAdjustments` is NOT a sufficient guard against a wrong-instrument backtest.**
A session that followed the tool's own advice and trusted `parityAdjustments` would receive genuine,
correct-looking metrics for a quantum-computing stock proxy and a Cosmos-ecosystem altcoin, and
nothing in the response would flag it. The only reliable check is to read `applied.displaySymbol` and
compare it, by eye, to what you asked for.

**Mechanism, confirmed not guessed.** `search_perps("NQ")` returns exactly one row — `IONQUSDT`,
baseCoin `IONQ`. The resolver is doing a substring match of the requested ticker against the crypto
catalog's base coins: `NQ` ⊂ `IONQ`, `YM` ⊂ `DYM`. **Any short futures root is therefore at risk of
matching an unrelated altcoin**, which is precisely why `US30`/`NAS100`/`USTEC`/`US500` fail loudly
(no substring match exists) while `NQ`/`YM` fail silently (one does).

---

## ██ FINDING 3 — A NON-CRYPTO DATA PATH EXISTS ON THIS ENGINE AND THIS LAB NEVER KNEW IT

This is a **correction to a conclusion already recorded in `STRATEGY-LEDGER.md`**, which is the
outcome the mandate says to prefer.

The ARCHIVED note concluded the index universe was unreachable and the lab narrowed to BTC-only.
That conclusion is correct **about indices**. But the lab tested four *index* tickers and then
generalised to "this engine is Bybit USDT perps only" — it **never tested a forex pair**. The tool's
own description says, in a clause nobody in this repo has ever quoted: *"Forex pairs (EURUSD) pass
through unchanged."*

Verified today with real calls:

| symbol | timeframe | applied `displaySymbol` | first bar | last bar | bars in window |
|---|---|---|---|---|---|
| `EURUSD` | 5m | **`EURUSD`** (unchanged) | 2009-09-25 | **2026-05-19 10:30Z** | 1,152,867 |
| `EURUSD` | 15m | **`EURUSD`** (unchanged) | 2009-09-25 | **2026-05-19 10:30Z** | 318,187 |
| `XAUUSD` | 5m | **`XAUUSD`** (unchanged) | 2009-09-27 | **2026-05-19 11:35Z** | 959,407 |

Three things follow, and only the first two are established:

1. **Established:** the engine carries a genuine non-crypto feed with ~17 years of history on both of
   the timeframes this workstream needs (5m and 15m). No remap, no substitution.
2. **Established:** that feed is **stale by roughly 3.5 months** — it ends 2026-05-19, where the
   crypto feed runs to 2026-09-01. Any forex window must be stated as ending 2026-05-19, and the
   most recent quarter is simply not testable. This is a real limitation, not a footnote.
3. **NOT established, and must not be assumed:** that a NY-session index system transfers to a forex
   pair. It almost certainly does not — HARD LESSON 9 (a gate is only good relative to the anatomy of
   its setup) and the repeated cross-lab inheritance failures both say a mechanism built for the
   Nasdaq's opening drive is a *hypothesis* on EURUSD, never an inheritance. **EURUSD is not a
   substitute for NQ.** It is only evidence that the "no non-crypto data" premise was wrong.

---

## ██ WHAT THIS TICK DID NOT ESTABLISH

- **Nothing about the Legacy Forex system's rules**, because no spec exists to read.
- **No performance number of any kind.** No backtest was run this tick. There is no PF, no drawdown,
  no trade count for this workstream and there must not be one written anywhere until a real `runId`
  produces it.
- **Whether NQ/YM data is reachable by some other alias.** Six tickers were tried
  (`NQ`, `YM`, `US30`, `NAS100`, `USTEC`, `US500`). Two remap, four hard-error. Other vendor
  conventions (`NQ1!`, `MNQ`, `DJI`, `NDX`, `SPX`) were **not** tried and remain open.
- **Which non-crypto symbols exist in total.** `search_perps` searches the crypto catalog only
  (its own description says so), so the forex/metals catalog has no enumerable listing from here.
  `EURUSD` and `XAUUSD` were found by direct probe, not by listing.

---

## ██ AN OBSERVATION ABOUT CREDIT ACCOUNTING, RECORDED BECAUSE IT CONTRADICTS THE LEDGER

`STRATEGY-LEDGER.md` states *"Each backtest costs 1 credit."* This tick ran **zero** backtests —
only eight `plan_backtest_window` calls (two of which hard-errored) and one `search_perps`. Balance
measured with `get_credits` at the start of the tick: **519**. Measured again after those calls:
**518**.

**One credit was consumed without a backtest being run.** I cannot attribute it to a specific call
(the two measurements bracket all of them), and I cannot rule out a concurrent session on the same
account spending it. Recording it as an observation, not a conclusion: **the cost model is not
"backtests only", or the balance is not exclusively this session's.** Worth one deliberate
measurement on a future tick — call `get_credits`, one `plan_backtest_window`, `get_credits` again —
before any tick budgets on the assumption that pre-flight calls are free.

---

## ██ QUEUE — IN PRIORITY ORDER

1. **FOR THE USER, BLOCKING EVERYTHING ELSE HERE: commit the Legacy Forex source.** Either
   `legacy-forex/SYSTEM.md` itself, or the transcript of the video it was decoded from, in
   `legacy-forex/transcripts/`. Until one of those lands, every future rotation tick that reaches
   this workstream will land exactly here and be able to do nothing — the same degenerate no-op loop
   the War Formation and 3M Elite streams have been stuck in for 32 and 29 checks respectively.
2. **FOR THE USER: confirm the instrument.** If the system genuinely requires NQ and YM cash-index or
   futures data, this engine cannot test it at all, and the workstream is Pine-and-decode-only here
   until a data path exists. If a related instrument is acceptable, say which — that is a trading
   decision, not one this lab should make on its own.
3. **Cheap and unblocked:** probe the remaining ticker conventions (`NQ1!`, `MNQ`, `DJI`, `NDX`,
   `SPX`, `GBPUSD`, `USDJPY`) with `plan_backtest_window` to map the non-crypto catalog's actual
   edges. Read `applied.displaySymbol` on every one — per FINDING 2, `parityAdjustments` will not
   warn you.
4. **Propagate FINDING 2 as a standing check.** Every backtest in every lab in this repo should
   assert `applied.displaySymbol` matches intent. All existing BTC results happen to be safe
   (`BTCUSDT` matches itself), so nothing recorded needs withdrawing — but the guard is currently
   absent from the ledger's platform-constraints section and should not be.

---

## ██ STATUS LINE

**LEGACY FOREX: BLOCKED, NOT FAILING.** No spec, no source material, no data path for its stated
instruments. Zero results recorded, correctly. The workstream cannot be advanced by this session and
will not be advanceable by any future session until the user commits the specification.

---

# ██ STATUS CORRECTION AND TICK #2, 2026-09-05 — THE SPEC EXISTS; THE ENGINE-SAFETY QUESTION IS NOW ANSWERED

## FIRST, A CORRECTION TO THIS FILE'S OWN FINDING 1

Everything above was written by a scheduled cloud run whose reasoning was sound and whose **premise
was stale**. It concluded "there is no `legacy-forex/SYSTEM.md`, and there never has been" and verified
that three ways against the remote it could see.

**`legacy-forex/SYSTEM.md` did exist at that moment — on a local machine, committed but never pushed.**
The cloud run was reading a remote that genuinely did not have it. Its checks were correct; its world
was incomplete, through no fault of its own. The spec, the 18 committed transcripts, and the Pine
visualiser are all in the repo now.

**Finding 1 above is therefore withdrawn.** It is left in place rather than deleted, because "an agent
concluded a file never existed when it existed unpushed" is exactly the kind of failure this project
records instead of tidying away. **Findings 2 and 3 of that entry — the remap mechanism and the
forex-feed discovery — are unaffected and stand.**

---

## FINDING 4 — THE TWO ENGINES BEHAVE DIFFERENTLY ON THE EXACT SYMBOLS THIS WORKSTREAM NEEDS

This had never been checked on `backtest-lab`, only on trader-dev. Checked now, zero credits:

| Symbol | trader-dev | `backtest-lab` |
|---|---|---|
| `NQ` | **silently remapped** → `BYBIT:IONQUSDT.P` (a crypto perp) | **hard error** — no data |
| `YM` | **silently remapped** → `BYBIT:DYMUSDT.P` (a crypto perp) | **hard error** — no data |
| `NAS100` | hard error | ✅ resolves → `^NDX`, real index (~29,344) |
| `US30` | hard error | ✅ resolves, real index |

`search_symbols("NQ")` on `backtest-lab` returns **empty across all four exchanges** — no `IONQ`
substring match, nothing to silently latch onto.

### THE ROUTING RULE THIS CREATES, AND IT INVERTS THE PROJECT'S DEFAULT

**Legacy Forex work must run on `backtest-lab`, NEVER on trader-dev.** That is the opposite of War
Formation and 3M Elite, which must run on trader-dev and must not be ported. The reason is not
preference, it is safety:

- On **trader-dev**, this workstream's two instruments fail in the **worst possible way** — a plausible
  backtest of a completely different asset, with `parityAdjustments` reporting only a date clamp and
  never naming the substitution. A cycle could bank a full result for `IONQUSDT` believing it had
  tested the Nasdaq.
- On **`backtest-lab`**, they fail in the **best possible way** — loudly, with no result at all.

A hard error is a good outcome here. It cannot be mistaken for a finding.

---

## FINDING 5 — THE FUTURES-VS-CASH OBJECTION IS WEAKER THAN THIS FILE CLAIMED, AND THE REASON IS HIS OWN SESSION RULE

`SYSTEM.md` records the futures/cash mismatch as a major declared deviation: NQ/YM are futures, the
engine has cash indices, and their sessions, overnight behaviour, roll and sizing all differ.

Research this tick says that objection **mostly does not apply to a strategy like his**, and the
reason is a rule he already states himself.

Practitioner guidance on backtesting index futures is explicit about session matching:

> "If you trade index futures during Regular Trading Hours (9:30 AM to 4:00 PM EST), **backtest on
> RTH**. If you trade the overnight session, backtest on ETH... **mixing sessions corrupts your
> results** because price action, volume, and spread behavior differ significantly."

**He trades New York session only, first entry 09:30 ET** (`8._SESSIONS_TO_TRADE`). That is RTH,
exactly. The differences that make NQ ≠ NAS100 — the near-24-hour Globex session, overnight gaps,
thin ETH liquidity — live almost entirely **outside the window he trades**. Cash-index RTH data is
therefore a *defensible* basis for an RTH-only strategy rather than the serious distortion this file
previously implied.

**What survives of the objection, and it is not nothing:**
- **Settlement and basis.** "YM settles at its own time, and its settlement print rarely matches the
  index's 4 p.m. close to the point." The basis is time-varying and must not be treated as a
  constant, "especially across a quarterly roll." Directionally aligned, never identical.
- **Sizing is still unmappable.** His stop is quoted in **points** with contract/tick values
  (`11._STOP_LOSS_ADJUSTMENT`: "that's a 25 point stop loss"). A cash index has no contract size, so
  the percentage-stop substitution remains a real declared deviation.

**Net effect on the workstream:** the instrument objection drops from *blocking* to *manageable and
declared*. **The data-depth blocker is untouched and is still the thing that stops this workstream.**

---

## WHERE THIS WORKSTREAM ACTUALLY STANDS

| | |
|---|---|
| Spec | ✅ complete, decoded from 18 transcripts with verbatim quotes |
| Pine visualiser | ✅ `legacy-forex/pine/VISUAL-legacy-forex-complete.pine` |
| Engine routing | ✅ resolved — `backtest-lab` only, never trader-dev |
| Instrument proxy | ✅ defensible for RTH, with declared deviations on sizing and basis |
| **Data depth** | ❌ **STILL BLOCKING** — 15m ~30 days (573 bars, ~21 sessions), 5m does not resolve |
| Backtest | ❌ none, and none should be run until the sample question is solved |

At his 2-trade daily cap, ~21 sessions caps the sample near 42 in a perfect world and near 20 in a
realistic one — below the 30-trade floor. **Nothing has been backtested and no number appears in this
file or in `SYSTEM.md` that came from a run, because no run has happened.**

## QUEUE

1. **Do not run a Legacy Forex backtest on trader-dev under any circumstances.** Finding 4 is the
   reason. If a future cycle is tempted, re-read it.
2. **The data-depth blocker is the only thing left.** A futures source with intraday depth (NQ/YM 5m
   over years) solves the sample and the instrument question together. Neither engine has one.
3. **Forward-testing needs no history** — run the Pine live on NQ/YM 5m during New York session and
   record signals as they occur. Slow, but honest, and available today.
4. If a 30m proxy is ever run to test whether the *structure + level-break + volume* stack has any
   edge at all, it must be labelled a proxy and **must never be recorded as a test of his system**.
5. The nine unnumbered `videoNNNN` transcripts (up to 68 minutes each) are committed but still not
   decoded; they may refine the rules above.

---

# ██ TICK #3, 2026-09-05 — I OVERSTATED THE DATA BLOCKER. BOTH HALVES OF IT WERE WRONG.

Zero credits. No backtest. Three `plan_backtest_window` calls on `backtest-lab`.

`SYSTEM.md` records the blocker as: *"15m resolves only over ~30 days (573 bars, ~21 sessions) and 5m
does not resolve at all over 60 days."* **Both halves are wrong, and the error was mine.**

| Symbol | TF | Window | Result |
|---|---|---|---|
| `NDX` | 15m | 2026-07-08 → 2026-09-05 | ✅ **1,119 bars**, ~41 sessions |
| `USTEC` | 15m | same | ✅ **1,119 bars** (identical — same underlying) |
| `NAS100` | 5m | 2026-08-20 → 2026-09-05 | ✅ **937 bars**, ~11 sessions |

**What I got wrong:**
1. **15m gives ~41 sessions, not ~21.** My earlier check requested only a 30-day span and I recorded
   the answer as if it were the cap. The documented ~60-day Yahoo limit is real and I simply
   under-requested. 1,119 bars, not 573.
2. **5m does resolve.** I recorded "not at all", having asked for a 60-day 5m window that exceeded
   its shorter cap. Ask for ~16 days and it returns 937 bars. An error window is not the same as no
   data, and I treated it as such.
3. `NDX` and `USTEC` return byte-identical coverage to `NAS100` — no alias has deeper retention, so
   that idea is closed.

**Revised sample arithmetic:** ~41 sessions at his 2-trade daily cap gives a ceiling near **82**, not
42. Against his no-trade-day rules a realistic figure is perhaps **20–40** — straddling the 30-trade
floor rather than sitting clearly below it. **The workstream is marginal, not hopeless.**

## THE BINDING CONSTRAINT IS THE ENGINE, NOT THE DATA

With the data claim corrected, what actually blocks a faithful backtest is unchanged and structural:

- **`backtest-lab` has the instruments but cannot express the method.** Its `custom` strategy is
  stateless numpy over OHLCV — no pivot function, no latched swing state. His method needs confirmed
  higher-highs *and* higher-lows, touch-validated S/R levels, break detection against those levels,
  and a daily trade counter. None of that is expressible.
- **`trader-dev` can express the method but not the instruments.** Pine holds all the state needed,
  but `NQ` and `YM` silently remap to `IONQUSDT` and `DYMUSDT`, and `NAS100`/`US30` hard-error.

**So the honest position is: neither engine can run this system faithfully.** That is the same shape
as War Formation's check #36 finding — the engine with the state lacks the data, the engine with the
data lacks the state — arrived at independently in a second workstream on the same day.

**What I will not do:** approximate his structure with a Donchian-plus-volume proxy on backtest-lab
and record it as a test of his method. It would run, it would produce numbers, and the numbers would
be about a different strategy.

## QUEUE

1. **Correct the blocker text in `SYSTEM.md`** — it currently states two figures now known wrong.
2. A faithful test needs either pivot/state support on `backtest-lab` or correct NQ/YM symbols on
   trader-dev. Neither is in this project's control.
3. **Forward-testing remains available today** and needs no history: run the Pine visualiser live on
   NQ/YM 5m during New York session and record signals as they occur.
4. Nine `videoNNNN` transcripts remain undecoded and may refine the rules.

---

# ██ TICK #4, 2026-09-05 — THE CORPUS IS TWO TRADERS, AND THE TARGET RULE WAS NEVER DECODED

Zero credits. **No backtest, no `plan_backtest_window`, no engine call of any kind.** This tick is
pure decode: the nine `videoNNNN` transcripts (queue item 4 of tick #3, and item 5 of the original
`SYSTEM.md` queue — outstanding since the workstream opened) plus the two numbered modules
`SYSTEM.md` had never cited, `4._WHAT_ARE_CONTRACTS_AND_TICKS` and `10._USING_DATA`.

Full detail, with every verbatim quote and timestamp, is in `SYSTEM.md` FINDINGS 6–10.

## THE HEADLINE — THE 18 TRANSCRIPTS ARE NOT ONE SYSTEM

`SYSTEM.md` opened with *"Source: … 18 videos"* and treated the whole directory as one man's method.
**Two coaches from the same prop firm are mixed in it**, and nothing in the filenames separates them:

- **Mamba** — New York session, NQ and YM, 5m/15m only, structure + level break + volume. This is the
  Legacy Forex Trader the workstream exists to specify. Eight numbered modules and five of the nine
  live streams.
- **Coach Luca ("Luca No Limit")** — **Asia session**, **gold (`MGC`)**, 1m through 1h, **ATR-derived
  stops**, **fair value gaps**, a **200 MA**, previous-day high/low, his own `edgematrix.com`
  indicator. Module `4.` (which he narrates *about* Mamba) and four of the nine live streams.

They are explicitly colleagues, not the same person: *"tomorrow morning during **mamba stream**"*
(`video1083955301` [53:19]); *"**Mamba** just called me"* (`4.` [00:00]).

**No existing rule in `SYSTEM.md` was corrupted** — all eight modules it decoded are Mamba's. But that
was luck: the two modules it had *not* cited included the one Luca narrates, and a tick that had read
the four long `videoNNNN` files as "more of the same trader" would have imported ATR stops, FVGs and a
200 MA into a system that has none of them. The file-by-file split is now recorded in `SYSTEM.md`
FINDING 6 and must be consulted before quoting any transcript in this directory again.

## THREE MECHANICAL RULES THAT WERE IN THE SOURCE AND NOT IN THE SPEC

1. **The target is an output, not a range.** `10._USING_DATA` — never cited before — gives the rule
   that sets it: average the achieved R of the last ~6 closed trades **with a loss scored 0**, round
   it, and trade that R tomorrow; recompute after every close. `SYSTEM.md` had recorded only *"1:3 to
   1:5 R"*, which is where that output usually lands. Three defects in the rule are recorded with it,
   including that it is **structurally biased downward** (a winner's recorded R is capped by the
   target it exited at, while a loss drags the mean toward 0) — written down before any run, per
   HARD LESSON 17.
2. **The stop has a hard maximum, and the maximum is a setup filter.** *"That's a 25 point stop loss,
   which is solid"* vs *"64 points. No, my account's gone if I do that"* (`11.` [00:07]/[01:26]). A
   structural stop wider than ~25–30 points **rejects the setup**; it is not re-stopped nearer. That
   is a gate, and gates change trade counts, which is this workstream's binding problem.
3. **The 2/day cap counts across NQ and YM together**, not per instrument — he runs both concurrently
   (*"bot nasdaq bot us 30"*, `video1038794732` [05:35]; *"we're taking two trades in a day"* while
   holding one of each, `video1263885792` [03:58]). A per-symbol reading would have doubled the
   ceiling.

## ONE CONTRADICTION, RECORDED AND NOT RESOLVED

The modules gate direction on structure (bullish → buys only). **The live streams show him pre-marking
a break level on both sides of both instruments and taking whichever goes** — *"Be prepared for all
four positions on the screen"* (`video1263885792` [01:28]). Stated method vs observed behaviour. The
course gate stays ON by default in the Pine; the forbidden counter-structure level is now drawn as a
dotted bracket so the disagreement is visible rather than buried. Only a run can settle it.

## THE SAMPLE ESTIMATE IS NOW ANCHORED ON HIS OWN NUMBER, AND IT GOT WORSE FOR 5m

Every prior estimate in this file was derived from the **cap** (2/day), because that was the only
figure available. `10._USING_DATA` gives the realised rate from his own journal: *"the last two weeks
of trades, which is typically anywhere from **six to eight trades**"* [00:38], and his worked example
is *"**six trades**… about **nine days** worth"* [02:22] — **0.67–0.89 trades per session, roughly a
third of his cap.**

Applied to tick #3's measured coverage:

| tf | bars measured (tick #3) | RTH sessions | × 0.67–0.89 | vs the 30-trade floor |
|---|---|---|---|---|
| 15m | 1,119 | ~43 | **~29–38** | straddles it |
| 5m | 937 | ~12 | **~8–11** | **short by ~3×** |

Tick #3 said the workstream was "marginal, not hopeless" on a 20–40 guess. That verdict survives for
15m and is now sourced rather than guessed. **For 5m it does not: 5m cannot produce a quotable sample
on this data source, and that is now a firmer statement than tick #3's.** This is an estimate, not a
result — HARD LESSON 4 says score it against the actual count and never build on it.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number here came from a run.** Nothing was backtested; no `runId` exists for this workstream and
  none should until the sample question is settled.
- The stated-vs-observed direction contradiction is **unresolved** and cannot be resolved from
  transcripts.
- Whether the rolling-mean target helps or hurts is **untested**, with a stated reason to expect it to
  ratchet down.
- The four gold transcripts were **identified, not decoded**. They are a different system; if they are
  ever worked they are a fifth workstream, and nothing from them may enter this one.
- The `US30`/`NQ` de-correlation claim (`video1038794732` [02:28], *"not in sync… out of sync
  completely"*) is a **descriptive** observation of the kind HARD LESSON 14 says to mine, it is cheap
  to measure, and **no engine in this project has both symbols with the depth to measure it.** Queued.

## QUEUE

1. **Before quoting any transcript in this directory, check FINDING 6's file-by-file split.** This is
   now the first rule of this workstream.
2. The engine deadlock from tick #3 is unchanged: `backtest-lab` has the instruments but cannot
   express the method; trader-dev can express the method but silently remaps the instruments. **Do not
   run a Legacy Forex backtest on trader-dev under any circumstances** (tick #2, FINDING 4).
3. If a run ever becomes possible, **measure the rolling-mean target against a fixed target** — that
   is the one pre-registered question this workstream now has, and FINDING 7 predicts the direction.
4. **Forward-testing still needs no history** and is still the only honest route available today: run
   `pine/VISUAL-legacy-forex-complete.pine` live on NQ/YM 5m during New York and record signals.
5. Measure the NQ/YM de-correlation claim if an engine ever carries both.

---

# ██ TICK #5, 2026-09-05 — THE ONE QUANTITATIVE CLAIM THIS WORKSTREAM HAD WAS COMPUTED ON THE WRONG DENOMINATOR

Zero credits. **No backtest, no `plan_backtest_window`, no engine call of any kind.** Pure re-analysis
of material already in the repo. Full detail in `SYSTEM.md` FINDINGS 11–12.

## THE HEADLINE — 15m IS BELOW THE SAMPLE FLOOR, NOT STRADDLING IT

Tick #4's FINDING 9 multiplied a trade rate of 0.67–0.89/session by ~43 sessions of `NDX` 15m coverage
and got ~29–38 trades, giving this workstream its standing "marginal, not hopeless" verdict.

**The two inputs are measured on different units.** The rate is his journal rate — *"every trade that
I took"* — and tick #4's own FINDING 10 had already established that his trades span **both** NQ and
YM and that his 2/day cap counts across the book. The bar count is **one** instrument (`NDX`). A
book-wide rate times single-instrument sessions double-counts.

**His own numbers force this.** A per-instrument rate of 0.67–0.89 implies 1.33–1.78/session across
two instruments = 13–18 trades per fortnight. He says the fortnight count is *"six to eight trades"*.
Off by ~2×. Only the book-wide reading is consistent with the source.

| tf | sessions | **single instrument** | **pooled NQ+YM** | vs the 30 floor |
|---|---|---|---|---|
| 15m | ~43 | **~13–17** | ~26–34 | single **below**; pooled straddles |
| 5m | ~12 | **~4–5** | ~7–10 | far below either way |

The pooled 15m band nearly recovers tick #4's figure — **but only under a two-instrument pooled
backtest that no tick here has ever declared, and that FINDING 9 was not describing.** Pooling to
clear a sample floor is a methodological choice needing its own justification, and it silently assumes
`US30` intraday depth matches `NAS100`, **which has never been measured.**

A second, smaller error rides along: the 0.89 top end came from dividing the *two-week* trade count by
the *nine-day* worked example's span. The internally consistent band is **0.60–0.80** book-wide.

## THE SECOND FINDING — THE TARGET RULE CANNOT RESOLVE ITS OWN RANGE

His worked example is `{3, 0, 2.5, 5, 5, 3}` → 18.5/6 = 3.08. His arithmetic reproduces to the cent.
But sample SD = 1.855, SE = 0.757, and the **95% CI on that 3.08 is [1.14R, 5.03R]** — wider than the
entire 1:3–1:5 range the rule is meant to select within. At n=6 the rule cannot distinguish 1:3 from
1:5, or either from 1:1.1. And the rounding is brutal: **two extra losses move the traded target a
full R.** Combined with FINDING 7's downward bias, that is a mechanism for ratcheting the target down
exactly after a bad run.

Searched for published evidence on the rule. **Found none specific to it, and recorded that absence
rather than substituting adjacent material.** What adjacent material says: the same idea done properly
uses 100–200 journal trades, not six; calibrating a target to realised R is itself sound; and his
"slow refresh rate" premise has real support in volatility clustering. **His intent is defensible, his
estimator is not.** A discriminating pre-registered test is now written down (window 6 vs ~20).

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` was created and none should be until the sample question
  is settled.
- Whether **pooling NQ and YM** is legitimate — the de-correlation claim that bears on it is still
  unmeasurable on both available engines.
- Whether **`US30` intraday coverage matches `NAS100`** — the pooled column assumes it, nobody checked.
- Whether the rolling-mean target helps or hurts. Two falsifiable predictions registered, both unrun.

## QUEUE

1. **Measure `US30` 15m and 5m depth on `backtest-lab`** (zero credits, one `plan_backtest_window`
   each). The pooled sample band is unverified without it, and it is the cheapest open item here.
2. **Decide and declare whether NQ+YM trades may be pooled into one sample** *before* any run uses the
   pooled count to clear the 30-trade floor. Pooling is how 15m gets over the line; doing it silently
   is how a sample floor gets defeated on paper.
3. Engine deadlock unchanged (tick #3): `backtest-lab` has the instruments but cannot express the
   method; trader-dev can express the method but silently remaps the instruments. **Do not run a
   Legacy Forex backtest on trader-dev under any circumstances** (tick #2, FINDING 4).
4. If a run becomes possible, the pre-registered questions are now (a) rolling-mean vs fixed target,
   and (b) window 6 vs ~20, which discriminates noise from bias.
5. **Forward-testing still needs no history** and remains the only honest route available today.
6. Check the trade rate against a real count the moment one exists — every figure here is an estimate
   (HARD LESSON 4).

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED ON THE ENGINE, AND NOW WORSE ON SAMPLE THAN RECORDED.** Single-instrument
15m is ~13–17 expected trades against a 30 floor. The workstream's "marginal, not hopeless" verdict
survives **only** as a statement about a pooled two-instrument backtest, and that pooling has never
been declared or justified. Zero results recorded, still correctly.

## ██ CREDIT NOTE, FOR CONTINUITY WITH TICK #1's OPEN QUESTION

Balance at the start of this tick, measured with `get_credits`: **500**. Tick #1 measured 518; the
scheduled prompt asserts 524. **This tick spent nothing** — one `get_credits` call and no engine call
of any kind — so it adds no evidence either way. The drift between ticks is expected: War Formation
and 3M Elite ran real backtests in between. **Tick #1's one-credit-without-a-backtest anomaly remains
unresolved, and the deliberate bracket it proposed (`get_credits` → one `plan_backtest_window` →
`get_credits`) was NOT performed this tick.** It stays queued for a tick that has a reason to call
`plan_backtest_window` anyway — queue item 1 above is exactly such a tick.

---

# ██ TICK #6, 2026-09-05 — THE POOLING QUESTION IS CLOSED, AND POOLING LOSES

Zero credits. **No backtest, no `plan_backtest_window`, no engine call of any kind.** Transcripts
already in the repo, plus web research. Full detail in `SYSTEM.md` FINDINGS 13–14.

## FIRST, WHAT THIS TICK COULD NOT DO

Tick #5's queue item 1 was *"measure `US30` 15m and 5m depth on `backtest-lab`"* — the cheapest open
item here. **This session has no `backtest-lab` connector.** Only trader-dev is attached, and
trader-dev is the engine this workstream is forbidden to touch (tick #2, FINDING 4: `NQ`→`IONQUSDT`,
`YM`→`DYMUSDT`, silently). The item is **blocked by session capability, not stale**, and it stays
queued for a session that has the connector. Tick #1's credit-bracket experiment, which was to ride
along with that call, is likewise still unperformed.

## THE HEADLINE — POOLING NQ+YM CANNOT CLEAR THE 30-TRADE FLOOR, AND THE VERDICT DOES NOT NEED ρ

HARD LESSON 56's corollary left this open as *"somewhere between N and 2N depending on a correlation
nobody has measured."* **The question is decidable without that measurement.**

His pooled book is **N pairs** — one NQ trade and one YM trade in the same session, evidenced in three
separate streams (*"bot nasdaq bot us 30"*; *"$60,000 on Nasdaq, $26,000 on us 30 — we're taking two
trades in a day"*; *"this is two positions one day"*). For paired outcomes with within-pair
correlation ρ, `N_eff = 2N/(1+ρ)`. Against FINDING 11's corrected band (~13–17 single, ~26–34 pooled):

| ρ | `N_eff`, bottom of band | `N_eff`, top of band | clears 30? |
|---|---|---|---|
| 0.0 | 26.0 | 34.0 | top only |
| 0.5 | 17.3 | 22.7 | **no** |
| 0.9 | 13.7 | 17.9 | **no** |

- **At the bottom of the band, 26 < 30 — pooling fails even at perfect independence.**
- **At the top, clearing 30 requires ρ ≤ ~0.13.** No published figure for two US equity index futures
  is remotely that low.
- **At ρ = 0.9, the pooled book is worth 13.7–17.9 independent trades against the single instrument's
  13–17 — running both buys less than one extra independent observation.**

**Declared, before any run:** NQ and YM trades **may not be pooled to clear the sample floor**. A
pooled count may describe his book; it may not be quoted as a sample size. Reversal condition stated
and falsifiable: a **trade-level, holding-period** ρ ≤ 0.13.

**And the trap is named in advance:** do **not** satisfy that condition by correlating 5m or 15m bars.
The **Epps effect** — measured correlation falls as sampling frequency rises, documented since Epps
(1979) — makes a short-horizon number systematically too low, and his trades are held for hours. The
independence question lives at the holding-period horizon, not the chart horizon.

## THE SECOND FINDING — HIS DE-SYNC OBSERVATION SURVIVES, BUT HIS OWN BOOK CONTRADICTS THE USE OF IT

FINDING 10.6 queued *"us 30 nasdaq… out of sync completely"* as the descriptive claim justifying two
instruments. Checked against the published record: **not falsified.** NQ/YM is the *loosest* US
equity-index pair (NQ↔ES ~0.93, ES↔YM ~0.95 in practitioner sources), and 2024–26 material reports the
Nasdaq-100/Dow relationship weakening on short timeframes. HARD LESSON 14's "traders see accurately"
pattern holds again, and its drop-the-source corollary does **not** trigger.

**But the inference does not survive, and the counter-evidence is in the same transcript.** In
`video1038794732`: [02:50] *"out of sync completely"* → [03:58] *"US 30 is going to push"* → [05:35]
*"bot nasdaq bot us 30 currently up"* → [06:09] *"target two for us 30 target four for Nasdaq"*. **He
declares them decoupled and then holds them long together and banks them together, minutes apart.**
Two instruments can decouple in magnitude while agreeing in sign; what fails is the leap from "out of
sync" to "two independent observations."

Recorded against my own reading: the other two-legged stream (`video1263885792`) may show opposite
directions, but that rests on reading the transcriber's *"cells"* as *"sells"* and **is not
established**. Two days settle nothing about ρ — which is why FINDING 13 was built not to need them.

**Caveat on all external figures:** `WebFetch` is egress-blocked in this session for every cited
domain. The published numbers are **as surfaced by web search, not read at source**, and are cited so a
session with working egress can verify them. None is a measurement by this project.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` was created; none should be until the sample question is
  settled — and this tick makes that question harder to satisfy, not easier.
- **ρ was not measured** at any horizon. FINDING 13 survives not knowing it; it does not replace it.
- **`US30` depth** — still unmeasured, engine absent from this session.
- The rolling-mean target predictions (FINDINGS 7, 12) and the direction contradiction (FINDING 10.1)
  are unchanged and unrun.

## QUEUE

1. **`US30` 15m/5m depth on `backtest-lab`** — unchanged, but now known to need a session that
   actually has that connector. Bracket `get_credits` around the call if it is ever made on an engine
   that meters (tick #1's open anomaly).
2. **The pooling declaration is made — honour it.** Any future run reaching 30 only by pooling is
   reporting an inadmissible sample size. If a tick wants to overturn it, the reversal condition and
   the horizon it must be measured at are both written down in `SYSTEM.md` FINDING 13.
3. **The realistic route to a legitimate sample is more calendar, not more instruments.** Both
   engines' index coverage is a rolling ~60-day Yahoo-style window (tick #3), so a single-instrument
   15m sample grows only by waiting — or by a data source with real intraday history. That is now the
   binding sample constraint, and pooling is no longer an escape from it.
4. Engine deadlock unchanged (tick #3). **Do not run a Legacy Forex backtest on trader-dev under any
   circumstances** (tick #2, FINDING 4).
5. **Forward-testing still needs no history** and remains the only honest route available today.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED, AND THE ONE ESCAPE ROUTE FROM THE SAMPLE FLOOR IS NOW CLOSED.**
Single-instrument 15m expects ~13–17 trades against a 30 floor; pooling NQ+YM was the only path over
that line and it is arithmetically unavailable at any correlation the published record supports. The
workstream's honest position is **not "marginal"** — it is **below the floor on the data reachable
today**, and the fix is calendar or a deeper data source, not a second instrument. Zero results
recorded, still correctly.

---

# ██ TICK #7, 2026-09-05 — THE SYMBOL SEARCH IS CLOSED BY EXHAUSTION, AND `SPX` IS A THIRD SILENT REMAP

**Zero credits, and this tick MEASURED that rather than assuming it.** No backtest, no `runId`. Nine
`plan_backtest_window` calls plus one `search_perps`, all pre-flight symbol resolution. Full detail in
`SYSTEM.md` FINDINGS 15–16.

**On tick #2's FINDING 4:** that rule forbids running a Legacy Forex *backtest* on trader-dev because
the instruments silently remap. Probing what the symbols resolve to is the measurement that rule came
from, not a violation of it. No strategy was created and nothing was run.

## THE HEADLINE — THIRTEEN CONVENTIONS TRIED, NOT ONE RETURNS A US EQUITY INDEX

Tick #1's queue item 3 had been open since this workstream was created, through five subsequent ticks,
and had never been performed. Performed now, and it closes.

Pre-registered before the calls: *if trader-dev's non-crypto feed carries a US index with intraday
depth, the tick-#3 engine deadlock breaks — trader-dev already has the Pine state this method needs.
If not, the deadlock is confirmed by exhaustion rather than by not having looked hard enough.*

**It does not.** `NDX`, `NQ1!`, `MNQ`, `DJI`, `US100`, `SPX500` all hard-error. With the six already on
file (`NQ`, `YM` silently remapped; `US30`, `NAS100`, `USTEC`, `US500` hard errors), **thirteen vendor
conventions have now been tested and none resolves to an index.** The trader-dev half of the deadlock
is now **permanent, not provisional** — this workstream can stop looking for a symbol.

## THE NEW HAZARD — AND IT BREAKS THE MECHANISM THIS REPO HAD RECORDED

**`SPX` silently remaps to `BYBIT:SPXUSDT.P` and returns 64,805 bars of 15m data.** The most common
alias for the S&P 500 returns a complete, healthy-looking coverage response for **SPX6900, a memecoin**.
`parityAdjustments` carries only a date clamp; `requested.symbol` comes back already rewritten.

The ledger explained the NQ/YM remaps as a **substring** match and drew the moral that *short futures
roots* are what to watch for. `search_perps("SPX")` returns `baseCoin: "SPX"` — **exactly**. This is an
**identity collision, not a substring collision**, so that moral does not protect anyone. The ledger's
platform-constraints section has been corrected accordingly. **The only guard is reading
`applied.displaySymbol` on every call, and no ticker may be assumed safe from inspection.**

## THE SELF-CORRECTION — LAST TICK'S REVERSAL CONDITION WAS ON THE WRONG QUANTITY

FINDING 13 (tick #6) declared pooling inadmissible and said clearing 30 would require **ρ ≤ 0.13**.
That silently set a second unmeasured parameter — the **pairing fraction `p`**, the share of pooled
trades actually sitting in same-session NQ+YM couples — to 1, its most favourable value for the
conclusion being drawn. The correct expression is `N_eff = T/(1 + pρ)`, so the condition is
**`pρ ≤ 0.133`**, which is materially looser (at `p = 0.5` it permits ρ ≤ 0.27).

**The ruling stands; the stated reason is withdrawn.** `N_eff ≤ T` always, so the bottom of the band
(T = 26 < 30) fails at *any* `p` and *any* `ρ` — that half never needed either parameter and is what
actually carries the verdict. The live streams are a **selected sample of the days he chose to
broadcast**, so they cannot pin `p`. Any future reversal attempt must now measure both `p` and `ρ`.

## THE CREDIT ANOMALY FROM TICK #1 IS CLOSED

Tick #1 recorded one credit disappearing across a batch of pre-flight calls and queued a deliberate
bracket to settle it. **Performed this tick, as designed:**

| step | balance |
|---|---|
| `get_credits` before | **492** |
| one `plan_backtest_window` (`NDX`, hard error) | — |
| `get_credits` after | **492** |
| one *successful* `plan_backtest_window` (`SPX`, 64,805 bars) + `search_perps` | — |
| `get_credits` after | **492** |

**`plan_backtest_window` is free — erroring *and* successful — and so is `search_perps`.** Nine such
calls this tick cost nothing. Tick #1's missing credit was therefore **not** caused by pre-flight
calls; a concurrent session on the same account remains the likely explanation and is now the only one
consistent with this measurement. The ledger's *"each backtest costs 1 credit"* is confirmed as
complete, and pre-flight probing may be budgeted as free from here on.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` was created for this workstream and none should be until the
  sample question is settled.
- **`p` and `ρ` are both still unmeasured.** FINDING 16 names the gap; it does not close it.
- **`US30` depth** — still unmeasured, `backtest-lab` still absent from this session.
- **Whether `backtest-lab` has an `SPX`-style identity collision of its own** — untestable here.
- The direction contradiction and the rolling-mean target predictions are unchanged and unrun.

## QUEUE

1. **The symbol hunt on trader-dev is CLOSED. Do not spend another tick on it.** Thirteen conventions,
   zero indices. Only a new data source changes this, not a new ticker string.
2. **`US30` 15m/5m depth on `backtest-lab`** — unchanged, still needs a session with that connector.
   It no longer needs a credit bracket riding along; pre-flight calls are now known free.
3. **The pooling declaration stands, on the corrected reasoning.** A reversal needs `p` AND `ρ`, with
   `ρ` measured at the holding-period horizon (the Epps trap in FINDING 13 still applies).
4. **The realistic route to a legitimate sample is more calendar or a deeper data source** — not a
   second instrument (tick #6) and not a different ticker string (this tick).
5. **Forward-testing still needs no history** and remains the only honest route available today.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED, AND THE TRADER-DEV HALF OF THE BLOCK IS NOW PERMANENT.** Thirteen symbol
conventions exhausted; no index data exists on the engine that can express the method. The sample floor
verdict from tick #6 survives a correction to its own reasoning. Zero results recorded, still correctly.
What this tick actually bought: one long-open queue item closed, one credit anomaly settled by
measurement, one new engine-wide safety hazard found, and one of my own claims narrowed.
