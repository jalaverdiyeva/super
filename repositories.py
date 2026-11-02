import json
import os

class FlightRepository:
    def __init__(self, filepath="flights.json"):
        self.filepath = filepath
        self.flights = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def search(self, destination=None, origin=None, date=None):
        results = self.flights
        if origin:
            results = [f for f in results if f["origin"]["city"].lower() == origin.lower() or f["origin"]["code"].lower() == origin.lower()]
        if destination:
            results = [f for f in results if f["destination"]["city"].lower() == destination.lower() or f["destination"]["code"].lower() == destination.lower()]
        if date:
            results = [f for f in results if f["departure_local"].startswith(date)]
        return results


class ProductRepository:
    def __init__(self, filepath="products.json"):
        self.filepath = filepath
        self.products = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def search(self, query=None, category=None):
        results = self.products
        if category:
            results = [p for p in results if p["category"].lower() == category.lower()]
        if query:
            q = query.lower()
            results = [
                p for p in results
                if q in p["name"].get("en", "").lower()
                   or q in p["name"].get("az", "").lower()
                   or q in p["name"].get("ru", "").lower()
                   or q in p["description"].lower()
            ]
        return results


class CinemaRepository:
    def __init__(self, movies_path="movies.json", showtimes_path="showtimes.json", cinemas_path="cinemas.json"):
        self.movies = self._load_json(movies_path)
        self.showtimes = self._load_json(showtimes_path)
        self.cinemas = self._load_json(cinemas_path)

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def search_movies(self, genre=None, query=None):
        results = self.movies
        if genre:
            results = [m for m in results if genre.lower() in [g.lower() for g in m["genre"]]]
        if query:
            q = query.lower()
            results = [m for m in results if q in m["title"].lower() or q in m["synopsis"].lower()]
        return results

    def get_showtimes_for_movie(self, movie_id, date=None):
        st_list = [s for s in self.showtimes if s["movie_id"] == movie_id]
        if date:
            st_list = [s for s in st_list if s["date"] == date]
        return st_list