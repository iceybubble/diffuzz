# Contributing to Diffuzz

Thanks for your interest in Diffuzz. The project is currently in **active early development** — the architecture is finalized and implementation is just beginning, so this is a great time to help shape core modules.

---

## Ground Rules

1. **Authorized use only.** Diffuzz is an offensive security tool. All contributions must assume the tool will only be used against targets the operator is explicitly authorized to test. Do not add features whose primary purpose is to evade authorization/consent controls (e.g. stripping scope checks).
2. **Architecture before code.** Diffuzz follows a layered design (see `README.md` / `ARCHITECTURE`). New features should fit an existing layer or propose a layer change explicitly, not bolt on ad hoc.
3. **Async-first.** All I/O (HTTP, DNS, OOB callbacks) must be non-blocking and built on `asyncio`/`aiohttp`. Blocking calls in the hot path will be rejected in review.
4. **Typed data.** All findings, configs, and fingerprints flow through `pydantic` v2 models. No loose dicts crossing module boundaries.

---

## Getting Started

### Prerequisites
- Python 3.11+
- [`poetry`](https://python-poetry.org/) for dependency management

### Setup
```bash
git clone https://github.com/<your-org>/diffuzz.git
cd diffuzz
poetry install
poetry shell
```

### Running tests
```bash
pytest
```
Tests run under `pytest-asyncio` with `asyncio_mode = "auto"` — you don't need to mark async tests manually.

### Linting & formatting
```bash
ruff check .
ruff format .
```
CI will reject PRs that fail `ruff check`.

---

## Project Layout

```
diffuzz/
├── cli/                # typer CLI entrypoints, rich dashboard
├── core/
│   ├── parser/         # request parsing, injection point detection
│   ├── payloads/       # payload manager, payload sets
│   ├── engine/         # async fuzzing engine, session manager, proxy layer
│   └── analysis/       # baseline diffing, error signatures, timing oracle
├── modules/             # attack modules: sqli, xss, ssrf, idor, lfi, ssti, ...
├── output/               # report generators, PoC replayer, integrations
├── fingerprints/         # YAML fingerprint/config data
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── docs/
```

> Exact paths may shift slightly as implementation lands — check the current tree before opening a PR that assumes structure.

---

## How to Contribute

### Reporting bugs
Open an issue with:
- Diffuzz version / commit hash
- Python version
- Minimal reproduction (target behavior can be mocked — no need to share real scan targets)
- Expected vs. actual behavior

### Proposing features
Open an issue tagged `enhancement` before submitting a large PR. For new attack modules, include:
- The vulnerability class and why baseline-diffing (rather than a static signature) adds value
- Expected payload set structure
- How false positives will be minimized

### Adding an attack module
Each module should:
1. Live under `modules/<name>/`
2. Expose a common interface (`async def run(target, injection_points, config) -> list[Finding]`)
3. Return `Finding` objects (`pydantic` models) — never raw strings
4. Ship with a payload set under `fingerprints/` or `modules/<name>/payloads.yaml`
5. Include tests using the `parametrize` pattern to cover variants (e.g. all SQL dialects) in a single test function rather than one test per variant

### Writing tests
- Unit tests for pure logic (diffing, parsing, payload generation) — no network calls.
- Integration tests for engine/module interaction — use `aioresponses` or a local mock server, never live targets.
- Fixtures belong in `tests/fixtures/` with realistic (but synthetic) HTTP request/response content.

---

## Pull Request Process

1. Fork and branch from `main` (`feature/<short-description>` or `fix/<short-description>`).
2. Keep PRs scoped to one module/layer where possible.
3. Include tests for new behavior — untested attack modules will not be merged.
4. Update relevant docs (`README.md`, module docstrings) in the same PR.
5. Ensure `ruff check`, `ruff format --check`, and `pytest` all pass locally before opening the PR.
6. Fill in the PR template describing what changed and why.
7. A maintainer will review; expect at least one round of feedback on async correctness and finding-schema consistency.

---

## Code Style

- Follow `ruff`'s default rule set (config lives in `pyproject.toml`).
- Type hints are required on all public functions.
- Prefer composition over inheritance for attack modules — they should be pluggable, not part of a deep class hierarchy.
- Docstrings on all public classes/functions (Google style).

---

## Security Disclosures

If you find a vulnerability *in Diffuzz itself* (not in a target scanned by Diffuzz), please do not open a public issue. Instead, contact the maintainers directly (see `SECURITY.md`, once published) so it can be fixed before disclosure.

---

## Code of Conduct

Be respectful, assume good faith, and keep discussion focused on the technical merits of a change. Harassment or bad-faith reviewing will not be tolerated.