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
