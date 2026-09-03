# 3M SYSTEM — vocabulary decoded from the videos

Built from **transcripts** (`transcripts/*.txt`, all 10 videos, ~29,000 words) and from **frames**
read with OpenCV. Quotes are the author's own words.

> Research notes for backtesting. Not trade recommendations.

---

## ✅ TYPE 1 AND TYPE 2 VALIDATION — DECODED
**Type 2 implemented and tested 2026-09-02** (`3m-elite-v2-validation.pine`, see SYSTEM.md queue 0a).
Result: PF 0.64 / maxDD 12.1%, worse than v1's PF 0.91 / maxDD 3.47% on both gates — rejected, v1
stays the best-known config. The loss diagnostic (avgBarsLosing well below avgBarsWinning) pointed at
the stop, not the gate — see queue item 0c.

**The protected low/high stop implemented and tested 2026-09-02** (`3m-elite-v3-protected-stop.pine`,
see SYSTEM.md queue 0c). On validation, the low (longs) / high (shorts) of the validating 48m candle
is captured and held as the stop reference instead of the 3H zone edge. Result: PF 0.65 / maxDD
11.04%, still worse than v1 on both gates — rejected. Marginally better than v2 on every metric, and
the avgBarsLosing/avgBarsWinning ratio improved from 0.52 to 0.64, so this decoded definition was a
real (if insufficient) fix — the stop was part of the v2 problem but not the whole problem.

Type 1 (the 3M candle itself) is still not implemented; its anatomy remains undefined below.

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
**Implemented and tested 2026-09-02** (`3m-elite-v4-zone-invalidation.pine`, built on v3, see
SYSTEM.md queue 0d). Result: PF 0.66 / maxDD 11.11%, worse than v1's PF 0.91 / maxDD 3.47% on both
gates — rejected, v1 stays the best-known config. Effectively identical to v3's numbers (PF
0.65→0.66, maxDD 11.04%→11.11%): the gate fired essentially never in this sample, most likely
because the await window (tap → engulfing validation or bias flip) is usually shorter than a 3H
bar, leaving little room for a fresh 3H close to breach the captured zone bound first. All three
decoded-but-previously-unimplemented gates (this one, Type 2 validation, protected low/high) are
now implemented and tested, individually and stacked, and none rescues the validation-gate
architecture against v1's plain instant-tap cascade.

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
**Implemented and tested 2026-09-02** (`3m-elite-v5-one-candle-rule.pine`, built on v1, see
SYSTEM.md queue 0e). Mechanical reading: a zone is mitigated once two consecutive completed 3H
candles close beyond the same prior edge without a pullback between them. Result: byte-identical
to v1 on every metric — the gate fired zero times in the sample. Diagnosis: v1's zone model has no
persistence across 3H bars (it's just "the most recently completed 3H candle," refreshed every
period), so the two-candle mitigation trigger is structurally near-incompatible with
`zoneBull`/`zoneBear` being true at the same time — the trigger needs a hard continuation move,
which is the opposite of the reversal `zoneBull`/`zoneBear` require. This is a null result caused
by the zone architecture, not evidence the rule itself is inert — SYSTEM.md queue 0g proposes a
retest on a persistent (arm-on-tap) zone.

Source: `2026-08-09 03-24-31.txt` (the whole video).

Governs **when a supply/demand zone counts as mitigated**.
> "Once the zone gets created with the engulfing candle, when you get the next candle tapping into it
> and also making a new high — this is called the one candle rule... **this one candle does not
> mitigate the zone yet.**"
> "So if we get a **second** candle that continues up without being a triple M, and it's not a
> pullback, then that **would** mitigate the zone."

Applies to structural-break zones *and* fractal zones — "this goes for every type of zone".

---

## ✅ CLUSTER AND STAGE ONE — SUPERSEDED, SEE FULL DECODE BELOW
> "A **cluster** is what puts us into **stage one**."
> "The cluster zone is **the deepest zone of any given range** that you're in."
> "This break right here is what creates the cluster, and it's also what puts us into stage one."

This was a partial read of the 156-minute video (`2026-08-09 04-42-54.txt`). **The full video has now
been mined (2026-09-03) — see "STAGE AND CLUSTER — FULLY DECODED" below for the complete cycle,
including stage two, both re-accumulation states, late stage two, and the reset rules.**

---

## ❌ STILL MISSING — and why
| Term | Status |
|---|---|
| **3M candle (triple M)** | **Anatomy never defined in these ten videos.** It is assumed knowledge from an earlier chapter and is detected automatically by their indicator. This is the single most important gap — Type 1 validation *is* this candle. |
| **Swing rule** | **Explicitly deferred by the author**: "you guys are going to learn about the swing rule, **I think next week**". Confirmed absent from this material, twice. |
| **Full stage sequence** | **DECODED 2026-09-03 — see the STAGE AND CLUSTER section below.** Was partially decoded (stage one, stage one re-accumulation only); the 156-minute video (`transcripts/2026-08-09 04-42-54.txt`) has now been fully mined and the complete cycle, cluster definition and reset rules are recorded below. |

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


---

# ⚠️ MAJOR CORRECTION, 2026-09-02 — THE ENGULFING CANDLE *CREATES* THE ZONE
Found by re-reading `transcripts/` after v7 showed the frequency ceiling came from the source-derived
conjunction, not from the lab's added gates. **Every build so far had this backwards.**

## What the source actually says, verbatim
> "Once the zone gets created **with the engulfing candle**"
> "You're looking at **the engulfing candle that made the zone**"
> "you have the engulfing candle that made the zone **and then the one extra candle**"
> "This candle is a wick, this candle **would need to be an engulfing candle for this to be a zone**"
> "this candle **can't be a zone because this candle is not engulfing**"
> "of the zone that **gets created by the engulfing candle**"

## The corrected model
1. **A zone is CREATED by an engulfing candle.** Its geometry is that engulfing candle plus one extra
   candle. A non-engulfing candle cannot form a zone at all.
2. Price later returns to **MITIGATE** the zone. Zones are tracked as mitigated or **unmitigated**,
   and the target is the **"deepest unmitigated zone"**.
3. **THE ONE CANDLE RULE IS ABOUT MITIGATION, NOT VALIDATION** — this entry in this file was
   previously mis-scoped:
   > "this one candle does not mitigate the zone yet ... We would need a second one ... the second
   > one is what makes the zone mitigated"
4. **Validation happens INSIDE the zone and is a separate event:** "need to get a 3M candle from this
   in the zone on the 15 minute, or an engulfing." That is Type 1 or Type 2, occurring within a zone
   that already exists.
5. Zones come in kinds: **S&D zones**, **fractal zones**, and zones from **structural breaks**. The
   rules are stated to apply to all of them.

## Why this matters more than any parameter
The builds so far defined a zone as **the previous 12H candle's high or low** and used the engulfing
candle as the *validation* of a tap on it. That made the engulf and the tap two unrelated events
required to coincide, which is precisely why v2 and v4 returned zero trades and why v6 and v7 were
stuck at exactly ten. **In the real model the engulf and the zone are the same event**, separated in
time from the mitigation that follows. The scarcity was an artefact of my specification, not of the
system.


## ZONE GEOMETRY — CORRECTED AGAIN, 2026-09-02 (v10)
The engulfing candle **creates** the zone, but the zone is **not the whole candle**. It is the BASE
the impulse left behind:

- **Demand zone** = [low, open] of the bullish engulfing candle — the region price accelerated up from.
- **Supply zone** = [open, high] of the bearish engulfing candle.

Using the candle's full high-to-low range puts the zone's proximal edge at the impulse extreme, so
price is inside the zone at the moment of creation and any mitigation rule fires immediately. v9 and
v10 both made exactly 3 trades for this reason, and their identical results are the proof: the zone
died before anything downstream could act on it.


## MITIGATION IS JUDGED ON THE BODY — CONFIRMED BY MEASUREMENT, 2026-09-02 (v13)
A zone is mitigated when a completed candle on the zone's own timeframe **CLOSES inside it**. A candle
that merely wicks through has not mitigated anything. The One Candle Rule then applies to those
closes: the first close inside does not mitigate, the second does.

Measured effect: counting wicks as touches left **15** opportunities in 4.7 years; counting bodies
left **40**. Wick-counting was killing most zones within about eight hours of creation.


## ENGULFING — CORRECTED 2026-09-02 (v19), AND THIS ONE WAS COSTLY
An engulfing candle, for a 24/7 market, is defined by **body containment alone**:

- **Bullish engulf** — the previous candle is bearish, this candle is bullish, and this close is above
  the previous open.
- **Bearish engulf** — the previous candle is bullish, this candle is bearish, and this close is below
  the previous open.

**There is NO gap requirement.** The equities definition also asks that this candle's open be beyond
the previous close, which requires an overnight gap. Crypto trades continuously, so an aggregated
candle's open equals the previous close almost exactly and that clause is never meaningfully true.

**Measured cost of getting this wrong:** the gap-requiring definition produced **10 engulfing candles
in 4.7 years** out of ~9,800 four-hour candles, silently disabling the validation gate in v16, v17 and
v18 — three zero-trade runs and three credits spent chasing the wrong terms.


---

## ENGULFING CANDLE — CORRECTED DEFINITION (v20, measured)

**Bullish engulf** = the previous candle is bearish, this candle is bullish, and this candle's close
is above the previous candle's open. **Bearish engulf** mirrors it. **Body containment only.**

**There is NO gap requirement.** The textbook form also demands this candle's open be below the
previous close, which presumes an overnight gap. Crypto trades 24/7: an aggregated candle's open
equals the previous close to within a tick, so that clause is decided by noise. With it, 10 engulfs
in 4.7 years. Without it, 2,711 — about 28% of all 4H candles.

An engulf **CREATES** a zone; it does not validate one. See [[3m-zone-lifecycle]].


---

## ZONE REPLACEMENT — MOST RECENT, NOT DEEPEST (v23, corrected)

**A new engulfing candle always creates or replaces its zone.** The freshest structure wins.

**The superseded rule** required a replacement demand zone to be *deeper* than the incumbent (and a
supply zone *higher*). It was meant to express "prefer the strongest zone". Mechanised as a monotone
ratchet with no expiry it becomes a **lock**: in a rising market no later engulf is ever deeper, so
the incumbent is never replaced, and if price never returns to close inside it, it never mitigates
either. v22 measured the damage — 2,711 engulfs produced **71** zone creations, and creation stopped
entirely on 2025-10-07.

**Why a human never hits this:** a trader silently retires stale zones. The rule only fails when
written down. See [[3m-zone-lifecycle]] and HARD LESSON 9.


---

## ⚠️ ANCHOR REPRODUCTION FAILED, 2026-09-02 (v31) — READ EVERY DEFINITION ABOVE AS UNVERIFIED PROSE
Every rule on this page (engulf creates the zone, [low, open] geometry, most-recent replacement, body
mitigation with the One Candle Rule, zone freshness) was re-coded in Pine exactly as described and
saved to `pine/3m-elite-v30-zone-freshness.pine`. It did not reproduce v30's recorded numbers — 2,469
trades and PF 0.639 against a recorded 811 trades and PF 0.897. See SYSTEM.md's v31 entry for the
full comparison and the leading hypothesis (an unguarded re-entry storm after a stop-out).

This does not mean the decoded definitions above are wrong — the reconstruction may simply be missing
an implicit guard no transcript ever stated. But until a saved, reproducible build confirms otherwise,
none of the trade counts or profit factors quoted in this file's zone-lifecycle sections should be
treated as verified against real code.

---

## ✅ UPDATE, 2026-09-03 — THE ANCHOR WAS FOUND, AND THE MODEL SURVIVED

v31 (SYSTEM.md) found the missing guard: the reconstruction was checking the entry conjunction on
every 15m bar with no memory of a prior stop-out from the same zone, producing a re-entry storm. A
single `dzTraded` latch (one entry per zone) took the trade count from 2,469 to 734 — a near-match to
v30's recorded 811. **So every definition on this page is essentially confirmed**, not merely
plausible: engulf creates the zone, `[low, open]`/`[open, high]` geometry, most-recent replacement,
body mitigation with the One Candle Rule, and zone freshness all survived contact with a real,
saved, reproducible build.

v32 then found the R floor (LESSON 3, 0.8% of price) was never enforced and bound on 77.5% of trades
— PF 0.889 → 1.225. **v33 split-tested that at 2024-06-08 and both halves cleared PF 1.0** (1.35 and
1.05 — see SYSTEM.md's v33 entry). This is the first validated positive result in the project. No new
vocabulary term was decoded this cycle; Type 1 (the 3M candle's anatomy) and the swing rule remain
undefined, per the table above, and are not currently blocking anything since the working entry uses
Type-2-adjacent (engulf) logic only.

## ✅ UPDATE, 2026-09-03 — SUPPLY ZONE GEOMETRY BUILT AND TESTED, NO EDGE FOUND (v34)

The demand-zone geometry above (`[low, open]` of a bullish engulfing candle, most-recent
replacement, body mitigation with the One Candle Rule) was mirrored on paper — not in code — into
its supply-side counterpart: **supply zone = `[open, high]` of a bearish engulfing 4H candle**, with
its own independent lifecycle state. This is a straight reading of VOCABULARY.md's own "ZONE
GEOMETRY" section applied to the opposite side; nothing new was decoded to build it.

**Built and tested short-only (SYSTEM.md v34): PF 0.73634167, DD 29.25265633%, 256 trades, 13.28%
win rate — rejected.** The definitions themselves are not in question (this is the same model that
produced the validated long leg); what this measures is that the supply side of this instrument's
price action, over 2022–2026, does not reward the same mechanism the demand side does. Long-only
remains this lab's only working leg, now confirmed rather than merely assumed.

## ✅ UPDATE, 2026-09-03 — THE ANCHOR REPRODUCES COLD, AND THE R FLOOR IS FULLY BOUNDED (v36)

No new vocabulary term was decoded this cycle. Two things were confirmed about the existing model
instead (SYSTEM.md's v36 entry has the full numbers): a byte-identical, independently-submitted
re-run of `pine/3m-elite-v32-r-floor.pine` reproduced every recorded metric exactly — the first
headline result in this project (any of the three labs) to pass that check — and the 0.8%-of-price
R floor (LESSON 3) now has both neighbours measured (0.50% and 1.20%), confirming a real interior
optimum rather than an artefact of an untested edge. Type 1 (the 3M candle's anatomy) and the swing
rule remain undefined, per the table above, and still do not block anything since the working entry
uses engulf-based (Type-2-adjacent) logic only.

## ✅ UPDATE, 2026-09-03 — v37 (FRESHNESS maxAge=6) SPLIT-TESTS CLEAN AND IS PROMOTED (v39)

No new vocabulary term was decoded this cycle either. The existing model (engulf creates the zone,
`[low, open]` geometry, most-recent replacement, body mitigation with the One Candle Rule, the 0.8%
R floor, and now a tighter freshness cap of 6 four-hour candles instead of v32's 12) was split-tested
at 2024-06-08 the same way v32 was in v33: byte-identical Pine, only the window changed. Both halves
clear PF 1.0 (H1 1.336 on 96 trades, H2 1.121 on 59 trades, partitioning the full 155-trade sample
exactly) — H2 here is stronger than v32/v33's own H2 (1.054), so this is not a weaker replication of
the same pattern, it is a cleaner one. v37 is now the champion of record (SYSTEM.md's v39 entry has
the full numbers). Type 1 and the swing rule remain undefined and still do not block the working
engulf-based entry.

## ✅ UPDATE, 2026-09-03 — FRESHNESS AXIS CLOSED, FIRST BEAR-REGIME EVIDENCE (v40/v41)

No new vocabulary term was decoded this cycle. Two measurements against the existing model instead
(SYSTEM.md's v40/v41 entry has the full numbers): tightening the freshness cap further, to
`maxAge=3`, reverses both the profit factor and drawdown gains v37 (`maxAge=6`) won over v32
(`maxAge=12`) — confirming 6 is a genuine local optimum on the recency axis, not an unfinished walk.
And a purpose-built isolated bear-market split (2022 calendar year alone, byte-identical v37 source)
clears PF 1.0 on 52 trades — the first regime-specific evidence (as opposed to a time-based half that
blends regimes) either this lab or either sister lab has produced — though its drawdown matches the
full sample's worst exactly, meaning the champion's single worst drawdown occurred inside that bear
year. Type 1 and the swing rule remain undefined and still do not block the working engulf-based
entry.

## ✅ UPDATE, 2026-09-03 — THE BULL-YEAR HALF LANDS, AND dzAge >= 1 IS CONFIRMED LOAD-BEARING (v42/v43)

No new vocabulary term was decoded this cycle either. Two more measurements against the existing
model (SYSTEM.md's v42/v43 entry has the full numbers): the isolated-regime pair is now complete —
2023 (byte-identical v37 source, window narrowed to the calendar year) clears PF 1.62 on 24 trades,
stronger and calmer than both the 2022 bear year (PF 1.17) and the full sample (PF 1.25), completing
the STANDING REQUIREMENT's regime-evidence cell alongside v41. And the binding test finally reached
`dzAge >= 1` (open since v36): removing it from the entry conjunction — allowing a zone to fire on
the same 4H bar it is created, not just on a later one — turns the champion unprofitable (PF 1.25 →
0.96, DD 8.73% → 12.51%, on 44 more trades). HARD LESSON 8's rationale for this term (setup and
trigger must not share a bar) is now confirmed empirically, not just by the mechanism it was written
to prevent. Type 1 and the swing rule remain undefined and still do not block the working engulf-
based entry. `close > dzBot`, the last untested signal term, is unchanged and still open — it is
duplicated in the entry block itself, so testing it needs removal from both places at once.

## ✅ UPDATE, 2026-09-03 — THE LAST SIGNAL TERM IS TESTED: `close > dzBot` IS REDUNDANT, NOT LOAD-BEARING (v44)

No new vocabulary term was decoded this cycle. One measurement against the existing model instead
(SYSTEM.md's v44 entry has the full numbers): `close > dzBot` was removed from both its occurrences in
the champion's source (it appears once inside the entry conjunction and again in the entry guard). The
result was predicted algebraically before running — the R-floor check already in the conjunction
(`close - dzBot >= minR`, with `minR` strictly positive) mathematically guarantees `close > dzBot` on
its own — and the backtest confirmed the prediction exactly: byte-identical PF 1.25172059, DD
8.72815312%, 155 trades. This closes the three-term signal queue opened at v36: the One Candle Rule
mitigation cap (`dzTouch < 2`) has been load-bearing since v13, `dzAge >= 1` is confirmed load-bearing
(v43), and `close > dzBot` is now confirmed redundant (v44) — implied by another term, not independently
doing any work. Type 1 (the 3M candle's anatomy) and the swing rule remain undefined and still do not
block the working engulf-based entry.

---

## ✅ STAGE AND CLUSTER — FULLY DECODED, 2026-09-03 (v45)

Source: `transcripts/2026-08-09 04-42-54.txt`, the 156-minute video, mined in full for the first time
this cycle. Quotes are the author's own words (lightly cleaned of filler).

**This is on the ENTRY timeframe, not the structure/zone/bias timeframes the champion's zone-lifecycle
model uses.** The author is explicit: "the one minute time frame is going to be the only time frame
that we actually pay attention to the stages on... whatever your entry time frame is." For 3M ELITE
that is the 3m entry per SYSTEM.md's shape table. **This decode is new vocabulary, not yet implemented
in any Pine — see SYSTEM.md's v45 entry for the scoping discussion and why a full build was deferred.**

### The cluster — the atomic event

> "The cluster zone is the deepest zone of any given range that you're in."
> "This candle is a wick, this candle would need to be an engulfing candle for this to be a zone."

A cluster requires, in order:
1. A **break up** (a structural break to a new high — the source never gives a mechanical definition
   of "break" beyond this; it is assumed knowledge from an earlier, uncaptured chapter).
2. That break leaves behind the **deepest unmitigated zone in the current range** — same primitive as
   this lab's already-validated demand zone (engulf-created; a non-engulfing candle "can't be a zone").
   **Only breaks UP can leave a cluster zone** — never a breakdown, never a fractal zone: "you can only
   ever get clusters from breaks up... do not draw out fractal zones... as cluster zones."
3. That zone gets **tapped** (touched — the source does not say body-close specifically here, unlike
   the separately-decoded mitigation rule: "all that needs to happen is that the zone gets tapped...
   it doesn't need to hold").
4. **Then** a further break up to a new high. That break is the cluster: "this break right here is what
   creates the cluster."

**A cluster can occur on any break in a sequence** — "the cluster can be on the eighth break up... it
still counts as a stage one beginning" — and if the current range has **zero unmitigated zones to
target** (everything already mitigated), the rule degrades: no zone needs to be drawn, and a plain
pullback followed by the next break up is itself a cluster. There is also a rarer double-break form
(break, break, return to the FIRST break's zone, then deliver) that the author flags as advanced and
does not fully specify.

### The five stages

> "There's gonna be five stages that we are always going to be in at any given time... sometimes we
> are in no stage."

| Stage | Entered when | Entries allowed? |
|---|---|---|
| **No stage** | Price chopping with no cluster yet (e.g. mid-distribution, no bullish break has clustered) | No |
| **Stage 1** | A cluster occurs | **Yes** |
| **Stage 1 re-accumulation** | At least one break down after stage 1, entering a re-accumulation model | **Yes** |
| **Stage 2** | The re-accumulation completes (breaks up again) | **Yes** |
| **Stage 2 re-accumulation** | At least one break down after stage 2 | **Yes** |
| **Late stage 2** | Stage 2 contained a cluster, its re-accumulation delivers, and the system is now waiting for a RESET | **No — never traded** |

> "We always have to be in one of these four stages... in order to actually enter a trade."
> "We never take entries in late stage two ever... because we're waiting for that reset."

**Stages and the model (accumulation/distribution) are independent.** A cluster can start stage 1
while the model is still bearish; a stage-1 entry is only actually taken once the model also agrees:
"we can be in a not valid model but be in a valid stage... we always wait until both of them are valid
to take a trade."

**In stage 2, clusters are not required for entries at all** — "we do not need clusters in stage two at
all, we could just buy stop any breaks in stage two." The cluster requirement is specific to stage 1.

### The cycle-back rule (stage 2 → new stage 1), and why it needs a RESET

Whether a **new** stage 1 can begin immediately after a stage-2 react depends on one binary fact:
**did stage 2 itself contain a cluster?**

- **If stage 2 had NO cluster:** the very next break up (with a new cluster) is immediately a new stage
  1. No reset needed.
- **If stage 2 DID have a cluster:** the system enters **late stage 2** on delivery of that react, and a
  **RESET** is required before a new stage 1 can be recognised. There are exactly two forms of reset:
  1. **The model turns bearish, then bullish again** ("switches to distribution... then we can wait for
     a new cluster"), or
  2. **A full set of breaks up with NO cluster in it, followed by another react** — i.e. an entire
     stage-2-shaped cycle that itself fails to cluster.

> "If stage two does not contain clusters, then the first break up after the stage two react can be a
> new stage one... [but] if stage two does contain clusters, then we need a reset before looking for a
> new stage one."

**One break up in stage 2 followed by an instant break down resets everything to no-stage / distribution**
regardless of clusters — the same "one break the wrong way flips the whole model" rule already used
elsewhere in this project's model-direction logic.

### ✅ UPDATE, 2026-09-03 (v46/v47) — "TAP" IS RESOLVED: A WICK TOUCH, NOT A BODY CLOSE

Queue item 1 from v45 asked whether a cluster "tap" needs a body close (like the separately-decoded
mitigation rule) or a mere wick touch. Re-reading `transcripts/2026-08-09 04-42-54.txt` for this
specific question (rather than the stage-sequence question it was originally mined for) turns up a
direct answer at [35:19]:

> "All that needs to happen is that the zone gets tapped. Okay, the zone doesn't need to hold."

**"Doesn't need to hold" is the tell: a tap is a wick touch.** This is the same word ("hold") the
source uses elsewhere to describe a candle staying closed inside a zone — explicitly saying tap does
NOT require that. This is deliberately weaker than the mitigation rule (which V13 confirmed requires a
BODY close) — the two are different mechanisms measuring different things: mitigation kills a zone,
tap starts a cluster's eligibility. v45's `dzTouch>=1` approximation for "tapped" was actually reusing
the mitigation counter, i.e. measuring body-close touches — the wrong primitive. Fixed at v47 (see
SYSTEM.md's v46/v47 entry): a separate latched `dzTapped` flag, true from the first wick touch
(`low <= dzTop`) while the zone is live, independent of the body-close `dzTouch` counter.

The second ambiguity from v45's queue item 1 (entry-timeframe mapping for the stage/cluster gate) is
NOT resolved by new source material — no transcript states how "whatever your entry timeframe is"
should map onto a 4.7-year 15m-base backtest versus the source's literal 3m entry. It remains a
data-availability convention (15m, per the champion's existing resolution), not a decoded fact.

### Why this matters for this lab specifically

**None of v1 through v44 have ever implemented this gate.** SYSTEM.md's original ENTRY-layer checklist
item ("determine stage — most recent stage 1 / no stage") was flagged as undefined from v1 onward and
every build since has instead pursued a *different* mechanism — the zone-lifecycle model on the
STRUCTURE/ZONE timeframe (4H reconstructed, engulf-creates-zone, mitigation, freshness), which is the
model that produced the validated champion v37. **Stage/cluster is a separate, ENTRY-timeframe gate
layered on top of — not a replacement for — that model.** It has never been measured, tested, or even
attempted, and per this project's own standing instruction ("a decoded definition not yet implemented
outranks other queue items"), it is now the highest-priority open item. See SYSTEM.md's v45 entry for
why a full implementation was deferred rather than rushed this cycle, and for the diagnostic that was
run instead (a first frequency read on an explicitly-approximate reading of "cluster").

### ⚠️ UPDATE, 2026-09-03 (v48/v49) — THE MACHINE WAS BUILT, AND IT LOCKS UP

The 5-state machine decoded above was mechanised for the first time (SYSTEM.md's v48/v49 entry has the
full numbers) and measured before being gated onto the champion, per this lab's own discipline. It
falls into LATE STAGE 2 early and stays there for most of a 4.7-year window rather than cycling through
all five states as the transcript describes. **This is not a correction to the vocabulary decode
itself** — every individual quote and rule above was read faithfully and nothing here contradicts them
— it is a finding about how the individually-correct rules COMPOSE: RESET condition 2 ("a full
cluster-free break-up cycle, then a react") turns out to be far stricter than it reads, because the tap
latch that gates a cluster candidate stays true for as long as any zone is live, making a genuinely
cluster-free cycle rare. Promoted to HARD LESSON 30 in STRATEGY-LEDGER.md. RESET condition 1 (the model
flip) remains unimplemented pending a user-confirmed bias/model definition (the same blocker as the
deferred Type 2 gate, 0-V26) — implementing it is one of the two live paths forward; the other is
re-reading the source for a looser take on RESET condition 2. Neither the swing rule nor the 3M
candle's anatomy were touched this cycle and remain genuinely absent from the transcripts.

### ⚠️ UPDATE, 2026-09-03 (v50) — THE LOOSER-READING RE-CHECK CAME BACK EMPTY

v48/v49's second live path (re-read the source for a looser take on RESET condition 2) was checked
this cycle. `transcripts/2026-08-09 04-42-54.txt` is confirmed as the ONLY transcript file in this
project that mentions "cluster" or "reset" at all (grep across all ten files: 171/25 hits there, zero
everywhere else) — the "last week I taught you guys about clusters" material this video references is
genuinely absent from the captured transcripts, not merely unmined. Re-reading [15:04]-[17:43] finds
the two reset forms stated exactly as already decoded above, with no looser variant on offer: (1) model
flips bearish then bullish again, or (2) a full set of breaks up containing no cluster, then a react.
The "one break up, instant break down" fast path ([11:20]-[11:37]) is a special case of condition 1
(an instant model flip), already the mechanism v48/v49 built for the whipsaw rule — not a third, looser
reading of condition 2. **No genuinely better-supported reading exists in this lab's source material.**
This closes v48/v49's item (a)/(b) choice with a negative finding on (b); the only remaining live path
for the stage machine is (a), a user-confirmed bias/model definition, which per 0-V26 this lab does not
invent on its own.
