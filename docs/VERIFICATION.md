# Reproducible verification and trust boundaries

CandleAudit is a **diagnostic CLI**, not a certification service or a trading strategy. Green output means only that the implemented checks did not flag the submitted rows.

## Verify the public source locally

```bash
git clone https://github.com/aliyousefiyan/candleaudit.git
cd candleaudit
python -m pip install -e .
python -m unittest discover -s tests -v
candleaudit candles examples/candles_clean.csv --interval 4h
candleaudit candles examples/candles_bad.csv --interval 4h
```

The bad candle fixture is supposed to produce diagnostics and a nonzero exit code. CI runs unit and smoke tests on Python 3.11 and 3.13. Compare the exact commit and [CI run](https://github.com/aliyousefiyan/candleaudit/actions) when reporting results; a passing badge on `main` is not independent third-party certification.

## What a reproducible report needs

- Git commit SHA, Python version and exact command or invocation.
- UTC/timeframe and candle open/close timestamp convention.
- Synthetic minimal CSV reproducer, never account credentials or restricted market data.
- Expected result versus actual JSON diagnostics (including exit status).
- Explanation of assumptions, exclusions and any manual steps.

## What this does not validate

- That a strategy's intended meaning was correctly translated into rules.
- That a feature was truly computed without future information merely because its metadata says it was available.
- Realistic fills, liquidity, funding, leverage, overlapping positions or true intrabar portfolio drawdown.
- Trading profitability or production readiness.

For a separate **strategy builder and backtesting engine**, see [CandleBacktest AI](https://github.com/aliyousefiyan/candlebacktest-ai). It currently integrates only CandleAudit's **candle-data** check when explicitly requested; full feature/trade audits are not integrated. The projects have separate scopes and test suites.

## Contributions and release evidence

See [contributing](../CONTRIBUTING.md), [maintenance policy](maintainer-policy.md) and [issues](https://github.com/aliyousefiyan/candleaudit/issues). A GitHub release or package registry artifact must not be claimed before its actual publication. Counts of stars, users or downloads must reflect organic, verifiable activity.
