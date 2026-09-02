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
3. **Add the "counter-move weakening" trigger**: require N consecutive counter-colour 3m candles with
   decreasing range before entry.
4. **Replace the exit** with the colour rule: hold while the 3m candle colour matches the trade;
   exit on colour flip. (This conflicts with the project's fixed-TP requirement — test it as a
   variant and report both.)
5. Optional: require the **singularity** (6h and 1h agreeing) and measure whether it improves results,
   since he calls it a bonus rather than a requirement.
