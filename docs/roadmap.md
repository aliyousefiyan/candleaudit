# Roadmap (proposals, not completed features)

- [x] v0.1: deterministic OHLCV validation
- [x] v0.1: feature availability timestamp check
- [x] v0.1: next-bar entry and toy realized fee/PnL checks
- [ ] v0.2: optional exchange maintenance/gap calendars
- [ ] v0.2: CSV streaming and memory-bounded duplicate checks
- [ ] v0.2: optional strategy signal/feature provenance manifest and tests
- [ ] v0.3: overlapping positions and true mark-to-market equity audit (separately specified and tested)
- [ ] v0.3: cross-asset survivorship/data universe metadata checks
- [ ] v0.3: reproducible sample notebooks using freely redistributable synthetic data

Each new feature needs a minimal failing test, its assumptions, and reproducible documentation. Do not add real or private trading data to examples.
