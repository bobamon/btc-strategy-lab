# backtests.json — record schema

`results/backtests.json` is a JSON array. It is the **only** source the dashboard reads.
`build_dashboard.py` refuses to emit any record that fails validation, so the dashboard
can never display estimated, projected, or hand-written numbers.

## Required on every record
| Field | Type | Notes |
|---|---|---|
| `id` | string | stable slug, e.g. `002-vol-term-structure` |
| `name` | string | display name |
| `symbol` | string | `US30` \| `NAS100` \| `YM` \| `NQ` |
| `timeframe` | string | `15m` \| `5m` |
| `direction` | string | `long` \| `short` \| `both` |
| `status` | string | `research` \| `testing` \| `passed` \| `rejected` |
| `createdDate` | string | ISO `YYYY-MM-DD` |
| `lastTestedDate` | string | ISO `YYYY-MM-DD` |
| `description` | string | 1–3 sentence rules summary |
| `backtestStart` | string | ISO date — actual first bar tested |
| `backtestEnd` | string | ISO date — actual last bar tested |
| `metrics` | object | see below — all six required, all numeric |
| `provenance` | object | see below — this is the anti-invention gate |

## `metrics` — all required, all must be real numbers
`netProfitPct`, `profitFactor`, `maxDrawdownPct`, `totalTrades`, `winRatePct`, `avgTradePct`

`totalTrades` must be an integer > 0. A backtest with zero trades is not a backtest.

## `provenance` — a record is rejected without this
| Field | Required | Notes |
|---|---|---|
| `source` | yes | `trader.dev` \| `tradingview` \| `python` |
| `jobId` | one of these two | backtest job id returned by `run_backtest` |
| `backtestUrl` | one of these two | permalink to the full report |
| `verifiedAt` | yes | ISO timestamp when the numbers were read off the real report |

## Optional
| Field | Notes |
|---|---|
| `pineSource` | full Pine v6 source — powers the "Pine script" button |
| `specPath` | path to the markdown spec, e.g. `strategies/001-....md` |
| `notes` | freeform caveats (cost model, warnings from the backtester) |

## Adding a record
1. Run the real backtest.
2. Read the metrics **off the returned report**, never from memory or estimate.
3. Append the record here.
4. `python build_dashboard.py` → regenerates `dashboard/dashboard.html`.
5. Republish that file to the same artifact URL.
