# Security policy

The CLI parses local CSV files only and intentionally has no network access or trading permissions. Treat untrusted CSV as potentially expensive to process: the current implementation keeps timestamp state in memory and is not intended for multi-billion-row feeds.

Please do not post sensitive credentials or private data in issues. To report vulnerabilities, contact the repository owner using a private GitHub vulnerability report if enabled. Do not claim security response SLAs until a real maintainer process is established.
