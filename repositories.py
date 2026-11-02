import json

class ProductRepository:
    def __init__(self, filepath="products.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            self.products = json.load(f)

    def search(self, query=None):
        if not query:
            return self.products
        q_lower = query.lower()
        matched = []
        for p in self.products:
            name_az = p.get("name", {}).get("az", "").lower()
            name_en = p.get("name", {}).get("en", "").lower()
            name_ru = p.get("name", {}).get("ru", "").lower()
            desc = p.get("description", "").lower()
            category = p.get("category", "").lower()
            brand = p.get("brand", "").lower()

            if q_lower in name_az or q_lower in name_en or q_lower in name_ru or q_lower in desc or q_lower in category or q_lower in brand:
                matched.append(p)
        return matched


class CinemaRepository:
    def __init__(self, movies_path="movies.json", cinemas_path="cinemas.json", showtimes_path="showtimes.json"):
        with open(movies_path, "r", encoding="utf-8") as f:
            self.movies = json.load(f)
        with open(cinemas_path, "r", encoding="utf-8") as f:
            self.cinemas = json.load(f)
        with open(showtimes_path, "r", encoding="utf-8") as f:
            self.showtimes = json.load(f)

    def search_movies(self, genre=None, query=None):
        if not query and not genre:
            return self.movies

        q_lower = (query or "").lower()
        matched = []
        for m in self.movies:
            title = m.get("title", "").lower()
            synopsis = m.get("synopsis", "").lower()
            genres = [g.lower() for g in m.get("genre", [])]

            if q_lower in title or q_lower in synopsis or any(q_lower in g for g in genres) or (genre and genre.lower() in genres):
                matched.append(m)
        return matched


class FlightRepository:
    def __init__(self, filepath="flights.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            self.flights = json.load(f)

    def search(self, destination=None, query=None):
        target = (destination or query or "").lower()
        if not target:
            return self.flights

        matched = []
        for f in self.flights:
            dest_city = f.get("destination", {}).get("city", "").lower()
            dest_code = f.get("destination", {}).get("code", "").lower()
            airline = f.get("airline", "").lower()

            if target in dest_city or target in dest_code or target in airline:
                matched.append(f)
        return matched