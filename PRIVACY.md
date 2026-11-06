# Privacy policy — candleaudit

Last updated: 2026-11-07

## Scope

This policy describes the **community-maintained, skills-only local/ChatGPT plugin candidate** and the command-line software in this repository. There is currently **no project-operated account system, telemetry collector, trading exchange connection, or hosted MCP endpoint**. This policy does not replace the terms or privacy policy of the platform on which a user runs the software.

## Data processed

The software can process user-provided historical OHLCV CSV files, feature-availability CSVs, and trade-record CSVs and generated educational diagnostic/backtest reports. Please do not submit API keys, passwords, account identifiers, confidential trading records, payment data, or non-redistributable content.

## Purpose

The software processes those files only to run the requested local educational integrity checks or historical simulations and display/save the resulting report. There is no live trading or investment account access.

## Recipients, storage and retention

- **Direct local use:** data is processed on the user's machine. The CLI has no developer-operated collection endpoint. If the user chooses `--output` or saves a report, the file remains where they save it until they delete it.
- **Use through ChatGPT:** uploaded text, files and generated responses are processed by OpenAI under the user's applicable ChatGPT plan and privacy settings. This project does not independently receive copies via an operator-controlled API. Consult [OpenAI's privacy policy](https://openai.com/policies/privacy-policy/) for the platform's retention and controls.
- **GitHub issues and pull requests:** any data voluntarily posted publicly to GitHub is visible to others and processed under [GitHub's privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). Remove personal/private information before posting.

The repository maintainer does not operate a separate file-retention database, send advertising analytics, or sell user data for this skills-only candidate. Any future hosted/MCP service will require an updated policy **before** it collects or receives user data.

## User controls and contact

Users can choose not to upload personal datasets, delete locally saved input/output files, and control ChatGPT uploads through platform settings. For project-specific privacy questions, use [repository discussions or issues](https://github.com/aliyousefiyan/candleaudit/issues) without sharing confidential content; for suspected vulnerabilities, follow [SECURITY.md](SECURITY.md) privately.

This document is about current software behavior, not a claim of independent security audit or official OpenAI approval.
