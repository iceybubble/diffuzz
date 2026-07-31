# tests/integration/test_scan.py
from engine.http_engine import HttpEngine
from modules.sqli import SQLiModule

async def test_full_sqli_scan(mock_server):
    engine = HttpEngine(base_url=str(mock_server.make_url("/")))
    module = SQLiModule(engine=engine)

    findings = await module.run(
        base_url=str(mock_server.make_url("/search")),
        params={"id": "1"},
    )

    assert len(findings) >= 1
    assert findings[0].vuln_type == "sqli"