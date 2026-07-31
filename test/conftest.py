import pytest
import pytest_asyncio
from pathlib import Path

# ── shared paths ──────────────────────────────────────────
FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_request_path():
    return FIXTURES_DIR / "sample_request.txt"

@pytest.fixture
def sample_request_text(sample_request_path):
    return sample_request_path.read_text()

# ── mock interactsh ───────────────────────────────────────
@pytest.fixture
def mock_interactsh(monkeypatch):
    """Replaces the live interactsh client with a stub that
    records what domains were polled and simulates a callback."""
    callbacks = []

    class FakeInteractsh:
        domain = "abc123.oast.fun"
        def poll(self):
            return callbacks

    monkeypatch.setattr("diffuzz.modules.ssrf.interactsh_client", FakeInteractsh())
    return callbacks   # test can append to this to simulate OOB hits

# ── temp output dir ───────────────────────────────────────
@pytest.fixture
def tmp_output(tmp_path):
    return tmp_path / "findings.json"