# Five-minute walkthrough

1. Install: `python -m pip install -e .` from a cloned checkout.
2. Inspect `examples/candles_clean.csv` to see the exact required columns.
3. Run `candleaudit candles examples/candles_clean.csv --interval 4h` (expected exit 0).
4. Run `candleaudit candles examples/candles_bad.csv --interval 4h` (expected exit 1 with issue codes).
5. Run `candleaudit features examples/features_bad.csv` (expected exit 1 for declared future feature).
6. Run `candleaudit trades examples/trades_clean.csv --candles examples/candles_clean.csv` (example exit 0).
7. Export any report with `--output audit.json` for CI or review.

The example CSV files are synthetic. On **real** datasets, timestamp must mean **candle open**, use timezone-aware UTC, and supply the correct interval. Execute `candles` before `trades`; malformed OHLCV may not be caught when `trades` only looks up candle open prices.

**Important:** The diagnostics do not establish the causality of arbitrary code, or that any backtest's position sizing, execution, drawdown or performance is realistic. No API calls, account access or live trading are performed.
