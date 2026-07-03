# Diffuzz

**Diff + Fuzz.** A smart async web fuzzer for bug bounty hunting, built around baseline-diffing anomaly detection instead of static pattern matching.

> ⚠️ **Status: Architecture complete, implementation not yet started.** This README documents the designed system prior to code being written.

---

## Why Diffuzz?

Most fuzzers tell you a request happened. Diffuzz tells you whether it *mattered* — by diffing every response against a baseline and surfacing genuine anomalies instead of noise.

| Tool | Smart Diffing | OOB (Blind) Detection | Free & Unthrottled | Programmable API |
|---|---|---|---|---|
| `ffuf` | ❌ | ❌ | ✅ | ⚠️ Limited |
| Burp Intruder | ❌ | ⚠️ Extension-only | ❌ (throttled in Community) | ❌ |
| `wfuzz` | ⚠️ Partial | ❌ | ✅ | ⚠️ Limited |
| `nuclei` | ❌ (static templates) | ⚠️ Template-based | ✅ | ⚠️ Limited |
| **Diffuzz** | ✅ Full baseline diffing | ✅ `interactsh` integration | ✅ | ✅ Python-native |

**Core differentiators:**
- **Baseline diffing** — every response is scored for similarity against a known-good baseline using `difflib.SequenceMatcher`, catching subtle behavioral changes that static signatures miss.
- **Out-of-band detection** — built-in `interactsh` client for confirming blind SSRF and other OOB-only vulnerability classes.
- **Programmable core** — a real Python API, not a templating DSL, for writing custom attack logic.

---

## Architecture

Diffuzz is organized into six layers:

```
┌─────────────────────────────────────────┐
│  UI Layer          — typer CLI + rich dashboard   │
├─────────────────────────────────────────┤
│  Input Processing  — request parser, injection    │
│                      point detector, payload mgr   │
├─────────────────────────────────────────┤
│  Fuzzing Engine    — async aiohttp engine,         │
│                      session manager, proxy layer  │
├─────────────────────────────────────────┤
│  Attack Modules    — SQLi · XSS · SSRF · IDOR ·    │
│                      LFI · SSTI · header injection ·│
│                      open redirect                  │
├─────────────────────────────────────────┤
│  Response Analysis — baseline diffing, error       │
│                      signature DB, timing oracle    │
├─────────────────────────────────────────┤
│  Output            — JSON/Markdown reports, PoC    │
│                      replayer, Burp/Slack integrations│
└─────────────────────────────────────────┘
```

### Layer details

**1. UI**
- `typer`-based CLI for scan configuration and control
- `rich` live dashboard for real-time progress, request rates, and finding counts

**2. Input Processing**
- Request parser (raw HTTP / curl / Burp export ingestion)
- Injection point detector (params, headers, path segments, JSON/XML bodies)
- Payload manager (payload sets per attack module, encoding pipelines)

**3. Fuzzing Engine**
- Fully async, built on `aiohttp` for concurrency at scale
- Session manager (cookies, auth state, rate limiting per target)
- Proxy layer (routing through Burp/upstream proxies for visibility)

**4. Attack Modules**
- SQL Injection
- Cross-Site Scripting (XSS)
- Server-Side Request Forgery (SSRF)
- Insecure Direct Object Reference (IDOR)
- Local File Inclusion (LFI)
- Server-Side Template Injection (SSTI)
- HTTP header injection
- Open redirect

**5. Response Analysis**
- Baseline diffing engine (`difflib.SequenceMatcher`-based similarity scoring)
- Error signature database (known error strings/patterns per stack)
- Timing oracle (statistical timing-based blind detection)

**6. Output**
- Findings reports in JSON and Markdown
- PoC replayer (re-issues the exact request that triggered a finding)
- Burp Suite and Slack integrations

---

## Tech Stack

| Purpose | Library |
|---|---|
| Language / runtime | Python 3.11+ |
| Concurrency | `asyncio` |
| Async HTTP | `aiohttp` (primary), `httpx` (HTTP/2 fallback) |
| DNS | `dnspython` |
| OOB / blind detection | `interactsh-client` |
| Response similarity | `difflib` |
| Data validation | `pydantic` v2 (typed finding schemas) |
| Config / fingerprints | `PyYAML` |
| CLI | `typer` |
| Terminal dashboard | `rich` |
| Testing | `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`) |
| Linting / formatting | `ruff` |
| Dependency management | `poetry` |

---

## Design Principles

- **Diff over signature.** Anomaly detection via response comparison, not brittle string matching.
- **Async-first.** Every network operation is non-blocking to support high-throughput scanning.
- **Typed data model.** All findings pass through `pydantic` schemas — no loose dicts.
- **Test-driven design.** Test suite is architected upfront, including parametrized coverage across SQL dialects and injection contexts in single test functions, to avoid test explosion as attack modules grow.
- **Composable API.** Every layer is usable independently — the diffing engine, the attack modules, and the OOB client can be imported and scripted directly.

---

## Roadmap

- [ ] Core async fuzzing engine + session manager
- [ ] Baseline diffing module
- [ ] Attack modules (starting with SQLi, XSS)
- [ ] `interactsh` OOB integration
- [ ] CLI + `rich` dashboard
- [ ] Reporting (JSON/Markdown) + PoC replayer
- [ ] Burp/Slack integrations

---

## Status

This project is in the **architecture-complete, pre-implementation** phase. Folder structure, data schemas, and the test suite design are finalized. Code implementation begins next.

---

## License

TBD

## Disclaimer

Diffuzz is intended for authorized security testing only (bug bounty programs, pentests with written scope/permission). Do not use against systems you don't have explicit authorization to test.