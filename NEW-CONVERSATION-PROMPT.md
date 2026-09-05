# START-HERE PROMPT — copy everything below into a new conversation

---

You are picking up an autonomous quantitative trading research project that has been running since
2026-09-01. There are **THREE SEPARATE STRATEGIES**. They are not variations of each other, they do
not share a codebase, and they must never be merged or cross-contaminated.

**Working folder:** `C:\Users\ecarr\Claude\index-strategy-lab`
**Git remote:** `https://github.com/bobamon/btc-strategy-lab.git`

**Backtest engine — USE THE NEW ONE:** the `backtest-lab` MCP (`https://backtester24.com/mcp`).
The old `trader-dev` MCP is still installed. Read "ENGINE NOTES" at the bottom before choosing.

**READ FIRST, BEFORE ANY WORK:**
1. `STRATEGY-LEDGER.md` — hard lessons numbered to 50. Each cost real credits and a wrong conclusion.
   Several forbid specific retests outright. **These outrank anything in this prompt.**
2. `CHAMPION-BOARD.md` — the invented lab's history.
3. `war-formation/ORACLE-RULES.md` and `war-formation/EXPERIMENT-LOG.md`
4. `three-m-elite/SYSTEM.md` and `three-m-elite/VOCABULARY.md`

---

# THE GOVERNING MANDATE

Stated by the owner on 2026-09-03, verbatim:

> ya so lets make sure that we are doing this correct look the 3 strategies are there own thing i gave
> you the rules and inforation for 2 of the strategies and the one one is going to be you making one up
> that works and always improving its self also the other 2 strategies i want you too build off the
> information that i provided and i want you too master them and do small tweaks too make them perfect
> for there strategy does this make sense you should always try too improve all 3

**What this means:**
- **War Formation and 3M Elite are the OWNER'S strategies.** Master what the source material says. Make
  SMALL, source-faithful tweaks. Do NOT replace the mechanism, re-engineer the frame, or decide a leg
  doesn't exist.
- **The third lab is YOURS to invent.** Build something that works, keep improving it indefinitely.
- **All three get worked. None is ever "done", "paused" or "closed."**

And on 2026-09-03, verbatim:

> now i need too say this my 3M and War Formation Should work in both directions not just longs or
> shorts 6Hr is the direction for War formatiion so if red we look for shorts but also depends on the
> inforation that i provided and same for 3M they should work on both long and shorting just look over
> the infromation i provided for that also please

**Both legs are a REQUIREMENT, not an option.**

---

# ═══ STRATEGY 1 — WAR FORMATION ═══

## The original request, verbatim (2026-09-01)

> i would also like a crazy btc to usd startegy that uses time frames like here is what im thinking
> 6 hr is the direction if it bullish or bearish we zoom down too the 1hr if there is lets say 4 green
> in the 6hr candle then we go bullish and zoom into the 15 min and look for a lower resistance or
> something i want you too make up the strategy and then we do the same on the 3 min and entry on the
> 1 min and we dont trade the first or last hr from the 6hr also we can have things too know but they
> arnt always right or on time
> https://youtu.be/nGOhtnNscxE https://youtu.be/9aiMle9xBZk
> i want this too be a sepreate test please and call it the war formation i want you too figure out how
> too do this and make it work please i want this again too be a test tweak it if need too but i want
> too master the 1 min chart in and out like a beast do the dashboard as your doing for the other test
> please but this is for itself

## Follow-up clarifications, verbatim

> your running the loop also right and thats its own thing and this is its own thing also right and
> please look at the images i sent too study and thats just the higher time frames and it goes down too
> the lower time frames too put in the trade dont worry about the gap that it was talking about and
> **this is on hiken ashki candles**

> can you look at youtube videos here are some links for the war formation please look at them and use
> the transcription if possible https://youtu.be/9aiMle9xBZk
> https://www.youtube.com/watch?v=YPh8ewMQIY0 https://youtu.be/thzLDN5UuaE
> i also just added some videos that need too transcribe for the war formation strategy

**THE BINDING CORRECTION (2026-09-02) — this overrides every earlier build:**

> **war formation dose not have a stop loss** look at this now we dont need too use these exact number
> but this is just what there strategy is saying its only for the war formation strategy the 3m should
> have it s own based off the videos i sent about it and the images i sent about it

## Source material — `C:\Users\ecarr\OneDrive\Desktop\Oracle\`

**Images (15 files):**
`1.webp` · `39d7841b-e5b5-45fd-9f9b-376905dca051.webp` · `6_witch_hr.webp` · `7.webp` ·
`8_velocity.webp` · `9.webp` · `WAR_UP.webp` · `chart.webp` · `enter.webp` · `exit_points.webp` ·
`lesson_5.webp` · `war_down.webp`

**Videos:** `2026-09-02 02-28-53.mp4` · `2026-09-02 02-31-40.mp4` · `2026-09-02 02-36-41.mp4`

**Transcripts already produced:** `war-formation/transcripts/` (3 local + a `youtube/` subfolder)

## The specification as currently understood

- **Cascade:** `6h → 1h → 15m → 3m → 1m`. **The 1m entry is part of the specification** — a 5m rescale
  was tried (E63) and the owner corrected it; it stands as a diagnostic only.
- **Direction:** the 6H candle. Red means look for shorts.
- **NO STOP LOSS.** The exit is the **A.L.C.M. shield** — a fixed DOLLAR gap to liquidation, adjusted
  with the Bitunix Pencil. A position ends at target or at liquidation. Nothing else.
- **Never add to a losing trade.**
- Runs before E35 used a structural stop and are **wrong on the exit** — do not cite them.
- The ~20–30 trade ceiling is a **property of the strategy on the available data**, not a defect to
  engineer away.

## Current state
- **No champion, no candidate.**
- Parent build: `e58a` (PF 1.24015239 / DD 9.82519609% / 36 trades, long, confirmed reproducible).
- `E38` and `E47` are **unreproducible** — never cite them.
- Data: 1m, 2025-12-16 → 2026-05-03. **4.5 months, ONE regime.** It cannot support a split test. Say
  that limitation out loud rather than engineering around it.
- **E74 produced the first profitable short (PF 1.16714444)** but is blocked by the ratchet — see the
  OPEN DECISION at the bottom.

---

# ═══ STRATEGY 2 — 3M ELITE ═══

## The original request, verbatim (2026-09-02)

> also i have another strategie that i want your help with just like the 1m and the other dashboard
> this is going too be another one that i want on a loop please and i also want too master there
> strategy and i need your help with making this possible its working for them i need you too look at
> the videos and everything carfully please and make sure you put it on a loop too make it better and
> improve the perfect strategy **call this one the 3m Elite!** i just need it too work as it seems like
> it should i need you too understand what they are trying too do and also i need you too make it work
> and do perfect entries and exits and i just want my strategys too be the best and perfect also make
> it done in the cloud so i dont have too have my computer on please

> please watch the videos and learn from them please and if possible i would love for you to get some
> sort of transcription or something and please add it too a loop also too continue too improve this
> strategy just like the other 3 dashboards please and **the 3 should be doing there own thing**

## Source material — `C:\Users\ecarr\Downloads\3m -20260902T072259Z-1-001\3m\`

**Videos (10):** `2026-08-09 03-24-31.mp4` · `04-18-22` · `04-32-59` · `04-42-54` · `05-08-26` ·
`05-45-14` · `07-20-21` · `09-49-18` · `10-54-02` · `2026-08-10 16-22-21.mp4`

**PDFs:** `3M SYSTEM CHECKLIST - 15SEC.pdf` · `3M SYSTEM CHECKLIST - 30SEC.pdf`

**Transcripts already produced:** `three-m-elite/transcripts/` — all 10, timestamped. **Use these.**
Key citations already extracted:
- `04-18-22 [06:19]` — *"all these advance models are the same thing on the bearish side just upside down"*
- `04-18-22 [05:12]` — *"the model is just going to be the same thing that the hard time frame is"*
- `09-49-18 [00:28]` — MAs *"help mainly on the 15 MINUTE time frame"*
- `09-49-18 [01:30]` — *"three MAs ... the twenty, the fifty and the two hundred"*
- `09-49-18 [04:20]` — bullish: *"the 200 is always gonna be on the bottom, then the 50, then the 20"*
- `09-49-18 [03:01]` — *"the average price of the last 200 candles"* → **SMA, not EMA**

## The specification as currently understood
- **15m chart. 4H supply/demand zones.** A zone is created by an engulfing 4H candle: demand zone
  top = the bullish candle's OPEN, bottom = its LOW.
- Zone **ages** (in 4H candles) and is **mitigated** after two body closes inside it.
- Entry = a tap of a still-fresh zone. Stop = the zone's own edge (structural). Target = **2R**.
- **3M KEEPS ITS OWN MODEL.** Do NOT port the War Formation A.L.C.M. shield into it.
- The legs are **NOT independent** — v24 showed removing shorts ADDED 84 long entries. A combined
  build is not the sum of two separate runs.

## Current state
- **CHAMPION: v37** — PF 1.25172059 / DD 8.72815312% / 155 trades. Split at 2024-06-08 into
  H1 1.33630490 (96) and H2 1.12058245 (59). Cold-reproduced digit-for-digit as v52.
- **Carried caveats:** H2 is weak, Sharpe falls 0.90 → 0.16, the edge concentrates in H1, and part of
  the headline is now known to be the 2023–25 bull market rather than the strategy.
- **CLOSED — do not reopen without a reason:** the R-floor neighbourhood, the freshness axis, and the
  **entire bias-gate axis** (see HARD LESSON 45 — every gate tried cuts >75% of the sample).
- Data: 15m, 2022-01-01 → 2026-09-01. 4.7 years, splittable at 2024-06-08.

---

# ═══ STRATEGY 3 — THE INVENTED LAB (currently "BTC Strategy Lab") ═══

## The original request, verbatim (2026-09-01) — NOTE THE ORIGINAL UNIVERSE

> You are an autonomous Trader for **US30, nas100, YM, NQ** 15m and 5m researcher every 15Min repeat
> this loop:
> 1. research the charts on these Pairs and study the NY Session research the internet for trading
>    concepts, indicators, academic ideas, quantitively methods, or existing strategies.
> 2. Create one genuinely new strategy for each pair **the strategy must work for all of them** on the
>    15 min and 5 m remember it must be one strategy that works for those pairs on those time frames.
>    do not repeat the lightly modify a strategy you have already produced
> 3. define precise, mechanical rules for : long entry, short entry, stop loss, take profit, position exit
> 4. **The stop loss and take profit must be defined when the trade opens. Do not use the trailing
>    stops as the primary risk management.**
> 5. include sensible risk managment and **avoid strategies that rely on martingale, averaging down,
>    grid recovery, or unlimited losses.**
> 6. explain the strategy breifly and provide the exact rules needed for another agent to code and
>    backtest it. keep a record of previously generated strategies so each 15min cycle explores a
>    substantially different idea.
>
> mission: continuously discover diverse, testable Pairs for 15m and 5 min strategies with clearly
> defined downside risk and profit targets also i would love to have it **buy and sell and understand
> when the market flips and changes**

**IMPORTANT — A DRIFT TO CORRECT OR CONFIRM.** The universe was changed to crypto shortly after, by:

> then lets change it too top crypto pairs

…and then narrowed to BTCUSDT-only, where it has stayed for ~62 records. **The repo is still named
`index-strategy-lab`.** The new engine supports the ORIGINAL universe — NAS100, US30, SPX500, GER40,
UK100, JP225 — which the old engine never could. **Ask the owner whether to return to the original
index mandate or stay on BTC.**

## Also standing, verbatim
> i want them both too work when market flips and changes please also i want it too be able too buy and
> sell or long and short i want to be the best the master of the chart

## Current state
- **No champion.** 47 attempts, 44 dead.
- **Attack 46 ADVANCED** — level-target geometry (buy a tap of the prior 20-bar low, target the prior
  20-bar HIGH — a level price actually traded at, NOT a multiple of the stop). Both halves clear:
  **1.17245633 (105 trades) / 1.58559241 (38 trades)**, cold-reproduced digit-for-digit.
- **Its caveats, which must travel with the number:** the 3.5 RR floor was chosen by watching the
  never-tuned half (declared selection effect); the clean half has only 38 trades; and inside it sits a
  **ten-month stretch that won 1 of 15 trades**.
- **The open weakness:** no out-of-sample test exists, and none was possible on BTCUSDT-only.

---

# ═══ THE SHARED PROTOCOL — applies to all three ═══

## The dashboard spec, verbatim (2026-09-01)
> build a control panel/dashboard for all the strategies that have been successfully coded and
> backtested in pine script … strategy name, symbol + timeframe, net profit/return%, profit factor,
> Max drawdown %, total trades, win rate, average trade / expectancy, backtest date range,
> long/short/both, status: research/testing/passed/rejected … a button to view the pine script, a
> button to view the full backtest, the strategy rules / short description, date it was created and
> last tested and filters and sorting … **only show strategies that have actually been backtested —
> never populate the dashboard with estimated or invented results.**

Enforced by `build_dashboard.py`, which **refuses to publish** any record without a `provenance` block
naming a real job or report URL. Run as `python build_dashboard.py --lab btc | --lab war | --lab 3m`.

**Each lab has its OWN results file. Never write a result into another lab's file.**
- `results/backtests.json` (invented lab) · `war-formation/results/backtests.json` ·
  `three-m-elite/results/backtests.json`

## RATCHET v2 — the keep rule
KEEP a change only if **(1)** profit factor improves, **(2)** drawdown does not worsen — except by up
to 0.50pp when PF improves by more than 0.02, and **(3)** trade count is at least 30. **(4)** A cut of
more than 50% of the trades must pass a split test BEFORE being kept.
A change that improves one half and breaks the other is **REJECTED, not averaged.**

## The kill rule
Split at **2024-06-08**. The earlier half is the **never-tuned** half and is always run first. If it
returns under 1.0, the idea is **DISCARDED** — no filters, no rescue, second backtest not run.

## The sample floor
A ratio on fewer than ~30 trades is a **DIRECTION, not a result**, and is never quoted as one.

## Evidence hygiene — non-negotiable
- **Never invent or hand-write a metric.** Copy every figure from the backtest response.
- **Pre-register** what each possible outcome would mean BEFORE running.
- **Cold re-run** any promotion from the saved spec file, as a fresh job, and match to the cent.
- Only record runs with real provenance.
- **A negative result is the normal output.** Report clean deaths with their reason.

## Execution assumptions (old engine's forced profile)
`0.05% commission per side · 100% of equity · 1× leverage · $10,000 initial capital · orders on bar
close`. **Stop and target FIXED AT ENTRY. No trailing stops, no averaging down, no martingale, no grid
recovery.**

## Pine v6 constraints (old engine)
Forbidden: `request.security`, arrays, user-defined functions, `strategy.cancel`/`strategy.order`,
`pyramiding > 1`, martingale, custom var-trail. `ta.sum` is unimplemented.

---

# ═══ ENGINE NOTES — READ BEFORE CHOOSING ═══

**`backtest-lab` (backtester24) — the new one.**
- Covers **the same data**: 163,585 bars for 2022-01-01→2026-09-01 on BTCUSDT vs the old engine's
  163,826. Sub-1%. Use `source="perp"` and **explicit `start`/`end`** — a bars-only window is anchored
  to *now* and will not reproduce.
- Has `split_test`, `walk_forward`, `monte_carlo`, `parameter_surface`, `sweep_backtest` (one strategy
  across a grid of pairs × timeframes — **this is the tool for the original "one strategy, four
  indices" mandate**).
- Has a **real perp margin model** with `stats.liquidations` and `stats.fundingPaid`.
- Reports `exposurePct` and a buy & hold baseline — neither exists in the current records.
- **LIMITATION, verified:** its `custom` strategy is **STATELESS** (numpy expressions over OHLCV).
  It CANNOT express 3M's zone lifecycle (age/touch/traded across bars), War Formation's `var` counters,
  or **any per-trade price-level exit** — it offers only fixed % stop/target. War Formation's fixed
  **$1,000 shield** has no percentage equivalent (1.1% at $92k, 1.6% at $63k).

**`trader-dev` — the old one.** Bybit USDT perps only, Pine v6, `tv_jul26_mc7`. **It is the only engine
that can run the three strategies as specified.** Every existing record references its job IDs.

**Recommendation:** keep both. Old engine for the three labs' Pine builds; new engine for cross-market
work, statistical validation, and the original index mandate.

---

# ═══ OPEN DECISIONS — the owner must rule on these ═══

1. **RATCHET clause 2.** It has blocked two strong results: E69b was short by **0.0103** of profit
   factor; **E74** — the first profitable War Formation short — is over by **0.45pp of drawdown**, on a
   build whose drawdown is only 3.6%, where the 0.50pp allowance was calibrated on builds carrying
   8–45%. A **proportional** allowance would behave identically on the old builds and differently here.
   **The rule has NOT been changed.**
2. **The invented lab's universe** — return to US30/NAS100/YM/NQ as originally asked, or stay on BTC?
3. **Attack 46's out-of-sample test** — now possible on other symbols via the new engine, but the Pine
   build cannot be ported faithfully. Decide whether an approximation is worth running.

---

# ═══ HOW TO WORK ═══

Run one cycle per lab, rotating. Each cycle: read the docs → pick ONE change or ONE new mechanism →
pre-register the outcomes → run → record with provenance → rebuild the dashboard → commit and push.

**THE DOCS OUTRANK THIS PROMPT.** If anything here contradicts `STRATEGY-LEDGER.md`, the ledger wins —
say so and work from the ledger.
