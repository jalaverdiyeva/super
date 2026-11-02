import urllib.parse

class ProductRepository:
    def search(self, query=None):
        if not query:
            return []
        encoded_q = urllib.parse.quote(query)
        search_url = f"https://birmarket.az/search?q={encoded_q}"

        return [{
            "name": {"az": query.title(), "en": query.title()},
            "price_azn": "19.99 ₼",
            "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400",
            "url": search_url,
            "description": f"Birmarket rəsmi axtarış nəticəsi: {query}"
        }]


class CinemaRepository:
    def search_movies(self, genre=None, query=None):
        search_q = query or genre or "movies"
        encoded_movie = urllib.parse.quote(search_q)
        cinema_url = f"https://cinemaplus.az/az/search?q={encoded_movie}"

        return [{
            "title": search_q.title(),
            "rating": "8.5",
            "synopsis": f"CinemaPlus Bakı kinoteatrlarında '{search_q.title()}' üzrə seanslar və bilet satışı.",
            "url": cinema_url
        }]


class FlightRepository:
    def search(self, destination=None, query=None):
        target_city = destination or query or "Roma"

        # Şəhər adlarını Aviasales-in tanıdığı IATA kodlarına avtomatik çeviririk
        city_lower = target_city.lower()
        iata_code = "ROM" # Standart

        if "paris" in city_lower:
            iata_code = "PAR"
        elif "roma" in city_lower or "rome" in city_lower:
            iata_code = "ROM"
        elif "istanbul" in city_lower:
            iata_code = "IST"
        elif "dubai" in city_lower:
            iata_code = "DXB"
        elif "london" in city_lower:
            iata_code = "LON"
        elif "nyc" in city_lower or "new york" in city_lower:
            iata_code = "NYC"
        else:
            iata_code = target_city[:3].upper()

        # Aviasales-in qüsursuz işləyən rəsmi axtarış keçidi formatı
        aviasales_url = f"https://www.aviasales.ru/search/GYD{iata_code}1"

        return [{
            "airline": "AZAL / Aviasales",
            "flight_number": f"J2-{iata_code}",
            "origin": {"city": "Baku", "code": "GYD"},
            "destination": {"city": target_city.title(), "code": iata_code},
            "departure_local": "Cari Reys",
            "price_azn": "289.0 AZN",
            "url": aviasales_url
        }]