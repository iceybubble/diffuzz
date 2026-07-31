import aiohttp

class ResponseMock:
    def __init__(self, status: int, body: str, elapsed: float):
        self.status = status
        self.body = body
        self.elapsed = elapsed

class HttpEngine:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def send(self, url: str, params: dict = None) -> ResponseMock:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                text = await resp.text()
                return ResponseMock(status=resp.status, body=text, elapsed=0.1)
