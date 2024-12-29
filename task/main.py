import asyncio
import aiohttp
import time

from .database import DatabaseHandler
from .page_loader import SteamPageLoader
from .parser import SteamParser

N_QUERIES = 5  
SEARCH_QUERIES = ["strategy", "action", "rpg", "indie", "simulation"]  
K_PAGES = 3  
REQUEST_DELAY = 1 
BASE_URL = "https://store.steampowered.com/search/"

async def fetch_and_save_games(session, db, query: str, page: int):
    async with SteamPageLoader(session, query, page, BASE_URL) as html:
        games = SteamParser.parse(html)

        for game in games:
            await db.insert_game(game)

async def main():
    queries = SEARCH_QUERIES[:N_QUERIES]

    async with aiohttp.ClientSession() as session:
        async with DatabaseHandler(db_path="results.db") as db:
            tasks = []
            for query in queries:
                for page in range(1, K_PAGES + 1):
                    tasks.append(fetch_and_save_games(session, db, query, page))
            
            await asyncio.gather(*tasks)

            time.sleep(REQUEST_DELAY)
    
    print("Парсинг завершён! Данные сохранены в results.db.")

if __name__ == "__main__":
    asyncio.run(main())
