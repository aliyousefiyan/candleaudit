# Maintenance and release policy

CandleAudit is a small community-oriented educational project. Contributions are reviewed on a best-effort basis. No uptime, support, response-time or compatibility guarantee is offered.

## Triage

- Bugs must include CLI invocation, Python version, expected result, actual result and a minimal **synthetic** CSV when possible.
- Label findings by effect: input integrity, feature time leakage, trade timing, documentation or CI.
- First assess whether a report exposes private or commercially sensitive information. If so, follow [SECURITY.md](../SECURITY.md) and do **not** publish the data.
- Requests for live trading connectors, strategy recommendations or proprietary source code are out of scope.

## PR review gates

1. Every behavior change has a deterministic test and a documented input contract.
2. CI passes on configured supported Python versions.
3. Review the effect on severity levels, codes, JSON keys, numerical interpretation and CLI exit codes.
4. Prefer additive compatible changes; document breaking changes before merging.
5. Do not publish downloaded real-world trading data or identify users in example fixtures.

## Versions and release checklist

The package currently reports version **0.2.0**. A GitHub tag or release should only be created after verifying the exact commit, CI result and package version. The tag and the public release are separate actions; neither should be claimed before it exists.

For a future release:
1. Update CHANGELOG and `pyproject.toml` as necessary.
2. Run unit tests and CLI smoke checks in a clean environment.
3. Verify that no keys, credentials, private algorithms or restricted datasets are present.
4. Create an immutable release tag matching the package version.
5. Publish accurate notes describing tested features and important limitations.
6. Capture links to tag, release and CI run. Do not claim PyPI publication unless it really happened.

## Community metrics

Only count verifiable, organic issues, external PRs, downloads or published dependent projects. GitHub stars are not a quality guarantee. Never create fake accounts, reciprocal engagements or inflated adoption statistics. Actual public use has not yet been established.
