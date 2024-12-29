from bs4 import BeautifulSoup
from typing import List
from .models import Game

class SteamParser:
    @staticmethod
    def parse(html: str) -> List[Game]:
        soup = BeautifulSoup(html, 'html.parser')
        game_cards = soup.find_all('a', class_='search_result_row')
        results = []

        for item in game_cards:
            title_elem = item.find('span', class_='title')
            title = title_elem.get_text(strip=True) if title_elem else 'No title'

            price_elem = item.find('div', class_='search_price')
            if price_elem:
                price_text = " ".join(price_elem.stripped_strings)
                price = price_text.replace('\n', '').strip()
            else:
                price = 'Free or Unknown'

            rating_elem = item.find('span', class_='search_review_summary')
            rating = rating_elem.get('data-tooltip-html', '') if rating_elem else 'No Reviews'

            developer = 'Unknown'
            dev_elem = item.find('div', {'class': 'search_developer'})
            if dev_elem:
                developer = dev_elem.get_text(strip=True)

            genre_elems = item.find_all('div', class_='search_tags')
            genres = []
            for g in genre_elems:
                texts = g.get_text(separator=',').split(',')
                genres.extend([text.strip() for text in texts if text.strip()])

            date_elem = item.find('div', class_='search_released')
            release_date = date_elem.get_text(strip=True) if date_elem else 'Unknown'

            game = Game(
                title=title,
                price=price,
                rating=rating,
                developer=developer,
                genres=genres,
                release_date=release_date
            )
            results.append(game)

        return results
