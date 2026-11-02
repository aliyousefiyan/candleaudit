# CandleAudit

[![CI](https://github.com/aliyousefiyan/candleaudit/actions/workflows/ci.yml/badge.svg)](https://github.com/aliyousefiyan/candleaudit/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Small, reproducible integrity checks for OHLCV datasets and educational backtests.**

[فارسی](README.fa.md) · [Design and limits](docs/design.md) · [Roadmap](docs/roadmap.md) · [Contributing](CONTRIBUTING.md)

Market-data mistakes and time leakage can silently invalidate a backtest. CandleAudit is a Python standard-library CLI that makes a few common problems visible **before** you trust a performance report.

### What it checks in v0.2.0

| Command | Checks |
| --- | --- |
| `candles` | Missing intervals, duplicated/out-of-order timestamps, inconsistent OHLC, negative volume, invalid timestamps, misaligned UTC candle opens |
| `features` | Recorded `available_at` is not later than `signal_time` (a necessary, not sufficient, anti-look-ahead check) |
| `trades` | Recorded entry is exactly the **next bar open** after the signal candle; entry bar exists; fill/open divergence is surfaced; illustrative fee-aware closed-trade PnL |

This is a **general-purpose tool**. It contains **no private trading strategies, exchange credentials, proprietary trade logs, or production execution code**. All examples are invented synthetic data.

## Quick start

Requires Python 3.10+. From the repository root:

```bash
python -m pip install -e .
candleaudit candles examples/candles_clean.csv --interval 4h
candleaudit candles examples/candles_bad.csv --interval 4h
candleaudit features examples/features_bad.csv
candleaudit trades examples/trades_clean.csv --candles examples/candles_clean.csv --interval 4h --fee-bps 5 --starting-cash 10000
python -m unittest discover -s tests -v
```

No nonstandard runtime packages, exchange accounts, API tokens, or network access required. `candleaudit` prints JSON to stdout and returns exit code `0` for no errors, `1` for detected errors, and `2` for invalid input. Warnings do not change exit code. Use `--output report.json` with any command to save JSON. A trade row with structural errors is **excluded** from illustrative PnL and counted in `trades_excluded`. Warnings do not exclude a row.

### Candle schema

```csv
timestamp,symbol,open,high,low,close,volume
2026-01-01T00:00:00Z,EXAMPLEUSDT,100,105,99,104,1000
```

- `timestamp` = candle **open** timestamp in UTC ISO-8601 with timezone or Unix epoch seconds/milliseconds.
- Candles should be in increasing timestamp order **within each symbol**; interleaving symbols is supported.
- Specify an expected interval such as `1m`, `15m`, `4h`, `1d`. Cryptocurrency-style continuous intervals are assumed; market closures on stocks are not modeled.

### Feature schema

```csv
symbol,feature,signal_time,available_at
EXAMPLEUSDT,indicator_demo,2026-01-01T04:00:00Z,2026-01-01T04:00:00Z
```

`signal_time` is the actual **decision timestamp**, **not** automatically the open time of the signal candle. `available_at` is the timestamp when the feature **actually became usable**. A pass only verifies the stated metadata; it cannot prove the feature computation did not leak future information.

### Trade schema

```csv
symbol,signal_candle_open,entry_candle_open,entry_price,side,exit_time,exit_price,quantity
EXAMPLEUSDT,2026-01-01T00:00:00Z,2026-01-01T04:00:00Z,104,LONG,2026-01-01T11:59:00Z,108,1
```

The strict demo contract is **signal assigned to 4H candle opened at 00:00 → fill at candle open at 04:00**. This alone does not verify when a feature was computed; check `features` separately. Trade PnL is quoted in the price currency using quantity and a fee in basis points **on both entry and exit notionals**. It is deliberately **not** a portfolio simulation.

### What it does *not* promise

- No profitable strategy, trading signals, predictions, live orders, or Binance connectivity.
- No claim that a green audit proves absence of look-ahead bias, survivorship bias, overfitting, or incorrect labels.
- No mark-to-market or floating drawdown. `max_closed_trade_drawdown_pct` is only calculated from exit-ordered realized PnL.
- No modeling of funding rates, liquidation, overlap/capital constraints, margin, spreads or full execution slippage.

See [design and limits](docs/design.md). We welcome reproducible bug reports and small, tested extensions.

## Install directly from GitHub

```bash
python -m pip install "git+https://github.com/aliyousefiyan/candleaudit.git"
candleaudit --help
```

For a development checkout, use `python -m pip install -e .` and then run the test suite. CSV inputs are **untrusted**: review them before processing, and keep raw data backups. `trades` should only be used after `candles` passes for its market-data file. See [example walkthrough](docs/quickstart.md).

## Try CandleAudit and contribute

For a reproducible, two-minute demonstration, see the [hands-on audit guide](docs/practical-audit.md). The tool accepts local CSV files and does not require an exchange account or API key.

New contributors can start with the [contributor walkthrough](docs/community-onboarding.md) and the project's [open issues](https://github.com/aliyousefiyan/candleaudit/issues). Maintainers follow the [maintenance and release policy](docs/maintainer-policy.md). Reports of real-world use are welcome, but please remove account identifiers, trading strategies, credentials, and non-redistributable data.

There is no PyPI package or official GitHub Release yet; the supported installation method is from this GitHub repository. Green audit results are limited to the checks documented above, not a certification of profitability or overall backtest correctness.

## Project status

**v0.2.0: initial educational release candidate.** Public adoption and maintainer activity have **not** been established. GitHub stars, community usage, and eligibility for any maintainer grant must not be assumed.

## License

MIT. See [LICENSE](LICENSE). No exchange affiliation. Not investment advice.
