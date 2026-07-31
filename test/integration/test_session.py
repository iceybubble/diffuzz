from engine.http_engine import HttpEngine

async def test_ssrf_endpoint_interaction(mock_server):
    engine = HttpEngine(base_url=str(mock_server.make_url("/")))
    resp = await engine.send(url=str(mock_server.make_url("/fetch")), params={"url": "http://example.com"})
    assert resp.status == 200
    assert "Fetching: http://example.com" in resp.body
