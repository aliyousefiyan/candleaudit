---
name: audit-candles
description: Check user-provided historical OHLCV CSV quality, recorded feature availability, and next-bar trade records with the packaged CandleAudit CLI. Use for educational diagnostics and reproducibility, not certification or trading advice.
---

# CandleAudit — evidence-first CSV checks

Use this workflow only for the user's uploaded local CSVs, or the packaged **synthetic** examples. There are no exchange credentials, live trading APIs or third-party data retrieval tools in this skill.

1. Identify whether the request needs `candles`, `features` or `trades`. Review the user's CSV headers and UTC timestamp conventions. Ask for any missing interval or required file; never guess a session calendar.
2. When Python 3.10+ execution and file access are available, call the bundled deterministic script:
   - `python skills/audit-candles/run.py candles "/path/candles.csv" --interval 4h`
   - `python skills/audit-candles/run.py features "/path/features.csv"`
   - `python skills/audit-candles/run.py trades "/path/trades.csv" --candles "/path/candles.csv" --interval 4h --fee-bps 5`
   The CLI code is already bundled in `runtime/src`; no pip download, web access or key is required. Resolve relative paths from the plugin root, not the user's home directory.
3. Treat exit 0 as no detected errors under this limited check, exit 1 as audit findings, and exit 2 as invalid input. Display actual reported counts and diagnostics without pretending an unexecuted check succeeded.
4. State the exact tool scope: candle gaps, duplicates and malformed OHLCV; **recorded** feature timestamps; next-bar trade fills and illustrative fee-aware **closed-trade** PnL. A clean audit does not establish absence of look-ahead or a correct strategy.
5. Return reproducible commands, a summary and clear caveats. If Python or input files are unavailable, give steps without claiming execution.

## Boundaries

Do not process secrets, confidential account data or protected scripts. No live orders, no investment recommendations. UTC 24/7 continuous-candle conventions are assumed; stock exchange holidays are not modeled. Neither funding/margin nor full portfolio drawdown is verified. Never claim OpenAI or ChatGPT endorsement.

Consult `docs/README.md` for CSV formats and `docs/verification.md` for implementation scope. Example files under `runtime/examples` are synthetic.
