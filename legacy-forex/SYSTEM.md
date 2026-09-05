# LEGACY FOREX TRADER — system notes, decoded from the course videos

> Research notes for backtesting. Not trade recommendations.

**Source:** `C:\Users\ecarr\OneDrive\Desktop\Legacy Forex Trader` — 19 videos, transcribed locally
with faster-whisper (`legacy-forex/transcribe.py`). Nothing left the machine. Every quote below is
verbatim from the audio, with its timestamp.

**This is a fourth, separate workstream.** It shares no base, board or ratchet history with the
invented BTC lab, War Formation or 3M Elite, and imports no construction from them.

---

## ⚠️ THE INSTRUMENT RULE — SETTLED, AND IT IS NARROWER THAN "NAS100/US30 ETC"

From `3._WHAT_TO_TRADE`, stated four separate times in 113 seconds:

> [00:05] "The good news is that there's only two. The bad news is that there's only two."
> [00:10] "If **NQ**, which is one of them, isn't trading so good, the volume's not great, market
> structure doesn't look great, we move on to **YM**."
> [00:22] "If YM is also not looking great, we move on to **trading nothing for that day**."
> [00:29] "If you don't trade NQ or YM, **we don't go looking for something else**. If those two
> aren't looking good, you're done for the day."
> [01:45] "**NQ and YM is the only thing we trade. We trade nothing else.**"

**So the universe is exactly two instruments: NQ (Nasdaq-100 futures) and YM (Dow futures).** Not
forex, despite the course's name. Not SPX500, not GER40, not any pair the engine happens to offer.

He also states an explicit **no-trade rule**, which is a rule in its own right and must be modelled,
not dropped: if neither instrument qualifies on volume and market structure, the correct action for
that day is **no position at all**. A backtest that always finds a trade is not running his system.

### The selection criteria he names for "looking good"
`volume` and `market structure` — both have dedicated videos (`9._VOLUME`,
`6._PRICE_ACTION_AND_MARKET_STRUCTURE`). Those define the day filter and are being decoded next.

---

## ⚠️ DATA CAVEAT — NQ/YM ARE FUTURES; THE ENGINE HAS THE CASH INDICES

This must be stated before any backtest is run, because getting it wrong is exactly the failure that
killed this universe once already.

`STRATEGY-LEDGER.md`'s archived note records that the **old** trader.dev engine silently remapped
`NQ` to `IONQUSDT` and `YM` to `DYMUSDT` — crypto perpetuals — and would have returned genuine
metrics for entirely the wrong instrument. **Any build here must verify symbol resolution before
trusting a single number.**

On `backtest-lab`, `list_pairs(source="yahoo")` offers `NAS100 -> ^NDX` and `US30`. These are the
**cash indices underlying** NQ and YM, not the futures contracts themselves. They are close but not
identical:

| | NQ / YM (what he trades) | NAS100 / US30 (what the engine has) |
|---|---|---|
| Instrument | futures contract | cash index |
| Session | nearly 23h, Globex | cash-hours only |
| Overnight | trades through | gaps |
| Contract roll | quarterly, price discontinuity | none |
| Tick/contract value | $5 (NQ) / $5 (YM) per point, minis | index points, no contract size |

**Consequence:** his session rules (`8._SESSIONS_TO_TRADE`) and his tick/contract sizing
(`4._WHAT_ARE_CONTRACTS_AND_TICKS`, `11._STOP_LOSS_ADJUSTMENT`) are futures-specific and will not
map cleanly onto cash-index bars. Where they cannot be modelled honestly, that must be **recorded as
a declared deviation**, not silently approximated. Yahoo's intraday caps (1h ≈ 2 years, 5m–30m ≈ 60
days, no usable 15m history) bind here too.

---

## DECODING STATUS

| Video | Transcribed | Decoded into rules |
|---|---|---|
| `3._WHAT_TO_TRADE` | ✔ | ✔ — instrument rule above |
| `4._WHAT_ARE_CONTRACTS_AND_TICKS` | ✔ | pending |
| `10._USING_DATA` | ✔ | pending |
| `11._STOP_LOSS_ADJUSTMENT` | ✔ | pending |
| `5._ANALYZING_TIME_FRAMES` | in progress | — |
| `6._PRICE_ACTION_AND_MARKET_STRUCTURE` | in progress | — |
| `7._SUPPORT_AND_RESISTANCE` | in progress | — |
| `8._SESSIONS_TO_TRADE` | in progress | — |
| `9._VOLUME` | in progress | — |
| 9 × `videoNNNNNNN` | in progress | — |

Nothing is backtested yet and no Pine exists yet. **No number will be written to this file that did
not come from a real recorded runId.**

## QUEUE

1. Finish transcription, then decode the five method videos (time frames, market structure, S/R,
   sessions, volume) into a mechanical specification before writing any Pine.
2. **Verify symbol resolution on the engine first** — `plan_backtest_window` on NAS100 and US30 —
   and record the applied symbol, exactly as the archived ledger note demands.
3. Model the **no-trade day** explicitly. A system that must sometimes decline to trade cannot be
   evaluated on trade count alone.
4. Decide and record how the futures/cash mismatch is handled, as a declared deviation.
