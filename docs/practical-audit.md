# Two-minute reproducible audit

CandleAudit is designed to flag common mistakes in CSV inputs **before** someone treats backtest results as evidence. All examples below are synthetic.

## Install

From a fresh checkout of this repository, with Python 3.10 or newer:

~~~bash
python -m pip install -e .
python -m unittest discover -s tests -v
~~~

If you do not wish to install a CLI command, use `python -m candleaudit` after installing the package.

## 1. Audit clean candles

~~~bash
candleaudit candles examples/candles_clean.csv --interval 4h --output candle-report.json
~~~

Expected: `ok: true`, exit code 0. The JSON file is created in the current directory. It is an output artifact, not an input.

## 2. Surface bad data

~~~bash
candleaudit candles examples/candles_bad.csv --interval 4h
~~~

Expected: `ok: false`, exit code 1, including error codes `GAP`, `INVALID_OHLC` and `DUPLICATE`. A failed audit is intentional in this demonstration.

## 3. Identify a future feature

~~~bash
candleaudit features examples/features_bad.csv
~~~

Expected: `FUTURE_FEATURE` and exit code 1. This detects metadata that says a feature was only available after a decision. A clean report does not prove the feature's computation was causal.

## 4. Check next-bar trades and fees

~~~bash
candleaudit trades examples/trades_clean.csv --candles examples/candles_clean.csv --interval 4h --fee-bps 5 --starting-cash 10000
~~~

For the synthetic fixture, expected: 1 priced trade, 0 excluded trades, `fees: 0.106`, `net_pnl: 3.894`. These are toy realized closed-trade values, not portfolio performance, floating drawdown or a recommendation to trade.

## Using your own CSV files

See the documented schemas in [README](../README.md). Export candles with **UTC open timestamps**, audit candle data first, then feature availability and finally the trade ledger. Resolve critical data errors before considering any PnL output.

- Do not publish private datasets, exchange keys, proprietary rules or trader-identifying metadata.
- No network requests are needed. Data stays on the user's machine.
- Candle gaps assume continuous trading; traditional exchange closure calendars are not supported.
- Exit codes: 0 = no errors; 1 = detected errors; 2 = invalid input. Warnings alone return 0.
- A successful audit is a *necessary narrow check*, not a guarantee of strategy quality.

Want to share a reproducible problem? [Open an issue](https://github.com/aliyousefiyan/candleaudit/issues/new/choose) with a **minimal synthetic fixture** and observed JSON diagnostic.
