import aiosqlite
from .models import Game

class DatabaseHandler:
    def __init__(self, db_path: str = 'results.db'):
        self.db_path = db_path
        self.conn = None

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_path)
        await self.create_table()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

    async def create_table(self):
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price TEXT,
                rating TEXT,
                developer TEXT,
                genres TEXT,
                release_date TEXT
            )
        ''')
        await self.conn.commit()

    async def insert_game(self, game: Game):
        query = '''
            INSERT INTO games (title, price, rating, developer, genres, release_date)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        await self.conn.execute(query, (
            game.title,
            game.price,
            game.rating,
            game.developer,
            ', '.join(game.genres),
            game.release_date
        ))
        await self.conn.commit()
