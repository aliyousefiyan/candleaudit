"""Causality-oriented checks for candle data, feature timestamps and trade fills.

All checks are deterministic and use only Python's standard library.
"""
from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable

UTC = timezone.utc
REQUIRED_CANDLES = {"timestamp", "symbol", "open", "high", "low", "close", "volume"}
REQUIRED_FEATURES = {"symbol", "feature", "signal_time", "available_at"}
REQUIRED_TRADES = {"symbol", "signal_candle_open", "entry_candle_open", "entry_price", "side", "exit_time", "exit_price", "quantity"}


class InputError(ValueError):
    """Invalid input schema or option."""


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    row: int
    symbol: str
    message: str


@dataclass
class Audit:
    check: str
    rows: int
    issues: list[Issue]
    metrics: dict

    def as_dict(self) -> dict:
        issues = [asdict(i) for i in self.issues]
        return {"check": self.check, "rows": self.rows, "ok": not any(i.severity == "error" for i in self.issues),
                "errors": sum(i.severity == "error" for i in self.issues),
                "warnings": sum(i.severity == "warning" for i in self.issues),
                "issues": issues, "metrics": self.metrics}


def read_csv(path: str | Path, required: set[str]) -> Iterable[tuple[int, dict[str, str]]]:
    try:
        with open(path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, strict=True)
            fields = reader.fieldnames or []
            columns = set(fields)
            if len(fields) != len(columns):
                raise InputError("CSV contains duplicate header names")
            missing = required - columns
            if missing:
                raise InputError("Missing columns: " + ", ".join(sorted(missing)))
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    raise InputError(f"Row {line_number}: unexpected extra CSV columns")
                yield line_number, {k: (v or "").strip() for k, v in row.items()}
    except (OSError, UnicodeError, csv.Error) as exc:
        raise InputError(str(exc)) from exc


def instant(raw: str) -> datetime:
    raw = raw.strip()
    try:
        if raw.isdigit() and len(raw) in (10, 13):
            seconds = int(raw) / (1000 if len(raw) == 13 else 1)
            return datetime.fromtimestamp(seconds, UTC)
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise InputError(f"Naive datetime is not permitted: {raw!r}; include Z or offset")
        return dt.astimezone(UTC)
    except (ValueError, OverflowError) as exc:
        raise InputError(f"Invalid timestamp: {raw!r}") from exc


def number(raw: str, *, positive: bool = False) -> Decimal:
    try:
        result = Decimal(raw)
    except (InvalidOperation, ValueError) as exc:
        raise InputError(f"Invalid decimal value: {raw!r}") from exc
    if not result.is_finite() or (positive and result <= 0):
        raise InputError(f"Invalid non-finite or non-positive decimal: {raw!r}")
    return result


def interval_seconds(value: str) -> int:
    if len(value) < 2 or value[:-1].isdigit() is False or value[-1] not in "mhd":
        raise InputError("Interval must be a positive integer followed by m, h, or d (e.g. 15m, 4h, 1d)")
    n = int(value[:-1])
    if n < 1:
        raise InputError("Interval must be positive")
    return n * {"m": 60, "h": 3600, "d": 86400}[value[-1]]


def audit_candles(path: str | Path, interval: str = "4h") -> Audit:
    step = interval_seconds(interval)
    seen: set[tuple[str, datetime]] = set()
    previous: dict[str, datetime] = {}
    issues: list[Issue] = []
    rows = 0
    symbols: set[str] = set()
    for rowno, row in read_csv(path, REQUIRED_CANDLES):
        rows += 1
        symbol = row["symbol"]
        if not symbol:
            issues.append(Issue("error", "EMPTY_SYMBOL", rowno, "", "Symbol is blank"))
            continue
        symbols.add(symbol)
        try:
            timestamp = instant(row["timestamp"])
            o, h, l, c = (number(row[name], positive=True) for name in ("open", "high", "low", "close"))
            v = number(row["volume"])
        except InputError as exc:
            issues.append(Issue("error", "BAD_VALUE", rowno, symbol, str(exc)))
            continue
        if v < 0:
            issues.append(Issue("error", "NEGATIVE_VOLUME", rowno, symbol, "Volume must be >= 0"))
        if not l <= min(o, c) or not h >= max(o, c) or h < l:
            issues.append(Issue("error", "INVALID_OHLC", rowno, symbol, "OHLC violates low <= open/close <= high"))
        if int(timestamp.timestamp()) % step != 0 or timestamp.microsecond:
            issues.append(Issue("warning", "MISALIGNED_OPEN", rowno, symbol, "Candle open is not aligned to the UTC interval"))
        key = (symbol, timestamp)
        if key in seen:
            issues.append(Issue("error", "DUPLICATE", rowno, symbol, "Duplicate symbol/timestamp"))
        seen.add(key)
        old = previous.get(symbol)
        if old is not None:
            delta = (timestamp - old).total_seconds()
            if delta < 0:
                issues.append(Issue("error", "OUT_OF_ORDER", rowno, symbol, "Candle time decreased relative to previous row for symbol"))
            elif delta > step:
                issues.append(Issue("error", "GAP", rowno, symbol, f"Expected {step}s; observed {delta:g}s gap"))
            if delta > 0 and delta % step:
                issues.append(Issue("error", "IRREGULAR_STEP", rowno, symbol, "Time difference is not an integer number of intervals"))
        previous[symbol] = timestamp
    if rows == 0:
        raise InputError("CSV contains no data rows")
    return Audit("candles", rows, issues, {"symbols": len(symbols), "interval": interval})


def audit_features(path: str | Path) -> Audit:
    issues: list[Issue] = []
    rows = 0
    for rowno, row in read_csv(path, REQUIRED_FEATURES):
        rows += 1
        symbol = row["symbol"]
        if not symbol or not row["feature"]:
            issues.append(Issue("error", "EMPTY_IDENTIFIER", rowno, symbol, "symbol and feature are required"))
        try:
            signal = instant(row["signal_time"])
            available = instant(row["available_at"])
        except InputError as exc:
            issues.append(Issue("error", "BAD_TIMESTAMP", rowno, symbol, str(exc)))
            continue
        if available > signal:
            issues.append(Issue("error", "FUTURE_FEATURE", rowno, symbol, "Feature becomes available after the signal decision"))
    if rows == 0:
        raise InputError("CSV contains no data rows")
    return Audit("features", rows, issues, {"contract": "available_at <= signal_time"})


def audit_trades(path: str | Path, candle_path: str | Path, interval: str = "4h", fee_bps: str = "5", starting_cash: str = "10000") -> Audit:
    """Toy long/short *closed-trade* PnL; NOT an overlapping-position portfolio simulation."""
    step = interval_seconds(interval)
    bps = number(fee_bps)
    capital = number(starting_cash, positive=True)
    if bps < 0:
        raise InputError("fee_bps cannot be negative")
    candles: dict[tuple[str, datetime], Decimal] = {}
    for rowno, row in read_csv(candle_path, REQUIRED_CANDLES):
        try:
            key = (row["symbol"], instant(row["timestamp"]))
            value = number(row["open"], positive=True)
        except InputError as exc:
            raise InputError(f"Candle row {rowno}: {exc}") from exc
        if key in candles:
            raise InputError(f"Duplicate candle key at line {rowno}; audit candles first")
        candles[key] = value
    issues: list[Issue] = []
    rows = 0
    gains: list[tuple[datetime, int, Decimal]] = []
    fees_sum = Decimal(0)
    excluded = 0
    for rowno, row in read_csv(path, REQUIRED_TRADES):
        rows += 1
        symbol = row["symbol"]
        row_invalid = False
        if not symbol:
            issues.append(Issue("error", "EMPTY_SYMBOL", rowno, symbol, "Symbol is blank"))
            excluded += 1
            continue
        try:
            signal = instant(row["signal_candle_open"])
            entry = instant(row["entry_candle_open"])
            exit_time = instant(row["exit_time"])
            price = number(row["entry_price"], positive=True)
            exit_price = number(row["exit_price"], positive=True)
            qty = number(row["quantity"], positive=True)
        except InputError as exc:
            issues.append(Issue("error", "BAD_TRADE_VALUE", rowno, symbol, str(exc)))
            excluded += 1
            continue
        side = row["side"].upper()
        if side not in {"LONG", "SHORT"}:
            issues.append(Issue("error", "BAD_SIDE", rowno, symbol, "side must be LONG or SHORT"))
            excluded += 1
            continue
        if (symbol, signal) not in candles:
            issues.append(Issue("error", "SIGNAL_BAR_MISSING", rowno, symbol, "Signal candle not found in market data"))
            row_invalid = True
        if entry != signal + timedelta(seconds=step):
            issues.append(Issue("error", "ENTRY_NOT_NEXT_BAR", rowno, symbol, "Expected entry on next candle open after signal candle"))
            row_invalid = True
        if exit_time <= entry:
            issues.append(Issue("error", "INVALID_EXIT_TIME", rowno, symbol, "Exit must occur after entry"))
            row_invalid = True
        candle_price = candles.get((symbol, entry))
        if candle_price is None:
            issues.append(Issue("error", "ENTRY_BAR_MISSING", rowno, symbol, "Entry candle not found in market data"))
            row_invalid = True
        elif abs(price - candle_price) > candle_price * Decimal("0.001"):
            issues.append(Issue("warning", "FILL_VS_OPEN", rowno, symbol, "Entry fill differs from next-bar open by > 10 bps; verify slippage"))
        if row_invalid:
            excluded += 1
            continue
        fees = (price + exit_price) * qty * bps / Decimal(10000)
        gross = (exit_price - price) * qty * (1 if side == "LONG" else -1)
        fees_sum += fees
        gains.append((exit_time, rowno, gross - fees))
    if rows == 0:
        raise InputError("CSV contains no data rows")
    # Accounting caveat: closed-trade PnL ordered by exit, NOT an exposure-constrained equity curve.
    equity = capital
    peak = capital
    max_closed_dd = Decimal(0)
    for _, _, pnl in sorted(gains):
        equity += pnl
        peak = max(peak, equity)
        drawdown = (peak - equity) / peak if peak > 0 else Decimal(1)
        max_closed_dd = max(max_closed_dd, drawdown)
    return Audit("trades", rows, issues, {"trades_priced": len(gains), "trades_excluded": excluded, "starting_cash": str(capital),
        "closed_trade_equity": str(equity), "net_pnl": str(equity - capital), "fees": str(fees_sum),
        "max_closed_trade_drawdown_pct": str((max_closed_dd * 100).quantize(Decimal("0.0001"))),
        "warning": "Not mark-to-market drawdown; overlapping positions, funding, liquidation, and constraints NOT modeled"})
