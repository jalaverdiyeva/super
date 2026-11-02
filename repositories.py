import json
import os
import requests

class FlightRepository:
    def __init__(self, filepath="flights.json", api_url=None):
        self.filepath = filepath
        self.api_url = api_url
        self.flights = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def search(self, destination=None, origin=None, date=None):
        if self.api_url:
            try:
                params = {"origin": origin, "destination": destination, "date": date}
                response = requests.get(f"{self.api_url}/flights", params=params, timeout=3)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass

        results = self.flights
        if origin:
            results = [f for f in results if f["origin"]["city"].lower() == origin.lower() or f["origin"]["code"].lower() == origin.lower()]
        if destination:
            results = [f for f in results if f["destination"]["city"].lower() == destination.lower() or f["destination"]["code"].lower() == destination.lower()]
        if date:
            results = [f for f in results if f["departure_local"].startswith(date)]
        return results


class ProductRepository:
    def __init__(self, filepath="products.json", api_url=None):
        self.filepath = filepath
        self.api_url = api_url
        self.products = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def search(self, query=None, category=None):
        if self.api_url:
            try:
                params = {"q": query, "category": category}
                response = requests.get(f"{self.api_url}/products", params=params, timeout=3)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass

        results = self.products
        if category:
            results = [p for p in results if p.get("category", "").lower() == category.lower()]
        if query:
            q = query.lower()
            filtered = []
            for p in results:
                name_az = p.get("name", {}).get("az", "").lower()
                name_en = p.get("name", {}).get("en", "").lower()
                name_ru = p.get("name", {}).get("ru", "").lower()
                desc = p.get("description", "").lower()
                brand = p.get("brand", "").lower()

                if q in name_az or q in name_en or q in name_ru or q in desc or q in brand:
                    filtered.append(p)
            results = filtered
        return results


class CinemaRepository:
    def __init__(self, movies_path="movies.json", showtimes_path="showtimes.json", cinemas_path="cinemas.json", api_url=None):
        self.movies = self._load_json(movies_path)
        self.showtimes = self._load_json(showtimes_path)
        self.cinemas = self._load_json(cinemas_path)
        self.api_url = api_url

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def search_movies(self, genre=None, query=None):
        if self.api_url:
            try:
                response = requests.get(f"{self.api_url}/movies", params={"genre": genre, "query": query}, timeout=3)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass

        results = self.movies
        if genre:
            results = [m for m in results if genre.lower() in [g.lower() for g in m.get("genre", [])]]
        if query:
            q = query.lower()
            results = [m for m in results if q in m.get("title", "").lower() or q in m.get("synopsis", "").lower()]
        return results

    def get_showtimes_for_movie(self, movie_id, date=None):
        if self.api_url:
            try:
                response = requests.get(f"{self.api_url}/showtimes", params={"movie_id": movie_id, "date": date}, timeout=3)
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass

        st_list = [s for s in self.showtimes if s.get("movie_id") == movie_id]
        if date:
            st_list = [s for s in st_list if s.get("date") == date]
        return st_list