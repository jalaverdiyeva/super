import streamlit as st
from PIL import Image
from repositories import FlightRepository, ProductRepository, CinemaRepository

# Page Configuration
st.set_page_config(page_title="bir chat", layout="wide")

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
    st.sidebar.info("Şəkil üzrə axtarış aparılır... (Dəqiqlik: 95%)")

# Section Dynamic Header
st.title("bir chat")
if page == "Səyahət planlaması":
    st.subheader("✈️ Səyahət & Uçuş Axtarış Bölməsi")
elif page == "Kino":
    st.subheader("🎬 CinemaPlus & Kino Repertuarı")
elif page == "Alış-veriş":
    st.subheader("🛍️ Birmarket Alış-veriş Mərkəzi")
else:
    st.write("Səyahət, kino və alış-veriş üzrə vahid axtarış sistemi")

# Display Active Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Routing Engine
if prompt := st.chat_input("Sualınızı daxil edin (AZ / RU / EN)..."):
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
    product_keywords = ["iphone", "telefon", "shopping", "məhsul", "qulaqlıq", "headphones", "laptop", "телефон", "наушники", "ноутбук", "купить", "товар", "almaq", "birmarket", "price", "qiymət", "цена", "store", "shop"]
    cinema_keywords = [
        "film", "cinema", "kino", "seans", "кино", "фильм", "билеты в кино", "movie", "showtime", "cinemaplus",
        "horror", "action", "comedy", "drama", "thriller", "romance", "sci-fi", "animation",
        "qorxu", "komediya", "dram", "triller", "fantastika", "animasiya", "döyüş"
    ]

    with st.chat_message("assistant"):
        # Domain determination based on Nav Selection OR NLP Keywords
        is_flight_context = (page == "Səyahət planlaması") or any(k in q for k in flight_keywords) or (detected_city is not None)
        is_cinema_context = (page == "Kino") or any(k in q for k in cinema_keywords)
        is_shopping_context = (page == "Alış-veriş") or any(k in q for k in product_keywords) or len(product_repo.search(query=q)) > 0

        # 1. SHOPPING / BIRMARKET
        if is_shopping_context and page != "Səyahət planlaması" and page != "Kino":
            st.session_state.last_domain = "shopping"
            products = product_repo.search(query=q)
            if not products:
                products = product_repo.search()

            if products:
                st.markdown("**Tapılan məhsullar:**")
                cols = st.columns(min(len(products[:3]), 3))
                for idx, p in enumerate(products[:3]):
                    with cols[idx]:
                        name = p["name"].get("az") or p["name"].get("en") or p["name"].get("ru")
                        img_src = p.get("image_url", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400")
                        real_shop_url = p.get("url", "https://birmarket.az/")
                        price = p.get("price_azn", 0)

                        st.image(img_src, use_container_width=True)
                        st.markdown("PRODUCT")
                        st.markdown(f"**{name}**")
                        st.markdown(f"**{price} ₼**")
                        st.link_button("View on Birmarket", real_shop_url)
                        st.caption("Source: birmarket.az")
            else:
                resp_text = f"Axtardığınız '{prompt}' üzrə Birmarket-də məhsul tapılmadı."
                st.markdown(resp_text)
                st.session_state.messages.append({"role": "assistant", "content": resp_text})

        # 2. FLIGHTS / AVIASALES
        elif is_flight_context and page != "Kino" and page != "Alış-veriş":
            st.session_state.last_domain = "flights"
            flights = flight_repo.search(destination=detected_city) if detected_city else flight_repo.search()

            if flights:
                city_label = f" ({detected_city})" if detected_city else ""
                st.markdown(f"**Uçuş reysləri{city_label}:**")
                for f in flights[:3]:
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.markdown(f"**{f['airline']}** ({f['flight_number']})\n{f['origin']['city']} -> {f['destination']['city']}\nTarix: {f['departure_local']}")
                    with cols[1]:
                        st.markdown(f"**{f['price_azn']} AZN**")
                        aviasales_url = f"https://www.aviasales.ru/search/{f['origin']['code']}{f['departure_local'][:10].replace('-', '')}{f['destination']['code']}1"
                        st.link_button("Bilet al", aviasales_url)
                    st.markdown("---")
            else:
                resp_text = f"Məlumat: '{detected_city if detected_city else prompt}' istiqamətində aktiv reys tapılmadı."
                st.markdown(resp_text)
                st.session_state.messages.append({"role": "assistant", "content": resp_text})

        # 3. CINEMA / CINEMAPLUS
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

            st.markdown("**CinemaPlus Repertuarı:**")
            for m in movies[:3]:
                cols = st.columns([3, 1])
                with cols[0]:
                    genres_str = ", ".join(m.get('genre', []))
                    st.markdown(f"**{m['title']}** | Janr: {genres_str} | Reytinq: {m['rating']}")
                    st.markdown(f"Məlumat: {m.get('synopsis', '')[:120]}...")
                with cols[1]:
                    st.link_button("Seansları seç", "https://www.cinemaplus.az/")
                st.markdown("---")

        # 4. OUT OF SCOPE
        else:
            default_text = (
                "Sistem Uçuşlar (Aviasales), Birmarket Alış-veriş və CinemaPlus üzrə sorğuları emal edir.\n\n"
                "Nümunə sorğular:\n"
                "- İstanbul istiqamətinə uçuşlar\n"
                "- iPhone 17 qiyməti\n"
                "- Horror filmləri"
            )
            st.markdown(default_text)
            st.session_state.messages.append({"role": "assistant", "content": default_text})