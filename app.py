import streamlit as st
from repositories import FlightRepository, ProductRepository, CinemaRepository

# Səhifə konfiqurasiyası
st.set_page_config(page_title="bir chat", page_icon="💬", layout="wide")

flight_repo = FlightRepository()
product_repo = ProductRepository()
cinema_repo = CinemaRepository()

# Yan panel (Sidebar)
st.sidebar.title("bir chat")
st.sidebar.markdown("Səyahət, kino və alış-veriş bir çatda")
st.sidebar.markdown("---")
page = st.sidebar.radio("Naviqasiya", ["✨ Yeni çat", "✈️ Travel planning", "🎬 Cinema", "🛍️ Shopping"])

st.title("bir chat 💬")
st.write("Səyahət, kino və alış-veriş bir çatda")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Oturum durumunda son aktif alanı tutalım (Follow-up takibi için)
if "last_domain" not in st.session_state:
    st.session_state.last_domain = None

# Çat tarixçəsini göstərmək
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sualınızı yazın (AZ / RU / EN)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    # Esnek Şehir Algılama (Yazım hataları dahil: isttanbul, istambul, baku vb.)
    detected_city = None
    if any(c in q for c in ["istanbul", "isttanbul", "istambul", "стамбул"]):
        detected_city = "Istanbul"
    elif any(c in q for c in ["baku", "bakı", "баку"]):
        detected_city = "Baku"
    elif any(c in q for c in ["paris", "париж"]):
        detected_city = "Paris"

    # Açar Söz Siyahıları (AZ, RU, EN)
    flight_keywords = [
        "bilet", "flight", "uçuş", "reys", "самолет", "билет", "рейс",
        "fly", "plane", "авиабилет"
    ]

    product_keywords = [
        "iphone", "telefon", "shopping", "məhsul", "qulaqlıq", "headphones", "laptop",
        "телефон", "наушники", "ноутбук", "купить", "товар", "almaq", "birmarket",
        "price", "qiymət", "цена", "store", "shop"
    ]

    cinema_keywords = [
        "film", "cinema", "kino", "seans", "кино", "фильм", "билеты в кино",
        "movie", "showtime", "cinemaplus"
    ]

    with st.chat_message("assistant"):
        # 1. UÇUŞLAR / FLIGHTS (Doğrudan uçuş kelimesi VEYA şehir adı VEYA önceki uçuş takibi)
        is_flight_intent = any(k in q for k in flight_keywords) or (detected_city is not None) or (st.session_state.last_domain == "flights" and not any(k in q for k in product_keywords + cinema_keywords))

        if is_flight_intent:
            st.session_state.last_domain = "flights"
            flights = flight_repo.search(destination=detected_city) if detected_city else flight_repo.search()

            if flights:
                city_label = f" ({detected_city})" if detected_city else ""
                st.markdown(f"✈️ **Tapılan Uçuşlar / Flights{city_label}:**")
                for f in flights[:3]:
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.markdown(f"**{f['airline']}** ({f['flight_number']})\n{f['origin']['city']} ➡️ {f['destination']['city']}\nVaxt: {f['departure_local']}")
                    with cols[1]:
                        st.markdown(f"### {f['price_azn']} AZN")
                        st.button("Al / Buy", key=f"flight_{f['flight_number']}")
                    st.markdown("---")
            else:
                resp_text = f"Üzr istəyirəm, '{detected_city if detected_city else prompt}' istiqamətində uçuş tapılmadı / Uyğun reys mövcud deyil."
                st.markdown(resp_text)
                st.session_state.messages.append({"role": "assistant", "content": resp_text})

        # 2. ALIŞ-VERİŞ / SHOPPING (AZ, RU, EN)
        elif any(k in q for k in product_keywords) or len(product_repo.search(query=q)) > 0:
            st.session_state.last_domain = "shopping"
            products = product_repo.search(query=q)
            if not products:
                products = product_repo.search()

            st.markdown("🛍️ **Tapılan Məhsullar / Товары / Products:**")
            cols = st.columns(min(len(products[:3]), 3))
            for idx, p in enumerate(products[:3]):
                with cols[idx]:
                    name = p["name"].get("az") or p["name"].get("ru") or p["name"].get("en")
                    st.image("https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300", use_container_width=True)
                    st.markdown(f"**{name}**")
                    st.markdown(f"Brend: {p['brand']}")
                    st.markdown(f"### {p['price_azn']} AZN")
                    st.button("View in Birmarket", key=f"prod_{p['id']}_{idx}")

        # 3. KİNO / CINEMA (AZ, RU, EN)
        elif any(k in q for k in cinema_keywords):
            st.session_state.last_domain = "cinema"
            movies = cinema_repo.search_movies()
            st.markdown("🎬 **Kinoteatrda olan filmlər / Фильмы / Movies:**")
            for m in movies[:3]:
                st.markdown(f"**{m['title']}** (Janr: {', '.join(m['genre'])}) - Reytinq: ⭐ {m['rating']}")
                st.markdown(f"*{m['synopsis'][:100]}...*")
                st.button("Seanslar / Showtimes", key=f"mov_{m['id']}")
                st.markdown("---")

        # 4. OUT OF SCOPE / DİGƏR SUALLAR (Dəqiqləşdirmə sualı)
        else:
            default_text = (
                "🤖 Mən Aviasales (uçuşlar), Shopping (alış-veriş) və CinemaPlus (kinolar) üzrə kömək edə bilərəm.\n\n"
                "Zəhmət olmasa axtardığınız mövzunu qeyd edin:\n"
                "- *İstanbula bilet* / *Билет в Стамбул*\n"
                "- *iPhone 15* / *Купить телефон*\n"
                "- *Bu gün kinoda nə var?* / *Что идет в кино?*"
            )
            st.markdown(default_text)
            st.session_state.messages.append({"role": "assistant", "content": default_text})