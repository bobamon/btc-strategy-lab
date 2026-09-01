# 001 — RSB-1 "Relative-Strength Baton"
Universe: US30, NAS100, YM, NQ · Timeframes: 15m and 5m · Session: NY RTH
Status: SPEC — not yet backtested

## Idea in one paragraph
The Dow complex and the Nasdaq complex are the two halves of the US large-cap tape, and their
intraday correlation (~0.80 on YM/NQ, the loosest of the majors) is low enough that they routinely
disagree. That disagreement is information. When one complex breaks its opening range **and the
other confirms**, real index-level flow is behind it — trade with the break. When one breaks out and
the other is going the *other way*, the move is idiosyncratic/rotational and typically retraces —
fade it. One trigger, two opposite responses, selected mechanically by the partner index. This is
the regime flip: the strategy switches between momentum and mean-reversion without a discretionary call.

## Definitions
Evaluate on the working timeframe TF ∈ {15m, 5m}. All times US/Eastern.
- **Session:** 09:30–16:00. **Opening Range (OR):** 09:30–10:00 (two 15m bars, or six 5m bars).
- `ORH`, `ORL` = OR high/low. `ORR = ORH - ORL`. `ORM = (ORH + ORL)/2`.
- `ATR14` = 14-period Average True Range on TF.
- **S** = symbol being traded. **P** = partner symbol from the *other* complex:
  - S ∈ {US30, YM} → P = NAS100 (or NQ, matching S's wrapper)
  - S ∈ {NAS100, NQ} → P = US30 (or YM, matching S's wrapper)
- **Normalized session position** (unit-free, so one rule fits all four symbols):
  `R_X(t) = (Close_X(t) - ORM_X) / ORR_X`
- **Dispersion:** `D(t) = R_S(t) - R_P(t)`
- **Breakout confirmation count** `N`: `N = 1` on 15m, `N = 2` on 5m (two consecutive closes beyond the level).

## Entry — evaluated at bar close only, window 10:00–15:00
**A. CONFIRMED BREAKOUT (momentum)**
- **Long:** last `N` closes of S > `ORH_S` AND `R_P >= +0.25` AND `|D| <= 0.75`
- **Short:** last `N` closes of S < `ORL_S` AND `R_P <= -0.25` AND `|D| <= 0.75`

**B. NON-CONFIRMED BREAKOUT (fade — the flip)**
- **Short:** last `N` closes of S > `ORH_S` AND `R_P < 0` AND `D >= +1.00`
- **Long:**  last `N` closes of S < `ORL_S` AND `R_P > 0` AND `D <= -1.00`

Entry at the open of the next bar, market. If A and B both qualify, take **A** (should be mutually
exclusive by the `|D|` bounds; the precedence rule only removes ambiguity).

## Risk — SL and TP are both fixed at entry. No trailing stop.
`X = max(0.50 * ORR_S, 0.80 * ATR14_S)`   (the risk unit, in price points)

| Trade type | Stop loss | Take profit |
|---|---|---|
| A — confirmed | entry ∓ `X` | entry ± `2.0 * X` |
| B — fade | entry ∓ `X` | entry ± `1.3 * X` |

(∓ / ± read as: long → stop below, target above; short → mirrored.)

**Position exit** — whichever comes first:
1. Stop loss hit, or
2. Take profit hit, or
3. **Time stop:** flat at the close of the last bar ending at or before 15:55.

## Position sizing and portfolio rules
- Risk **0.50%** of account equity per trade. `size = (0.005 * equity) / (X * point_value)`.
- **One position per symbol** at a time.
- **Max 2 entries per symbol per session.**
- No re-entry in the same direction on the same symbol after a loss in that session.
- **Correlation cap (important):** trade **at most one symbol per complex** concurrently — US30 and YM
  are the same bet, as are NAS100 and NQ. Max concurrent risk 1.0% (one Dow-side + one Nasdaq-side).
- No new entries in the 10 minutes surrounding a scheduled high-impact US release (FOMC, CPI, NFP).

## Why this has defined downside
Fixed stop set at entry, fixed target set at entry, hard time stop, capped entries per session,
fixed fractional sizing. No averaging down, no grid, no martingale, no position added to a loser.
Worst case per symbol per session is 2 × 0.50% = 1.0%.

## Backtest instructions for the coding agent
- Data: 15m and 5m OHLCV for all four symbols, RTH-aligned to US/Eastern, ≥3 years.
- The partner series must be **time-aligned bar-for-bar** with S. If a partner bar is missing, skip
  the signal for that bar rather than forward-filling.
- Run each symbol independently (4 symbols × 2 TFs = 8 runs), then a portfolio run honouring the
  correlation cap.
- Report: net return, max drawdown, Sharpe, profit factor, win rate, avg R, trade count,
  and **A-trades vs B-trades broken out separately** — if the fade leg has no edge, the strategy
  collapses to a confirmation-filtered ORB and should be recorded as such in the ledger.
- Costs: model spread + commission per wrapper (CFD spread on US30/NAS100; per-contract commission
  on YM/NQ). This matters — B-trades have a 1.3R target and are cost-sensitive.

## Falsifiable claim
Confirmed breakouts (A) outperform unconditional opening-range breakouts on the same symbols,
and non-confirmed breakouts (B) have negative forward drift over the following 2–8 bars.
If B's edge is nil, the cross-complex filter is only useful as a *filter*, not as a signal flipper.

---
## Platform note (added 2026-09-01)
**EXTERNAL-BACKTEST-ONLY.** trader.dev's Pine codegen forbids `request.security`, so the partner-index
series `R_P` cannot be referenced there. Backtest this in Python (pandas/vectorbt) with both symbol
series loaded and time-aligned, per the instructions above.

**Single-symbol degradation (if you want a trader.dev-runnable cousin):** replace the partner test
`R_P` with the traded symbol's own *internal* breadth proxy — e.g. whether the 5m realized-vol ratio
is expanding or contracting at the break. This is a different mechanism and must be logged as its
own ledger entry, not as a variant of 001.
