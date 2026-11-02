# Design and validity boundaries

CandleAudit checks **observed input metadata** with deterministic rules. It never guesses whether a reported strategy is profitable.

## Threat model

1. **Time series corruption:** duplicate or missing OHLCV records, impossible candle ranges, non-finite values, inconsistent timestamps.
2. **Temporal leakage:** datasets whose declared feature availability is after decision time, or trade logs that place the entry before next candle open under an explicit next-bar convention.
3. **Presentation risk:** closed-PnL drawdown being mislabeled as mark-to-market drawdown.

## Explicit assumptions

- Candle timestamp is the UTC **open** of the candle. Expected spacing is uninterrupted and fixed at the specified interval. Calendar market sessions and exchange downtime are not exempted.
- The `features` check trusts supplied `available_at` metadata. Independent computation graph provenance is out of scope.
- The `trades` check expects entries at the next candle open after the signal candle open. It does **not** establish that a decision occurred after signal-candle close; that is a separate responsibility.
- A fill can differ from the reference candle open due to slippage. A >10 bps difference is a **warning**, not automatic invalidation.
- Fees are assumed symmetric bps applied to both the entry and exit notional. Trade quantity is units of the underlying asset. No rounding rules for exchange-specific lot sizes are used.
- Realized PnL is added by exit timestamp. This is a diagnostic only, not a capital-feasible portfolio equity curve. It can include logically incompatible overlapping positions; no exposure/risk cap is simulated.

## Reproducibility

- No network I/O or environment secrets are required.
- Python built-in `decimal.Decimal` is used for prices, volume and trade PnL.
- JSON is machine readable and errors have stable short codes.
- Synthetic datasets are redistributable and contain no third-party market data.

## Security and privacy

Never commit credentials, exact exchange account statements, unlicensed datasets, research source files, or production strategy implementations. The `.gitignore` is a convenience, not a complete prevention system. Always review a `git diff --cached` before publishing.
