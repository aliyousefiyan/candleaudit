## Unreleased

- Add practical reproducible audit walkthrough and contributor onboarding instructions.
- Document public maintenance practices, release gates and limits of support.
- Refresh CI setup-python GitHub Action after reviewing the dependency bot's suggested update.

# Changelog

## 0.2.0 — 2026-11-02

- Publishable, installable standalone CLI with GitHub examples and documentation.
- Exclude structurally invalid trades from illustrative realized PnL; report `trades_excluded`.
- Reject empty CSV datasets instead of claiming a clean audit.
- Require signal candle to exist for next-bar trade auditing.
- Add safety regression tests, onboarding guide and issue templates.

## 0.1.0 — 2026-11-02

- Initial private preparation of candle, feature-timestamp and trade-log checks.
