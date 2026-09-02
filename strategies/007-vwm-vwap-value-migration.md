# 007 — VWM-1 "VWAP Value Migration"
Universe: BTCUSDT · Timeframes: 15m and 5m
Status: **REJECTED** — ladder rung A, PF 0.89
Family consumed: `session-VWAP band mechanics`

## Idea
VWAP with 2σ bands is the institutional fair-value frame. The literature distinguishes two different
events at a band, and this strategy trades one with each leg rather than mirroring:
- **LONG — accepted value.** Price stretched to +2σ recently (higher value was accepted), then pulls
  back to VWAP and holds above it while VWAP itself is rising. A pullback in an accepted uptrend.
- **SHORT — rejected value.** A wick *through* +2σ that closes back **inside** the bands while VWAP
  is falling. A failed attempt to establish higher value. No pullback involved at all.

## Flip signal (objective B)
`close` crossing VWAP. On a flip, `sinceFlip` resets and no entries fire for 20 bars; after that the
opposite leg is the one that can arm. The crossing of fair value *is* the regime change.

## Pre-run audit (LESSONS 3, 5, 6)
| Leg | Stop | Structural? | R floor | Signal level |
|---|---|---|---|---|
| LONG | 20-bar swing low − 0.25×ATR14 | yes | 0.8% | VWAP — a different object |
| SHORT | 20-bar swing high + 0.25×ATR14 | yes | 0.8% | +2σ band; entry closes back inside it |

Target 2R both sides, fixed at entry. Time stop 96 bars. Legs audited separately.

## Commission gate
Estimated **400–1,200 trades**. **Actual: 564.** First estimate to land inside its range.

## RESULT — 15m, 2022-01-01 → 2026-09-01
| Net | PF | Trades | Win rate | avgWin/avgLoss | Max DD |
|---|---|---|---|---|---|
| −31.7% | **0.89** | 564 | 33.7% | 1.76 | 39.2% |

Leg split — **longs 457 trades (175 winners, 38.3%, −$2,310)**, **shorts 107 (15 winners, 14.0%, −$865)**.
Both legs lose. Commission $4,661 against $26,198 gross profit (18%).

Ladder stopped at rung A. No 5m run.

## What it shows
The payoff geometry was fine again (1.76:1, break-even ~36%) and the long leg came close at 38.3%
before costs — but 564 trades at 18% fee drag turns a marginal edge negative. The short leg at 14%
is the weaker half by far, consistent with every short leg this project has tested.

Notably the pullback-to-VWAP long is the *most* conventional idea tried so far, and it still failed
on this instrument at this cost level. That is informative: on BTC perps at 0.05% per side, textbook
mean-reversion-to-VWAP does not clear its own transaction costs.

## Falsifiable claim
Acceptance and rejection at the 2σ band predict opposite forward moves. At 38.3% (long, acceptance)
versus 14.0% (short, rejection), acceptance is clearly the better half — but neither clears costs, so
the claim is not supported as implemented.
