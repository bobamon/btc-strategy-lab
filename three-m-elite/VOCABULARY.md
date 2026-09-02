# 3M SYSTEM — vocabulary decoded from the videos

Built from **transcripts** (`transcripts/*.txt`, all 10 videos, ~29,000 words) and from **frames**
read with OpenCV. Quotes are the author's own words.

> Research notes for backtesting. Not trade recommendations.

---

## ✅ TYPE 1 AND TYPE 2 VALIDATION — DECODED
Source: `2026-08-09 07-20-21.txt`, a dedicated 10-minute lesson.

> "The two types of validations: **type 1 validation is just going to be a 3M candle.** Okay, and
> **type 2 is going to be an engulfing candle. Candle in direction of bias.**"

**The gate:** after a zone is tapped, you may NOT drop to the entry timeframe until the zone produces
**either** a 3M candle **or** an engulfing candle in the direction of bias.

> "If we're looking for longs, we need a **green** triple-M candle or a **bullish** engulfing candle.
> If we had a supply zone and we're looking for shorts, we would need a **bearish** engulfing candle
> or a **red** triple-M candle."

**Which timeframe:** validation happens **only on the structure timeframe**, never on the zone's own.
> "This type one or type two validation, **it is only on the 15 minute**. That is the only timeframe we
> get this validation on... However we can get this 15 minute validation inside 15 minute zones **or
> inside one hour zones**... even though it's a one hour zone, the validation we use is still on the
> 15 minutes."

In his 1-minute variant, entry = 1m and validation = 15m. That is the **structure** timeframe from the
checklists (4m for the 15sec variant, 8m for the 30sec variant, ~16x the entry). **For 3M ELITE the
validation timeframe is therefore 48m**, which is what the current build uses.

**After validating:** mark the protected level.
> "The second we get that, we can **draw out our 15 minute low** and we are now valid."
That low is the **protected low** (protected high for shorts) — the structural reference for the stop.

---

## ✅ ZONE INVALIDATION — DECODED
> "The second that we get a candle that **body closes below the zone**, this entire zone is **invalid**.
> We can no longer take trades from this zone."

And it is judged on the **zone's own** timeframe, not the validation timeframe:
> "In order for this zone to invalidate with a body close below, **since it is a one hour zone**, if we
> get a 15 minute candle that body closes below the zone, that does **not** necessarily make the zone
> [invalid]."

**Immediate re-validation rule:**
> "If the next candle right after this just is a body closed down here, then that immediately
> invalidates it. And then we just need a new triple M or a new engulfing candle."

---

## ✅ ONE CANDLE RULE — DECODED
Source: `2026-08-09 03-24-31.txt` (the whole video).

Governs **when a supply/demand zone counts as mitigated**.
> "Once the zone gets created with the engulfing candle, when you get the next candle tapping into it
> and also making a new high — this is called the one candle rule... **this one candle does not
> mitigate the zone yet.**"
> "So if we get a **second** candle that continues up without being a triple M, and it's not a
> pullback, then that **would** mitigate the zone."

Applies to structural-break zones *and* fractal zones — "this goes for every type of zone".

---

## ✅ CLUSTER AND STAGE ONE — PARTIALLY DECODED
> "A **cluster** is what puts us into **stage one**."
> "The cluster zone is **the deepest zone of any given range** that you're in."
> "This break right here is what creates the cluster, and it's also what puts us into stage one."

Stage progression seen: **stage one → stage one re-accumulation**, the latter entered on a breakdown.
> "This break down right here is what puts us into stage one re-accumulation."

The full stage list is taught in the 156-minute video (`2026-08-09 04-42-54.txt`) and has not been
fully extracted yet. Clusters themselves were taught in an **earlier week** not included here.

---

## ❌ STILL MISSING — and why
| Term | Status |
|---|---|
| **3M candle (triple M)** | **Anatomy never defined in these ten videos.** It is assumed knowledge from an earlier chapter and is detected automatically by their indicator. This is the single most important gap — Type 1 validation *is* this candle. |
| **Swing rule** | **Explicitly deferred by the author**: "you guys are going to learn about the swing rule, **I think next week**". Confirmed absent from this material, twice. |
| **Full stage sequence** | Partially decoded (stage one, stage one re-accumulation). The rest is in the 156-minute video, not yet fully mined. |

---

## ⚠️ THE BIGGEST FINDING — this system runs on a proprietary indicator
> "You guys are very privileged that we have **our own alert system in our 3M indicator**... go to the
> drop down, go to the **3M Elite indicator**, and then you can set an alert for any of these things."

Alerts it exposes: **bullish and bearish structure breaks**, **triple M**, and **model changes**
("if it's an accumulation, you can set an alert for when it turns to distribution").

So the numbered break labels on his charts, the model classification, and triple-M detection are all
**computed by a closed-source TradingView indicator we do not have.** Any implementation here is a
reconstruction of that indicator's logic from its described behaviour, not a port of it.

**"Model" = accumulation / distribution** — Wyckoff-style market phase, which is what the checklists'
"model/structural bias" refers to.

---

## CONFIRMED FROM FRAMES
- Author: **SPENNYFX | 3M TRADING — "PATIENCE | DISCIPLINE | EXECUTION"**
- Platform: **TradingView Replay** (replay backtesting, not live trades)
- Instruments: **NAS100, GBPUSD, BTCUSDT**; watchlist also US30, SPX500, XAUUSD, XAGUSD, COPPER,
  NGAS, ETHUSD, SOLUSD. **Not a BTC-specific system.**
- Break counts are **numbered labels** — green for up-breaks, red for down-breaks, **resetting when
  direction flips**.
- Supply/demand zones drawn as **rectangles extending right from a base**.
- Three moving averages plus an **ATR value** displayed.
- Workflow: colour-code the watchlist (green = valid long, red = valid short, blue = still setting
  up), set alerts for everything, use two monitors.

---

## HOW THIS WAS OBTAINED
**Audio → text:** `transcribe.py` extracts audio with the ffmpeg binary bundled in `imageio_ffmpeg`,
then runs **faster-whisper** (`small`, int8, CPU) locally. All ten videos — 4.2 hours — transcribed in
about 13 minutes. Nothing is uploaded anywhere.

**Video → images:** OpenCV seeks to a frame, resizes, writes a JPEG, and the image is read directly.
Recovers anything shown but not spoken — chart state, drawn zones, indicator settings, title cards.

Both are reproducible: rerun `transcribe.py <folder>` on any new material.
