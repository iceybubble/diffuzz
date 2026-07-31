# tests/unit/test_modules.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from modules.sqli import SQLiModule

@pytest.fixture
def mock_engine():
    engine = MagicMock()
    # Simulate a MySQL error response for the injected payload
    engine.send = AsyncMock(return_value=MagicMock(
        status=500,
        body="You have an error in your SQL syntax near '''' at line 1",
        elapsed=0.4,
    ))
    return engine

async def test_sqli_detects_error_based(mock_engine):
    module = SQLiModule(engine=mock_engine)
    findings = await module.run(
        base_url="http://test.local",
        params={"id": "1"},
    )
    assert len(findings) == 1
    assert findings[0].vuln_type == "sqli"
    assert findings[0].param == "id"
    assert "syntax" in findings[0].evidence.lower()

async def test_sqli_no_false_positive_on_normal_response(mock_engine):
    mock_engine.send = AsyncMock(return_value=MagicMock(
        status=200,
        body="<html><body>Welcome back, user!</body></html>",
        elapsed=0.3,
    ))
    module = SQLiModule(engine=mock_engine)
    findings = await module.run(base_url="http://test.local", params={"id": "1"})
    assert findings == []