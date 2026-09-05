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
