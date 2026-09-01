# BTC Strategy Lab

Autonomous strategy research for **BTCUSDT** (Bybit USDT linear perpetual) on **15m and 5m**.
One research cycle per hour: invent a mechanism, spec it, code it in Pine v6, backtest it, and
record the real result.

## Read this first
**[STRATEGY-LEDGER.md](STRATEGY-LEDGER.md)** is the memory of this project. It holds the mechanism
registry (what has already been tried, and what it scored), the families still open for exploration,
the platform constraints, and the hard lessons learned from failed cycles. **A cycle that does not
read the ledger will repeat work that has already been rejected.**

## Layout
| Path | What it is |
|---|---|
| `STRATEGY-LEDGER.md` | Mechanism registry, open families, hard lessons, platform constraints |
| `strategies/NNN-*.md` | One spec per strategy — rules, risk, backtest instructions, falsifiable claim |
| `strategies/pine/*.pine` | Pine v6 source, written to the trader.dev engine allowlist |
| `results/backtests.json` | The only data source for the dashboard. Real backtest records only. |
| `results/SCHEMA.md` | Record schema and the provenance requirements |
| `build_dashboard.py` | Generates the dashboard; **rejects any record without backtest provenance** |
| `dashboard/template.html` | Dashboard template (`/*__BACKTESTS__*/` is the data injection point) |
| `dashboard/dashboard.html` | Generated output — published as an Artifact |

## The one rule that matters
**No estimated, projected, or hand-written numbers ever reach the dashboard.** Every metric must be
copied from an actual backtest response. `build_dashboard.py` enforces this: a record without a
`provenance` block naming a real job ID or report URL fails the build, and the build aborts without
writing output rather than publishing partial data.

## Running a cycle
```bash
python build_dashboard.py          # regenerate the dashboard from results/backtests.json
python build_dashboard.py --check  # validate records without writing
```

Then republish `dashboard/dashboard.html` to the existing artifact URL.

## Backtesting
Backtests run through the **trader.dev MCP server**. Key facts, learned the hard way:
- The engine covers **Bybit USDT linear perpetuals only**. Index symbols are either rejected or
  silently remapped to unrelated crypto perps — always call `plan_backtest_window` first.
- The engine **forces** `commission 0.05%`, `percent_of_equity 100`, `margin 100/100`. It overrides
  whatever the spec says about sizing, so a backtest tests the *signal*, not the spec's risk model.
- Commission is the dominant cost at high trade frequency. See HARD LESSON 1 in the ledger.
- Each backtest costs 1 credit against a weekly grant.
