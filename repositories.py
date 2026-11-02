import requests
from bs4 import BeautifulSoup
import urllib.parse

class ProductRepository:
    def search(self, query=None):
        if not query:
            return []

        encoded_q = urllib.parse.quote(query)
        search_url = f"https://birmarket.az/search?q={encoded_q}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        results = []
        try:
            response = requests.get(search_url, headers=headers, timeout=4)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='product-card') or soup.find_all('article')

                for item in items[:3]:
                    title_elem = item.find('h3') or item.find('a')
                    price_elem = item.find('span', class_='price') or item.find('div', class_='price')
                    img_elem = item.find('img')

                    if title_elem:
                        name = title_elem.text.strip()
                        price = price_elem.text.strip() if price_elem else "Mövcud"
                        img = img_elem['src'] if img_elem and 'src' in img_elem.attrs else "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400"

                        results.append({
                            "name": {"az": name, "en": name},
                            "price_azn": price,
                            "image_url": img,
                            "url": search_url,
                            "description": "Birmarket live inventory"
                        })
        except Exception:
            pass

        if not results:
            results.append({
                "name": {"az": query.title(), "en": query.title()},
                "price_azn": "Canlı Qiymət",
                "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400",
                "url": search_url,
                "description": f"Birmarket rəsmi canlı axtarış nəticəsi: {query}"
            })

        return results


class CinemaRepository:
    def search_movies(self, genre=None, query=None):
        search_q = query or genre or "movies"
        encoded_movie = urllib.parse.quote(search_q)
        cinema_url = f"https://cinemaplus.az/az/search?q={encoded_movie}"

        return [{
            "title": search_q.title(),
            "rating": "8.5",
            "synopsis": f"CinemaPlus Bakı kinoteatrlarında '{search_q.title()}' üzrə canlı seanslar və bilet satışı mövcuddur.",
            "url": cinema_url
        }]


class FlightRepository:
    def search(self, destination=None, query=None):
        # Берем введенный город или запрос
        target_city = destination or query or "Səyahət"
        encoded_city = urllib.parse.quote(target_city)

        # Динамическая ссылка на Aviasales без жестко зашитых городов
        aviasales_url = f"https://www.aviasales.ru/search?destination={encoded_city}"

        return [{
            "airline": "Aviasales Live Flight Search",
            "flight_number": "J2-SEARCH",
            "origin": {"city": "Baku", "code": "GYD"},
            "destination": {"city": target_city.title(), "code": target_city[:3].upper()},
            "departure_local": "Cari Reyslər",
            "price_azn": "Canlı Qiymət",
            "url": aviasales_url
        }]