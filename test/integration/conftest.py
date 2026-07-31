# tests/integration/conftest.py
import pytest_asyncio
from aiohttp import web

async def vulnerable_app():
    """A tiny aiohttp app with intentionally vulnerable endpoints."""
    app = web.Application()

    async def sqli_endpoint(request):
        val = request.rel_url.query.get("id", "")
        if "'" in val:
            # Simulate a real DB error leaking into the response
            return web.Response(
                status=500,
                text="You have an error in your SQL syntax near ''' at line 1"
            )
        return web.Response(text="<html>Normal response</html>")

    async def ssrf_endpoint(request):
        url = request.rel_url.query.get("url", "")
        # Simulate server making an outbound request (we just echo it back)
        return web.Response(text=f"Fetching: {url}")

    app.router.add_get("/search", sqli_endpoint)
    app.router.add_get("/fetch",  ssrf_endpoint)
    return app

@pytest_asyncio.fixture
async def mock_server(aiohttp_server):
    app = await vulnerable_app()
    server = await aiohttp_server(app)
    return server