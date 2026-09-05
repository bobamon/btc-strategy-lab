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
