# Contributor onboarding

We welcome reproducible bug reports, documentation fixes and small Python contributions. This is an early-stage educational tool with no public adoption claims.

## Find a task

1. Read [README](../README.md), [design limits](design.md) and the [hands-on walkthrough](practical-audit.md).
2. Visit the [issue tracker](https://github.com/aliyousefiyan/candleaudit/issues). Look for tasks that describe expected behavior and synthetic fixtures.
3. Comment with your intended approach before starting a larger change. Avoid duplicate work.
4. Fork, create a branch and use a pull request.

## Local setup and test

~~~bash
git clone https://github.com/aliyousefiyan/candleaudit.git
cd candleaudit
python -m pip install -e .
python -m unittest discover -s tests -v
candleaudit candles examples/candles_clean.csv --interval 4h
~~~

Code is Python standard-library-only at runtime. A new validator should use deterministic behavior and avoid requiring live exchange data, network access or personal credentials in tests.

## Definition of done

- A unit test demonstrates the regression or new behavior.
- Inputs, UTC conventions, errors, output fields and limitations are documented.
- The 0/1/2 CLI exit code contract is preserved or its change is clearly identified.
- CI passes; a maintainer reviews and merges.
- Example data is synthetic, safely redistributable and clearly labeled.

## Suggested contribution areas

- Improve public JSON output documentation and backward compatibility examples.
- Add more synthetic multi-symbol and timezone fixtures.
- Add test coverage for malformed CSV inputs and edge timestamps.
- Improve plain-language documentation for non-programmers.

Please do not fabricate stars, downloads, reviews, or contributions. The project is maintained for genuine use, not inflated metrics. See [maintenance policy](maintainer-policy.md).
