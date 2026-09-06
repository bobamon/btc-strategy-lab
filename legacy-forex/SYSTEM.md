# LEGACY FOREX TRADER — system, decoded from the course videos

> Research notes for backtesting. Not trade recommendations.

**Source:** `C:\Users\ecarr\OneDrive\Desktop\Legacy Forex Trader` — 18 videos, transcribed locally
with faster-whisper (`legacy-forex/transcribe.py`). Nothing left the machine. Every quote is verbatim
with its timestamp.

**This is a fourth, separate workstream.** It shares no base, board or ratchet history with the
invented BTC lab, War Formation or 3M Elite, and imports no construction from them.

---

## ⚠️ ONE CREDIBILITY NOTE, STATED ONCE AND THEN SET ASIDE

The author repeatedly promotes a prop firm he owns (`6._PRICE_ACTION_AND_MARKET_STRUCTURE` [00:27]–
[01:14], `9._VOLUME` [10:07]–[10:38]) and makes unverified profitability claims — *"if you're
consistent with everything I just mentioned, you're profitable regardless"* (`11.` [09:39]). His
demonstrations are hand-picked chart replays, and he says so himself: *"I don't want cherry pick too
much"* (`9.` [08:34]).

**None of that changes the method, and this file does not argue with him.** It matters only for how
his *results* claims are read: they are marketing, not evidence. The point of this lab is to measure
the method. Per HARD LESSON 14 — mine a trader's observations, not his prescriptions.

---

## THE UNIVERSE — TWO INSTRUMENTS, AND A NO-TRADE DAY IS A VALID OUTCOME

From `3._WHAT_TO_TRADE`, stated four times in 113 seconds:

> [00:05] "The good news is that there's only two. The bad news is that there's only two."
> [00:10] "If **NQ** isn't trading so good, the volume's not great, market structure doesn't look
> great, we move on to **YM**."
> [00:29] "If you don't trade NQ or YM, **we don't go looking for something else.** If those two
> aren't looking good, **you're done for the day.**"
> [01:45] "**NQ and YM is the only thing we trade. We trade nothing else.**"

In `8._SESSIONS_TO_TRADE` [00:20] he says *"we're trading NQ and US30"* — confirming he uses **YM and
US30 interchangeably**, which matters for symbol mapping below.

**The no-trade day is a rule, not an absence of one.** A backtest that always finds a trade is not
running this system.

## TIMEFRAMES — 5m AND 15m ONLY

`5._ANALYZING_TIME_FRAMES`:
> [01:00] "We have to go **five minute**. We have to go **15 minute**."
> [01:06] "There is times where I'll go to the one minute, but **it's very rare**."
> [01:14] "Five minute, 15 minute every single day. **We don't go to the H4.**"
> [03:18] "**15 and 5 is the only place we're ever going to be.**"
> [03:00] "There's **no overall bias**. We're not seeing what the daily is doing."

Explicitly **no higher-timeframe bias filter** — which is the opposite of War Formation's 6h-God-of-
direction and 3M's 4H zones. Structure is read on the trading timeframe itself.

## SESSION — NEW YORK ONLY

`8._SESSIONS_TO_TRADE`:
> [00:14] "**We only trade during one session.** Because we're trading NQ and US30, we are **only
> trading during New York session**."
> [00:44] "**9:30am Eastern**" ("6:30am Pacific").
> [01:03] "**Be on 20 minutes early** every single day... you get on at 6:10, analyze the markets."
> [01:43] "If you try to trade this strategy during London session or Asia session **you're gonna
> screw yourself**."
> [02:05] "You're gonna have the most amount of **volume**. Market structure is gonna look the best."

**09:10 ET is analysis-only. 09:30 ET is the first legal entry.**

## MARKET STRUCTURE — THE DIRECTION FILTER

`6._PRICE_ACTION_AND_MARKET_STRUCTURE`:
> [01:29] "There's only two kinds... **bullish** and **bearish**. There is a third, but it's that
> little gray zone where **we don't trade it** — **consolidation**."
> [01:53] "**Higher highs followed by higher lows**" = bullish.
> [03:41] "Lower low, back up lower high, back down lower low — **we are now in a bearish market
> structure**."
> [03:56] "When we are in a bullish market structure, we are looking for **buys**... **we're gonna go
> with traffic. We don't want to go against traffic.**"
> [06:22] "**We do not trade consolidation.** If the markets are consolidating we stay out."
> [02:38] "Some days are ugly... **if it's extremely ugly and you can't really tell what's going on,
> we don't trade it.**"

**Mechanical:** bullish = a confirmed higher high AND a confirmed higher low. Bearish = lower low AND
lower high. Anything else = consolidation = **no trade**. Longs only in bullish, shorts only in
bearish. Never counter-structure.

## SUPPORT / RESISTANCE — THE LEVEL

`7._SUPPORT_AND_RESISTANCE`:
> [00:27] "Think of **support** as a **floor**... **resistance** is a **ceiling**."
> [00:41] "One touch, two touch, three, four, five, six, **seven touches** with those wicks to this
> support zone. Price can't break it."
> [01:51] "**Support/resistance turns into each other.** This support broke below... retested that
> floor now as a ceiling."

**Mechanical:** a level is validated by **repeated touches** (he counts 3–8). A broken level flips
role — broken support becomes resistance, broken resistance becomes support.

## THE ENTRY — A BREAK OF THE LEVEL, IN THE DIRECTION OF STRUCTURE, WITH VOLUME

`7.` [03:00]–[03:25] names the confluence stack explicitly:
> "Market structure's bearish. We broke through a support... **that's two things. But wait, there's a
> third. We now just retested as resistance.** So we have **three key things** telling us we are going
> to the downside."

And on whether the retest is required — it is **not**:
> [05:35] "We could wait for price to come up, come back down and retest... **But we don't have to do
> that** because we already know it's a bullish market structure and we're breaking out of our
> resistance. **As we start to break out we can take our long position.**"

**Mechanical entry (long):** bullish structure **AND** price breaks above a validated resistance
**AND** volume is present. Enter on the break. Retest is a bonus, not a gate.
**Short:** mirror — bearish structure, break below validated support, volume present.

## VOLUME — THE GO/NO-GO

`9._VOLUME`:
> [00:41] "Volume is **how fast are the markets moving**."
> [00:51] "When there's **no volume we get stopped out a lot**."
> [01:03] "If price breaks out and **slowly starts to consolidate**, more than likely price is going
> to lose."
> [02:25] "Price is **moving sideways**... because we have **no volume**... it **resets the entire
> market**."
> [07:51] "**If there's no volume, there's no trading.**"

**And a live-management rule that is genuinely unusual and must be modelled:**
> [03:18] "**We're out of this trade.** Yes, we're negative right now, but we would rather lose this
> small amount — about **seven points** — than let it go all the way up and take us out for **15
> points**, more than double that. **Take your loss, cut it off early.**"

**Mechanical:** after entry, if price goes sideways instead of running — volume dies — **exit early
for a partial loss rather than waiting for the stop.**

## THE STOP — JUST BEYOND THE BROKEN LEVEL, NOT AT THE FAR ONE

`11._STOP_LOSS_ADJUSTMENT`:
> [00:07] "We're placing them **just below support/resistance**... That's a **25 point** stop loss,
> which is solid."
> [01:26] "I'm **not** going to use this support down here as my protection zone. I don't want a stop
> loss that big. That's ridiculous. **64 points. No, my account's gone if I do that.**"

**This is exactly this project's own LESSON 5** (never put the stop just beyond the level you entered
at) in tension with his rule — his stop *is* just beyond the broken level. Recorded as a conflict to
measure, not to silently resolve.

## THE TARGET AND THE TRAIL

> `9.` [05:53] "Typically **one to three to one to five** is that sweet zone."
> `11.` [02:12] "Every time this thing moves up the **same distance as our stop loss**... we're going
> to adjust our stop loss."
> `11.` [02:28] "Price is at 43 points. We're going to put our **stops to break even**."
> `11.` [03:21] "Take your stop loss and **move it 25 points into profit**... you're **guaranteed a 25
> point win**."
> `11.` [08:02] "**At worst, please put your stops to break even at a one to one point five.**"

**Mechanical:** target 1:3 to 1:5 R. At **+1R** move stop to break-even (he says no later than
+1.5R). At **+2R** move stop to +1R. Trail onward from there.

## POSITION SIZING AND TRADE COUNT

> `9.` [09:45] "The volume is okay, the setup looks good **but not great**. I'm gonna **risk less**...
> **not** a tighter stop loss, **my contract size is going to get smaller**."
> `9.` [12:01] "We're only taking **up to two trades max per day**. Sometimes three if we really feel
> good about that re-entry."
> `9.` [12:16] "**Just because we lost does not mean we give up.** If a support line breaks again,
> we're going to enter again."

**Mechanical:** max 2 trades/day (3 exceptionally). Lower conviction → smaller size, never a tighter
stop. Re-entry after a loss on the same level is explicitly allowed.

---

## THE COMPLETE MECHANICAL SPECIFICATION

| Element | Rule |
|---|---|
| Instruments | NQ and YM only. Neither qualifies → no trade that day. |
| Timeframes | 5m and 15m. No HTF bias filter, by design. |
| Session | New York only. First legal entry 09:30 ET. |
| Direction | Bullish (HH+HL) → longs only. Bearish (LL+LH) → shorts only. Consolidation → no trade. |
| Level | Support/resistance validated by repeated touches; broken levels flip role. |
| Trigger | Break of the level in the structure's direction. Retest optional. |
| Filter | Volume must be present. No volume → no trade. |
| Stop | Just beyond the broken level (~20–25 pts on NQ), never the far level. |
| Target | 1:3 to 1:5 R. |
| Management | +1R → break-even (by +1.5R at the latest). +2R → lock +1R. Then trail. |
| Early exit | Post-entry consolidation / volume death → cut for a small loss. |
| Sizing | Lower conviction → smaller size, not a tighter stop. |
| Frequency | Max 2/day, 3 exceptionally. Re-entry after a loss allowed. |

## ⚠️ DATA CAVEAT — NQ/YM ARE FUTURES; THE ENGINE HAS CASH INDICES

`STRATEGY-LEDGER.md`'s archived note records that the **old** trader.dev engine silently remapped
`NQ`→`IONQUSDT` and `YM`→`DYMUSDT` — crypto perpetuals — and would have returned real metrics for the
wrong instrument. **Symbol resolution gets verified before any number here is trusted.**

`backtest-lab` offers `NAS100 -> ^NDX` and `US30`: the **cash indices underlying** NQ and YM.

| | NQ / YM (what he trades) | NAS100 / US30 (what the engine has) |
|---|---|---|
| Instrument | futures contract | cash index |
| Session | ~23h Globex | cash hours only |
| Overnight | trades through | gaps |
| Roll | quarterly discontinuity | none |
| Sizing | $ per point, minis/micros | index points |

**Consequences, declared rather than hidden:**
1. His **point-based** stop (25 pts) and contract sizing cannot map onto cash-index bars. Modelled as
   a **percentage** stop instead — a declared deviation.
2. Cash-hours-only data means the NY-session filter is **partly redundant** — the data is already
   mostly session hours. That weakens the session rule as a *test*, and must be said.
3. Yahoo caps intraday history: **no usable 15m/5m depth** (5m–30m ≈ 60 days). **His 5m/15m
   requirement collides directly with the data available.** This is the binding constraint on the
   whole workstream and is unresolved.

## STATUS

Specification complete. **Nothing backtested. No number in this file came from a run, because no run
has happened.** Next: the Pine visualiser, then resolve the timeframe/data collision before any
backtest is trusted.

## QUEUE

1. **Resolve the 5m/15m data collision first.** Yahoo gives ~60 days of 5m–30m. Sixty days of NY-
   session-only 5m bars may not clear the 30-trade floor at 2 trades/day max. Measure it with
   `plan_backtest_window` before building — if the sample cannot exist, say so rather than backtesting
   on 1h and pretending it is his system.
2. **Verify `NAS100`/`US30` symbol resolution** and record the applied symbol.
3. Model the **no-trade day** and the **2-trade cap** explicitly; they bound trade count by design.
4. **Measure his stop rule against LESSON 5**, which contradicts it. Do not quietly substitute a
   structural stop.
5. The nine unnumbered `videoNNNN` files are longer sessions (up to 68 min) and are transcribed but
   not yet decoded — they may contain refinements to the above.

---

# ██ THE DATA COLLISION, NOW MEASURED (2026-09-05) — HIS SYSTEM CANNOT YET BE VALIDLY BACKTESTED HERE

Queue item 1 said to measure this before building anything. Measured with `plan_backtest_window`,
zero credits:

| Symbol | TF | Window requested | Result |
|---|---|---|---|
| NAS100 | 5m | 2026-07-07 → 2026-09-01 | **ERROR — no data** |
| NAS100 | 15m | 2026-07-07 → 2026-09-01 (60d) | **ERROR — no data** |
| US30 | 15m | 2026-07-07 → 2026-09-01 | **ERROR — no data** |
| **NAS100** | **15m** | **2026-08-06 → 2026-09-05 (30d)** | ✅ **573 bars** |
| NAS100 | 30m | 2026-07-08 → 2026-09-05 (60d) | ✅ 560 bars |

**Symbol resolution verified, and the old engine's failure is confirmed fixed here too:**
`appliedSymbol: NAS100`, `source: yahoo`, closes ≈ 29,344 — that is the Nasdaq-100 index level. **No
silent remap to a crypto token.**

## THE ARITHMETIC THAT BLOCKS THIS

**[CORRECTED 2026-09-05, see STATUS.md tick #3: 15m actually gives ~1,119 bars / ~41 sessions, and 5m DOES resolve over a shorter window. The figures below were produced by under-requesting the window and are left for the record.]** ~~15m tops out at ~30 days = 573 bars ≈ 21 trading sessions.** His cap is **2 trades per day**, so the
absolute ceiling is **~42 trades** — and that assumes *every single session* produces two valid
setups. His own rules make that impossible: consolidation days are skipped, no-volume days are
skipped, and he says outright *"you may miss three days in a row because the markets aren't good"*
(`9.` [07:13]).

A realistic qualifying rate of even half the sessions puts the sample at **~20 trades — below RATCHET
v2 clause 3's floor of 30.** 5m is worse: it does not resolve at all over 60 days.

**So the honest position is: this system's real timeframes cannot produce a quotable sample on this
data source.** Recorded rather than worked around. Specifically, the following would all be
dishonest and are refused:

- Backtesting it on **1h or 30m** and calling it his system. He rules those out explicitly:
  *"15 and 5 is the only place we're ever going to be"* (`5.` [03:18]). A 30m test measures something
  he does not trade.
- Dropping the **2-trade cap** to manufacture sample size. The cap is one of his rules.
- Dropping the **no-trade day** for the same reason.
- Quoting a profit factor on ~20 trades.

## WHAT WOULD ACTUALLY UNBLOCK IT

1. **A futures data source with intraday depth** — NQ/YM continuous contracts at 5m/15m over years.
   That is what he actually trades and it would solve the sample and the instrument mismatch at once.
   Neither engine currently offers it; `search_perps` on trader-dev covers crypto perps, not CME.
2. **Forward-testing**, which needs no history: run the Pine visualiser live on NQ/YM 5m during New
   York session and record signals as they occur. Slow, but it is the only honest route with the data
   available today.
3. Accepting a **30m proxy explicitly labelled as a proxy** — measuring whether the *structure +
   level-break + volume* stack has any edge at all, while stating plainly it is not his system. That
   is a legitimate experiment, but it must never be recorded as a test of the Legacy method.

**Nothing has been backtested. No number in this file came from a strategy run, because none was run.**

---

# ██ TICK #4, 2026-09-05 — THE NINE `videoNNNN` TRANSCRIPTS DECODED, AND THE CORPUS IS NOT ONE SYSTEM

Zero credits. No backtest. No engine call of any kind. This tick did what queue item 5 of the
original decode and queue item 4 of STATUS tick #3 both asked for: read the nine undecoded
`videoNNNN` transcripts, plus the two numbered modules this file had never cited (`4.` and `10.`).

**The single most important result is a provenance finding, and it comes first because it changes how
every other quote in this file must be read.**

## ██ FINDING 6 — THE 18 TRANSCRIPTS ARE TWO DIFFERENT TRADERS RUNNING TWO DIFFERENT SYSTEMS

This file's header says *"Source: … 18 videos"* and treats the whole committed corpus as one man's
method. **It is not.** Two coaches from the same prop firm (Legacy Funded) are mixed in the same
directory, and nothing in the filenames distinguishes them.

| | **"Mamba"** — the Legacy Forex Trader this file specifies | **"Coach Luca" / Luca No Limit** |
|---|---|---|
| Session | **New York**, first entry 09:30 ET | **Asia session**, plus "power hour" |
| Instrument | **NQ and YM / US30** | **gold — `MGC` (micro) / `GC`** |
| Timeframes | **5m and 15m only**, "we don't go to the H4" | **1m, 5m, 15m, 30m and 1h**, split-screen |
| Stop basis | fixed points (20 NQ / 30 YM), placed at structure | **ATR-derived**, read off his own indicator |
| Extra tooling | none named | 200 MA + "three smooth moving averages", **fair value gaps**, previous-day high/low, session high/low bands, `edgematrix.com` "no limit indicator" |
| Directional stance | structure decides; consolidation = no trade | **"I'd rather be wrong trading with the trend than wrong trading against it"** |

Verbatim, so this cannot be argued with later:

> `video1083955301` [00:04] "welcome back to another **Asia session** stream"
> `video1083955301` [00:48] "looking at **gold**. Let's go over to **MGC**"
> `video1639421319` [00:50] "**Coach Luca**… Luca no limit"
> `video1639421319` [00:58] "I trade the **Asia session** here"
> `video1083955301` [12:00] "the **200 moving average**"
> `video1870420481` [20:34] "**What is ATR**, ATR stands for the average true range"
> `video1083955301` [19:02] "**fair value gaps** only valid when you hold it"

And the two men are explicitly colleagues, not the same person:

> `video1083955301` [53:12] "You play golf in **mamba** luka. Yes, sir."
> `video1083955301` [53:19] "tomorrow morning during **mamba stream**"
> `4._WHAT_ARE_CONTRACTS_AND_TICKS` [00:00] "**Mamba** just called me, told me exactly what's going on"
> `4._WHAT_ARE_CONTRACTS_AND_TICKS` [13:30] "hearing it from me **or hearing it from Mamba**"

### THE SPLIT, FILE BY FILE — USE THIS BEFORE QUOTING ANY TRANSCRIPT AGAIN

| Mamba — **in scope for this spec** | Luca — **OUT OF SCOPE, a different system** |
|---|---|
| `3._WHAT_TO_TRADE`, `5._ANALYZING_TIME_FRAMES`, `6._PRICE_ACTION_AND_MARKET_STRUCTURE`, `7._SUPPORT_AND_RESISTANCE`, `8._SESSIONS_TO_TRADE`, `9._VOLUME`, `10._USING_DATA`, `11._STOP_LOSS_ADJUSTMENT` | `4._WHAT_ARE_CONTRACTS_AND_TICKS` (narrated by Luca *about* Mamba) |
| `video1038794732`, `video1263885792`, `video1270175432`, `video1855004398`, `video1979454677` — five NY live sessions on Nasdaq + US30 | `video1083955301`, `video1142991957`, `video1639421319`, `video1870420481` — four Asia live sessions on gold |

**Nothing in this file was corrupted by the mix** — every rule above was decoded from the eight
numbered Mamba modules, and all eight are in the left column. But it was luck, not method: the two
uncited modules included the one Luca narrates, and a tick that had decoded the four long
`videoNNNN` files as "more of the same trader" would have imported ATR stops, fair value gaps and a
200 MA into an NQ/YM system that has none of them. **The four gold transcripts must not be used to
refine any rule in this file.** If they are ever worked, they are a fifth workstream, not this one.

---

## ██ FINDING 7 — THE TARGET IS NOT "1:3 TO 1:5". IT IS A ROLLING MEAN OF ACHIEVED R, RECOMPUTED DAILY

`10._USING_DATA` was never cited in this file, and it contains the most mechanical rule in the whole
course — the one that actually sets the target. The row in THE COMPLETE MECHANICAL SPECIFICATION
above reads *"Target: 1:3 to 1:5 R"*, which reads as a discretionary range. It is not a range. It is
an output.

**His procedure, verbatim and in order:**

> [00:38] "what I like to do is like to go over **the last two weeks of trades**, which is typically
> anywhere from **six to eight trades** depending on the day."
> [00:49] "I'm gonna analyze every trade that I took and figure out the median of where I either got
> stopped out or the risk to a war that I was able to capture overall."
> [01:18] "We have a loss. That's okay, loss has happened." → **scored as `0`**, see [02:56].
> [02:48] "if you notice, I only calculated the **second number**. I don't care about the one."
> [02:56] "We take the three, **zero for a loss**, two point five, five, five and a three."
> [03:47] "That equals **18.5**. We divide that by **six** because we did six days worth. Boom, we are
> averaging a one, two, three."
> [04:02] "we know we're averaging a one to three, which means **we are going to go for one, two,
> threes**."
> [05:06] "we just hit a two. So we add plus two… That equals **20.5**. We would then divide that by
> now **seven** trades and see we're down to **2.9**."
> [05:43] "One to five gets hit, three days in a row. Okay, the average is now one to four. **We're
> going to now do a one to four on our trades.**"

**Mechanised, exactly:**

1. Keep the achieved R multiple of each closed trade. A loss contributes **0**, not −1.
2. Window = the last ~6–8 closed trades (his worked example uses **6**; he calls it "the last two
   weeks", "about nine days worth").
3. `targetR = sum(achieved R) / count`, rounded to the nearest whole R for use.
4. Set **tomorrow's** target to that number. Recompute after every trade closes.
5. His stated justification is persistence, not prediction: [07:30] *"The markets have a **slow
   refresh rate**… if the markets are giving you one to fives every day, they're probably going to
   continue to do so for a little while longer, and then slowly taper back down."*

### THREE THINGS THAT MUST BE RECORDED ALONGSIDE IT, BECAUSE THEY ARE DEFECTS IN THE RULE ITSELF

1. **He says "median" and computes the arithmetic mean, twice.** [00:52] and [05:59] both say
   *median*; every calculation he performs is a sum divided by a count. His own example cannot expose
   the error — the set is `{0, 2.5, 3, 3, 5, 5}`, whose mean is 3.083 and whose median is 3.0, and he
   rounds both to "one to three". **Mechanise the arithmetic he performs, not the word he uses**, and
   note that the two diverge on any skewed sample.
2. **Scoring a loss as 0 makes this NOT an expectancy figure**, and it must never be read as one. It
   is the mean achieved R across all trades with losses zeroed — a number that is positive by
   construction, for a system with any winners at all. It is a target-selection heuristic. Treating it
   as evidence of profitability would be a straightforward misreading, and he does not claim otherwise.
3. **It is self-referential in a way that can only ratchet the target down.** The recorded R of a
   winner is capped by the target that was set for it, because he exits there. A run of 1:3 exits can
   therefore never lift the average above 3, while any loss drags it toward 0. The only thing that
   can raise it is a trade left running past target — which his own management rule ([05:43] onward)
   discourages. **This is a testable structural claim about the rule and it is the first thing a
   backtest of this system should measure.** It is written down here before any run, per HARD
   LESSON 17.

**This also explains the "1:3 to 1:5" quote in `9.` [05:53] — *"typically one to three to one to five
is that sweet zone"* — as a description of where the output usually lands, not as the rule.** The
rule is `10.`; the range is its observed range.

---

## ██ FINDING 8 — THE STOP HAS A HARD MAXIMUM, AND THAT MAXIMUM IS A SETUP FILTER

This file records the stop as *"just beyond the broken level (~20–25 pts on NQ), never the far level"*
and flags the tension with this project's own LESSON 5. Both halves of that were right, and both were
incomplete: there is a **second, independent constraint** — a cap on how far the structural stop is
allowed to be, and a setup whose structure sits beyond the cap is **rejected**, not re-stopped.

> `11._STOP_LOSS_ADJUSTMENT` [00:07] "We're placing them **just below support/resistance**… That's a
> **25 point** stop loss, which is solid."
> `11.` [01:26] "I'm **not** going to use this support down here as my protection zone. I don't want a
> stop loss that big. That's ridiculous. **64 points. No, my account's gone if I do that.**"

And, second-hand through Luca but consistent with the above, the fixed sizes he is said to work to:

> `4._WHAT_ARE_CONTRACTS_AND_TICKS` [04:09] "**Mamba uses 20 points on NASDAQ**, let's say **30 points
> on YM**, 20 point stop loss on NASDAQ"
> `4.` [10:40] "let's just do 30 because I know a lot of you guys do **30 point stop losses** on, you
> know, whether it's NASDAQ or YM"
> `4.` [12:44] "if you guys are someone who uses a **fixed stop loss** when it comes to 20 points, 30
> points, you'll know what contract size to use every single time"

**⚠ Provenance caveat, stated because it changes the weight of the number:** the "20 on NQ / 30 on YM"
figures are **Luca reporting Mamba's practice**, not Mamba's own words. Mamba's first-hand numbers are
"25 points, which is solid" (accepted) and "64 points" (rejected). Treat 20/30 as corroborating
evidence for the magnitude, not as a quoted rule.

**Mechanised:** place the stop just beyond the broken level; if the resulting distance exceeds roughly
**25–30 points on NQ / YM** (~0.10–0.13% of price at 2026 index levels), **do not take the trade.**

**Why this matters more than it looks.** It is a *gate*, and gates change trade counts, which is the
binding problem for this whole workstream (STATUS.md). It also partially answers this project's
LESSON 5 objection: LESSON 5 says a stop planted just past the entry level sits in the noise. A
maximum-distance rule does not fix that, but it does mean his stop distance is bounded from above as
well as anchored from below, so the two rules are not the same object and must be measured
separately.

### THE CONTRACT ARITHMETIC, RECORDED BECAUSE IT MAKES THE POINT-STOP TRANSLATABLE

`4.` gives the sizing identity explicitly ([03:54]): `contracts = risk$ / (stopPoints × $perPoint)`.

| instrument | per tick | ticks per point | **$ per point** |
|---|---|---|---|
| **NQ** (E-mini Nasdaq) | $5.00 | 4 (0.25 increments) | **$20** |
| **MNQ** (micro) | $0.50 | 4 | **$2** |
| **YM** (E-mini Dow) | $5.00 | **1 — no decimals** | **$5** |
| **MYM** (micro) | $0.50 | 1 | **$0.50** |
| GC (gold, Luca's) | $10.00 | 10 | $100 |

This does **not** repair the cash-index deviation recorded in the DATA CAVEAT above — a cash index has
no contract size — but it does mean a **20-point NQ stop is a known dollar quantity ($400 per mini)**
rather than an unmappable one, and it makes the fixed-percentage substitution auditable instead of
merely declared.

---

## ██ FINDING 9 — HIS OWN STATED TRADE RATE IS ~0.7–0.9 PER SESSION, NOT THE 2/DAY CAP

The largest open question in this workstream is whether a sample can exist at all (STATUS.md).
Every estimate so far has been derived from the **cap** — "max 2 trades/day" — because that was the
only number in the record. `10._USING_DATA` supplies the realised rate, from his own journal:

> [00:38] "the last two weeks of trades, which is typically anywhere from **six to eight trades**"
> [02:22] "this is the last one, two, three, four, five, **six trades** from Monday to Monday. So
> nearly two weeks of trading. Okay, **about nine days worth**."

**6 trades / 9 sessions = 0.67 per session. 8 trades / ~10 sessions = 0.8 per session.** Call it
**0.67–0.89**, i.e. roughly **one third of his own cap.** The cap is not the operative number and
never was; the no-trade day, the consolidation skip and the volume gate do the actual work, exactly as
`9.` [07:13] says (*"you may miss three days in a row because the markets aren't good"*).

**Consequence for the sample arithmetic** — using STATUS tick #3's corrected coverage, which is
measured, not assumed:

| tf | measured bars (`NAS100`/`NDX`, tick #3) | RTH sessions | **× 0.67–0.89** |
|---|---|---|---|
| 15m | 1,119 | ~43 (26 bars/session) | **~29–38 trades** |
| 5m | 937 | ~12 (78 bars/session) | **~8–11 trades** |

So: **15m straddles the 30-trade floor and 5m cannot reach it by a factor of three.** This is the
first sample estimate in this workstream anchored on a figure the trader himself stated rather than on
a ceiling I derived. It is still an estimate — HARD LESSON 4 says to score it against the actual count,
never to build on it — and it is recorded here as a pre-registered prediction for whenever a run
becomes possible.

---

## ██ FINDING 10 — WHAT THE FIVE NY LIVE SESSIONS SHOW HIM ACTUALLY DOING, AND WHERE IT CONTRADICTS THE COURSE

Per HARD LESSON 14, the live streams are mined for what they SHOW, not for their results claims —
which are pure marketing (`$250,000`, `a quarter mill`, `put the house on it`) and are not evidence of
anything. Five behaviours are mechanical, repeated, and either new or contradictory.

### 1. He pre-marks BOTH directions on BOTH instruments before the open — four levels, not one

> `video1263885792` [01:28] "Be prepared for **all four positions** on the screen."
> `video1855004398` [01:57] "if I'm going to take **a buy position, it's going to be above this high**
> here; **for cells we could drop right below**." → [02:37] "here's our **two little positions** here."
> `video1263885792` [00:31] "also kind of like this **long position above** the previous support…"
> [03:02] "**US 30 cells are here as well**"

**This contradicts the course rule as this file states it.** `6.` says bullish structure → buys only,
bearish → sells only, and this file's spec table encodes that as a hard directional gate. In the live
sessions he marks a break level on *each* side of the current range, on *each* of NQ and YM, and takes
whichever breaks. That is a **bracket**, not a directional filter.

**Not resolved here, and deliberately so.** The course modules are the stated method and the streams
are the observed behaviour; this project's rule is to record the contradiction rather than pick a
winner (HARD LESSON 14 is about the seam between what a trader says and what he does, and this is that
seam). The visualiser now draws the un-armed counter-structure level as a dotted bracket so the
difference is visible on the chart, with the course's gate left ON by default.

### 2. Both instruments are traded CONCURRENTLY, and the 2/day cap counts across the book

> `video1038794732` [05:35] "as you can see **bot nasdaq bot us 30**"
> `video1263885792` [03:58] "$60,000 on Nasdaq, $26,000 on us 30 — **we're taking two trades in a day**"
> `video1979454677` [12:29] "**this is two positions one day**" (one US30, one Nasdaq, sequential)

`3._WHAT_TO_TRADE`'s *"if NQ isn't trading so good… we move on to YM"* reads as a sequential fallback.
In practice both are live at once, and **"two trades" means two across the pair**, typically one each.
A backtest must count the cap across the two instruments, not per instrument — that halves the ceiling
against a naive per-symbol reading.

### 3. No entry before 09:30, stated first-hand as a rule he has been punished for breaking

> `video1270175432` [00:14] "We try to sell **two minutes before session opens** and **get destroyed**."
> [00:42] "Yeah, we'll wait now. **We'll definitely wait. It's not worth it.** Trust me."
> [00:47] "Even if it does work out — and **most of the time it doesn't** — it's not worth it."

Corroborates `8.`'s 09:30 gate from a second, independent source. The 09:10 analysis window is
analysis only; this is the clearest first-hand statement of it in the corpus.

### 4. The target is a numbered ladder and he scales out along it — he does not exit once

"Target one / two / three / four / five" appears in **all five** NY streams (27 mentions), and the
exits are partial:

> `video1270175432` [03:12] "I'm gonna **start closing some of these positions**" … [03:45] "target
> three just got smashed"
> `video1038794732` [05:43] "**take my quarter mill**, a lot of positions"
> `video1979454677` [14:29] "**I'll close most my position here.** I'm actually happy with another 50"
> `video1263885792` [06:27] "**Target two** over here if you took it, **target four** over here, looks
> like it might even hit the **target five**"

**This joins up with FINDING 7.** The ladder is the 1R…5R rungs; `10._USING_DATA`'s rolling mean is the
rule that says *which rung to call the day at*. This file previously had the ladder nowhere and the
rolling mean nowhere, and recorded only the descriptive range between them. Scaling out also means a
single-exit backtest is not modelling him, and that the "achieved R" fed back into FINDING 7 is
ambiguous between the first rung closed and the last — **his own examples use the final target hit**
(`10.` [01:07] "I was able to catch a one to three").

### 5. Risk is a percentage of account with a stated base and a stated halving

> `video1263885792` [00:15] "this first position I would risk **very very little**, maybe **one two
> percent** of your account"
> [00:26] "**Most of time I'll risk like five percent**"
> [00:27] "So like I'll probably go **two and a half percent**, **cut my risk in half** on a trade like
> this. Just because it's so small"
> `video1979454677` [02:46] "the markets have been very horrible to us this week. **I'm going very
> small positions**"

This file's spec table said only *"lower conviction → smaller size, never a tighter stop"* — correct,
but with no magnitudes. The magnitudes are: **base ~5% of account per trade, halved to ~2.5% on a
lower-conviction setup, and 1–2% on a marginal or early one**, with a further reduction applied to a
whole bad *week*, not just a bad setup.

**Stated plainly because the number is extreme:** 5% of account per trade is roughly ten times the
conventional 0.5%, and at that risk a run of six losses is a ~26% drawdown. That is an observation
about his sizing, not an endorsement of it, and it does not affect any profit-factor measurement of
the *signal* (leverage and sizing are ratio-invariant — see the ledger's LEVERAGE note). It matters
only for reading his results claims, which are already set aside as marketing.

### 6. One descriptive observation worth mining rather than his prescriptions

> `video1038794732` [02:28] "I've noticed **us 30 nasdaq have not been in sync**" … [02:50] "not only
> not in sync, even **out of sync completely**"

Per HARD LESSON 14 this is the class of claim that survives mechanisation — it is a statement about
the market, cheap to measure (rolling correlation of NQ vs YM returns during RTH), and it is the
actual justification for watching two instruments rather than one. **Queued, not tested.** No engine
in this project has both symbols with the depth to measure it.

---

## ██ CORRECTIONS THIS TICK MAKES TO THE SPEC TABLE ABOVE

The table under THE COMPLETE MECHANICAL SPECIFICATION is superseded on four rows. It is left in place
rather than edited, per this project's habit of not tidying away superseded claims.

| Row | Was | **Now, with source** |
|---|---|---|
| Target | "1:3 to 1:5 R" | **`targetR` = mean achieved R of the last ~6 trades, losses scored 0, recomputed daily** (`10.` [00:38]–[05:43]). 1:3–1:5 is where that output usually lands, not the rule. |
| Stop | "just beyond the broken level (~20–25 pts on NQ), never the far level" | unchanged, **plus a hard maximum**: a structural stop beyond ~25–30 pts **rejects the setup** (`11.` [01:26]) |
| Frequency | "max 2/day, 3 exceptionally" | cap unchanged, but **realised rate is ~0.67–0.89 per session** (`10.` [00:38]/[02:22]), and the cap **counts across NQ+YM together**, not per instrument |
| Direction | "Bullish → longs only. Bearish → shorts only." | that is the **stated** rule; the live sessions show **both sides pre-marked on both instruments**. Contradiction recorded, not resolved. |

## ██ WHAT THIS TICK DID NOT ESTABLISH

- **No number here came from a run.** No backtest, no engine call, zero credits. The sample estimate
  in FINDING 9 is a pre-registered prediction, explicitly not a result.
- **The stated-vs-observed direction contradiction is unresolved**, and cannot be resolved from
  transcripts alone — only a run that measures both configurations can.
- **Whether the rolling-mean target actually helps** is untested and, per FINDING 7's third defect,
  there is a specific structural reason to expect it to ratchet downward. Written before any run.
- **The four gold transcripts were identified, not decoded.** They are a different system and out of
  scope for this file.

---

# ██ TICK #5, 2026-09-05 — THE SAMPLE ESTIMATE WAS COMPUTED ON THE WRONG DENOMINATOR, AND THE TARGET RULE CANNOT RESOLVE ITS OWN RANGE

Zero credits. **No backtest, no engine call of any kind.** This tick re-analyses two things already
in the repo — FINDING 9's sample arithmetic and FINDING 7's target rule — against the transcripts
they were derived from. Both come back changed. Per the mandate's preference for correcting a
previous conclusion over adding a new unverified one, that is the whole of this tick.

## ██ FINDING 11 — FINDING 9 APPLIED A **BOOK-WIDE** TRADE RATE TO **SINGLE-INSTRUMENT** COVERAGE

FINDING 9 is the only quantitative claim this workstream has ever made. It is the basis for the
standing verdict that 15m is "marginal, not hopeless". **Its two inputs are measured on different
units, and multiplying them double-counts.**

The arithmetic it recorded:

| tf | bars (tick #3) | RTH sessions | × 0.67–0.89 | verdict recorded |
|---|---|---|---|---|
| 15m | 1,119 | ~43 | ~29–38 | "straddles the 30 floor" |
| 5m | 937 | ~12 | ~8–11 | "short by ~3×" |

The session counts are right. RTH is 09:30–16:00 ET = 6.5h = **26 bars/session on 15m** (1,119/26 =
43.0) and **78 bars/session on 5m** (937/78 = 12.0). Both reproduce exactly.

**The rate is the problem.** Those bars were measured on `NDX`/`NAS100` — **one instrument**. The rate
0.67–0.89 comes from his journal, and `10._USING_DATA` [00:49] says what the journal contains:
*"I'm gonna analyze **every trade that I took**"*. FINDING 10 of this file already established that
"every trade he took" spans **both** NQ and YM, and that his 2/day cap counts across the book, not per
instrument. So the rate is **trades per session across a two-instrument book**, and it was multiplied
by **sessions of a one-instrument feed**.

### HIS OWN NUMBERS FORCE THE BOOK-WIDE READING — THIS IS NOT AN INTERPRETATION

If 0.67–0.89 were a *per-instrument* rate, his book-wide rate across two instruments would be
**1.33–1.78 trades per session**, which over the two weeks he describes (10 RTH sessions) is
**13–18 trades**. He says the two-week count is *"anywhere from **six to eight trades**"* [00:41].
The per-instrument reading contradicts his own stated total by roughly a factor of two. **Only the
book-wide reading is consistent with the source.**

### THE RATE BAND ITSELF WAS ALSO SLIGHTLY OVERSTATED, IN THE FLATTERING DIRECTION

FINDING 9 obtained 0.67–0.89 by dividing **both** ends of the "six to eight" range by the **nine**
days of his worked example. But "six to eight" is attached to *"the last two weeks"* [00:40] while
"about nine days worth" [02:29] is the span of the specific six-trade example. Dividing a two-week
count by a nine-day span mixes denominators. The two internally consistent readings are:

- *"the last two weeks of trades… six to eight"* ÷ 10 RTH sessions = **0.60–0.80 / session**
- the worked example, *"six trades… about nine days worth"* = **0.67 / session**

**Defensible band: 0.60–0.80 book-wide.** 0.89 is above anything he states.

### THE CORRECTED ARITHMETIC

All five NY streams cover both instruments, and `video1038794732` [08:37] closes both in one session
(*"Target two for us 30, target four for NASDAQ"*). Treating the book as split evenly between them —
an **assumption**, but the observed one — the per-instrument rate is **0.30–0.40 / session**.

| tf | sessions measured | **single instrument** (0.30–0.40) | **pooled NQ+YM** (2× sessions) | vs the 30-trade floor |
|---|---|---|---|---|
| 15m | ~43 | **~13–17** | **~26–34** | single: **clearly below**. pooled: straddles |
| 5m | ~12 | **~4–5** | **~7–10** | **far below either way** |

**What changes, and what survives.** The pooled 15m band (~26–34) lands close to what FINDING 9
reported (~29–38), so the "straddles the floor" verdict is *recoverable* — **but only under a
two-instrument pooled backtest that no tick in this workstream has ever declared, and that FINDING 9
was not describing.** On the single instrument whose coverage was actually measured, the expectation
is ~13–17: **below the floor, not straddling it.** The 5m verdict hardens further.

### THREE THINGS THIS CORRECTION DOES NOT ESTABLISH

1. **That pooling is legitimate.** Pooling NQ and YM trades into one sample to clear a sample floor is
   a methodological choice, not a free doubling. It needs justifying before it is used, and his own
   descriptive observation cuts both ways: *"I've noticed nasdaq and us 30 have not been in sync…
   out of sync completely"* (`video1038794732` [02:28]/[02:50]). If true, pooling is more defensible
   (the two legs carry partly independent information); if false, the pooled sample is closer to 43
   correlated observations than 86 independent ones. **Unmeasured — no engine in this project has both
   symbols with the depth to check it.**
2. **That `US30` has coverage equal to `NAS100`.** Tick #3 measured 15m and 5m depth on `NDX`/
   `NAS100`/`USTEC` only. **`US30` intraday depth has never been measured on `backtest-lab`**, and the
   pooled column above silently assumes it matches. That check costs nothing and is queued.
3. **Any of it as a result.** These are estimates against a measured bar count, exactly as FINDING 9
   was. HARD LESSON 4 stands: score them against a real trade count if a run ever happens, and never
   build on them meanwhile.

## ██ FINDING 12 — THE ROLLING-MEAN TARGET CANNOT RESOLVE ITS OWN OPERATING RANGE AT n=6

FINDING 7 recorded three defects in the target rule. **There is a fourth, and it is the one that
decides whether the rule can work at all.** It is computable from the numbers he reads out on the
video, so it needs no run.

His worked example [01:05]–[02:07], with a loss scored 0 exactly as he scores it:

```
R outcomes:  3,  0,  2.5,  5,  5,  3      sum = 18.5,  n = 6
his answer:  18.5 / 6 = 3.08  →  "we are going to go for one, two, threes"
```

His arithmetic reproduces to the cent (and so does his update, 20.5/7 = 2.93). But the six values have
a **sample SD of 1.855**, so the standard error of that mean is 1.855/√6 = **0.757**, and the 95%
confidence interval on his 3.08 is:

> **[1.14 R, 5.03 R]**

**That interval spans the entire range the rule is supposed to choose within.** `SYSTEM.md` originally
recorded the target as "1:3 to 1:5" because that is where the output lands; at n=6 the output cannot
statistically distinguish 1:3 from 1:5, or either from 1:1.1. After his own +2 update the interval is
[1.32, 4.54] — no better. **The rule's precision is an artefact of rounding, not of the data.**

This sharpens FINDING 7's third defect rather than replacing it. That defect said the rule is
*biased downward* (a winner's R is capped by the target it exited at, a loss drags the mean to 0).
This one says it is also **too noisy to act on**: the discretisation is brutal, because a single extra
loss moves the rounded target a whole R —

| further losses appended to his window | mean | rounded target |
|---|---|---|
| +0 | 3.08 | **3** |
| +1 | 2.64 | **3** |
| +2 | 2.31 | **2** |
| +3 | 2.06 | **2** |

**Two losses change the traded target by a full R.** Combined with the downward bias, that is a
mechanism for ratcheting the target down after a bad run — precisely when a system's realised R is
most likely to be mean-reverting upward.

### WHAT THE LITERATURE SAYS, INCLUDING WHERE IT DOES NOT SUPPORT ME

Searched for published evidence for or against this specific rule. **There is none that I could find**
— it appears to be his own construction, and I am recording that absence rather than dressing up
adjacent material as a verdict on it. What the adjacent material does say:

- **On the window length, against him.** Practitioner guidance on deriving targets from a journal is
  explicit that the log must be large: *"export your last 100–200 trades and get your win rate,
  average win, average loss, and average R before writing down a single target"*
  ([fortraders.com](https://fortraders.com/blog/how-to-create-a-realistic-profit-target-plan)). His
  window is **six**. Same idea, sample size smaller by a factor of ~20.
- **On calibrating targets to realised R at all, for him.** The principle he is using is sound and
  independently stated: *"If your win rate data shows your average winner closes at 1.8R, setting 3R
  targets is statistically counterproductive"*
  ([journalplus.co](https://journalplus.co/learn/guides/trading-journal-metrics-guide/)). **The rule's
  intent is defensible. Its estimator is not.**
- **On his "slow refresh rate" premise, partly for him.** He justifies the rule by claiming R
  outcomes persist: *"if the markets are giving you one to fives every day, they're probably going to
  continue to do so for a little while longer"* [07:33]. The standard model treats trade outcomes as
  independent, but real series are not: volatility clustering (Cont) means bad stretches do cluster
  ([earnforex.com](https://www.earnforex.com/guides/measuring-winning-and-losing-streaks-in-forex/)).
  **That supports persistence in the *volatility* that caps achievable R — not the leap to a 6-trade
  mean being the right estimator of it.** His premise is more defensible than his arithmetic.

### THE PRE-REGISTERED QUESTION, NOW SHARPER — WRITTEN BEFORE ANY RUN, PER HARD LESSON 17

If a run ever becomes possible, measure `targetR = rolling mean of last 6, losses scored 0` against a
**fixed** target. **Predicted: the rolling-mean variant underperforms the fixed target**, from the
downward bias (FINDING 7 defect 3) plus the discretisation shown above. Two supporting predictions
that make the claim falsifiable rather than vague:

1. The realised `targetR` series **spends more time below its own starting value than above it**.
2. **Widening the window from 6 to ~20 recovers most of the gap** — if the loss is noise-driven as
   claimed here, a longer window should fix it; if it is bias-driven alone, it should not.

Prediction 2 is the discriminating test between FINDING 7's defect and this one. **Neither has been
run. Neither may be recorded as a result until a real `runId` produces one.**

## ██ WHAT TICK #5 DID NOT ESTABLISH

- **Nothing was backtested. No `runId` exists for this workstream and none was created.** Every number
  above is either arithmetic on figures already in the repo, or arithmetic on figures he speaks aloud.
- **Whether pooling NQ and YM is legitimate** — unmeasured, and the de-correlation claim that bears on
  it remains unmeasurable on both available engines.
- **Whether `US30` intraday coverage matches `NAS100`** — never checked, and the pooled column assumes
  it does.
- **Whether the rolling-mean target actually helps or hurts.** Two predictions are now registered. The
  engine deadlock from tick #3 is unchanged, so they stay unrun.

---

# ██ TICK #6, 2026-09-05 — POOLING NQ+YM CANNOT CLEAR THE SAMPLE FLOOR, AND THE ANSWER DOES NOT DEPEND ON MEASURING THE CORRELATION

Zero credits. **No backtest, no `plan_backtest_window`, no engine call of any kind.** Two inputs only:
the transcripts already committed here, and web research (URLs cited).

**Environment note, recorded because it changes what a tick can do.** Tick #5's queue item 1 —
*"measure `US30` 15m and 5m depth on `backtest-lab`"* — **could not be attempted this tick. This
session has no `backtest-lab` connector at all**; only trader-dev is present, and trader-dev is the
engine this workstream is forbidden to touch (tick #2, FINDING 4). The item is not stale, it is
**blocked by session capability**, and it stays queued for a session that has the connector.

---

## ██ FINDING 13 — THE POOLING QUESTION IS DECIDABLE WITHOUT KNOWING THE CORRELATION, AND THE ANSWER IS NO

HARD LESSON 56's corollary left this open in exactly these words:

> *"Pooling two correlated instruments does not give you 2N independent observations; it gives you
> somewhere between N and 2N depending on a correlation nobody has measured."*

That framing implied the question was stuck behind a measurement no engine here can make. **It is
not.** The verdict is invariant across the entire plausible range of that correlation, and at the
bottom of the expected band it does not depend on the correlation at all.

### THE MODEL, STATED BEFORE THE ARITHMETIC

FINDING 10.2 established what a pooled day actually looks like: **one NQ trade and one YM trade, the
same session, typically one each.** Three independent streams say so:

> `video1038794732` [05:35] *"as you can see **bot nasdaq bot us 30** currently up"*
> `video1263885792` [03:51] *"$60,000 on Nasdaq, $26,000 on us 30 — **we're taking two trades in a day**"*
> `video1979454677` [12:29] *"**this is two positions one day**"*

So the pooled book is **N pairs**, not 2N loose draws. Model each pair as two outcomes with equal
variance σ² and within-pair correlation ρ, pairs independent of each other. Then

```
Var(pooled mean) = σ²(1 + ρ) / (2N)      ⇒      N_eff = 2N / (1 + ρ)
```

`N_eff` is the number of *independent* trades the pooled sample is worth. ρ = 0 gives the full 2N;
ρ = 1 gives N, i.e. pooling buys nothing.

### THE ARITHMETIC, ON THIS WORKSTREAM'S OWN CORRECTED BAND

FINDING 11's corrected expectation on the measured `NDX` 15m coverage (~43 RTH sessions at 0.60–0.80
book-wide trades/session): **~13–17 trades per instrument, ~26–34 pooled.** Against the 30-trade floor:

| ρ assumed | `N_eff` at the **bottom** of the band (2N = 26) | `N_eff` at the **top** (2N = 34) | clears 30? |
|---|---|---|---|
| 0.0 (perfectly independent) | 26.0 | 34.0 | top only |
| 0.3 | 20.0 | 26.2 | **no** |
| 0.5 | 17.3 | 22.7 | **no** |
| 0.7 | 15.3 | 20.0 | **no** |
| 0.9 | 13.7 | 17.9 | **no** |

**Two things fall out, and neither needs ρ to be measured:**

1. **At the bottom of the band, pooling cannot reach 30 even if the two instruments were perfectly
   independent.** 26 < 30. No correlation assumption rescues it.
2. **At the top of the band, clearing 30 requires ρ ≤ ~0.13** (34/30 − 1 = 0.133; ~0.15 on the
   unrounded 34.4). **Nothing in the published record puts two US equity index futures anywhere near
   0.13**, and FINDING 14 below sets out what the record actually says.

**And the number that makes the point plainest:** at ρ = 0.9, the pooled book is worth **13.7–17.9**
independent trades against the single instrument's **13–17**. Running both instruments buys **less
than one extra independent observation.**

### THE DECLARATION TICK #5's QUEUE ITEM 2 ASKED FOR, MADE NOW AND BEFORE ANY RUN

> **NQ and YM trades MAY NOT be pooled to clear the 30-trade sample floor in this workstream.**
> A pooled count may be reported as a description of his book. It may not be quoted as a sample size.
> Any future run that reaches 30 only by pooling is reporting a number that this file has already
> declared inadmissible.

**What would reverse it, stated so the declaration is falsifiable (HARD LESSON 17):** a measurement of
the **trade-level** correlation between concurrent NQ and YM positions, over the actual holding period,
returning **ρ ≤ 0.13** — and even then only for the top of the expected band. Any ρ above that, and the
declaration stands. Note the asymmetry deliberately: this verdict is cheap to defend and expensive to
overturn, which is the right way round for a threshold that protects a sample floor.

### THE TRAP THAT WOULD DEFEAT THIS, NAMED IN ADVANCE — DO NOT MEASURE ρ ON 5m BARS

The obvious way a later tick would try to satisfy the reversal condition is to correlate NQ and YM
**5m or 15m bar returns** and quote the result. **That number would be systematically too low, and it
would not answer this question.**

The **Epps effect** — measured cross-correlation between two assets falls as the sampling frequency
rises — is a documented, decades-old empirical regularity, first reported by Epps in 1979 and studied
since ([arXiv:0704.3798](https://arxiv.org/pdf/0704.3798),
[On the origin of the Epps effect](https://www.sciencedirect.com/science/article/abs/pii/S0378437107004712),
[The Epps effect revisited](https://www.tandfonline.com/doi/abs/10.1080/14697680802595668)). The
literature attributes it mainly to trading asynchronicity and lead–lag structure, with the
characteristic time scale tied to participants' reaction time.

**Why that matters here:** his positions are held for **hours inside one RTH session**, scaling out
along a target ladder (FINDING 10.4). The independence question therefore lives at the **holding-period
horizon**, not the bar horizon. A low 5m correlation is compatible with a high holding-period
correlation and is not evidence for pooling. **If ρ is ever measured for this purpose, it must be
measured on the P&L of the concurrent trades themselves, or on returns sampled at the holding
period — never on the chart timeframe.**

---

## ██ FINDING 14 — HIS DE-SYNC OBSERVATION IS NOT FALSIFIED BY THE PUBLISHED RECORD, BUT IT IS CONTRADICTED BY HIS OWN BOOK IN THE SAME SESSION HE MAKES IT

FINDING 10.6 flagged this as the one descriptive claim worth mining per HARD LESSON 14, and queued it
as unmeasurable. It is still unmeasurable **on this project's engines** — but it is not unexaminable.

> `video1038794732` [02:28] *"I've noticed **us 30 nasdaq have not been in sync**"*
> [02:50] *"not only not in sync, even **out of sync completely**"*

### WHAT THE PUBLISHED RECORD SAYS — AND IT PARTLY SUPPORTS HIM

**A caveat on this evidence, stated first.** This session's network egress blocks `WebFetch` on every
one of these domains; the figures below are **as surfaced by web search**, not read from the primary
documents. They are cited so a later session with working egress can verify them, and **none of them is
a measurement made by this project.**

1. **NQ/YM is the *loosest* of the US equity-index futures pairs, not the tightest.** Practitioner
   sources put **NQ↔ES at ~0.93** and **ES↔YM at ~0.95**, with YM/ES described as the tightest pair
   ([stsfutures.com](https://stsfutures.com/learn/nq-es-correlation),
   [futures.aeromir.com](https://futures.aeromir.com/post/110/understanding-futures-correlation-what-every-trader-should-know)).
   NQ and YM sit at opposite ends of that complex — the tech-concentrated index against the
   price-weighted industrial one — so **if any equity-index pair de-syncs, it is his.**
2. **The 2024–2026 period he is speaking in is exactly the period the sources describe as diverging.**
   The Nasdaq-100/Dow relationship is reported as having *"weakened on shorter timeframes"* with
   rotation out of tech into value
   ([forex.com](https://www.forex.com/en/news-and-analysis/nasdaq-100-dow-ratio-focus-on-concentration-rather-than-timing-risk-trends/),
   [forex.com](https://www.forex.com/en-us/news-and-analysis/nasdaq-100-lags-dow-jones-divergent-signals-among-nvidia-apple-meta/)),
   and index-provider dashboards report rising dispersion with falling within-sector correlation
   ([S&P DJI dispersion dashboard](https://www.spglobal.com/spdji/en/documents/performance-reports/dashboard-dispersion-volatility-correlation.pdf)).
3. **But the baseline is high, not zero.** Rolling correlations across the US benchmark complex are
   reported climbing over three decades, with SPX↔NDX 12-month rolling correlation of daily returns
   reaching ~0.98 in March 2026
   ([CME Group](https://www.cmegroup.com/insights/economic-research/2026/why-us-equity-benchmarks-are-moving-together-and-drifting-apart.html)),
   and academic work on DJIA vs NASDAQ daily log returns reports persistent positive cross-correlation
   bounded roughly **0.49–0.93** across scales ([arXiv:2607.06324](https://arxiv.org/pdf/2607.06324)).
   **"Out of sync completely" is a relative statement inside a complex that never leaves strong
   positive territory.**

**Verdict on the claim itself: NOT falsified, and HARD LESSON 14's corollary does not trigger.** He is
describing the loosest pair in the complex during the period the literature says it loosened. That is
a trader seeing accurately again, which is the pattern that lesson predicts. **What is falsified is
the use his own arithmetic would be put to** — "out of sync" does not mean ρ ≤ 0.13, and nothing in
the record suggests it does.

### THE CONTRADICTION, AND IT IS INTERNAL TO ONE TRANSCRIPT

The strongest evidence against operating on the de-sync claim is **in the same seven-minute stream, on
the same day, three minutes later.** `video1038794732` in order:

| ts | what he says | what it shows |
|---|---|---|
| [00:00] | *"I think I'm **buying Nasdaq** waiting for us 30"* | long NQ, intending YM next |
| [02:28]/[02:50] | *"us 30 nasdaq have not been in sync… **out of sync completely**"* | the claim |
| [03:58] | *"**US 30 is going to push**"* | expecting YM **up** — the same direction as the NQ long |
| [05:35] | *"**bot nasdaq bot us 30** currently up"* | **both legs long, concurrently** |
| [06:09] | *"**target two for us 30 target four for Nasdaq**"* | **both legs winning together** |

**He asserts the two instruments are out of sync and then, minutes later, holds them long together and
banks them together.** That is not a contradiction in his *observation* — both can be true, since two
instruments can decouple in magnitude while agreeing in sign. It is a contradiction in the **inference
this workstream was about to draw from it**: the de-sync claim was queued as *"the actual justification
for watching two instruments rather than one"* (FINDING 10.6), and the book it justifies is, on this
day, **one directional bet expressed twice.**

**One honest counterweight, recorded rather than suppressed.** The other stream that holds both may
show them in *opposite* directions: `video1263885792` has *"Gonna **buy** Nasdaq"* [02:23] alongside
*"US 30 **cells** are here as well"* [03:02] and *"a beautiful **cell** position"* [03:13] — "cells"
almost certainly being the transcriber's rendering of "sells" — with both banked at [03:51]. **The
direction of the YM leg there is inferred from a mis-transcribed word and is not established.** So the
corpus shows one clearly same-direction pooled day and one probably-opposite one. **Two days settle
nothing about ρ**, which is precisely why FINDING 13 was built not to need them.

### THE PRACTITIONER LITERATURE IS BLUNT ABOUT THIS EXACT BOOK

Per the mandate's instruction to record the evidence *against*, not only *for*: holding two highly
correlated index futures concurrently is a **named, documented failure mode**, not a neutral choice.
The sources describe it as *"one bet doubled, not diversification"*, note that the correlation *"rises
toward 1.0 exactly when markets are stressed"* — i.e. it fails when it is being relied on — and one
directly poses the day-trader's question *"they are very correlated… is it better to just stick to 1 of
the 2 for day trading?"*
([stsfutures.com](https://stsfutures.com/learn/nq-es-correlation),
[futures.aeromir.com](https://futures.aeromir.com/post/110/understanding-futures-correlation-what-every-trader-should-know),
[Forex Factory thread](https://www.forexfactory.com/thread/699928-trading-nq-and-sp500-vs-the-dow)).

**The corresponding statistical statement is standard.** Bailey & López de Prado's deflated-Sharpe work
formalises effective trials as a function of the trial-correlation matrix (the eigenvalue participation
ratio), and the worked example most often quoted from that line has **22,500 nominal strategies across
9 ETFs collapsing to roughly 39 effective independent bets**
([SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551),
[Deflated Sharpe ratio](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)). **Nominal count and
effective count are different quantities whenever the things counted are correlated.** FINDING 13 is
that same correction applied to a sample floor instead of to a Sharpe ratio.

**One observation about his risk, stated because it is a property of the book and not advice.**
FINDING 10.5 recorded a base risk of ~5% of account per trade. Two concurrent same-direction legs at
5% each is **~10% on one direction**, not two diversified 5% bets. This does not touch any
profit-factor measurement (ratios are sizing-invariant — see the ledger's LEVERAGE note); it matters
only for reading his results claims, which are already set aside as marketing.

---

## ██ WHAT TICK #6 DID NOT ESTABLISH

- **Nothing was backtested. No `runId` exists for this workstream and none was created.** Every figure
  in FINDING 13 is arithmetic on a **stated model** applied to a band already in this repo, and it is
  labelled as such — it is not a measurement of anything.
- **ρ between NQ and YM was NOT measured**, at any horizon, by this project. FINDING 13 is built to
  survive not knowing it; that is its point, not a substitute for it.
- **The external figures in FINDING 14 were not read at source.** `WebFetch` is egress-blocked in this
  session for every cited domain; they are as reported by web search and need verification by a
  session with working egress before anything is built on them.
- **`US30` intraday depth is still unmeasured** — the required engine is absent from this session, so
  the pooled band's second unverified assumption is untouched.
- **The direction of the YM leg in `video1263885792` is not established** — it rests on reading
  "cells" as "sells".
- **The stated-vs-observed direction contradiction (FINDING 10.1) is still unresolved**, and the
  rolling-mean target predictions (FINDINGS 7, 12) are still unrun.

---

# ██ TICK #7, 2026-09-05 — THE SYMBOL SEARCH IS CLOSED BY EXHAUSTION, A THIRD SILENT REMAP IS FOUND, AND FINDING 13's REVERSAL CONDITION WAS STATED ON THE WRONG QUANTITY

Zero credits — and this tick **measured** that rather than assuming it (see the credit note in
`STATUS.md`). No backtest, no `runId`. Nine `plan_backtest_window` calls and one `search_perps` on
trader-dev, all pre-flight resolution only.

**Why calling trader-dev at all is not a breach of tick #2's FINDING 4.** That rule forbids running a
Legacy Forex *backtest* on trader-dev, because the instruments silently remap. Probing *which symbols
resolve to what* is the opposite activity — it is the measurement that rule was derived from, and it
is how the rule gets extended. No strategy was created and no run was executed.

## ██ FINDING 15 — TRADER-DEV CARRIES NO US EQUITY INDEX UNDER ANY CONVENTION, AND `SPX` IS A THIRD SILENT REMAP

Tick #1's queue item 3 — *"probe the remaining ticker conventions … to map the non-crypto catalog's
actual edges"* — has been open since this workstream was created and had never been performed. It is
performed here and now closes.

**Pre-registered before the calls (HARD LESSON 17):** *does trader-dev's non-crypto feed — the one that
passes `EURUSD`/`XAUUSD` through unchanged with ~17 years of history — carry any US equity index under
any vendor convention?* **If YES with intraday depth, the tick-#3 engine deadlock breaks**, because
trader-dev already has the Pine state this method needs and would then also have the data. **If NO, the
deadlock is confirmed by exhaustion rather than by not having looked hard enough.**

### THE ANSWER IS NO. EVERY INDEX CONVENTION TESTED FAILS.

`displaySymbol` read on every row, per FINDING 2 — never `parityAdjustments`.

| requested | tf | `applied.displaySymbol` | verdict |
|---|---|---|---|
| `NDX` | 15m | — hard error, *"not in the Bybit USDT perp catalog (639 instruments)"* | loud fail |
| `NQ1!` | 15m | — hard error, same | loud fail |
| `MNQ` | 15m | — hard error, same | loud fail |
| `DJI` | 15m | — hard error, same | loud fail |
| `US100` | 15m | — hard error, same | loud fail |
| `SPX500` | 15m | — hard error, same | loud fail |
| **`SPX`** | 15m | **`BYBIT:SPXUSDT.P`** | ⚠️ **SILENT REMAP — 64,805 bars returned** |

Combined with the six already on file (`NQ`→`IONQUSDT`, `YM`→`DYMUSDT`, and hard errors on `US30`,
`NAS100`, `USTEC`, `US500`), **thirteen conventions have now been tried on trader-dev and not one
returns a US equity index.** This is no longer "the right ticker has not been found yet"; the vendor
conventions are exhausted. **The trader-dev side of the engine deadlock is permanent.**

### THE NEW HAZARD, AND IT IS WORSE THAN THE ONE ALREADY RECORDED

`SPX` — the single most common alias for the S&P 500 — returns a **complete, healthy-looking coverage
response**: 64,805 bars of 15m data, first bar 2024-10-29, a normal date clamp. `parityAdjustments`
contains **only** `clamped_to_clickhouse_first_bar`. Nothing names the substitution. `requested.symbol`
comes back already rewritten to `SPXUSDT`. It is `SPX6900`, a memecoin.

**And the mechanism is not what this repo has recorded.** `STRATEGY-LEDGER.md` explains the NQ/YM
remaps as a *substring* match (`NQ` ⊂ `IONQ`, `YM` ⊂ `DYM`) and draws the moral that **short futures
roots** are the things at risk. `search_perps("SPX")` returns exactly one row:

```json
{ "wire": "SPXUSDT", "display": "BYBIT:SPXUSDT.P", "baseCoin": "SPX" }
```

`baseCoin` is **`SPX` exactly**. This is an **identity collision, not a substring collision** — the
crypto catalog contains a coin whose ticker *is* the index's ticker. No "avoid short roots that could
be substrings of a coin name" heuristic catches it, because there is no substring involved.

**The corrected rule, and it is the only safe one:** the length or shape of the requested ticker tells
you nothing about the risk. **Read `applied.displaySymbol` and compare it by eye to what you asked for,
on every single call, in every lab.** That guard is unchanged; what changes is that no ticker may be
assumed safe from inspection because it "looks too specific to collide."

### WHAT THE SWEEP CONFIRMS ABOUT THE FOREX FEED (unchanged, re-measured)

| symbol | tf | `applied.displaySymbol` | first bar | last bar | bars |
|---|---|---|---|---|---|
| `GBPUSD` | 15m | **`GBPUSD`** — unchanged | 2009-09-25 | **2026-05-19 10:45Z** | 411,264 |
| `USDJPY` | 15m | **`USDJPY`** — unchanged | 2009-09-27 | **2026-05-19 11:15Z** | 409,213 |

FINDING 3 generalises cleanly: the non-crypto feed is a real, deep, multi-pair FX feed, and its
**~3.5-month staleness is a property of the feed, not of `EURUSD`** — both new pairs end on the same
2026-05-19 date. **None of this helps this workstream.** FINDING 3 item 3 stands unamended: a
NY-session index method is a *hypothesis* on a currency pair, never an inheritance, and no tick here
may treat FX depth as a substitute for the instruments the system actually trades.

## ██ FINDING 16 — FINDING 13's REVERSAL CONDITION IS STATED ON THE WRONG QUANTITY. THE VERDICT SURVIVES; THE STATED REASON DOES NOT.

Correcting my own claim from one tick ago, which is the outcome the mandate says to prefer.

FINDING 13 modelled the pooled book as **N pairs** — every trade sitting in a same-session NQ+YM
couple — giving `N_eff = 2N/(1+ρ)` and the reversal condition **ρ ≤ 0.13**.

**That sets an unmeasured parameter to 1 without saying so.** Let `T` be the pooled trade count and
`p` the fraction of those trades that actually sit in same-session cross-instrument pairs. With `k`
pairs and `u = T − 2k` singles, and `p = 2k/T`:

```
Var(sum) = σ²(T + 2kρ)   ⇒   N_eff = T² / (T + 2kρ) = T / (1 + pρ)
```

FINDING 13 is the `p = 1` special case. **The real reversal condition is `pρ ≤ 0.133`, not `ρ ≤ 0.13`.**

**Is `p = 1` defensible?** It is *consistent* with the evidence but not *implied* by it. The three
cited streams do show paired days. But live streams are a **selected sample — the days he chose to
broadcast** — and his realised book-wide rate is 0.60–0.80 trades/session (FINDING 11). Both readings
fit that rate: `p = 1` means he trades on ~30–40% of sessions taking a pair each time; `p = 0.5` means
he trades on ~50% of sessions, half of them paired. **The transcripts cannot distinguish these**,
because the unstreamed days are exactly the ones not observed. `p` is as unmeasured as `ρ` was, and
FINDING 13 pinned it at the value most favourable to its own conclusion.

### WHAT THIS DOES AND DOES NOT CHANGE

| top-of-band requirement | `p = 1` (FINDING 13) | `p = 0.5` | `p = 0.25` |
|---|---|---|---|
| ρ needed to clear 30 | ≤ 0.13 | ≤ 0.27 | ≤ 0.53 |

**The verdict is unchanged and the declaration stands.** Two reasons, and the first is the load-bearing
one:

1. **`N_eff ≤ T` always**, for any `p` and any `ρ ≥ 0`. So at the bottom of the band `T = 26 < 30`
   **fails regardless of both parameters.** This half of FINDING 13 never needed either quantity and is
   the part that actually carries the conclusion.
2. At the top of the band, even the loosest column above (`ρ ≤ 0.53` at `p = 0.25`) sits below any
   holding-period correlation the published record reports for two US equity index futures
   (FINDING 14). The declaration is not rescued by relaxing `p`.

**So the correction is to the reasoning, not the ruling.** FINDING 13's conclusion — *NQ and YM may not
be pooled to clear the 30-trade floor* — holds. Its headline claim that *"clearing 30 requires ρ ≤ 0.13"*
is **withdrawn and replaced** by *"clearing 30 requires `pρ ≤ 0.133`, and is impossible at the bottom of
the band at any `p` and any `ρ`."* Any future tick attempting the reversal must now measure **both** `p`
(the pairing fraction, from a trade log) and `ρ` (at the holding-period horizon, never the chart
horizon — the Epps trap in FINDING 13 is unaffected by this correction and still applies).

## ██ WHAT TICK #7 DID NOT ESTABLISH

- **Nothing was backtested. No `runId` exists for this workstream and none was created.** FINDING 16 is
  arithmetic on a stated model, exactly as FINDING 13 was, and is not a measurement.
- **`p` and `ρ` are both still unmeasured.** FINDING 16 makes that fact explicit; it does not fix it.
- **`US30` intraday depth is still unmeasured** — `backtest-lab` is still absent from this session.
- **Whether `backtest-lab` has a silent-remap hazard of its own was not tested** here; tick #2 found it
  hard-errors on `NQ`/`YM`, but no `SPX`-style identity collision was probed on that engine, and the
  connector is unavailable to do so.
- The direction contradiction (FINDING 10.1) and the rolling-mean target predictions (FINDINGS 7, 12)
  are untouched and still unrun.

---

# ██ TICK #8, 2026-09-06 — THE DELIVERABLE ITSELF HAD NEVER BEEN AUDITED, AND ITS LEVEL GATE WAS COUNTING THE WRONG THING

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Pure code-vs-source
audit: `pine/VISUAL-legacy-forex-complete.pine` read line by line against the transcripts it claims to
mechanise. Every defect below is verifiable from the committed code and the committed transcript, with
no market data involved.

**Why this and not another symbol/sample tick.** Every route out of the sample-and-engine deadlock is
closed or out of this project's control (ticks #3, #6, #7). The one route the workstream has repeatedly
called "the only honest one available today" is **forward-testing the Pine live**. That makes the Pine
the workstream's entire deliverable — and in eight ticks **nobody had ever checked whether it does what
the file says it does.** It does not, in six places.

## ██ FINDING 17 — SIX DEFECTS IN THE VISUALISER, ONE OF WHICH INVERTS THE MEANING OF ITS LEVEL GATE

### 17.1 — THE TOUCH COUNTER COUNTED BARS, NOT TOUCHES, OVER A WINDOW CONTAINING THE LEVEL'S OWN PIVOT

v1's validator:

```
f_touches(lvl) =>
    int n = 0
    for i = 0 to 199
        if math.abs(high[i] - lvl) <= tol or math.abs(low[i] - lvl) <= tol
            n += 1
```

Two independent errors compound here.

**(a) It increments once per BAR inside the band, not once per visit.** His definition is visits, and he
counts them out loud, one per approach:

> *"We have one touch two touch three four five six seven touches **with those wicks** to this support
> zone price can't break it."* — `7._SUPPORT_AND_RESISTANCE` [00:47]
> *"one touch two touch three touch four touch almost another touch there"* — `7.` [01:04]

A single approach that loiters for eight bars scores 8 under v1 and 1 under his own counting.

**(b) The scan includes the level's own formation window.** `resLvl = lastPH`, a `ta.pivothigh`. The
pivot bar satisfies `|high − lvl| = 0` and scores a touch **by construction**, and each of the
`2 × pivLen = 10` neighbouring bars scores one whenever the local swing is smaller than the tolerance
band (`0.10%` of price).

**The consequence, stated as a falsifiable condition rather than a measurement:** `minTouch = 3` is
satisfied *at the instant the pivot confirms, with zero revisits,* whenever at least two of the ten bars
adjacent to the pivot have an extreme within 0.10% of it — i.e. **whenever the 11-bar pivot window spans
less than ~0.1% of price.** On a 5-minute index chart that is not a corner case. I have **not measured**
how often it holds and no number here claims to; the point is that the gate's pass rate is governed by
local quietness, which is the opposite of what "a level price cannot break" means.

**So the defect does not make the gate too strict — it makes it near-inert, and inert in a way that
selects for quiet swings.** A gate advertised as "validated by repeated touches" was, in the common case,
passing every fresh pivot.

**⚠ THE FIX IS EXPECTED TO BE DANGEROUS, AND THAT IS RECORDED BEFORE ANYONE RUNS IT.** Counting distinct
visits and excluding the pivot window is strictly stricter. Combined with `resLvl` being the *most recent*
pivot — a level price has by definition only just made, and usually has not had time to revisit three
times before it breaks — **`minTouch = 3` on the corrected counter may take the signal count to zero.**
That is HARD LESSON 8's exact tell and HARD LESSON 10's exact instruction: **measure the term before
testing the conjunction.** So:
- `minTouch` was **NOT retuned.** Retuning a threshold to keep signals alive, with no measurement, is
  curve-fitting against a number nobody has looked at.
- v2 computes **both** counts every bar, shows them side by side on the dashboard
  (`3 visits / 47 bars-in-band`), and plots all four to the data window. The first live session on a
  chart settles the magnitude in seconds, for free, without a credit.
- v1's counting is retained behind a `touchMode` input so the two are diffable on one chart. It is there
  for comparison, not for use.

### 17.2 — THE ROLE FLIP WAS ADVERTISED IN THE FILE HEADER AND ABSENT FROM THE CODE

v1's header listed, as step 3 of the stack, *"a broken level flips role (7. 00:27 / 01:51)"*. **No line of
v1 implemented it.** `resLvl`/`supLvl` were simply the last two pivots; nothing was ever remembered after
a break. The source states the rule three times and calls it common:

> *"But guess what support resistance does it turns into each other?"* — `7.` [01:51]
> *"So support broke and then became resistance so you see how they can turn into each other and they do
> very often."* — `7.` [02:16-02:19]
> *"Resistance now support... a break and a retest of support into resistance"* — `7.` [07:14]

v2 tracks flipped levels (a broken support becomes a resistance candidate and vice versa), voids one when
price closes back through it, and draws both. **It does not let them fire signals by default** — that
would alter the signal set in the same commit that corrects the level test, and then neither change could
be attributed. The input exists and is off.

**Note that the stop placement was already consistent with the flip** and this is worth recording as the
one thing v1 got right here: *"We can have our stop loss below where it would come back to retest"*
(`7.` [05:43]) — the stop sits behind the broken level in its new role, which is what both versions do.

### 17.3 — INTRABAR SEQUENCING: THE STOP WAS MOVED WITH THIS BAR'S CLOSE, THEN TESTED AGAINST THIS BAR'S LOW

v1's order of operations was: manage the stop using `close` → compute `hitS` using `low` → book the exit.
A bar that closed at +2R therefore lifted the stop to +1R and was then tested against **its own low**,
which may have printed before the run-up that justified the lift. That books trail-exits that never
happened. v2 manages on the previous bar's R (`close[1]`), which is the standard no-lookahead ordering.

### 17.4 — AN AMBIGUOUS BAR BOOKED THE WIN

`outR = hitT ? tgtR : ...` — when a bar touched both target and stop, v1 recorded the **target**. The
conservative convention is the stop, and here it is not merely convention: **achieved R feeds the
rolling-mean target rule** (`10._USING_DATA`), so an optimistic tie-break biases the *target itself*
upward on every such bar, which then widens the target, which produces more ambiguous bars. v2 books the
stop and labels a break-even exit as break-even rather than as a trail.

### 17.5 — ONE MAX-STOP INPUT FOR TWO INSTRUMENTS THAT NEED DIFFERENT ONES

v1 had a single `maxStopPts = 30.0` whose own tooltip read *"Luca reports him at 20 on NQ / 30 on YM"* —
the file stated the two-number rule and implemented the one-number version. The source, with Luca
explicitly relaying Mamba's figures (module 4 is Luca's per FINDING 6, but here he is quoting Mamba
directly, so it is admissible for this and only this):

> *"Mamba uses 20 points on NASDAQ, let's say 30 points on YM"* — `4._WHAT_ARE_CONTRACTS_AND_TICKS` [04:09]

And Mamba's own module-11 charts show **25 points** (*"that's a 25 point stop loss, which is solid"*
[00:20]), **20 points** (*"yeah, we had a 20 point stop"* [06:50]) and a refusal at **64** (*"my account's
gone if I do that"* [01:26]).

**30 points is ~0.14% of NQ and ~0.07% of YM.** The same integer is a materially different gate on the two
instruments, and a gate that changes trade counts is precisely this workstream's binding problem. v2
resolves per instrument, defaults 20/30 from the quote, and **prints the resolved instrument on the
dashboard** — per FINDING 15, a ticker string is never trusted silently, so the resolution is shown for
eye-checking rather than assumed.

### 17.6 — THE TRAIL RULE IS UNDER-DETERMINED IN THE SOURCE, AND v1 HARD-CODED ONE READING SILENTLY

This is the finding I expected to be a defect and which turned out to be an **ambiguity in the source**,
so the correction is to stop pretending it is settled. Module 11 supports three different rules inside
nine minutes:

| reading | evidence |
|---|---|
| **Step every +1R** | *"Every time this thing moves up in the same distance as our stop loss, which is 25 points, we're going to adjust our stop loss"* [02:13-02:17]; *"as price starts to push up even higher, you just adjust with it"* [03:59] |
| **Freeze at +1R** | what his **worked example actually does**: *"we're now at a one to five... we're going to take our stop loss tool and we're going to put that down to a one to one"* [06:27-06:38] |
| **Break-even only** | offered as a complete alternative: *"or don't adjust your stops at all"* [09:01] |

Only the floor is stated as non-negotiable: *"at worst, at the least, please put your stops to break even
at a one to one point five at the worst"* [08:02-08:19].

v1 implemented **freeze at +1R** and presented it in the header as the rule. v2 makes it an input across
all three readings, **defaults to freeze** — because that is the one he *demonstrates* rather than
*describes*, and HARD LESSON 14 says the demonstration is the more reliable half of a trader's account —
and the dashboard names the live mode. **This is a source ambiguity, not a modelling choice, and it must
not be resolved by taste.** It is also now a pre-registered question: if a run ever becomes possible, the
three modes are a clean three-way comparison on one mechanism.

### A SEVENTH ITEM, RECORDED AS A KNOWN LIMITATION RATHER THAN FIXED

The simulator exits in **one piece** at `tgtR` while drawing the 1R–5R ladder he scales out along
(FINDING 10.4). A scale-out would make "achieved R" a weighted blend, and **nothing in the source states
the weights** — how much comes off at target one versus target three is never said. Inventing weights to
make the simulator prettier would put a fabricated number into the rolling-mean target. Left as-is, and
now stated in the code rather than silently true.

## ██ WHAT THE AUDIT DOES *NOT* CHANGE

- **The decoded rules in this file are unaffected.** Every FINDING 1–16 stands. This is a defect report
  against the *implementation*, not against the specification.
- **No signal count, hit rate or performance figure appears anywhere in this tick**, corrected or
  otherwise. The v2 code has never been run on a chart by this session and cannot be — there is no
  TradingView here and the engine deadlock is unchanged.
- **17.1's "near-inert" verdict is an argument from the code and the definition of a pivot, not a
  measurement.** It is falsifiable exactly as stated, and v2 was built to make the measurement free.

## ██ WHAT TICK #8 DID NOT ESTABLISH

- **Nothing was backtested; no `runId` exists for this workstream and none was created.**
- **Whether v2 compiles.** It is `//@version=6` and uses only constructs already present in v1 plus
  `str.upper`/`str.contains` and a tuple return. **It has not been compiled** — there is no Pine compiler
  in this session — and the first person to load it should expect to fix syntax, not logic.
- **How much 17.1 actually changes the level gate.** That is a one-chart observation and it is now
  instrumented, not argued.
- **Whether any of the six defects would have changed a conclusion.** None could have: this workstream has
  never banked a result, so there is nothing to withdraw. **That is the one piece of luck here** — had the
  engine deadlock broken earlier and a run been banked off v1, four of these six defects
  (17.1, 17.3, 17.4, 17.6) would have silently shaped its numbers.
- `US30` depth, `p`, `ρ`, and the direction contradiction are all untouched and unchanged.

---

## ██ FINDING 18 — THE PADDING AND THE CAP ARE IN DIFFERENT UNITS, AND THE PADDING WAS EATING 62–78% OF THE ENTIRE RISK BUDGET

**Tick #9, 2026-09-06. Zero credits, no backtest, no engine call.** This is a second defect report
against the implementation, found by carrying tick #8's own audit one step further: FINDING 17.5 fixed
the max-stop **cap** per instrument and never asked what units the **padding** was in.

### THE DEFECT

v2 computes the two halves of the stop-width gate in incompatible units:

```
padNow      = close * stopPad / 100        // stopPad = 0.05  -> a PERCENTAGE of price
maxStopPts  = isYM ? maxStopYM : maxStopNQ  // 20 / 30         -> ABSOLUTE index points
projRlong   = (close - brkLvlLong) + padNow
stopOKlong  = projRlong <= maxStopPts
```

The gate therefore has only `maxStopPts - padNow` points of room for the thing it is supposed to be
measuring — the distance from the entry close to the level it just broke.

### THE ARITHMETIC, ON HIS OWN SCREEN PRICES

Both price levels below are **read off his own charts in the committed transcripts**, not assumed:

> `[03:06]` "you see **24, 9, 5, 4.5**. This 0.5 and stuff is once again still the ticks."  (`4.` NQ)
>
> `[07:23]` "It's **$46,942**. It's not 42.25.5.5. All this type of stuff. No, it is whole numbers."  (`4.` YM)

| | price (source) | pad @ 0.05% | cap (v2) | pad as % of cap | pts left for entry→level |
|---|---|---|---|---|---|
| **NQ** | 24,954.50 | **12.48 pts** | 20 | **62.4%** | **7.52** |
| **YM** | 46,942 | **23.47 pts** | 30 | **78.2%** | **6.53** |

**`useMaxStop` is ON by default.** So v2 was silently rejecting every break whose close sat more than
about seven points beyond the level it had just broken — on a system whose entire published stop is
20–25 points.

### THE PART THAT MAKES IT WORSE THAN A BAD DEFAULT — THE GATE HAS AN EXPIRY DATE

The pad scales with price; the cap does not. When `padNow >= maxStopPts` the gate is
**unsatisfiable at any distance** — `projR >= padNow >= cap`, so no setup can pass even if the close
sits exactly on the level. That threshold is:

| | pad ≥ cap at price | where the index was in the source |
|---|---|---|
| NQ, cap 20 | **40,000** | 24,954.50 — already 62% of the way there |
| NQ, cap 25 | 50,000 | |
| YM, cap 30 | **60,000** | 46,942 — already 78% of the way there |

A percentage pad measured against a fixed point cap is a gate that tightens every year the index
rises, with no mechanism anywhere in the file to notice it happening.

### WHY THE PAD SHOULD NEVER HAVE BEEN A PERCENTAGE

**Nothing in the source states a padding distance at all.** What it states is a *position*:

> `[05:43]` "We can have our stop loss below / `[05:46]` Where it would come back to retest"  (`7.`)
>
> `[00:15]` "our stop loss just needs to simply **start just below** that support" / `[00:20]` "That's a
> 25 point stop loss, which is solid."  (`11.`)

The pad is the word **"just"** — and in v2 that word was worth 12.5 points on NQ, i.e. **half of the
entire 25-point stop the very same sentence describes**. The one padding quantity the source actually
defines is the tick:

> `[02:06]` "A tick when we're talking about Nasdaq is a **0.25 increment**. There [are] four ticks in
> one point."  ·  `[07:07]` "there's no decimal places on YM... **one tick equals one point** on YM"  (`4.`)

**v3 makes the pad an input in ticks, defaulting to one tick** (0.25 pts on NQ = 1.0% of the cap;
1 pt on YM = 3.3%). This is labelled in the code as the **minimal source-expressible reading of "just
below", an interpretation and not a stated rule** — the same treatment FINDING 17.6 gave the trail
rule. The % mode is retained so v1/v2 behaviour stays reproducible for diffing, exactly as `touchMode`
retains v1's counting.

### A SECOND, INDEPENDENT DEFECT IN THE SAME GATE — THE NQ CAP CAME FROM THE WEAKER SOURCE

`maxStopNQ = 20` traces to module 4 `[04:09]` — **Luca describing** what Mamba uses, and this file's own
header already flags module 4 as the single Luca-sourced exception it draws on. Module 11 is **Mamba
demonstrating**:

> `[00:20]` "That's a **25 point stop loss, which is solid**." / `[00:23]` "That's actually a really good
> number." · `[01:43]` "And we have a **25 point stop**." · `[06:50]` "Yeah, we had a **20 point stop**."
> · `[01:36-01:37]` "**64 points.** No, my account's gone if I do that."  (`11.`)

**A 20-point cap rejects the exact worked example module 11 is built around.** v2's trail-mode fix
already set this file's precedent for a source that supports several readings — *default to the one he
demonstrates rather than the one he describes* — so **v3 moves the NQ cap default 20 → 25**. The source
brackets the acceptable stop at **20–25 and refuses 64**; it does not pin a single number, and the input
is where that ambiguity belongs. **YM's 30 is unchanged** and is now flagged in its tooltip as
single-sourced and Luca-relayed: module 11 contains no YM worked example, so there is no demonstrated
number to prefer over it.

### A THIRD, MINOR ONE — THE PAD FORMULA WAS WRITTEN TWICE

The projection used `padNow`; the trade-open block recomputed `close * stopPad / 100` inline. Two copies
of one rule that any future edit could silently desynchronise. v3 has one definition.

### THE CONSEQUENCE FOR TICK #8's QUEUED MEASUREMENT — IT WOULD HAVE BEEN UNINTERPRETABLE

Tick #8 queued a live-chart observation as queue item 1, warning that the corrected touch counter
**may take the signal count to zero** (HARD LESSON 8's tell) and instrumenting both touch counts so the
chart would settle it.

**That measurement was not yet decisive, and this finding is why.** v2 carried *two* independent gates
capable of producing zero signals — the corrected touch counter and a stop-width gate with 6–8 points
of room — and only one of them was instrumented. A zero-signal chart could not have been attributed to
either. v3 therefore adds a **Stop budget** dashboard row and three data-window plots (`Pad (pts)`,
`Pad as % of max stop`, `Stop budget left (pts)`), including an explicit **"PAD ≥ CAP — no setup can
ever pass"** state, so the two causes are separable on the first chart rather than confounded on it.

### WHAT FINDING 18 DOES NOT ESTABLISH

- **No number here came from a run.** No `runId` exists for this workstream and none was created. The
  table above is arithmetic on the file's own defaults and two prices quoted in the transcripts — it is
  not a measurement of how many signals the gate actually removed.
- **How often the gate actually binds is still unmeasured**, because that needs the distribution of
  (entry close − broken level) on a real chart. What is established is the *budget*, not the *hit rate*.
- **Whether one tick is the right pad.** It is the minimal source-expressible reading, offered as an
  input precisely because the source does not state one. It is not a measured optimum and must not be
  quoted as one.
- **Whether v2 or v3 compiles.** Still unknown, still no Pine compiler in this session — and this tick
  **could not close tick #8's queue item 2** for a reason worth recording: `tradingview.com` is blocked
  by this environment's network egress proxy, so the Pine v6 language reference could not be reached and
  a syntax audit would have been memory against memory. **No compile-error claim is made here.** v3 adds
  one new built-in, `syminfo.mintick`, and otherwise reuses constructs already in the file.
- **No past conclusion changes.** This workstream has still never banked a result. As in tick #8, that is
  luck rather than process: had a run been banked off v2, this gate would have shaped its trade count
  invisibly, and the resulting sample would have been blamed on the touch counter.

---

# ██ TICK #10, 2026-09-06 — THE LEVEL'S OWN WIDTH IS 2–3× WIDER THAN THE STOP THAT HAS TO SIT OUTSIDE IT

**Zero credits. No backtest, no `plan_backtest_window`, no engine call of any kind.** Tick #9's queue
item 4 asked for exactly this: *"audit the remaining gates for the same class of defect… `touchTol`
(0.10% of price) is the obvious next suspect and has never been examined."* It is the suspect, and it
is worse than the one tick #9 found.

## ██ FINDING 19 — THE TOUCH TOLERANCE AND THE STOP BUDGET ARE IN DIFFERENT UNITS, AND THEIR ACCEPTANCE REGIONS DO NOT OVERLAP

### THE DEFECT

`touchTol = 0.10` is a **percent of price**. Everything it has to be commensurable with — the max-stop
cap (`maxStopNQ = 25`, `maxStopYM = 30`), the pad (v3: one tick), the projected stop width — is in
**absolute index points**. This is FINDING 18's defect exactly, in a different gate, one order of
magnitude larger, and untouched since v1.

### THE ARITHMETIC, ON HIS OWN SCREEN PRICES

Both prices are read off his own charts in the committed transcripts (`4.` 03:06 and 07:23), the same
two used in FINDING 18 so the two findings are directly comparable.

| | price | tol = 0.10% | band (±tol) | cap | tol as % of cap | band as % of cap |
|---|---|---|---|---|---|---|
| **NQ** | 24,954.50 | **24.95 pts** | 49.91 pts | 25 | **99.8%** | **199.6%** |
| **YM** | 46,942 | **46.94 pts** | 93.88 pts | 30 | **156.5%** | **312.9%** |

### THE PART THAT IS NOT MERELY A BAD DEFAULT — TWO GATES WHOSE ACCEPTANCE REGIONS ARE DISJOINT

The stop-width gate accepts a break only if the entry sits within `stopBudget = cap − pad` of the
level. The touch counter calls any bar within `tol` of the level a **touch** — *"price can't break it,
it's stuck"* (`7.` 00:47).

| | stop budget = cap − pad (v3) | touch tolerance | budget − tol |
|---|---|---|---|
| **NQ** | 25 − 0.25 = **24.75 pts** | 24.95 pts | **−0.20** |
| **YM** | 30 − 1 = **29.00 pts** | 46.94 pts | **−17.94** |

**`tol > budget` on both instruments.** So **every break this system is capable of trading lies inside
the band its own level definition still calls "touching."** One gate scores the bar as a touch of the
level; the other scores the same bar, on the same level, as a break of it. That is not a mistuned
threshold — it is two halves of the file disagreeing about what a level is.

The comparison with FINDING 18 makes the point sharper still. v3 spent a full tick moving the pad into
the cap's units and settling on **one tick — 0.25 pts on NQ, 1 pt on YM.** The tolerance is **100× the
pad on NQ and 47× on YM.** The file was padding the stop by a quarter of a point beyond a level whose
own identity was fuzzy to twenty-five.

### THE PRICE-SCALING PROPERTY, AND WHERE IT DIFFERS FROM FINDING 18

`tol` scales with price; the cap does not. At **NQ 40,000** the band is 80 pts = **320%** of the cap;
at **YM 60,000**, 120 pts = **400%**. **This is a degradation, not an expiry** — unlike the pad, `tol`
does not enter the stop budget, so it can never make the gate mathematically unsatisfiable the way
FINDING 18's pad could. Stated precisely so the two are not conflated: the pad had a hard failure date,
the tolerance just gets steadily more wrong.

### WHY THE SOURCE CANNOT SETTLE THE NUMBER, AND WHAT CAN

He is explicit that a level **is a zone** and never once says how wide:

- *"seven touches with those wicks to this support **zone**"* (`7.` 00:47)
- *"I like to call support **zones**"* (`7.` 01:21)
- *"You make this little **thicker** because it's the whole thing"* (`7.` 04:35)
- *"if we were to **drag this to where we think** it support is"* (`7.` 01:37) — explicitly subjective

So any number is an interpretation, exactly as the pad was. The one constraint that is **not** an
interpretation is **commensurability: a level's own width must be smaller than the stop that has to sit
outside it**, or *"just below that support"* (`11.` 00:15) is undefined. v4 therefore anchors the
tolerance to the live max-stop cap — `tolFrac = 0.20` → **±5 pts on NQ, ±6 on YM** — which satisfies
that constraint by construction and removes the price-scaling drift for free. **0.20 is a labelled
interpretation exposed as an input, pre-registered as a one-dimensional test. It is not a measured
optimum and must not be quoted as one.**

**Why not ATR, the obvious volatility-relative fix.** ATR stops are **Coach Luca's**, and FINDING 6
established that nothing from Luca belongs in this indicator. The corpus split, decided five ticks ago
for a different reason, rules out the fix a generic S/R build would reach for first.

### WHAT THE DIRECTION OF THE BIAS IS — AND IT IS NOT DETERMINED

An over-wide band pushes the touch count **both ways at once**:

- **Up:** a bar 24 points from the level scores as a touch of it.
- **Down:** with v2's distinct-visit counting, a visit only ends when price leaves the band entirely,
  so price must travel more than 25 NQ points away *and come back* before a second visit can be
  counted. A wider band **merges** visits.

Which dominates is a property of the bar-range distribution, not of arithmetic, and **this tick does
not claim to know it.** That is precisely why v4 instruments it rather than asserting it.

### A THIRD, MINOR DEFECT IN THE SAME LINE

`tol = close * touchTol / 100` sizes the band off the **current bar's close**, not off the level being
tested, and recomputes it every bar. A fixed level's touch count can therefore change on a bar where
nothing happened anywhere near that level, purely because price drifted elsewhere — and since
`resValid` gates `brokeResRaw`, a level's *tradeability* can flip with it. The magnitude is small
(a 1% drift moves the NQ band by 0.25 pts) but the count is not stationary, which it should be.
**v4's default mode removes this by construction** (the band no longer depends on price at all);
% mode keeps it, deliberately, so that mode still reproduces v1–v3 exactly for diffing.

### ONE GATE THE AUDIT CLEARS — RECORDED BECAUSE A CLEAN RESULT IS ALSO A RESULT

`minTouch = 3` is the one level-gate number the source **does** support: *"We have all these touches
one two three is resistance"* (`7.` 04:31). It is the smallest count he ever labels a level with,
against 7 (`7.` 00:47), 4 (01:04) and 8 (01:41) elsewhere. It is a floor he **demonstrates**, not a
threshold he **states**, and it is not retuned here — but unlike the tolerance it is not invented.

## ██ WHAT v4 CHANGED

1. **Tolerance is a fraction of the live max-stop cap** (default 0.20), not a % of price. % mode
   retained for reproducing v1–v3, including its close-anchoring defect, exactly as `touchMode` retains
   v1's counting and `padMode` retains v1/v2's padding.
2. **`breakClears` — the break may be required to clear the band.** **OFF by default**: turning it on
   changes the signal set, and a correction tick does not audit and alter what fires in the same pass
   (v2's precedent with `flipTrades`). Worth recording that under v1–v3 tolerance this option was not
   merely off but **unsatisfiable** — clearing a 24.95-pt band leaves **−0.2 pts** of stop budget on NQ.
   At v4's tolerance it leaves 19.75, so it becomes a real pre-registered test for the first time.
3. **Instrument resolution moved above the level block**, since the tolerance now depends on the cap.
   Reads inputs and `syminfo` only; no behaviour change.
4. **Instrumentation** — a **Level width** dashboard row (tol in points, band width, % of cap, and an
   explicit **"TOL > BUDGET — every tradeable break is still inside the touch band"** state) plus four
   data-window plots. The dashboard now carries all three zero-signal causes side by side: the touch
   counter (tick #8), the stop budget (tick #9), and the level width (this tick).

## ██ WHAT FINDING 19 DOES NOT ESTABLISH

- **No number here came from a run.** No `runId` exists for this workstream and none was created. Every
  figure above is arithmetic on the file's own defaults and two transcript-quoted prices.
- **How much the tolerance actually changed the touch count** — unmeasured, and per the section above
  not even signed. It needs a chart.
- **Whether 0.20 of the cap is right.** It is a labelled interpretation satisfying one arithmetic
  constraint (tol ≤ budget). Nothing more.
- **Whether v2, v3 or v4 compiles.** Still unknown, still no Pine compiler here, and `tradingview.com`
  is still blocked by this environment's egress proxy (tick #9). **No compile-error claim is made.**
  v4 adds no new built-ins; it reuses constructs already in the file.
- **The literature was searched and could not be read.** `WebSearch` returns results; **every**
  `WebFetch` in this session was refused by the egress proxy — `arxiv.org`, `mdpi.com`, `vecviz.com`
  and `investopedia.com` were each tried and blocked. The following are therefore recorded as **leads
  for a session with fetch access, not as citations, and nothing in this tick rests on them**:
  Osler, *Support for Resistance: Technical Analysis and Intraday Exchange Rates*
  (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=888805); *Evidence and Behaviour of Support and
  Resistance Levels in Financial Time Series* (https://arxiv.org/abs/2101.07410);
  https://www.mdpi.com/2227-7390/10/20/3888; and
  https://www.tandfonline.com/doi/abs/10.1080/09603107.2012.663469 (identifying horizontal S/R levels
  empirically). The one claim the search summary makes that bears on this tick — that S/R zone width is
  conventionally an **arbitrary interval**, and that S/R levels can predict trend interruptions while
  still failing to beat buy-and-hold — is **unverified against any source** and is written down here
  only so a later session knows what to check.
- **No past conclusion changes.** This workstream has still never banked a result, and that remains the
  correct state.

---

## ██ FINDING 20 — THE VOLUME GATE'S THRESHOLD IS FINE. THE QUANTITY UNDER IT IS NOT HIS, THE PLACE IT SITS IS NOT HIS, AND ITS BASELINE IS OVERNIGHT FOR 77% OF THE 15m SESSION

**Tick #11, 2026-09-06. Zero credits. No backtest, no `plan_backtest_window`, no engine call of any
kind.** Everything below is arithmetic on the file's own defaults, on the session hours the source
states, and on verbatim quotes from `9._VOLUME` and `8._SESSIONS_TO_TRADE`.

Tick #10's queue item 4 named the next un-audited gate: *"`volMult = 1.0` against
tick-volume-vs-contract-volume on index CFDs, and `pivLen = 5`."* The volume gate was audited. The
CFD tick-volume question turned out **not** to be the interesting defect and is recorded below as a
secondary caveat; four larger things were found first. `pivLen` was **not** audited this tick and
remains open.

### THE PATTERN THIS BREAKS, AND WHY THAT MATTERS

Ticks #8, #9 and #10 each found a gate whose **units or counting basis** were wrong. That run created
an expectation that the next gate would fail the same way. **It does not.** `volMult = 1.0` is
dimensionless and comparing a bar's volume to an average of bar volumes is unit-consistent. Had this
tick gone looking only for a units mismatch it would have reported the gate clean. The defects are of
three different kinds, and the threshold — the thing a tuning pass would have reached for — is the
one part with nothing wrong with it.

### DEFECT 1 (THE HEADLINE) — `volLen` IS A BAR COUNT ON A SYSTEM THAT TRADES TWO TIMEFRAMES, SO IT IS TWO DIFFERENT GATES

The New York session he trades is **09:30–16:00 ET = 390 minutes** (`8.` [00:36]/[00:44], which states
both clocks explicitly: *"6:30 a.m. Pacific Standard Time is when session starts... if you're on the
east coast of the US it is going to be 9:30 a.m. Eastern"*). `volLen = 20` bars against that:

| tf | 20 bars = | baseline at the 09:30 open reaches back to | session bars | bars judged against a partly-overnight baseline |
|---|---|---|---|---|
| **5m** | 100 min | **07:50 ET** — pre-open | 78 | first **20 of 78 = 26%** |
| **15m** | **300 min (5 h)** | **04:30 ET** — entirely overnight | 26 | first **20 of 26 = 77%** |

The baseline is not composed purely of session bars until **11:10 ET on 5m** and **14:30 ET on 15m**.
On 15m, **more than three-quarters of the only session he trades is scored against an average that is
mostly overnight**, and the baseline never becomes clean before 14:30 — by which time `FINDING 9`'s
~0.7–0.9 trades per session have usually already happened.

**This is the ledger's HARD LESSON 10 shape** ("a flat % R floor binds harder on the tighter
timeframe") in a different parameter: a single default cannot serve two timeframes when the quantity
it controls is a *duration* and the parameter is a *count*. It sits in a file whose own header
insists 5m and 15m are the entire universe (`5.` [03:18]).

**And unlike FINDING 19, the direction of the bias is signed.** Overnight index-futures volume is
structurally below cash-session volume, so a mostly-overnight baseline makes `volume > avg × 1.0`
**easier**, not harder. The gate is therefore **loosest at 09:30** — the moment his own course says
the volume is best anyway (*"you're gonna have the most amount of volume"*, `8.` [02:05]) and the
moment he takes most of his trades — and only begins to bind in the afternoon, when he has usually
finished. **It does most of its filtering at the time of day he barely trades.**

**MAGNITUDE IS NOT ASSERTED.** How much this moves the gate's hit rate is a chart measurement. v5 adds
a `Vol baseline` dashboard row (span in minutes, and how many of the baseline's bars are outside the
session) plus data-window plots, so one live chart settles it. A `Session-to-date average` baseline is
added as a **pre-registered option, OFF by default** — switching it changes the signal set, and this
file's precedent (v2 `flipTrades`, v4 `breakClears`) is that a correction tick does not audit and
alter at the same time.

### DEFECT 2 — THE QUANTITY IS NOT THE ONE THE SOURCE USES

He defines volume kinematically and then reads it off **price displacement**, every single time:

> [00:41] *"Volume is **how fast is the markets moving** how fast are the markets moving?"*
> [02:30] *"Price is not moving down. It's **moving sideways**, which means we're **moving left to
> right** and creating consolidation."*
> [06:18] *"Boom that is a good volume. **We're not going left to right. We are going straight up**
> like price is supposed to."*
> [09:24] *"Prices moving... okay, but it is **a little bit sideways**. Not the best volume like the
> examples we just saw, but it is there."*

**He never reads a volume bar aloud in 831 seconds, never states a threshold, and never names a
lookback.** `volume > ta.sma(volume, 20)` is an **interpretation with no source support** — the only
gate in the visualiser whose underlying quantity is not the one the source uses. It is left in place,
because there is nothing *measured* to replace it with and inventing a displacement threshold would be
the fabrication this project forbids, but it is now labelled as an interpretation in the input tooltip
and in the file header.

### DEFECT 3 — AND IT IS IN THE WRONG PLACE. HIS PRE-ENTRY PROXY FOR VOLUME IS THE SESSION.

Every one of those three diagnoses is made on bars **after** the break:

> [00:56] *"If **price breaks out** and slowly starts to consolidate, more than likely price is going
> to lose."*

The 17:30 example is judged after the short is already open (*"if we were to take our short position
here"* [02:02], then *"that's already not good"* [02:23]). The 06:30 example's *"boom that is a good
volume"* [06:18] comes after *"let's take our long position as we break right there"* [05:45].

His **pre-entry** proxy is not a histogram at all:

> [06:31] *"**Why did we have volume? Because we traded during New York session** like we're supposed
> to. We're not trading outside of our session."*
> [02:12] *"This is what happens when there's no volume, and because **I'm trading at 1730, which is
> way out of the session.**"*

**v1–v4 have this exactly backwards: a hard pre-entry gate and no post-entry test at all.** It also
means the pre-entry gate is **partly redundant with the session gate already in the file** — War
Formation E82's shape, where `h1Bull`/`h1Bear` turned out fully redundant with `brokeBelow`/
`brokeAbove`. **That redundancy is recorded as a pre-registered ablation, not claimed**: whether it is
partial or total is exactly the kind of thing E82 needed a run to settle.

*(The 17:30 timestamp is on his own screen clock, which `8.` [00:36] fixes as **Pacific**. 17:30 PT =
20:30 ET — several hours past the 16:00 close, consistent with "way out of the session". The 6:30
examples are 09:30 ET, the session open. This is corroboration of the session anchor from a second
module, not a new finding.)*

### DEFECT 4 — TWO STATED RULES WERE IN THIS FILE'S OWN MECHANICAL SPEC AND ABSENT FROM THE CODE

Both appear in the SPEC TABLE above (rows **Early exit** and **Sizing**), decoded at tick #1. Neither
was ever implemented. **This is v2's role-flip defect exactly** — advertised in the documentation,
missing from the build — and it has now happened twice in this one file.

**(a) The volume-death early exit.**

> [03:22] *"**No volume doesn't look good. We're out of this trade.** Yes, we're negative right now,
> but we would rather lose this small amount right here, which would be about **seven points**, then
> let it go all the way up and take us out for **15 points**, more than double that. **Just take your
> loss, cut it off early.**"*

Now implemented in v5, **OFF by default** (it changes the trade record). The exit is evaluated *after*
the stop/target block, because an intrabar stop or target touch precedes the close this exit is taken
at — the conservative convention v2's fix #4 already set for this file.

**(b) Conviction sizing — a three-state rule against a binary gate.**

> [09:45] *"The volume is okay? The setup looks good **but not great**. I'm gonna **risk less**. Okay,
> **not** stop loss. I'm **not** gonna make a tighter stop loss, but instead **my contract size is
> going to get smaller**."*

Three states — no volume → no trade; okay → smaller size; good → full size — against a binary gate.
This file is an **indicator and takes no positions**, so v5 renders it as a dashboard row only. The
band edge separating "okay" from "good" is **UNSOURCED**; it is printed inside the cell so it reads as
a knob rather than a finding, and it never touches `volOK` or any signal.

### THE DERIVED CONSEQUENCE — HIS EARLY-EXIT RULE AND HIS TARGET RULE PULL AGAINST EACH OTHER

This follows from two of his own stated rules and needs no data.

A loss scores **zero** in the rolling window that sets his target, **regardless of its size**:
*"we take the three, **zero for a loss**, two point five, five, five and a three"* (`10.` [02:56]).
So, relative to letting a trade run:

| what the cut-early rule does to a trade | effect on the rolling-mean window |
|---|---|
| turns a would-be **full stop** (−1R) into a small loss (−0.47R in his example) | **none** — both score 0 |
| turns a would-be **winner** into a small loss | replaces a positive entry with a **0** |

**The cut is invisible on the loss side of that computation and can only remove winners from it.** So
the more disciplined he is about cutting early, the lower his rolling-mean target drifts — and the
target is recomputed daily off that same window. The rule saves real money and simultaneously degrades
the statistic he uses to set his targets. **Derived, not measured**, and stated here as a structural
property of his two rules rather than a prediction about their magnitude.

### THE SECONDARY CAVEAT TICK #10 ACTUALLY NAMED — CONTRACT VOLUME vs TICK VOLUME

The visualiser's header offers `NAS100` / `US30` as alternatives to NQ/YM. On CME futures the volume
series is **real contract volume**; on an index CFD it is **tick count**. `volMult` is a *ratio*
against a same-series average, so a uniform substitution of one series for the other does not
by itself break the ratio — which is why this is a caveat and not a defect. What it does mean is that
a live-chart reading of the `Vol baseline` row **is not transferable between a futures chart and a CFD
chart**, and the instrument the measurement was taken on must be recorded with it. **Unverified
against any external source** — `tradingview.com` and every `WebFetch` target remain blocked by this
environment's egress proxy (ticks #9, #10), so this rests on the definition of the two series and
nothing was fetched to confirm it.

### WHAT v5 CHANGED

1. **A `Vol baseline` dashboard row and four data-window plots** — the baseline's span in minutes, how
   many of its bars fall outside the session, the live ratio, and whether the gate passed. This is the
   fourth zero/near-inert-signal cause the dashboard can name and separate, after touch counting (#8),
   stop budget (#9) and level width (#10).
2. **A `Session-to-date average` baseline option, OFF by default.** Default behaviour unchanged.
3. **The volume-death early exit, implemented and OFF by default**, with `volDeadBars` labelled
   UNSOURCED and `volDeadR = 0` as the minimal source-expressible reading of "not moving".
4. **A `Conviction` dashboard row**, display only, with its unsourced threshold printed.
5. **`inSessRaw` split from `inSess`**, so the baseline instrumentation reports the real session even
   when the session gate is switched off.

**With default inputs, v5's signal set and trade record are identical to v4's.** Every addition is
either instrumentation or an explicitly-off pre-registered option. That is a checkable claim about the
diff, not a measurement.

### ██ WHAT FINDING 20 DOES NOT ESTABLISH

- **No number here came from a run.** No `runId` exists for this workstream and none was created. Every
  figure above is arithmetic on session hours the source states and on the file's own defaults.
- **The magnitude of defect 1.** The *direction* is signed by the structure of overnight vs cash-session
  volume; **how much** it moves the gate's hit rate is unmeasured and instrumented, never asserted.
- **Whether the volume gate is wholly or only partly redundant with the session gate.** Named as a
  pre-registered ablation. Not claimed.
- **What the right displacement measure would be.** Defect 2 says the quantity is wrong; it does not say
  what the correct one is, and no substitute was invented.
- **Whether `volDeadBars = 3` is anything.** It is a placeholder on an off-by-default feature. The source
  states the behaviour and its outcome and never a bar count.
- **The 15-point stop at [03:38] is NOT used to retune anything.** It is a third stop-width figure in
  this corpus alongside module 11's 25 and 20 and module 4's 20/30, but the instrument is not identified
  in that passage and the trade is one he is holding up as a **mistake**. `maxStopNQ` and `maxStopYM` are
  unchanged. Recorded as an observation only.
- **Whether any version compiles — queue item 2 is still open**, still blocked by the egress proxy, still
  no Pine compiler here. **No compile-error claim is made.** v5 adds three built-ins not previously in the
  file: `math.sum`, `timeframe.in_seconds()` and `inSessRaw`'s reuse of `time()`; expect to fix syntax,
  not logic.
- **`pivLen = 5` was not audited.** It remains the last un-audited number in the file and the source
  states none.
- **No past conclusion changes.** This workstream has still never banked a result, and that remains the
  correct state. As in ticks #8–#10, a run banked off v4 would have had its trade count shaped by this
  gate invisibly — luck, not process.

---

## ██ FINDING 21 — `pivLen = 5` WAS THE LAST UN-AUDITED NUMBER, AND THE DEFECT IS NOT IN THE NUMBER: THE STRUCTURE GATE KILLS A BROKEN STRUCTURE AT LEAST `pivLen` BARS LATE

**Tick #12, 2026-09-06. Zero credits. No backtest, no `plan_backtest_window`, no engine call of any
kind.** Source: `6._PRICE_ACTION_AND_MARKET_STRUCTURE` and `5._ANALYZING_TIME_FRAMES`, both Mamba
(FINDING 6 checked first, per the standing first rule of this workstream), plus arithmetic on the
Pine file's own constructs. Deliverable: `pine/VISUAL-legacy-forex-complete.pine` **v6**.

Tick #11's queue item 4 named this as the last un-audited number. It was audited, and — as in tick
#11, and against the pattern ticks #8/#9/#10 had established — **the number itself is not what is
wrong with it.**

### 21.1 THE HEADLINE — INVALIDATION IS A PRICE EVENT IN THE SOURCE AND A CONFIRMED-PIVOT EVENT IN THE CODE

He kills a market structure the instant price trades through the swing that defines it, and he says
so twice in nine seconds:

> [03:30] *"You see this level here. We did not break past the previous spot"*
> [03:35] *"So that previous higher high and higher low we didn't break past that now if price would have"*
> [03:41] *"Came down here and started to push down in this way **boom that is now a lower low**"*
> [03:47] *"Back up lower high back down lower low meaning we are now in a bearish market structure and prices no longer bullish"*
> — `6._PRICE_ACTION_AND_MARKET_STRUCTURE`

*"Boom that is now a lower low"* is a call made **as price pushes down**, not one made after a swing
has completed and been confirmed from both sides.

**v1–v5 had no invalidation rule of their own.** `bullStruct = hh and hl` compares the two most
recent confirmed pivot highs and the two most recent confirmed pivot lows, and it stays true until
a *new pivot confirms* and changes one of those comparisons. `ta.pivotlow(low, pivLen, pivLen)`
cannot return a value until **pivLen bars after the swing low itself**. So:

| | lag before a broken bullish structure can turn the gate off |
|---|---|
| **5m** | ≥ 5 bars = **≥ 25 minutes**, plus the length of the down leg |
| **15m** | ≥ 5 bars = **≥ 75 minutes**, plus the length of the down leg |

Against a 390-minute session and a trader whose stated purpose is *"we need to get in and we need
to get out"* (`5.` [00:27]), **75 minutes is 19% of the entire trading day.** Throughout that
window the direction gate still read BULLISH and `goLong` was still permitted into a structure that
had already broken. The bias direction is signed and it is the harmful one: **the stale state always
permits the direction price has just left.**

**v6 fixes it, ON by default.** `bullStruct` now dies the moment a close prints below `lastPL` — the
higher low it is built on — and re-arms only on a fresh confirmed pivot low; `bearStruct` mirrors it
on `lastPH`. `"Confirmed pivots only (v1-v5)"` reproduces the old behaviour for diffing.

**Two things are recorded before anyone loads a chart.**

1. **This may take the signal set to zero in chop** — HARD LESSON 8's exact tell. It is instrumented
   (a `Struct guard` dashboard row that names it as the blocker, plus three data-window plots),
   not tuned. No threshold was invented to soften it.
2. **HARD LESSON 8's generalised check was run first, and it passes.** The arming event is a
   confirmed pivot low; `ta.pivotlow` guarantees the `pivLen` bars following that low all have
   *higher* lows, so the confirming bar's close necessarily sits **above** `lastPL`. The latch
   therefore cannot be killed by the same price action that arms it — the failure that killed 3M
   Elite v16 and v17.

**This is also the first version since v2 whose default signal set differs from its predecessor's.**
v3, v4 and v5 each shipped their correction behind a switch defaulting to the old behaviour, because
each was replacing an interpretation with another interpretation. This one replaces *no rule* with
**a rule the source states outright**, which is the treatment v2 gave the touch counter. The
distinction is deliberate and is the reason the default moved.

### 21.2 `pivLen` IS NOT A ONE-DIMENSIONAL KNOB, AND THE PRE-REGISTERED TEST LIST IMPLIED IT WAS

`pivLen` appears in **three** places in the file:

| where | what it controls |
|---|---|
| `ta.pivothigh/ta.pivotlow(…, pivLen, pivLen)` | the structure gate's direction reading |
| `resLvl = lastPH`, `supLvl = lastPL` | **the traded levels themselves** — every entry, stop and target price |
| `math.abs(bi - lvlBar) <= pivLen` in `f_touches` | the exclusion window of the touch counter (tick #8's fix) |

Sweeping it moves the direction gate, the price of every level, and the level-validation test **at
once**. Any future test of `pivLen` is a three-parameter change and must be reported as one. It is
struck from the workstream's list of one-dimensional pre-registered tests.

### 21.3 THE CODE CANNOT BUILD A STRUCTURE STATE FROM INSIDE A 15m NEW YORK SESSION

A state needs `prevPH`, `lastPH`, `prevPL` and `lastPL` — two pivot highs **and** two pivot lows.
Two same-side pivots must sit at least `pivLen + 1` bars apart, and the outermost two each need
`pivLen` bars of confirmation, so the floor is

`pivLen + (pivLen + 1) + pivLen + 1` = **17 bars at pivLen 5**,

and a realistic alternating H–L–H–L sequence with half-swings of `pivLen + 1` is **~29 bars**.
Against the session he trades (`8.` [00:36]/[00:44]: 09:30–16:00 ET = 390 min):

| tf | session bars | floor (17) | realistic (~29) |
|---|---|---|---|
| **5m** | 78 | 22% of the session | 37% of the session |
| **15m** | **26** | **65% of the session** | **exceeds the whole session** |

**So on 15m the structure state is always inherited from bars that formed before 09:30**, and on 5m
it is for the first fifth to third of the day. There is also **no recency bound anywhere in the
file** on the pivots that define the state and the levels — `lastPH` can be days old while `lastPL`
is minutes old, and nothing notices.

**Whether that is wrong is not resolvable from the source.** He reads structure off a chart that
shows overnight bars, and he never says structure resets at the open. So this is **instrumented, not
corrected**: a `Struct age` dashboard row reports the age of the oldest defining pivot in bars and
minutes, how many of the four formed before today's open, and the two numbers above for comparison.
That is a deliberate difference from 21.1, where the source *does* state the rule.

### 21.4 WHAT IS CLEAN — RECORDED, BECAUSE A CLEARED GATE IS ALSO A RESULT

- **`bullStruct = hh AND hl` is faithful.** *"higher highs followed by higher lows"* (`6.` [01:53]),
  and the bearish mirror *"lower low, back up lower high"* ([03:47]). The conjunction is his.
- **The `consolidating` residual reaches the right verdict on a loose label.** `hh`/`lh` and
  `hl`/`ll` are mutually exclusive, so the residual holds two shapes: a broadening range (higher
  high + lower low) and the sideways one he actually describes (*"prices moving sideways… up down up
  down"*, `6.` [06:04]). Only the second is his "consolidation", but **both are correctly excluded
  from trading**, so the gate outcome is right and only the label is loose. Not changed.
- **`pivLen = 5` itself is UNSOURCED and was NOT retuned.** He draws swings by eye and states no bar
  count anywhere in the corpus. Retuning it would have been a three-parameter change (21.2) made
  against no measurement — the failure this project exists to avoid.

### WHAT FINDING 21 DOES NOT ESTABLISH

- **No number here came from a run.** No `runId` exists for this workstream and none was created.
  The tables above are arithmetic on Pine semantics, on the file's own defaults, and on the session
  length the source states — **budgets and bounds, never hit rates.**
- **How often the new invalidation actually fires**, and therefore whether it thins the signal set
  slightly or to zero. Instrumented on the dashboard and in the data window; not asserted.
- **Whether inheriting structure from before the open is a defect or is simply how he reads a
  chart.** The source does not say. 21.3 measures it and stops there.
- **Whether `pivLen = 5` is a good value.** Unaudited by construction — 21.2 says a test of it is not
  a one-parameter test, and no such test has been designed.
- **Whether any version compiles — queue item 2 is still open**, still blocked by this environment's
  egress proxy (`tradingview.com` unreachable), still no Pine compiler here. **No compile-error claim
  is made.** v6 adds `nz()` on a bool and one new user function; everything else reuses constructs
  already in the file. Expect to fix syntax, not logic.
- **With default inputs v6's signal set is NOT identical to v5's** — unlike v3, v4 and v5, which each
  preserved theirs. This is stated as a property of the diff, not as a result, and 21.1 gives the
  reason the default was moved.
- **No past conclusion changes.** This workstream has still never banked a result. As in ticks
  #8–#11, a run banked off v5 would have had its long signals shaped by a stale direction gate
  invisibly — luck, not process.
