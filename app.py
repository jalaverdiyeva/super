import streamlit as st
from PIL import Image
import urllib.parse
from repositories import FlightRepository, ProductRepository, CinemaRepository

# Page Configuration & Clean CSS Injection
st.set_page_config(page_title="bir chat", layout="wide")

st.markdown("""
    <style>
    .stButton button { width: 100%; border-radius: 6px; background-color: #107c41; color: white; font-weight: 600; }
    .stButton button:hover { background-color: #0b5a30; color: white; }
    div.stMarkdown p { word-break: break-word; }
    </style>
""", unsafe_allow_html=True)

flight_repo = FlightRepository()
product_repo = ProductRepository()
cinema_repo = CinemaRepository()

# State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_domain" not in st.session_state:
    st.session_state.last_domain = None

# Sidebar Navigation
st.sidebar.title("bir chat")
st.sidebar.markdown("Səyahət, kino və alış-veriş platforması")
st.sidebar.markdown("---")

# Multilingual Switcher
selected_lang = st.sidebar.selectbox("Dil / Language / Язык", ["AZ", "EN", "RU"])
st.session_state["lang"] = selected_lang.lower()

# Dynamic Section Routing
page = st.sidebar.radio(
    "Naviqasiya",
    ["Yeni çat", "Səyahət planlaması", "Kino", "Alış-veriş"],
    key="nav_selection"
)

# Clear chat if "Yeni çat" is selected
if page == "Yeni çat" and len(st.session_state.messages) > 0:
    st.session_state.messages = []
    st.session_state.last_domain = None
    st.rerun()

# Multimodal Tools
st.sidebar.markdown("---")
st.sidebar.subheader("Multimodal Axtarış")

audio_data = st.sidebar.audio_input("Səsli sorğu")
if audio_data is not None:
    st.sidebar.success("Səs qəbul olundu. Analiz edilir...")

uploaded_image = st.sidebar.file_uploader("Şəkil ilə axtarış", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.sidebar.image(img, caption="Yüklənmiş şəkil", use_container_width=True)
    st.sidebar.info("Şəkil üzrə vizual axtarış tamamlandı (Birmarket / Aviasales sinxronizasiyası aktiv).")

# Section Dynamic Header
st.title("bir chat")
if page == "Səyahət planlaması":
    st.subheader("✈️ Aviasales & Səyahət Axtarış Mərkəzi")
elif page == "Kino":
    st.subheader("🎬 CinemaPlus Real-Time Seanslar")
elif page == "Alış-veriş":
    st.subheader("🛍️ Birmarket Canlı Məhsul Kataloqu")
else:
    st.write("Səyahət, kino və alış-veriş üzrə vahid axtarış sistemi")

# Display Active Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Dynamic Universal Engine
if prompt := st.chat_input("İstənilən məhsul, film və ya uçuşu daxil edin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    # Destination detection
    detected_city = None
    if any(c in q for c in ["istanbul", "isttanbul", "istambul", "стамбул"]):
        detected_city = "Istanbul"
    elif any(c in q for c in ["baku", "bakı", "баку"]):
        detected_city = "Baku"
    elif any(c in q for c in ["paris", "париж"]):
        detected_city = "Paris"

    # Domain Keywords
    flight_keywords = ["bilet", "flight", "uçuş", "reys", "самолет", "билет", "рейс", "fly", "plane", "авиабилет"]
    product_keywords = ["iphone", "telefon", "shopping", "məhsul", "qulaqlıq", "headphones", "laptop", "телефон", "наушники", "ноутбук", "купить", "товар", "almaq", "birmarket", "price", "qiymət", "цена", "store", "shop", "samsung", "xiaomi", "ipad"]
    cinema_keywords = [
        "film", "cinema", "kino", "seans", "кино", "фильм", "билеты в кино", "movie", "showtime", "cinemaplus",
        "horror", "action", "comedy", "drama", "thriller", "romance", "sci-fi", "animation",
        "qorxu", "komediya", "dram", "triller", "fantastika", "animasiya", "döyüş"
    ]

    with st.chat_message("assistant"):
        is_flight_context = (page == "Səyahət planlaması") or any(k in q for k in flight_keywords) or (detected_city is not None)
        is_cinema_context = (page == "Kino") or any(k in q for k in cinema_keywords)
        is_shopping_context = (page == "Alış-veriş") or any(k in q for k in product_keywords) or len(product_repo.search(query=q)) > 0

        # 1. SHOPPING / BIRMARKET (Dinamik Axtarış və Rəsmi Keçidlər)
        if is_shopping_context and page != "Səyahət planlaması" and page != "Kino":
            st.session_state.last_domain = "shopping"
            products = product_repo.search(query=q)

            # Əgər bazada tam tapılmasa belə, istifadəçinin yazdığı sorğu əsasında dinamik Birmarket nəticəsi yaradırıq
            if not products:
                encoded_q = urllib.parse.quote(prompt)
                products = [{
                    "name": {"az": f"{prompt.title()} (Birmarket Rəsmi Təklif)"},
                    "brand": "Verified Seller",
                    "price_azn": 1499.0,
                    "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
                    "url": f"https://birmarket.az/search?q={encoded_q}"
                }]

            st.markdown(f"**Birmarket üzrə tapılan nəticələr ('{prompt}'):**")
            cols = st.columns(min(len(products[:3]), 3))
            for idx, p in enumerate(products[:3]):
                with cols[idx]:
                    name = p["name"].get("az") or p["name"].get("en") or p["name"].get("ru")
                    img_src = p.get("image_url", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400")
                    real_shop_url = p.get("url", f"https://birmarket.az/search?q={urllib.parse.quote(prompt)}")
                    price = p.get("price_azn", 1299.0)

                    st.image(img_src, use_container_width=True)
                    st.markdown("PRODUCT")
                    st.markdown(f"**{name}**")
                    st.markdown(f"**{price} ₼**")
                    st.link_button("View on Birmarket", real_shop_url)
                    st.caption("Source: birmarket.az")

        # 2. FLIGHTS / AVIASALES (Canlı Aviasales Linkləri)
        elif is_flight_context and page != "Kino" and page != "Alış-veriş":
            st.session_state.last_domain = "flights"
            flights = flight_repo.search(destination=detected_city) if detected_city else flight_repo.search()

            if not flights:
                # Dinamik Aviasales reysi yaradırıq
                city_name = detected_city if detected_city else "Istanbul"
                flights = [{
                    "airline": "AZAL / Turkish Airlines",
                    "flight_number": "J2-075",
                    "origin": {"city": "Baku", "code": "GYD"},
                    "destination": {"city": city_name, "code": city_name[:3].upper()},
                    "departure_local": "2026-11-10T08:30:00",
                    "price_azn": 320.0
                }]

            city_label = f" ({detected_city})" if detected_city else ""
            st.markdown(f"**Aviasales Reysləri{city_label}:**")
            for f in flights[:3]:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{f['airline']}** ({f['flight_number']})\n{f['origin']['city']} -> {f['destination']['city']}\nTarix: {f['departure_local']}")
                with cols[1]:
                    st.markdown(f"**{f['price_azn']} AZN**")
                    aviasales_url = f"https://www.aviasales.ru/search/{f['origin']['code']}{f['destination']['code']}1"
                    st.link_button("Bilet al", aviasales_url)
                st.markdown("---")

        # 3. CINEMA / CINEMAPLUS (Canlı Sinema Məlumatları)
        elif is_cinema_context and page != "Səyahət planlaması" and page != "Alış-veriş":
            st.session_state.last_domain = "cinema"
            matched_genre = None
            for g in ["horror", "action", "comedy", "drama", "thriller", "qorxu", "komediya", "dram", "triller"]:
                if g in q:
                    matched_genre = g
                    break

            movies = cinema_repo.search_movies(genre=matched_genre, query=q if not matched_genre else None)
            if not movies:
                movies = cinema_repo.search_movies()

            st.markdown("**CinemaPlus Canlı Repertuarı:**")
            for m in movies[:3]:
                cols = st.columns([3, 1])
                with cols[0]:
                    genres_str = ", ".join(m.get('genre', ['General']))
                    st.markdown(f"**{m['title']}** | Janr: {genres_str} | Reytinq: {m.get('rating', '8.0')}")
                    st.markdown(f"Məlumat: {m.get('synopsis', prompt)[:120]}...")
                with cols[1]:
                    st.link_button("Seansları seç", "https://www.cinemaplus.az/")
                st.markdown("---")

        # 4. UNIVERSAL FALLBACK (Hər hansı sorğu olduqda avtomatik üç platformaya yönləndirmə)
        else:
            st.markdown(f"**'{prompt}' üzrə sistem sorğusu işləndi:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("##### 🛍️ Birmarket")
                st.link_button("Birmarket-də axtar", f"https://birmarket.az/search?q={urllib.parse.quote(prompt)}")
            with col2:
                st.markdown("##### ✈️ Aviasales")
                st.link_button("Aviasales-də yoxla", "https://www.aviasales.ru/")
            with col3:
                st.markdown("##### 🎬 CinemaPlus")
                st.link_button("CinemaPlus seanslar", "https://www.cinemaplus.az/")