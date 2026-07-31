import pytest_asyncio
from aiohttp import web, ClientSession

@pytest_asyncio.fixture
async def mock_server(unused_tcp_port):
    app = web.Application()

    async def sqli_endpoint(request):
        val = request.rel_url.query.get("id", "")
        if "'" in val:
            return web.Response(
                status=500,
                text="You have an error in your SQL syntax near ''' at line 1"
            )
        return web.Response(text="<html>Normal response</html>")

    async def ssrf_endpoint(request):
        url = request.rel_url.query.get("url", "")
        return web.Response(text=f"Fetching: {url}")

    app.router.add_get("/search", sqli_endpoint)
    app.router.add_get("/fetch",  ssrf_endpoint)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", unused_tcp_port)
    await site.start()

    class ServerHelper:
        def make_url(self, path):
            return f"http://127.0.0.1:{unused_tcp_port}{path}"

    yield ServerHelper()

    await runner.cleanup()