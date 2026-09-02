#!/usr/bin/env python3
"""Generate dashboard/dashboard.html from results/backtests.json.

The point of this script is the validation gate. A strategy row can only reach the
dashboard if it carries provenance pointing at a real backtest and a non-zero trade
count. If any record fails, the build aborts and the existing dashboard is left
untouched -- so estimated or invented numbers cannot be published by accident.

Usage:  python build_dashboard.py [--lab btc|war] [--check]
        --lab    which lab to build (default: btc)
        --check  validate only, do not write output
"""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "dashboard" / "template.html"

# Each lab gets its own results file, output page, and identity. Adding a lab is a
# one-line change here -- the validation gate is shared, so no lab can bypass it.
LABS = {
    "btc": {
        "data": ROOT / "results" / "backtests.json",
        "out": ROOT / "dashboard" / "dashboard.html",
        "title": "Strategy Control Panel",
        "subtitle": "Backtested BTCUSDT strategies. Every row is generated from a recorded "
                    "backtest &mdash; nothing here is estimated.",
    },
    "war": {
        "data": ROOT / "war-formation" / "results" / "backtests.json",
        "out": ROOT / "war-formation" / "dashboard" / "war-formation.html",
        "title": "War Formation",
        "subtitle": "The 6h &rarr; 1h &rarr; 15m &rarr; 3m &rarr; 1m cascade on BTCUSDT, tested on the "
                    "1-minute chart. Every row is a recorded backtest &mdash; nothing here is estimated.",
    },
}

STATUSES = {"research", "testing", "passed", "rejected"}
DIRECTIONS = {"long", "short", "both"}
# Bybit USDT linear perpetuals (639-instrument catalog). Validated by shape, not
# an enumerated list, so new pairs do not require a code change.
SYMBOL_RE = re.compile(r"^[A-Z0-9]{2,15}USDT$")
# Timeframes the engine actually serves. 3m has no bars at all.
TIMEFRAMES = {"1m", "5m", "15m", "1h", "4h"}
SOURCES = {"trader.dev", "tradingview", "python"}

TEXT_FIELDS = ["id", "name", "symbol", "timeframe", "direction", "status",
               "createdDate", "lastTestedDate", "description",
               "backtestStart", "backtestEnd"]
METRIC_FIELDS = ["netProfitPct", "profitFactor", "maxDrawdownPct",
                 "totalTrades", "winRatePct", "avgTradePct"]

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def iso_ok(value):
    if not isinstance(value, str) or not ISO.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate(record, index):
    """Return a list of human-readable problems with one record."""
    problems = []
    label = record.get("id") or record.get("name") or "record #%d" % index

    for field in TEXT_FIELDS:
        if not record.get(field):
            problems.append("%s: missing required field '%s'" % (label, field))

    if record.get("status") and record["status"] not in STATUSES:
        problems.append("%s: status '%s' not one of %s"
                        % (label, record["status"], sorted(STATUSES)))
    if record.get("direction") and record["direction"] not in DIRECTIONS:
        problems.append("%s: direction '%s' not one of %s"
                        % (label, record["direction"], sorted(DIRECTIONS)))
    if record.get("symbol") and not SYMBOL_RE.match(record["symbol"]):
        problems.append("%s: symbol '%s' is not a Bybit USDT perp (expected e.g. BTCUSDT)"
                        % (label, record["symbol"]))
    if record.get("timeframe") and record["timeframe"] not in TIMEFRAMES:
        problems.append("%s: timeframe '%s' not one of %s"
                        % (label, record["timeframe"], sorted(TIMEFRAMES)))

    for field in ("createdDate", "lastTestedDate", "backtestStart", "backtestEnd"):
        if record.get(field) and not iso_ok(record[field]):
            problems.append("%s: %s='%s' is not a valid YYYY-MM-DD date"
                            % (label, field, record[field]))

    if iso_ok(record.get("backtestStart", "")) and iso_ok(record.get("backtestEnd", "")):
        if record["backtestStart"] > record["backtestEnd"]:
            problems.append("%s: backtestStart is after backtestEnd" % label)

    # --- metrics -----------------------------------------------------------
    metrics = record.get("metrics")
    if not isinstance(metrics, dict):
        problems.append("%s: missing 'metrics' object" % label)
    else:
        for field in METRIC_FIELDS:
            if field not in metrics:
                problems.append("%s: metrics.%s is missing" % (label, field))
                continue
            value = metrics[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                problems.append("%s: metrics.%s must be a number, got %r"
                                % (label, field, value))
        trades = metrics.get("totalTrades")
        if isinstance(trades, int) and not isinstance(trades, bool) and trades <= 0:
            problems.append("%s: totalTrades is %d -- a run with no trades is not a backtest"
                            % (label, trades))
        pf = metrics.get("profitFactor")
        if isinstance(pf, (int, float)) and not isinstance(pf, bool) and pf < 0:
            problems.append("%s: profitFactor cannot be negative" % label)
        dd = metrics.get("maxDrawdownPct")
        if isinstance(dd, (int, float)) and not isinstance(dd, bool) and dd < 0:
            problems.append("%s: maxDrawdownPct cannot be negative" % label)
        wr = metrics.get("winRatePct")
        if isinstance(wr, (int, float)) and not isinstance(wr, bool) and not 0 <= wr <= 100:
            problems.append("%s: winRatePct %r is outside 0-100" % (label, wr))

    # --- provenance: the anti-invention gate -------------------------------
    prov = record.get("provenance")
    if not isinstance(prov, dict):
        problems.append("%s: missing 'provenance' -- a row without a real backtest "
                        "behind it cannot be published" % label)
    else:
        if prov.get("source") not in SOURCES:
            problems.append("%s: provenance.source must be one of %s"
                            % (label, sorted(SOURCES)))
        if not prov.get("jobId") and not prov.get("backtestUrl"):
            problems.append("%s: provenance needs a jobId or a backtestUrl" % label)
        if not prov.get("verifiedAt"):
            problems.append("%s: provenance.verifiedAt is missing" % label)

    return problems


def main():
    check_only = "--check" in sys.argv

    lab_name = "btc"
    for i, arg in enumerate(sys.argv):
        if arg == "--lab" and i + 1 < len(sys.argv):
            lab_name = sys.argv[i + 1]
    if lab_name not in LABS:
        sys.exit("error: unknown lab '%s'. Known: %s" % (lab_name, ", ".join(sorted(LABS))))
    lab = LABS[lab_name]
    DATA_FILE = lab["data"]
    OUTPUT = lab["out"]

    if not DATA_FILE.exists():
        sys.exit("error: %s not found" % DATA_FILE)
    if not TEMPLATE.exists():
        sys.exit("error: %s not found" % TEMPLATE)

    try:
        records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.exit("error: %s is not valid JSON -- %s" % (DATA_FILE.name, exc))

    if not isinstance(records, list):
        sys.exit("error: %s must contain a JSON array" % DATA_FILE.name)

    problems = []
    for i, record in enumerate(records):
        if not isinstance(record, dict):
            problems.append("record #%d is not an object" % i)
            continue
        problems.extend(validate(record, i))

    ids = [r.get("id") for r in records if isinstance(r, dict) and r.get("id")]
    for dupe in {i for i in ids if ids.count(i) > 1}:
        problems.append("duplicate id '%s'" % dupe)

    if problems:
        print("BUILD REJECTED -- %d problem(s); dashboard not written:\n" % len(problems),
              file=sys.stderr)
        for p in problems:
            print("  - %s" % p, file=sys.stderr)
        print("\nNothing was published. Fix the records in results/backtests.json "
              "and run again.", file=sys.stderr)
        sys.exit(1)

    print("[%s] validated %d record(s) -- all carry backtest provenance"
          % (lab_name, len(records)))
    if check_only:
        return

    built = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__BACKTESTS__*/[]",
                        json.dumps(records, indent=2, ensure_ascii=False))
    html = html.replace("__BUILT__", built)
    html = html.replace("__TITLE__", lab["title"])
    html = html.replace("__SUBTITLE__", lab["subtitle"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print("wrote %s (%d strategies, built %s)" % (OUTPUT.name, len(records), built))


if __name__ == "__main__":
    main()
