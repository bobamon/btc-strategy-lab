# ██ THE 950 RULE & ROUND NUMBER PHENOMENON — SUPPLIED BY THE USER, 2026-09-02

**This is now the top of the queue.** It arrived as an annotated infographic ("Titans"), and it is the
first material this lab has received that is **natively bidirectional** — the same setup produces a
long or a short depending on one discriminator, exactly the design the user has been asking for.

## THE RULE AS STATED

| Step | Rule |
|---|---|
| 1 | **950 advance signal.** When price reaches x950 of a whole number, that whole number **will** be taken. Mark it. |
| 2 | **Whole number taken.** Once it breaks over, watch the **strength** of the break, not the break itself. |
| 3 | **Read velocity.** Strong → follow the move. Weak → look for exhaustion and a short. |
| 4 | **Next whole number.** If strong, ride toward it. **If weak, short above the whole number.** |

**Strong velocity break:** large full-bodied candles, little or no wicks, momentum continues.
**Weak velocity break:** small bodies, wicks on top, momentum fades — "the Green Army is exhausted".

**"Time doesn't matter."** No session or clock gate. If 950 is hit at 8am and the next wave is at 2pm,
the whole number still gets taken. Patience, not timing.

**Stated failure modes** (these are the author's, and they are diagnostic): killing the first whole
number; seeing price mid-range and assuming the next whole number is about to break; **shorting too
early**; confusing the end of one move with the start of the next.

**Claimed evidence:** price clusters at round numbers ~2.05x more than chance; order books show more
resting orders at 00 and 50; abnormal buying pressure below and selling pressure above round numbers.

## WHY THIS MATTERS MORE THAN THE ORACLE QUEUE DID

**1. It is the first genuinely new SHORT discriminator this lab has been given.** Ten short
constructions have failed here and in the BTC lab, and every one of them decided *where* to short. The
level-based family peaked at PF 0.749 (E13), continuation scored 0.555 (E29), and adding the coil
scored 0.490 (E28). **This rule does not propose a new location — it proposes a new TEST at a
location the strategy is already at.** Strong break, go with it; weak break, fade it. That is a
discriminator, not another geometry, and it is the axis nothing has tried.

**2. It directly answers the failure E29 exposed.** E29 established that entering at a level is not
what breaks the shorts — level-based builds are the better half of the record. What was missing was a
way to tell a break that will continue from one that will fail. **That is precisely what step 3 is.**

**3. It is one strategy, both directions, decided mechanically.** Matches the user's standing
requirement without bolting a second system onto the first.

## WHAT THIS LAB ALREADY HAS, AND THE REDUNDANCY THAT MUST BE CHECKED (E14)

**The champion already carries a crude version of this idea.** `inMiddle` bans entries when price sits
400–600 past a whole number — the dead zone *between* round numbers. The 950 rule works the same
geography from the other side: it acts in the 950–000 approach and just above the break.

**So `inMiddle` and the 950 gate are not independent, and any test must check whether the new gate is
doing anything `inMiddle` is not.** They could easily be two encodings of one effect, which is exactly
how E14's weakening trigger failed against the coil. **Test the 950 rule with `inMiddle` REMOVED**, or
the result is uninterpretable.

**Second redundancy, on the short side:** step 4's weak-break short is an exhaustion fade above a
level. E13's near-touch rejection short is also an exhaustion fade at a level, and it scored 0.749.
**The velocity test is the only genuinely new term**, so the honest experiment isolates it.

## IMPLEMENTATION QUEUE — 950 RULE

**950-1. COUNT THE POPULATION FIRST (HARD LESSON 10, and this lab has now been burned four times).**
Before building anything, count how often price reaches x950 and then takes the whole number within a
reasonable horizon. Counter build, one-bar exit, so `totalTrades` is the event count. **If the 950
signal fires 20 times in the sample there is nothing to test.** This is the single most important step
and it is cheap.

**950-2. DEFINE VELOCITY MECHANICALLY, THEN COUNT THE SPLIT.** "Large full bodies, no wicks" needs a
number: body / (high−low) above a threshold, plus range relative to `atr(30)`, measured on the break
candle and the one after. Then count how many breaks land STRONG versus WEAK. **A discriminator that
labels 95% of breaks one way is not a discriminator** — measure the split before trusting it.

**950-3. THE LONG: strong break, ride toward the next whole number.** Target becomes the next round
number rather than a fixed R multiple — note this changes the exit from the fixed-R rule the labs use,
so it must be tested as a separate variable, not smuggled in.

**950-4. THE SHORT: weak break, short above the whole number.** Judged ALONE on its own profit factor,
against E13's 0.74897196. This is short construction number eleven and the first with a new term.

**950-5. ONLY THEN combine, with `inMiddle` removed and both legs reported separately.**

## THE HONEST CAVEAT, STATED UP FRONT
The Oracle queue finished **1 of 5**, and the one item that helped was the *diagnostic* one — his
explanation of why entries fail — not any rule he stated as a rule. **This material is also a stated
rule set from a trader, and the base rate for those in this lab is poor.** What makes it worth
spending credits on is not that it is stated confidently; it is that step 3 names a term nothing here
has ever measured. **Mine it for the discriminator, not for the ritual.**

---

# ██ DESIGN CLARIFICATION FROM THE USER, 2026-09-02 — READ THIS FIRST

**"War formation should be any direction, it all depends on the higher time frames. That's what makes
the entries longs or shorts."**

**This is ONE bidirectional strategy, not a long strategy with a short bolted on.** The 6h/1h cascade
decides the SIDE; the 15m/3m/1m mechanics then execute in whichever direction the higher timeframes
indicate. That is the author's own framing — *"The six hour is the God of direction"* and *"We do not
short a long direction."*

**What this changes about how this lab has been working:**
- The v6 champion is **long-only, and is therefore an INCOMPLETE implementation**, not a finished
  strategy. It should be described that way everywhere.
- Every short experiment (E9, E9b, E13, E25, E26, E27) treated the short as a *separate system to be
  designed*. Under this clarification that framing was wrong: the short is the same cascade with the
  6h regime pointing down.

**AND THERE IS A REAL TENSION TO RESOLVE, STATED HONESTLY:**
The lab's standing rule is *never mirror the short off the long* — earned from E9/E9b, where mirrored
shorts went 2 winners in 15 and 14 in 69. **But the user's design IS a symmetric cascade**, which is
close to what "mirroring" meant here.

The evidence says the concept is not the problem, the *location* is. E13 added the 3m cycle-position
gate to a mirrored short and lifted it from PF 0.68 to 0.75 — the single best short result — because
it stopped the strategy shorting after price had already fallen. Longs get that location filter
implicitly (a reclaim only happens after a sweep down); shorts had to be given it explicitly.

**So the reconciliation is:** build the symmetric cascade the user describes, but the short side needs
an explicit location gate that the long side gets for free. The no-mirror rule is downgraded from
"never symmetric" to **"never symmetric WITHOUT solving location for the short side."**

**The next build should be a single strategy that takes longs when the 6h is bullish and shorts when
it is bearish, with the cycle-position gate on the short side, reported with both legs split out.**

---

# The Oracle's rules — decoded from his own videos

Sources: three local recordings (`transcripts/*.txt`) and three YouTube lessons
(`transcripts/youtube/*.txt`), all transcribed locally with faster-whisper, plus the annotated
images. **Every quote below is verbatim from his audio.**

> Research notes for backtesting. Not trade recommendations.

---

## ⚠️ A NAMING CORRECTION, STATED BY HIM
> "People at the consultation, **war formation has nothing to do with entering here.** I use it.
> I'm not going to go into that now."

**What this project calls "War Formation" is actually his *3-minute cycle drill-down*.** The real
"war formation" is a separate thing he uses and does not explain in this material. The lab name is
kept for continuity, but the strategy being built is the drill-down, not the war formation.

---

## LAYER 1 — DIRECTION. "The six hour is the God of direction."
> "**Clear direction is either more than one green bar on the six hour.**"
> "But if you're lucky enough to get the same thing on the one hour, you got an absolute winner."
> "Six hour and the one hour. Look the same, same colour. **This is the singularity event.**"

**Mechanical:**
- **Clear direction long** = more than one consecutive green 6h candle. Mirrored for short.
- **Singularity** = 6h and 1h the same colour. A bonus, not a requirement: *"if you got it on the one,
  you got double clarity, **but don't wait for that**."*
- **"We do not short a long direction."** Never counter-trend.

This is simpler and better specified than the current build's "4+ green HA 1h candles inside the
previous 6h block". **His rule is a straight count of consecutive 6h candles.**

## LAYER 2 — ENTRY. The 3-minute cycle decides *when*.
> "How do you enter and exit? **Three minute cycle.**"
> "**You don't want to enter at the top.** Well, we go down to the three minute and use the cycle."
> "**Don't long the top or short the bottom.**"
> "**I don't care what the one minute says**, as long as you've got direction on the six."

**Wait for the counter-move to finish:**
> "We want to wait for our turn to long. **We must let the Red Army finish.** See, if you go ahead and
> you long down here... **people who longed here got wrecked. They were guessing.** People who longed
> here missed the move. They were guessing."
> "People who have my consultation know about **entering the enemy's camp** and not entering the
> enemy's camp."

**The trigger is the counter-move weakening:**
> "**You can see this dump is getting weaker.** You're waiting your turn patiently. It's getting
> weaker... **There is your moment.** Your moment to long was no other place but here."
> "So you watch the candles. **Candles get smaller. The move gets shorter. The move gets weaker.**"
> "**The size of the candles shows you the direction.**"

**Mechanical entry (long):** with 6h direction long, on the 3m chart wait through the red sequence
until consecutive red candles are **shrinking in range**, then enter as price turns up. Never enter
while the red candles are still expanding — that is "the enemy's camp".

## LAYER 3 — EXIT. Stay while it is your colour.
> "It's already starting to slip. That was your last three minute candle. Look at your next one.
> **It's smaller compared to this one. It's growing a tail. The price is dropping.** But **you stay in
> the trade because... it's still your colour. You stay.** You're in profit."
> "Now you would close your trade."

> "**I only use tails on the lower time frames** — like the one minute and three minute."
> "**A growing tail is a sign of weakness.**"

**Mechanical exit:** hold while the 3m candle colour still matches the trade direction. Shrinking
candles and a growing tail are *warnings*, not exits. Exit when the colour flips.

## OTHER STATED RULES
- **"The bigger the candle, the bigger the move."**
- **"Price versus candle"** — the named failure mode: entering because a candle looks right rather
  than because price is in the right *location*.
- **"All this is, is waiting."** · "I wait, let them buy the dip, even if you've got to walk away."
- **"See where you enter starts the timer."**
- **"The market can go against you longer than you can be liquid."**
- One green candle at the bottom of the 3m is a stand-down signal for shorts.
- **Tactical awareness, explicitly secondary**: stock-market open, the AM pump, whole numbers
  ("we just dumped a lot from over the whole number 28"). Equities are "only confirmation of what I
  know to be the direction here that we follow".

## FROM THE ANNOTATED IMAGES
- `chart.webp` — XBTUSD 1m; three "Short" marks at rallies into the thick blue MA, three "TP" marks
  at the swing lows. (Strategy 004 was built from this.)
- `enter.webp` / `exit_points.webp` — **BitMEX XBTUSD 3-minute.** Entry arrowed at the base of a run;
  "CLOSE" arrowed at the first rejection candle after it.
- `WAR_UP.webp` / `war_down.webp` — exchange order panel, platform mechanics, not strategy rules.

---

## WHY THIS EXPLAINS EVERY FAILED SHORT
E10/E11 proved the bear label is sound but that **both** directions lose across bear bars. E9/E9b
showed two different short geometries failing with healthy payoff ratios and ~20% win rates.

His rule accounts for exactly that. **Every short this project built entered after price had already
fallen** — the bottom of the cycle, into the enemy's camp, shorting into weakness. He states plainly
that this "wrecks an absolutely perfect trade" even when the direction is right.

**The defect was never the geometry. It was the location.**

## IMPLEMENTATION QUEUE (supersedes earlier items)
1. ~~Replace the direction rule with his~~ — **TESTED (v7), REVERTED.** PF 1.69→1.14, DD 3.10%→4.19%,
   win rate 56.3%→40.9%. His stated rule underperforms this lab's HA 1h green-count on this data.
   His words describe how he *reads* a chart; they are not automatically the best mechanisation of it.
   Sample caveat: 22 vs 32 trades. Keep v6's direction rule.
2. ~~Add the 3m cycle-position gate~~ — **TESTED (E13). IT HELPS.** On the short leg: PF 0.68→0.75,
   win rate 20.3%→23.1%, net loss halved −5.9%→−3.0%, trades 69→39. The trades it removed were
   disproportionately bad, which is exactly what he predicts. **His diagnosis is directionally
   confirmed.** Still PF 0.75 < 1.0, so the short is not yet viable — the gate is necessary but not
   sufficient. Keep the gate in all future short builds.
3. ~~Add the "counter-move weakening" trigger~~ — **TESTED (E14), REVERTED.** PF 1.69->0.73,
   win rate 56.3%->45.0%, trades 32->20. It removed disproportionately GOOD trades because it is
   **redundant with the 3m coil**, which already measures a move losing force. His observation is
   sound and already implemented under a different name. Do not re-run as an additive gate; the only
   open variant is weakening-run *instead of* the coil, head to head.
4. ~~Replace the exit with the colour rule~~ — **TESTED (E15), REVERTED.** PF 1.69->0.31, win rate
   56.3%->20.0%, average hold 12.8 bars. The flip fires on the first red 3m HA candle, which inside
   an uptrend is noise, so winners are cut at twenty minutes while losers run to the stop. **The
   fixed 2R target is load-bearing.** His rule presumes a human judging whether a flip means
   anything; taken literally it is not mechanisable at this resolution.
5. ~~Require the singularity~~ — **TESTED (E16), REVERTED.** PF 1.69->0.52, win rate 56.3%->34.6%,
   trades 32->26. **He was right and we should have believed him:** "but don't wait for that."

---

## THE QUEUE IS FULLY WORKED. SCORE: 1 OF 5.
Only item 2, the 3m cycle-position gate, ever improved anything -- and it was the one item that was
**diagnostic rather than prescriptive**, his explanation of why entries fail rather than a rule for
taking them. Every rule he stated as a rule underperformed this lab's own mechanisation of the same
idea. Mine a trader's material for the *why*, not the *what*.
