import aiohttp

class SteamPageLoader:
    def __init__(self, session: aiohttp.ClientSession, query: str, page: int, base_url: str):
        self.session = session
        self.query = query
        self.page = page
        self.base_url = base_url
        self.text = None

    async def __aenter__(self):
        params = {
            'term': self.query,
            'page': self.page,
            'snr': '1_7_7_151_7_7' 
        }
        async with self.session.get(self.base_url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Failed to load page {self.page} for query '{self.query}'")
            self.text = await response.text()
        return self.text

