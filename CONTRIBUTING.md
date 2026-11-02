# Contributing

Thanks for considering a contribution. Please keep changes small and reproducible.

1. Open an issue describing the bug/use case, expected behavior and a **synthetic** minimal CSV.
2. Fork the repository, create a branch, and add or update unit tests.
3. Run `python -m unittest discover -s tests -v` and the CLI examples.
4. Submit a pull request explaining any new assumptions, error codes or breaking changes.

Never submit API keys, account data, private strategy rules or restricted datasets. Code is MIT-licensed. Please disclose security issues privately according to SECURITY.md, not in public issues.

## First-time contributors

Start with [community onboarding](docs/community-onboarding.md) and choose an existing issue or open a new one before major changes. Keep each pull request focused on one documented behavior. Please include a synthetic failing example, the expected diagnostic code, and a regression test for any bug fix. Do not open low-value, automated or artificial PRs just to increase project metrics.

## Maintainer review

A maintainer checks reproducibility, data provenance, effects on the public JSON output, CLI exit codes and the regression suite before merging. Refer to [maintenance policy](docs/maintainer-policy.md). Response times are best effort; no service-level guarantee is made.
