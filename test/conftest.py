import sys
from pathlib import Path

# Add workspace root to sys.path so modules can be imported directly
root_dir = Path(__file__).parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Shared paths
FIXTURES_DIR = Path(__file__).parent / "fixtures"

import pytest

@pytest.fixture
def sample_request_path():
    return FIXTURES_DIR / "sample_request.txt"

@pytest.fixture
def sample_request_text(sample_request_path):
    return sample_request_path.read_text()

@pytest.fixture
def mock_interactsh(monkeypatch):
    """Replaces the live interactsh client with a stub."""
    callbacks = []

    class FakeInteractsh:
        domain = "abc123.oast.fun"
        def poll(self):
            return callbacks

    return callbacks

@pytest.fixture
def tmp_output(tmp_path):
    return tmp_path / "findings.json"