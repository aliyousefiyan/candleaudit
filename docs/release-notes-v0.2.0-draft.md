# Draft release notes — CandleAudit v0.2.0

> **Draft only.** This file is not a GitHub Release. Do not represent the version as officially released until `v0.2.0` is published and verified.

## Source commit

`0b009aa88efa7bd5cd91eb0bfe2af9066a4b84b3`

This is the initial public source commit where `pyproject.toml` declares version `0.2.0` and the full source/test examples are present. Later documentation and CI updates on `main` are post-version maintenance.

## Highlights

- Local-only standard-library Python CLI for OHLCV time-series integrity checks.
- Duplicate timestamps, missing intervals, out-of-order rows, invalid OHLC and invalid volumes.
- Recorded feature availability versus decision timestamp, to catch known future-data violations.
- Next-candle entry verification against market bars, with illustrative fee-aware realized trade PnL.
- Explicit exclusion of structurally invalid trades from sample PnL calculations.
- Synthetic CSV examples, English/Persian documentation, MIT license and public CI.

## Quality checks

The v0.2.0 source was tested with 23 unit tests, and the initial public GitHub main CI run completed successfully. Verify the exact tagged source before release, rather than relying solely on this draft.

## Installation

~~~bash
python -m pip install "git+https://github.com/aliyousefiyan/candleaudit.git@v0.2.0"
candleaudit --help
~~~

**Use the tag-based install only after that tag actually exists on GitHub.** Before that, use the documented repository installation.

## Important limits

This is an educational integrity checker, **not** a trading system or complete financial backtest engine. A pass does not prove absence of all look-ahead bias or establish performance reliability. No floating drawdown, funding, leverage, portfolio overlap, slippage model or real exchange execution is simulated. No PyPI distribution is claimed.

## Maintainer publication checklist

- [ ] Confirm commit `0b009aa88efa7bd5cd91eb0bfe2af9066a4b84b3` contains exact v0.2.0 source.
- [ ] Re-run tests on the target commit.
- [ ] Create GitHub tag `v0.2.0` pointing to that commit and verify it remotely.
- [ ] Publish a GitHub Release from that tag using the notes above.
- [ ] Confirm release URL and update project status links.
