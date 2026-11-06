# ChatGPT plugin — release and review readiness

Project: **CandleAudit 0.2.0**. Current approach: **skills-only**, with bundled, offline-capable deterministic Python CLI. It is a **candidate for local testing and possible submission**, not an OpenAI-verified or publicly approved plugin.

## Build from the public repository

```bash
python -m unittest discover -s tests -v
python scripts/build_chatgpt_plugin.py --smoke
```

The generated ZIP is placed under `dist/`, and must include `plugin.json`, `skills/audit-candles/SKILL.md`, the Python runner plus source, synthetic fixtures, and a generated logo. Build requires Python 3.10+ and no third-party libraries or internet access; the CLI is packaged with the skill. The repo's GitHub Actions [plugin packaging workflow](https://github.com/aliyousefiyan/candleaudit/actions/workflows/plugin-package.yml) checks Python 3.11 and 3.13.

You can unpack the ZIP and run this smoke example from its root:

```bash
python skills/audit-candles/run.py candles skills/audit-candles/runtime/examples/candles_clean.csv --interval 4h
```

**Important:** this is not an MCP-backed integration. The plugin needs a Python-capable execution environment to actually run the bundled code. It cannot promise execution in every ChatGPT surface. If the host cannot access the user's files or execute Python, it must give truthful instructions rather than fabricated results.

## How to submit when ready

1. Verify the developer identity for the publisher in the [OpenAI Platform Dashboard](https://platform.openai.com/).
2. Review the official [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines), [package spec](https://developers.openai.com/plugins/build/plugins), and [submission requirements](https://developers.openai.com/plugins/deploy/submission). Eligibility for public listing of skills-only plugins is subject to OpenAI review.
3. Keep [privacy](../PRIVACY.md), [terms](../TERMS.md), [support](https://github.com/aliyousefiyan/candleaudit/issues), and project description accurate. The packaged URLs resolve through GitHub HTTPS.
4. Upload the generated ZIP in the plugin submission portal; correct any automated validation or safety-scan findings.
5. Run real user prompts in the supported ChatGPT/Codex surfaces. Do **not** claim cross-platform functionality until it is directly tested.
6. Only the verified publisher can complete policy attestations, submit for review, and publish if approved. No repository age, star count or GitHub release guarantees acceptance.

## Positive scenarios to verify

1. Clean four-hour OHLCV file returns no structural errors.
2. Synthetic bad candles flag duplicates and gaps.
3. Recorded feature availability later than decision time is reported.
4. Next-bar trade timing is checked against supplied candle file.
5. Fee-aware illustrative closed-trade PnL is labelled as non-portfolio.

## Negative scenarios to verify

1. User uploads secrets/API keys: refuse to include or publish.
2. User requests a guaranteed-profitable signal: decline.
3. User provides an unsupported market holiday calendar: do not claim calendar-aware gap checking.

## Limitations and submission blockers

- Public directory approval and verified developer status are **not** established.
- These cases are written review plans, not independently verified ChatGPT test outcomes.
- No public HTTPS MCP endpoint or GUI is deployed; those would require separate engineering and security review.
- The current scope is educational; no user brokerage account, trading automation or profitability claim.
- A GitHub Release tag and release notes, if desired, must be explicitly created and checked; a green CI badge is not an official GitHub Release.

For bugs or missing behavior, open a reproducible issue with synthetic data, not private account details.
