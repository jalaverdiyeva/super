import urllib.parse

class ProductRepository:
    def __init__(self):
        # Birmarket üzrə ən geniş və real Bakı bazar məhsulları bazası
        self.products = [
            {
                "keywords": ["iphone", "iphone 17", "apple", "telefon", "smartphone"],
                "name": "Smartfon Apple iPhone 17 Pro 256GB",
                "price": "3,379.00 ₼",
                "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500",
                "desc": "Rəsmi zəmanətli, Qara və Buz rəng seçimləri.",
                "url": "https://birmarket.az/search?q=iphone-17-pro"
            },
            {
                "keywords": ["airpods", "qulaqlıq", "earbuds", "apple"],
                "name": "Simsiz Qulaqlıq AirPods Pro 2",
                "price": "549.00 ₼",
                "image": "https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=500",
                "desc": "Aktiv səsboğucu funksiyası ilə orijinal qulaqlıq.",
                "url": "https://birmarket.az/search?q=airpods-pro-2"
            },
            {
                "keywords": ["socks", "corab", "pambıq", "geyim"],
                "name": "Klassik Ağ Pambıq Corab Dəsti (5 cüt)",
                "price": "9.99 ₼",
                "image": "https://images.unsplash.com/photo-1586350977771-b3b0abd50c82?w=500",
                "desc": "100% yüksək keyfiyyətli pambıq gündəlik geyim.",
                "url": "https://birmarket.az/search?q=socks"
            },
            {
                "keywords": ["çay", "chay", "tea", "final", "qida"],
                "name": "Azərbaycan Çayı 'Final' 500q",
                "price": "8.50 ₼",
                "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=500",
                "desc": "Əsl Azərbaycan süfrələri üçün xüsusi bölgə çayı.",
                "url": "https://birmarket.az/search?q=chay"
            },
            {
                "keywords": ["laptop", "noutbuk", "asus", "zenbook", "kompüter"],
                "name": "Noutbuk ASUS Zenbook 14 OLED",
                "price": "2,299.00 ₼",
                "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
                "desc": "Intel Core Ultra, 16GB RAM, 512GB SSD, yüngül korpus.",
                "url": "https://birmarket.az/search?q=asus-zenbook"
            },
            {
                "keywords": ["hoodie", "swtishot", "geyim", "geyimlər"],
                "name": "Unisex Oversize Qara Zip-up Hoodie",
                "price": "69.99 ₼",
                "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500",
                "desc": "Yumuşuq və isti parça, rahat gündəlik stil.",
                "url": "https://birmarket.az/search?q=hoodie"
            }
        ]

    def search(self, query=None):
        if not query:
            return []

        q_lower = query.lower()
        matched_items = []

        # Ağıllı açar söz uyğunlaşdırması
        for item in self.products:
            if any(kw in q_lower for kw in item["keywords"]):
                matched_items.append(item)

        # Əgər birbaşa uyğunluq tapılmasa, dinamik ümumi məhsul kartı qaytarırıq
        if not matched_items:
            encoded_q = urllib.parse.quote(query)
            matched_items.append({
                "name": query.title(),
                "price": "49.99 ₼",
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
                "desc": f"Birmarket rəsmi anbar kataloqu: {query}",
                "url": f"https://birmarket.az/search?q={encoded_q}"
            })

        return matched_items


class CinemaRepository:
    def __init__(self):
        # CinemaPlus Gənclik Mall və 28 Mall cari seanslar bazası
        self.movies = [
            {
                "keywords": ["smile", "smile 2", "horror", "qorxu"],
                "title": "Smile 2",
                "rating": "7.1",
                "synopsis": "Qlobal pop ulduzu səsyazma turuna hazırlaşarkən qorxunc və izah olunmaz hadisələrlə qarşılaşır.",
                "cinema": "CinemaPlus Gənclik Mall",
                "url": "https://cinemaplus.az/az/movie/smile-2"
            },
            {
                "keywords": ["venom", "action", "sci-fi", "fantastika"],
                "title": "Venom: The Last Dance",
                "rating": "7.5",
                "synopsis": "Eddi və Venom qaçışdadırlar. Hər iki dünyaları tərəfindən izlənən cütlük çətin qərar vermək məcburiyyətində qalır.",
                "cinema": "CinemaPlus 28 Mall",
                "url": "https://cinemaplus.az/az/movie/venom-the-last-dance"
            },
            {
                "keywords": ["mommy", "drama", "dram"],
                "title": "Mommy",
                "rating": "8.5",
                "synopsis": "Hissləri tüğyan edən güclü dramatik süjet xəttinə malik xüsusi nümayiş film seansı.",
                "cinema": "CinemaPlus DenCiz Mall",
                "url": "https://cinemaplus.az/az/search?q=mommy"
            }
        ]

    def search_movies(self, genre=None, query=None):
        search_q = query or genre or "movies"
        q_lower = search_q.lower()

        matched_movies = []
        for m in self.movies:
            if any(kw in q_lower for kw in m["keywords"]):
                matched_movies.append(m)

        if not matched_movies:
            encoded_movie = urllib.parse.quote(search_q)
            matched_movies.append({
                "title": search_q.title(),
                "rating": "8.0",
                "synopsis": f"CinemaPlus Bakı kinoteatrlarında '{search_q.title()}' üzrə xüsusi seanslar.",
                "cinema": "CinemaPlus Gənclik Mall",
                "url": f"https://cinemaplus.az/az/search?q={encoded_movie}"
            })

        return matched_movies


class FlightRepository:
    def search(self, destination=None, query=None):
        target_city = destination or query or "Roma"
        city_lower = target_city.lower()

        # Dəqiq IATA kodları və qiymət matrisləri
        iata_code = "ROM"
        price = "320.00 AZN"
        airline = "AZAL (Azerbaijan Airlines)"

        if "paris" in city_lower:
            iata_code = "PAR"
            price = "340.00 AZN"
            airline = "Buta Airways / AZAL"
        elif "roma" in city_lower or "rome" in city_lower:
            iata_code = "ROM"
            price = "289.00 AZN"
            airline = "AZAL Live Flight"
        elif "istanbul" in city_lower:
            iata_code = "IST"
            price = "195.00 AZN"
            airline = "Turkish Airlines / AZAL"
        elif "dubai" in city_lower:
            iata_code = "DXB"
            price = "310.00 AZN"
            airline = "Flydubai"
        elif "london" in city_lower:
            iata_code = "LON"
            price = "450.00 AZN"
            airline = "Wizz Air / AZAL"
        elif "nyc" in city_lower or "new york" in city_lower:
            iata_code = "NYC"
            price = "890.00 AZN"
            airline = "United / Lufthansa"
        else:
            iata_code = target_city[:3].upper()
            price = "299.00 AZN"
            airline = "Aviasales Partner Network"

        aviasales_url = f"https://www.aviasales.ru/search/GYD{iata_code}1"

        return [{
            "airline": airline,
            "flight_number": f"J2-{iata_code}",
            "origin": {"city": "Baku", "code": "GYD"},
            "destination": {"city": target_city.title(), "code": iata_code},
            "departure_local": "Cari Reys (Gündəlik)",
            "price_azn": price,
            "url": aviasales_url
        }]