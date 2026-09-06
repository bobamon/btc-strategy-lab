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

---

# ██ TICK #8, 2026-09-06 — THE ONE THING THIS WORKSTREAM CAN ACTUALLY SHIP HAD NEVER BEEN AUDITED

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Full detail in
`SYSTEM.md` FINDING 17.

## WHY THIS TICK IS AN AUDIT AND NOT ANOTHER SAMPLE ARGUMENT

Seven ticks have now established, from different directions, that this workstream cannot be backtested
faithfully anywhere reachable: the symbol hunt is closed by exhaustion (tick #7), pooling cannot rescue
the sample floor (tick #6), and the engine deadlock — state without data, data without state — is outside
this project's control (tick #3). Each of those ticks ended by naming **forward-testing the Pine** as the
only honest route available today.

**So the Pine is the deliverable, and in eight ticks nobody had ever read it against the transcripts it
claims to mechanise.** Read now, line by line. It does not do what its own header says, in six places.

## THE HEADLINE — THE LEVEL GATE WAS COUNTING BARS, AND COUNTING THE LEVEL'S OWN PIVOT

His validation rule is repeated distinct touches, and he counts them out loud one per approach:
*"one touch two touch three four five six seven touches with those wicks"* (`7.` [00:47]).

v1 incremented a counter once **per bar** whose high or low sat inside a 0.10% band, scanning a 200-bar
window that **included the level's own formation neighbourhood**. Since `resLvl` is a `ta.pivothigh`, the
pivot bar scores a touch by construction and its ten neighbours score one each whenever the local swing is
quieter than the tolerance. **`minTouch = 3` was therefore satisfiable at the instant a pivot confirmed,
with zero revisits.**

The defect does not make the gate too strict. **It makes it near-inert, and inert in a way that selects
for quiet swings** — the opposite of "a level price cannot break."

**The fix is expected to be dangerous and that is written down before anyone runs it.** Counting distinct
visits is strictly stricter, and the level is always the *most recent* pivot, which price has usually not
had time to revisit three times before breaking. **The corrected gate may produce zero signals** — HARD
LESSON 8's exact tell. So `minTouch` was **not** retuned: v2 shows **both** counts on the dashboard
(`3 visits / 47 bars-in-band`) and plots all four to the data window, so one live chart settles the
magnitude for free. Retuning a threshold nobody has measured is the failure this project exists to avoid.

## THE OTHER FIVE, IN ONE LINE EACH

2. **The role flip was in the header and not in the code.** *"Support broke and then became resistance...
   they do very often"* (`7.` [02:16]), stated three times, implemented nowhere. Now tracked and drawn —
   and deliberately **not** allowed to fire signals, so the level-test correction can be attributed alone.
3. **Intrabar lookahead.** v1 moved the stop using this bar's close, then tested this bar's low against
   the moved stop — booking trail-exits on lows that preceded the move that caused them. Now managed on
   the previous bar.
4. **An ambiguous bar booked the win.** Target and stop both touched recorded the target. It matters
   because achieved R feeds his rolling-mean target rule, so the bias compounds into the target itself.
   Now books the stop.
5. **One max-stop for two instruments.** The tooltip already said *"20 on NQ / 30 on YM"* and the code
   applied 30 to both. 30 points is ~0.14% of NQ and ~0.07% of YM. Now resolved per instrument, with the
   resolution **printed on the dashboard** for eye-checking (FINDING 15: never trust a ticker string).
6. **The trail rule is under-determined in the source — and this one is not a bug.** Module 11 supports
   step-every-1R [02:13], freeze-at-1R (what his worked example does, [06:38]) and break-even-only
   [09:01] within nine minutes; only the break-even floor is stated as non-negotiable. v1 hard-coded one
   and presented it as the rule. Now an input across all three, defaulting to the one he **demonstrates**
   rather than describes, with the live mode named on the dashboard.

A seventh item is recorded as a limitation rather than fixed: the simulator exits in one piece while
drawing the ladder he scales out along, because **nothing in the source states the scale-out weights** and
inventing them would push a fabricated number into the rolling-mean target.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` exists for this workstream and none was created.
- **Whether v2 compiles.** There is no Pine compiler in this session. It uses only v1's constructs plus
  `str.upper`/`str.contains` and one tuple return; expect to fix syntax, not logic.
- **How much defect 1 actually moves the level gate.** That is now an instrumented one-chart observation,
  not an argument — which is the point of instrumenting it.
- **Whether any defect changed a past conclusion.** None could have: this workstream has never banked a
  result. **Had the deadlock broken earlier and a run been banked off v1, four of the six defects would
  have silently shaped its numbers.** That is luck, not process, and it is the argument for auditing a
  deliverable before it is needed rather than after.
- `US30` depth, `p`, `ρ`, the direction contradiction and the rolling-mean-target predictions are all
  unchanged and unrun.

## QUEUE

1. **First live chart settles defect 1.** Load v2 on NQ or YM 5m and read the two touch counts off the
   dashboard. If the distinct count rarely reaches 3, `minTouch` needs a measured value — not a guessed
   one — and the level definition itself (most-recent pivot vs a persistent zone) is the next suspect.
2. **v2 has never been compiled.** Fix syntax on first load and commit the corrected file.
3. **The three trail modes are now a clean pre-registered three-way test** if a run ever becomes possible,
   alongside the two questions already registered (rolling-mean vs fixed target; window 6 vs ~20).
4. **The symbol hunt stays closed** (tick #7). **Do not run a Legacy Forex backtest on trader-dev under
   any circumstances** (tick #2, FINDING 4).
5. `US30` 15m/5m depth on `backtest-lab` — still needs a session with that connector.
6. **Forward-testing still needs no history** and is still the only honest route available today. It is
   now the route with a deliverable worth trusting slightly more than it was yesterday.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED ON THE ENGINE — BUT THE DELIVERABLE IS NO LONGER SILENTLY WRONG.** The
external blockers are unchanged and outside this project's control. What changed is internal: the one
artefact this workstream can actually ship had six defects, one of which inverted the meaning of its level
gate, and none had been looked for in eight ticks. Zero results recorded, still correctly.

---

# ██ TICK #9, 2026-09-06 — THE STOP-WIDTH GATE HAD 7 POINTS OF ROOM, AND WOULD HAVE BEEN BLAMED ON THE TOUCH COUNTER

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Full detail in
`SYSTEM.md` FINDING 18.

## WHAT THIS TICK SET OUT TO DO, AND WHY IT DID SOMETHING ELSE

Queue item 2 from tick #8 was **"v2 has never been compiled."** The honest version of that with no Pine
compiler present is a static language-conformance audit — but only if the claims can be checked against
the Pine v6 reference rather than recalled. **`tradingview.com` is blocked by this environment's network
egress proxy**, so that audit would have been memory arguing with memory. It was abandoned rather than
faked, and **queue item 2 remains open**. No compile-error claim appears anywhere in this tick.

What was done instead is checkable without any external resource: arithmetic on the file's own defaults,
against two prices quoted in the committed transcripts.

## THE HEADLINE — THE PAD IS A PERCENTAGE, THE CAP IS POINTS, AND THE PAD WAS WINNING

Tick #8's FINDING 17.5 fixed the max-stop **cap** per instrument. Nobody asked what units the **padding**
was in. They do not match:

| | price, from his own screen | pad @ 0.05% | cap (v2) | pad as % of cap | left for entry→level |
|---|---|---|---|---|---|
| **NQ** | 24,954.50 (`4.` 03:06) | **12.48 pts** | 20 | **62.4%** | **7.5 pts** |
| **YM** | 46,942 (`4.` 07:23) | **23.47 pts** | 30 | **78.2%** | **6.5 pts** |

`useMaxStop` is **ON by default**, so v2 silently rejected any break whose close sat more than ~7 points
past the level it had just broken — inside a system whose entire published stop is 20–25 points. The pad
is the word *"just"* in *"just below that support"* (`11.` 00:15), and on NQ it was consuming **half of
the 25-point stop that same sentence describes**.

**And it gets tighter every year.** The pad scales with price, the cap does not, so at **NQ 40,000** and
**YM 60,000** the pad alone equals the cap and the gate becomes unsatisfiable at any distance. The
indicator had a built-in expiry date and nothing in it would have noticed.

## THE SECOND DEFECT IN THE SAME GATE — THE NQ CAP REJECTED HIS OWN WORKED EXAMPLE

`maxStopNQ = 20` comes from module 4 [04:09], which is **Luca describing** Mamba. Module 11 is **Mamba
demonstrating**: *"That's a 25 point stop loss, which is solid. That's actually a really good number"*
[00:20-00:23], *"we have a 25 point stop"* [01:43], a 20-pt stop at [06:50], and 64 refused [01:36].
A 20-pt cap **rejects the exact setup module 11 teaches**. v2's own trail-mode fix set this file's
precedent — default to what he *demonstrates*, not what he *describes* — so **v3 moves the NQ default
20 → 25**, with the 20–25 bracket recorded in the tooltip. **YM's 30 is unchanged** and now flagged as
single-sourced and Luca-relayed; module 11 has no YM example, so there is nothing to prefer over it.

## THE CONSEQUENCE THAT MATTERS MOST — TICK #8's QUEUED MEASUREMENT WAS NOT YET DECISIVE

Tick #8 warned that its corrected touch counter **may take the signal count to zero** and instrumented
both touch counts so one live chart would settle it. **v2 carried two independent gates capable of
producing zero signals, and only one was instrumented.** A zero-signal chart could not have been
attributed to either — and the touch counter, being the tick's headline, would have taken the blame.

v3 closes that by instrumenting the other one: a **Stop budget** dashboard row (pad in points, pad as a
% of the cap, points remaining, and an explicit **"PAD ≥ CAP — no setup can ever pass"** state) plus
three data-window plots. The two causes are now separable on the first chart instead of confounded on it.

## WHAT v3 CHANGED

1. **Padding is now an input in ticks**, defaulting to one tick — 0.25 pts on NQ, 1 pt on YM (`4.` 02:06 /
   07:07), the only padding quantity the source actually defines. Labelled in code as the *minimal
   source-expressible reading of "just below" — an interpretation, not a stated rule*. % mode retained for
   reproducing v1/v2, exactly as `touchMode` retains v1's counting.
2. **NQ cap default 20 → 25**, on the demonstrated-over-described precedent. YM unchanged, now flagged.
3. **One definition of the pad.** v2 wrote the formula twice — once as `padNow`, once inline in the
   trade-open block — so the two could silently diverge.
4. **Stop-budget instrumentation** on the dashboard and in the data window.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` exists for this workstream and none was created. The table
  above is arithmetic on the file's own defaults and two transcript-quoted prices — **the budget, not the
  hit rate.** How often the gate actually binds needs a real chart and is unmeasured.
- **Whether one tick is the right pad.** It is the minimal source-expressible reading, exposed as an input
  precisely because the source states none. It is not a measured optimum and must not be quoted as one.
- **Whether v2 or v3 compiles — queue item 2 is still open**, now with a recorded reason (egress block).
  v3 adds one new built-in, `syminfo.mintick`; everything else reuses constructs already in the file.
- **No past conclusion changes.** This workstream has still never banked a result. As in tick #8 that is
  luck, not process: a run banked off v2 would have had its trade count shaped by this gate invisibly.
- `US30` depth, `p`, `ρ`, the direction contradiction and the rolling-mean-target predictions are all
  unchanged and unrun.

## QUEUE

1. **The first live chart now settles TWO questions, not one, and can tell them apart.** Read the touch
   counts (tick #8) and the Stop budget row (this tick) off the same dashboard. If signals are zero, the
   dashboard now says which gate did it.
2. **v2/v3 have never been compiled** — unchanged, and blocked here by egress, not just by the absence of a
   compiler. A session with TradingView access, or one that can reach the Pine v6 reference, closes it.
3. **The pad is now a pre-registered one-dimensional test** (1 tick vs the old 0.05%), alongside the three
   trail modes, rolling-mean vs fixed target, and window 6 vs ~20.
4. **Audit the remaining gates for the same class of defect.** Two ticks have now each found a gate whose
   *units or counting basis* were wrong rather than whose threshold was mistuned. `touchTol` (0.10% of
   price = 25 pts on NQ, 47 on YM) is the obvious next suspect and has never been examined.
5. **The symbol hunt stays closed** (tick #7). **Do not run a Legacy Forex backtest on trader-dev under any
   circumstances** (tick #2, FINDING 4).
6. `US30` 15m/5m depth on `backtest-lab` — still needs a session with that connector.
7. **Forward-testing still needs no history** and is still the only honest route available today.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED ON THE ENGINE — AND THE DELIVERABLE'S SECOND SILENT GATE IS NOW VISIBLE.**
External blockers unchanged. What changed internally: the stop-width gate had 6–8 points of room on a
20–25 point system because its padding and its cap were in different units, it would have become
impossible outright at NQ 40,000, and its NQ cap rejected the worked example the source is built around.
None of it had been looked for in nine ticks, and it would have been misattributed to tick #8's headline
correction the first time anyone loaded the chart. Zero results recorded, still correctly.

---

# ██ TICK #10, 2026-09-06 — THE LEVEL IS 2–3× WIDER THAN THE STOP THAT MUST SIT OUTSIDE IT

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Full detail in
`SYSTEM.md` FINDING 19.

## WHAT THIS TICK DID

Tick #9's queue item 4 named the next suspect exactly: *"`touchTol` (0.10% of price) is the obvious
next suspect and has never been examined."* It was, and it is a bigger instance of the same defect
class — a percentage quantity colliding with a points quantity — than the one tick #9 found.

## THE HEADLINE — TWO GATES WHOSE ACCEPTANCE REGIONS DO NOT OVERLAP

`touchTol = 0.10` % of price, against caps and pads measured in index points:

| | price (his own screen) | tol = 0.10% | band (±tol) | cap | band as % of cap |
|---|---|---|---|---|---|
| **NQ** | 24,954.50 (`4.` 03:06) | **24.95 pts** | 49.9 | 25 | **200%** |
| **YM** | 46,942 (`4.` 07:23) | **46.94 pts** | 93.9 | 30 | **313%** |

The stop-width gate accepts a break only within `cap − pad` of the level — **24.75 pts on NQ, 29.0 on
YM.** The tolerance exceeds that on both (**−0.20** and **−17.94**). So **every break this system can
trade sits inside the band its own level definition still calls "touching"** — *"price can't break it,
it's stuck"* (`7.` 00:47). One gate scores the bar a touch, the other scores the same bar on the same
level a break.

And against tick #9's own result: v3 settled the pad at **one tick** (0.25 pts NQ, 1 pt YM). The
tolerance is **100× the pad on NQ, 47× on YM.** The file was padding the stop by a quarter-point
beyond a level whose own identity was fuzzy to twenty-five.

## WHAT v4 CHANGED

1. **Tolerance is now a fraction of the live max-stop cap** (0.20 → ±5 pts NQ, ±6 YM). The source says
   the level *is* a zone (*"support zones"* 01:21, *"you make this little thicker"* 04:35) and never
   how wide, so any number is an interpretation — but **commensurability is not**: a level's width must
   be smaller than the stop that sits outside it. % mode retained for reproducing v1–v3.
   **ATR was ruled out on corpus grounds** — ATR stops are Coach Luca's (FINDING 6).
2. **`breakClears`** — the break may be required to clear the band. **OFF by default**; under v1–v3
   tolerance it was not merely off but *unsatisfiable* (−0.2 pts of budget on NQ).
3. **A "Level width" dashboard row + four data-window plots.** The dashboard now shows all three
   zero-signal causes together: touch counter (#8), stop budget (#9), level width (#10).
4. **`minTouch = 3` audited and CLEARED** — it is the one level-gate number the source supports
   (*"one two three is resistance"*, `7.` 04:31). A clean gate is also a result.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` exists for this workstream and none was created.
- **The direction of the bias is not even signed.** A wide band makes each bar easier to score as a
  touch *and* makes distinct visits harder to separate (price must leave the band entirely). The two
  push opposite ways; which dominates is a chart measurement. This tick instruments it rather than
  asserting it — and that is the one thing three consecutive audit ticks have in common.
- **Whether 0.20 of the cap is right** — a labelled interpretation satisfying one arithmetic
  constraint, nothing more.
- **Whether any version compiles — queue item 2 is still open**, still blocked by the egress proxy.
- **The literature could not be read.** `WebSearch` works; **every** `WebFetch` was refused by the
  proxy (`arxiv.org`, `mdpi.com`, `vecviz.com`, `investopedia.com` all tried). Four URLs are recorded
  in SYSTEM.md as leads, explicitly **not** as citations; nothing in this tick rests on them.
- `US30` depth, `p`, `ρ`, the direction contradiction and the rolling-mean-target predictions are all
  unchanged and unrun.

## QUEUE

1. **The first live chart now settles THREE questions and can tell them apart** — touch counts (#8),
   Stop budget (#9), Level width (#10). If signals are zero, the dashboard names the gate.
2. **v2/v3/v4 have never been compiled** — unchanged, blocked by egress here.
3. **Pre-registered one-dimensional tests now number five:** tolerance (0.20 of cap vs 0.10% of price),
   `breakClears` on/off, pad (1 tick vs 0.05%), the three trail modes, rolling-mean vs fixed target,
   window 6 vs ~20.
4. **The gate audit is now three-for-three and should continue.** Ticks #8, #9 and #10 each found a
   gate whose *units or counting basis* were wrong rather than whose threshold was mistuned — and none
   of the three would have been visible in a backtest result. Remaining un-audited: `volMult = 1.0`
   against tick-volume-vs-contract-volume on index CFDs, and `pivLen = 5` (the only structure number,
   and the source states none).
5. **The symbol hunt stays closed** (tick #7). **Do not run a Legacy Forex backtest on trader-dev under
   any circumstances** (tick #2, FINDING 4).
6. `US30` 15m/5m depth on `backtest-lab` — still needs a session with that connector.
7. **Forward-testing still needs no history** and is still the only honest route available today.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED ON THE ENGINE — AND THE DELIVERABLE'S THIRD SILENT GATE IS NOW VISIBLE.**
External blockers unchanged. What changed internally: the object the whole system trades — the level —
was defined 2–3× wider than the stop that has to sit outside it, so its two gates disagreed about
whether a given bar was a touch or a break, and the tolerance was 100× the pad that tick #9 spent a
whole tick getting right. Ten ticks, zero results recorded, still correctly.

---

# ██ TICK #11, 2026-09-06 — THE VOLUME GATE'S THRESHOLD IS THE ONE PART OF IT THAT IS FINE

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Full detail in
`SYSTEM.md` FINDING 20.

## WHAT THIS TICK DID

Tick #10's queue item 4 named the next un-audited gate: *"`volMult = 1.0` ... and `pivLen = 5`."*
The volume gate was audited against `9._VOLUME` and `8._SESSIONS_TO_TRADE`. `pivLen` was not and
stays open.

## THE PATTERN THIS BREAKS — AND THAT IS THE POINT

Ticks #8, #9 and #10 each found a gate whose **units or counting basis** were wrong. Three in a row
creates an expectation, and **the expectation was wrong here.** `volMult = 1.0` is dimensionless and
unit-consistent; the threshold is the one part of this gate with nothing wrong with it. Had this tick
gone looking only for the previous defect class it would have reported the gate clean and moved on.
Four defects were found, of three different kinds.

## THE HEADLINE — `volLen` IS A BAR COUNT ON A SYSTEM THAT TRADES TWO TIMEFRAMES

NY session = 09:30–16:00 ET = 390 min (`8.` [00:36]/[00:44], which states both clocks outright).

| tf | 20 bars = | baseline at 09:30 reaches back to | session bars | judged against a partly-overnight baseline |
|---|---|---|---|---|
| **5m** | 100 min | 07:50 ET | 78 | first **20 of 78 = 26%** |
| **15m** | **300 min** | **04:30 ET** | 26 | first **20 of 26 = 77%** |

On 15m **more than three-quarters of the only session he trades** is scored against a mostly-overnight
average, and the baseline is not clean before 14:30 — by which time FINDING 9's ~0.7–0.9 trades per
session have usually already happened. This is HARD LESSON 10's shape (a flat parameter binding
differently per timeframe) in a file whose header insists 5m and 15m are the entire universe.

**Unlike tick #10, the direction is signed.** Overnight volume is structurally below cash-session
volume, so the gate is **loosest at 09:30** — when his own course says volume is best anyway (`8.`
[02:05]) and when he takes most of his trades — and only binds in the afternoon. **It filters at the
time of day he barely trades.** Magnitude is unmeasured and instrumented, never asserted.

## THE OTHER THREE, IN ONE LINE EACH

2. **The quantity is not his.** He defines volume as *"how fast is the markets moving"* [00:41] and
   reads it off **price displacement** every time — *"moving left to right"* [02:30], *"we are going
   straight up"* [06:22], *"a little bit sideways"* [09:29]. In 831 seconds he never reads a volume bar
   aloud, states no threshold and names no lookback. `volume > sma(volume,20)` is an interpretation with
   no source support — now labelled as one. **No substitute was invented.**
3. **It is in the wrong place.** All three of his diagnoses are made on bars *after* the break. His
   **pre-entry** proxy for volume is the SESSION: *"why did we have volume? because we traded during New
   York session"* [06:31]. v1–v4 have it backwards — hard pre-entry gate, no post-entry test — which
   also makes it **partly redundant with the session gate already in the file** (War Formation E82's
   shape). Recorded as a pre-registered ablation, not claimed.
4. **Two stated rules were in this file's own spec table and absent from the code** — v2's role-flip
   defect, for the second time in one file. The **early exit** (*"we're out of this trade... about seven
   points, then let it go all the way up and take us out for 15"* [03:22–03:38]) and **conviction
   sizing** (*"risk less... not a tighter stop loss, my contract size is going to get smaller"*
   [09:45–09:58]). Both now rendered; the exit ships OFF because it changes the trade record.

## THE DERIVED CONSEQUENCE — TWO OF HIS OWN RULES PULL AGAINST EACH OTHER

A loss scores **zero** in the window that sets his target, regardless of size (`10.` [02:56]). So
relative to letting a trade run, cutting early turns a would-be full stop into a small loss (**no
effect** — both score 0) and a would-be winner into a small loss (**replaces a positive with a 0**).
**The cut is invisible on the loss side of the target computation and can only remove winners from
it.** The more disciplined he is about cutting early, the lower his rolling-mean target drifts.
Derived from two stated rules, not measured.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` exists for this workstream and none was created.
- **The magnitude of the headline defect.** Direction is signed by structure; size is a chart
  measurement. v5 adds a `Vol baseline` dashboard row and six data-window plots so it can be made.
- **Whether the volume gate is wholly or only partly redundant with the session gate.**
- **What the correct displacement measure would be.** Defect 2 says the quantity is wrong, not what
  replaces it.
- **The 15-point stop at [03:38] did NOT retune anything.** Third stop-width figure in the corpus, but
  the instrument is unidentified and the trade is one he presents as a mistake. Caps unchanged.
- **Whether any version compiles — queue item 2 still open**, still blocked by egress. v5 adds
  `math.sum` and `timeframe.in_seconds()`; expect syntax fixes, not logic.
- **`pivLen = 5` is now the last un-audited number in the file**, and the source states none.
- **No past conclusion changes.** Never banked a result; still correct. **With default inputs v5's
  signal set and trade record are identical to v4's** — a checkable claim about the diff, not a result.

## QUEUE

1. **The first live chart now settles FOUR questions and can tell them apart** — touch counts (#8),
   Stop budget (#9), Level width (#10), Vol baseline (#11). Load on **15m first**: that is where the
   baseline defect is largest, and the row should read "20 of 20 outside the session" at the open.
2. **v2–v5 have never been compiled** — unchanged, blocked by egress here.
3. **Pre-registered one-dimensional tests now number eight:** session-to-date vs trailing baseline,
   the volume-gate ablation (is it redundant with the session gate?), the early exit on/off, tolerance,
   `breakClears`, pad, the three trail modes, rolling-mean vs fixed target, window 6 vs ~20.
4. **`pivLen = 5` is the last un-audited number.** Four ticks of gate auditing have found four defects;
   the run should finish rather than stop one short.
5. **The symbol hunt stays closed** (tick #7). **Do not run a Legacy Forex backtest on trader-dev under
   any circumstances** (tick #2, FINDING 4).
6. `US30` 15m/5m depth on `backtest-lab` — still needs a session with that connector.
7. **Forward-testing still needs no history** and is still the only honest route available today.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED ON THE ENGINE — AND THE DELIVERABLE'S FOURTH SILENT GATE IS NOW VISIBLE.**
External blockers unchanged. What changed internally: the volume gate measures a quantity the source
never uses, at a point in the trade where he never uses it, against a baseline that is overnight for
77% of the 15m session — and the two volume behaviours he *does* state had been sitting in this file's
own spec table, unimplemented, for eleven ticks. The threshold, the only part a tuning pass would have
touched, is fine. Eleven ticks, zero results recorded, still correctly.

---

# ██ TICK #12, 2026-09-06 — THE DIRECTION GATE KEPT PERMITTING LONGS FOR 75 MINUTES AFTER THE STRUCTURE BROKE

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Full detail in
`SYSTEM.md` FINDING 21. Deliverable: `pine/VISUAL-legacy-forex-complete.pine` **v6**.

## WHAT THIS TICK DID

Tick #11's queue item 4: *"`pivLen = 5` is the last un-audited number. Four ticks of gate auditing
have found four defects; the run should finish rather than stop one short."* It was audited, against
`6._PRICE_ACTION_AND_MARKET_STRUCTURE` and `5._ANALYZING_TIME_FRAMES` (both confirmed as Mamba's per
FINDING 6, which is this workstream's standing first rule before quoting anything).

**The number is fine. The rule around it was missing.** That is the second tick in a row where the
threshold turned out to be the sound part — and this time the search was not for units, which is what
ticks #8, #9 and #10 each found.

## THE HEADLINE — HE INVALIDATES ON PRICE, THE CODE INVALIDATED ON A CONFIRMED PIVOT

> [03:35] *"So that previous higher high and higher low we didn't break past that now if price would have"*
> [03:41] *"Came down here and started to push down in this way **boom that is now a lower low**"*

That call is made **as price pushes through**. v1–v5 had no invalidation rule at all: `bullStruct`
stayed true until a *new* pivot confirmed, and `ta.pivotlow(low, 5, 5)` cannot confirm until **five
bars after the swing low** — plus however long the down leg runs.

| tf | minimum staleness after the break | as a share of his 390-min session |
|---|---|---|
| 5m | **≥ 25 min** | 6% |
| 15m | **≥ 75 min** | **19%** |

**The bias is signed and it is the harmful direction: the stale state always permits the side price
has just left.** v6 kills a bullish structure on the first close below the higher low it is built on,
and re-arms only on a fresh confirmed pivot low.

**It ships ON by default — the first version since v2 whose default signal set differs from its
predecessor's.** v3, v4 and v5 each shipped behind a switch defaulting to the old behaviour because
each swapped one interpretation for another. This one replaces *no rule* with **a rule the source
states outright**. And it **may take the signal set to zero in chop** — written down here before any
chart is loaded, instrumented as a named blocker, and not softened by an invented threshold.
HARD LESSON 8's generalised check was run first and passes: a confirmed pivot low guarantees the
confirming bar closes *above* it, so the latch cannot be killed by the event that arms it.

## THE SECOND FINDING — `pivLen` IS NOT A ONE-DIMENSIONAL KNOB, AND THE TEST LIST SAID IT WAS

It sets three things at once: the structure gate, **the traded levels themselves** (`resLvl` *is* the
last pivot high, so every entry, stop and target price moves with it), and the ±`pivLen` exclusion
window inside tick #8's touch counter. Any sweep of it is a three-parameter change. It is struck from
this workstream's list of one-dimensional pre-registered tests.

## THE THIRD — A 15m STRUCTURE STATE CANNOT BE BUILT INSIDE THE SESSION HE TRADES

Two pivot highs *and* two pivot lows, with same-side pivots ≥ `pivLen+1` apart and the outer two each
needing `pivLen` bars of confirmation, floors the requirement at **17 bars** (≈29 for a realistic
four-swing sequence). The NY session is **26 bars on 15m** and 78 on 5m.

**So on 15m the state is always inherited from before 09:30**, and there is no recency bound anywhere
in the file on the pivots that define both the state and the levels. Unlike the headline, **the source
does not settle whether that is wrong** — he reads structure off a chart that shows overnight bars — so
v6 **instruments it and asserts nothing**: a `Struct age` row giving the oldest defining pivot's age
and how many of the four formed pre-open.

## AND ONE GATE CLEARED

`hh AND hl` is exactly *"higher highs followed by higher lows"* ([01:53]). The `consolidating`
residual labels a broadening range as "consolidation" alongside the sideways one he describes, but
**both are correctly excluded from trading**, so the label is loose and the verdict is right.
`pivLen = 5` is UNSOURCED and was **not retuned** — that would have been a three-parameter change made
against no measurement.

## WHAT THIS TICK DID NOT ESTABLISH

- **No number came from a run.** No `runId` exists for this workstream and none was created. Every
  figure above is arithmetic on Pine semantics, the file's own defaults, and the session length the
  source states — **budgets and bounds, never hit rates.**
- **How often the new invalidation fires**, and so whether it thins the signal set slightly or to
  zero. Instrumented, not asserted.
- **Whether inheriting structure from before the open is a defect at all.** Measured; not judged.
- **Whether `pivLen = 5` is a good value** — unaudited by construction, since no one-parameter test
  of it exists.
- **Whether any version compiles — queue item 2 still open**, still blocked by the egress proxy.
- **With default inputs v6's signal set is NOT identical to v5's**, unlike v3/v4/v5. A property of
  the diff, stated as one.
- `US30` depth, `p`, `ρ`, the direction contradiction and the rolling-mean-target predictions are all
  unchanged and unrun.

## QUEUE

1. **The gate audit is COMPLETE — every number in the file has now been audited.** Ticks #8–#12 found
   defects in five of five gates: the touch counter, the stop pad/cap, the touch tolerance, the volume
   baseline, and now the structure invalidation. **This queue item closes and should not be reopened
   as "audit the next gate"; there is no next gate.**
2. **The first live chart now settles FIVE questions and can tell them apart** — touch counts (#8),
   Stop budget (#9), Level width (#10), Vol baseline (#11), Struct guard + Struct age (#12). Load on
   **15m first**: that is where both the volume-baseline defect and the structure-staleness defect are
   largest.
3. **v2–v6 have never been compiled** — unchanged, blocked by egress here.
4. **Pre-registered one-dimensional tests, corrected count: eight.** Structure invalidation on/off
   (new), session-to-date vs trailing volume baseline, the volume-gate ablation, the early exit
   on/off, tolerance, `breakClears`, pad, the three trail modes, rolling-mean vs fixed target,
   window 6 vs ~20. **`pivLen` is NOT among them** — see the second finding above.
5. **The next honest work in this workstream is no longer a code audit.** The remaining open items are
   all external: an engine that can run the method (deadlock, tick #3), a data source with real
   intraday depth (tick #6), or a forward test. A twelfth tick spent re-reading a file that has now
   been read five times would be motion, not progress.
6. **The symbol hunt stays closed** (tick #7). **Do not run a Legacy Forex backtest on trader-dev under
   any circumstances** (tick #2, FINDING 4).
7. `US30` 15m/5m depth on `backtest-lab` — still needs a session with that connector.
8. **Forward-testing still needs no history** and is still the only honest route available today.

## STATUS LINE

**LEGACY FOREX: STILL BLOCKED ON THE ENGINE — AND THE GATE AUDIT IS NOW FINISHED, FIVE FOR FIVE.**
External blockers unchanged and outside this project's control. What changed internally: the direction
gate — the first condition in the signal and the one the whole method is built on — had no invalidation
rule of its own, so it kept permitting longs for at least 75 minutes on 15m after price had broken the
structure, in a system whose stated purpose is to get in and get out. The number the tick set out to
audit, `pivLen = 5`, turned out to be the sound part; the rule that should have surrounded it was
absent. Twelve ticks, zero results recorded, still correctly.
