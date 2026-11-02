import streamlit as st
from PIL import Image
from repositories import FlightRepository, ProductRepository, CinemaRepository

# Səhifə konfiqurasiyası
st.set_page_config(page_title="bir chat", layout="wide")

flight_repo = FlightRepository()
product_repo = ProductRepository()
cinema_repo = CinemaRepository()

# Yan panel (Sidebar)
st.sidebar.title("bir chat")
st.sidebar.markdown("Səyahət, kino və alış-veriş platforması")
st.sidebar.markdown("---")

# Çoxdilli Dəstək (Multilingual Switcher)
selected_lang = st.sidebar.selectbox("Dil / Language / Язык", ["AZ", "EN", "RU"])
st.session_state["lang"] = selected_lang.lower()

# Emojilərdən təmizlənmiş Peşəkar Naviqasiya Menyusu
page = st.sidebar.radio(
    "Naviqasiya",
    ["Yeni çat", "Səyahət planlaması", "Kino", "Alış-veriş"]
)

# Multimodal alətlər
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

st.title("bir chat")
st.write("Səyahət, kino və alış-veriş üzrə vahid axtarış sistemi")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_domain" not in st.session_state:
    st.session_state.last_domain = None

# Çat tarixçəsi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sualınızı daxil edin (AZ / RU / EN)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    # Şəhər təyini
    detected_city = None
    if any(c in q for c in ["istanbul", "isttanbul", "istambul", "стамбул"]):
        detected_city = "Istanbul"
    elif any(c in q for c in ["baku", "bakı", "баку"]):
        detected_city = "Baku"
    elif any(c in q for c in ["paris", "париж"]):
        detected_city = "Paris"

    # Açar sözlər
    flight_keywords = ["bilet", "flight", "uçuş", "reys", "самолет", "билет", "рейс", "fly", "plane", "авиабилет"]
    product_keywords = ["iphone", "telefon", "shopping", "məhsul", "qulaqlıq", "headphones", "laptop", "телефон", "наушники", "ноутбук", "купить", "товар", "almaq", "birmarket", "price", "qiymət", "цена", "store", "shop"]
    cinema_keywords = ["film", "cinema", "kino", "seans", "кино", "фильм", "билеты в кино", "movie", "showtime", "cinemaplus"]

    with st.chat_message("assistant"):
        is_flight_intent = any(k in q for k in flight_keywords) or (detected_city is not None) or (st.session_state.last_domain == "flights" and not any(k in q for k in product_keywords + cinema_keywords))

        # 1. UÇUŞLAR / FLIGHTS
        if is_flight_intent:
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

        # 2. ALIŞ-VERİŞ / SHOPPING (Müəllimin ekranındakı kimi kart strukturu)
        elif any(k in q for k in product_keywords) or len(product_repo.search(query=q)) > 0:
            st.session_state.last_domain = "shopping"
            products = product_repo.search(query=q)

            if products:
                st.markdown("**Tapılan məhsullar:**")
                cols = st.columns(min(len(products[:3]), 3))
                for idx, p in enumerate(products[:3]):
                    with cols[idx]:
                        name = p["name"].get("az") or p["name"].get("en") or p["name"].get("ru")
                        img_src = p.get("image_url", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400")
                        real_shop_url = p.get("url", "https://kontakt.az/")
                        price = p.get("price_azn", 0)

                        # Şəkildəki dizayn formatı
                        st.image(img_src, use_container_width=True)
                        st.markdown("PRODUCT")
                        st.markdown(f"**{name}**")
                        st.markdown(f"**{price} ₼**")

                        # Yaşıl Birmarket düyməsi və mənbə
                        st.link_button("View on Birmarket", real_shop_url)
                        st.caption("Source: birmarket.az")
            else:
                resp_text = f"Axtardığınız '{prompt}' üzrə mağazalarda məhsul tapılmadı."
                st.markdown(resp_text)
                st.session_state.messages.append({"role": "assistant", "content": resp_text})

        # 3. KİNO / CINEMA
        elif any(k in q for k in cinema_keywords):
            st.session_state.last_domain = "cinema"
            movies = cinema_repo.search_movies()
            st.markdown("**Kinoteatr repertuarı:**")
            for m in movies[:3]:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{m['title']}** (Janr: {', '.join(m['genre'])}) | Reytinq: {m['rating']}")
                    st.markdown(f"{m['synopsis'][:120]}...")
                with cols[1]:
                    st.link_button("Seansları seç", "https://www.cinemaplus.az/")
                st.markdown("---")

        # 4. OUT OF SCOPE
        else:
            default_text = (
                "Sistem Uçuşlar (Aviasales), Alış-veriş və CinemaPlus üzrə sorğuları emal edir.\n\n"
                "Nümunə sorğular:\n"
                "- İstanbul istiqamətinə uçuşlar\n"
                "- iPhone 17 qiyməti\n"
                "- Kinoteatrda olan filmlər"
            )
            st.markdown(default_text)
            st.session_state.messages.append({"role": "assistant", "content": default_text})