"""Command-line interface for CandleAudit."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import InputError, audit_candles, audit_features, audit_trades


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="candleaudit", description="Auditable OHLCV and backtest integrity checks")
    sub = parser.add_subparsers(dest="command", required=True)
    candles = sub.add_parser("candles", help="Check OHLCV quality and time gaps")
    candles.add_argument("csv")
    candles.add_argument("--interval", default="4h")
    features = sub.add_parser("features", help="Check whether recorded features existed before signal time")
    features.add_argument("csv")
    trades = sub.add_parser("trades", help="Check next-bar execution and illustrative closed-trade PnL")
    trades.add_argument("csv")
    trades.add_argument("--candles", required=True)
    trades.add_argument("--interval", default="4h")
    trades.add_argument("--fee-bps", default="5")
    trades.add_argument("--starting-cash", default="10000")
    for item in (candles, features, trades):
        item.add_argument("--output", help="Optional JSON result file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        if args.command == "candles":
            result = audit_candles(args.csv, args.interval)
        elif args.command == "features":
            result = audit_features(args.csv)
        else:
            result = audit_trades(args.csv, args.candles, args.interval, args.fee_bps, args.starting_cash)
        payload = result.as_dict()
        rendered = json.dumps(payload, indent=2, ensure_ascii=False)
        print(rendered)
        if args.output:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        return 0 if payload["ok"] else 1
    except (InputError, OSError) as exc:
        print(json.dumps({"ok": False, "input_error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
