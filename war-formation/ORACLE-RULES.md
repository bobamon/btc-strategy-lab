# War Formation — the Oracle's own rules, from his videos

Decoded from transcripts of the recordings in the Oracle folder (`transcripts/*.txt`) plus the
annotated images. Quotes are verbatim from the audio.

> Research notes for backtesting. Not trade recommendations.

---

## THE CENTRAL RULE — the 3-minute cycle is the entry gate
This is the single most important thing in the new material, and it is the rule the strategy has
been missing. Direction comes from the 6h and 1h. **But direction alone does not permit an entry —
position within the 3-minute cycle does.**

> "So direction is clearly confirmed on the six hour and the one hour to be short at the moment...
> **but if you shorted at the bottom of this cycle**... well the size matters, and if not you got
> caught in this, and **this is where your trade is now against you 60%** — even though you have the
> right to short."

> "Even if you had direction to short **you can wreck an absolutely perfect trade**. We take direction
> from here and here. **But before you enter your trade, see where we are here.** Does this look like
> the bottom of a move? It only goes up and down. Does it look like the top of a move? **Do you want
> to short down here?**"

**Mechanical statement:** in a bear regime, do NOT short after price has already fallen inside the
current 3m cycle. Short only from the **upper** part of the cycle. Mirrored for longs.

## WAIT FOR THE PUMP
> "Down here too low and **you don't wait for this pump to come** — you are going to have the most
> difficult trade. It's going to go against you heavily."
> "Look at this pump. **All this is, is waiting.**"
> "I still want to wait. I want to see some green buying... **I wait, let them buy the dip**, even if
> you've got to walk away."

The entry is not the signal — the *retrace against the trend* is the entry. Short into strength
inside a downtrend; do not short into weakness.

## THE 1-MINUTE LIES — this is why the entry timeframe must be gated
> "Look how **the one minute lures you in**. You see the green candle there, you might want to go
> long. But look at the three minute — **the three minute says no, wait.** It's a preventative
> measure. This is exactly what I always tell you: **refer to the three minute before you make a move
> on the one minute.** It could save your trade."

> "**Shorting at the wrong point of the three minute chart — I don't care what the one minute says —
> will wreck your trade.**"

## PRICE VERSUS CANDLE
> "Watch the price go up. **This is called price versus candle.** It is very tempting, very hard —
> especially when you see this going down like this — to not enter more shorts."

Entering because a candle looks right, rather than because price is in the right *location*, is the
named failure mode.

## OTHER STATED RULES
- **"The bigger the candle, the bigger the move."**
- **A growing tail is a sign of weakness**: "look, this can change, it's growing a tail, it's a sign
  of weakness."
- **One green candle at the bottom of the 3m is a stand-down signal**: "there was one green candle on
  the bottom of the three minute — if you short down here too low..."
- **Entering late is the recurring sin**: "I enter a trade too late on the three minute because I
  cannot wait... and then this happens, and many times because of this I have to fight my way out."
- **Tactical awareness** (secondary, explicitly not primary): stock-market open, the AM pump, and
  whole numbers — "we just dumped a lot from over the whole number 28". He calls equities "only
  confirmation of what I know to be the direction here that we follow."
- **"Singularity"** — used as a 1h condition ("the one hour, the singularity, to short"). Not defined
  in this material.

## FROM THE ANNOTATED IMAGES
- `chart.webp` — XBTUSD 1-minute. Three "Short" marks, each at a rally into the thick blue MA;
  three "TP" marks at the swing lows. (This is the image strategy 004 was built from.)
- `enter.webp` / `exit_points.webp` — **BitMEX XBTUSD on the 3-minute chart.** Entry arrowed at the
  base of a run; "CLOSE" arrowed at the first rejection candle after it. Large numbered order
  markers (2,500 / 14,900 / 10,000 / 9,300) stack as price rises.
- `WAR_UP.webp` / `war_down.webp` — an exchange order panel with "Buy Order UP" / "Buy Order DOWN"
  and auto-sell at 200% profit. Platform mechanics, not strategy rules.

---

## WHY THIS MATTERS FOR THE STRATEGY — the diagnosis was right, the fix is here
E10/E11 established that the bear label is sound but that **both** directions lose across bear bars,
because those periods drift slightly up most of the time and fall hard occasionally. E9/E9b showed
two different short geometries failing with healthy payoff ratios and ~20% win rates.

**The Oracle's rule explains exactly that pattern.** Both failed short builds entered *after* price
had already moved down — shorting into weakness, at the bottom of the cycle — which is precisely
what he says wrecks the trade. The strategy has had the right direction and the wrong location.

**The fix is a cycle-position gate**, not more geometry:
- Reconstruct the 3-minute cycle from 1m bars (3 × 1m, exactly as the War Formation already
  reconstructs 15m/1h/6h).
- Compute where price sits inside the current 3m cycle range.
- **Shorts only permitted in the upper portion of that range; longs only in the lower portion.**
- Require the retrace first — a green push against a bear regime before a short is allowed.

## Open questions this raises
1. What exactly bounds "the cycle"? A fixed lookback of 3m candles, or a swing-to-swing measure?
2. What counts as "waiting for the pump" mechanically — N consecutive green 3m candles, or a
   retrace of X% of the prior leg?
3. What is the "singularity" on the 1h?
