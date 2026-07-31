from engine.http_engine import HttpEngine

async def test_engine_send_request(mock_server):
    engine = HttpEngine(base_url=str(mock_server.make_url("/")))
    resp = await engine.send(url=str(mock_server.make_url("/search")), params={"id": "1"})
    assert resp.status == 200
    assert "Normal response" in resp.body
