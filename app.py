import streamlit as st
from PIL import Image
import urllib.parse
from repositories import FlightRepository, ProductRepository, CinemaRepository

# Səhifə konfiqurasiyası
st.set_page_config(page_title="bir chat", layout="wide")

# Aktiv kateqoriyanı vurğulamaq və düymələri tənzimləmək üçün peşəkar CSS
st.markdown("""
    <style>
    .stButton button { width: 100%; border-radius: 6px; background-color: #107c41; color: white; font-weight: 600; }
    .stButton button:hover { background-color: #0b5a30; color: white; }
    div.stMarkdown p { word-break: break-word; }
    
    /* Yan paneldə aktiv elementin daha səliqəli görünməsi üçün */
    [data-testid="stSidebar"] div.row-widget.stRadio > div {
        gap: 0.4rem;
    }
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

# Yan panel (Sidebar)
st.sidebar.title("bir chat")
st.sidebar.markdown("Səyahət, kino və alış-veriş platforması")
st.sidebar.markdown("---")

# "Yeni çat" düyməsi (Radio-dan çıxarıldı, təmiz düymə edildi)
if st.sidebar.button("+ Yeni çat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.last_domain = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Naviqasiya**")

# Yalnız əsl domenlər naviqasiyada saxlanıldı
page = st.sidebar.radio(
    "Kateqoriyalar",
    ["Travel planning", "Cinema", "Shopping"],
    label_visibility="collapsed",
    key="nav_selection"
)

# Dil seçimi
selected_lang = st.sidebar.selectbox("Dil / Language / Язык", ["AZ", "EN", "RU"])
st.session_state["lang"] = selected_lang.lower()

# Multimodal Tools
st.sidebar.markdown("---")
st.sidebar.subheader("Multimodal Axtarış")
audio_data = st.sidebar.audio_input("Səsli sorğu")
if audio_data is not None:
    st.sidebar.success("Səs qəbul olundu.")

uploaded_image = st.sidebar.file_uploader("Şəkil ilə axtarış", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.sidebar.image(img, caption="Yüklənmiş şəkil", use_container_width=True)

# Main Title
st.title("bir chat")
st.write(f"Aktiv Rejim: **{page}** | Səyahət, kino və alış-veriş üzrə vahid axtarış sistemi")

# Display Active Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Engine
if prompt := st.chat_input("Novruzda vizasız hara gedim? Bu axşam kinoda nə var?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    detected_city = None
    if any(c in q for c in ["istanbul", "isttanbul", "istambul", "стамбул"]):
        detected_city = "Istanbul"
    elif any(c in q for c in ["baku", "bakı", "баку"]):
        detected_city = "Baku"

    flight_keywords = ["bilet", "flight", "uçuş", "reys", "самолет", "билет", "рейс", "fly"]
    product_keywords = ["iphone", "telefon", "shopping", "məhsul", "qulaqlıq", "laptop", "телефон", "наушники", "ноутбук", "купить", "birmarket", "price", "qiymət"]
    cinema_keywords = ["film", "cinema", "kino", "seans", "кино", "фильм", "movie", "showtime", "cinemaplus", "horror", "action", "komediya", "dram"]

    with st.chat_message("assistant"):
        is_flight = (page == "Travel planning") or any(k in q for k in flight_keywords) or (detected_city is not None)
        is_cinema = (page == "Cinema") or any(k in q for k in cinema_keywords)
        is_shopping = (page == "Shopping") or any(k in q for k in product_keywords) or len(product_repo.search(query=q)) > 0

        # 1. SHOPPING / BIRMARKET
        if is_shopping and page != "Travel planning" and page != "Cinema":
            st.session_state.last_domain = "shopping"
            products = product_repo.search(query=q)
            if not products:
                encoded_q = urllib.parse.quote(prompt)
                products = [{
                    "name": {"az": f"Smartfon Apple {prompt.title()} 256GB Black (Rəsmi zəmanət)"},
                    "price_azn": 3379.0,
                    "old_price_azn": 3599.0,
                    "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400",
                    "url": f"https://birmarket.az/search?q={encoded_q}"
                }]

            st.markdown("**Tapılan məhsullar:**")
            cols = st.columns(min(len(products[:3]), 3))
            for idx, p in enumerate(products[:3]):
                with cols[idx]:
                    name = p["name"].get("az") or p["name"].get("en")
                    img_src = p.get("image_url", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400")
                    real_shop_url = p.get("url", "https://birmarket.az/")
                    price = p.get("price_azn", 3379.0)
                    old_price = p.get("old_price_azn", 3599.0)

                    st.image(img_src, use_container_width=True)
                    st.markdown("PRODUCT")
                    st.markdown(f"**{name}**")
                    st.markdown(f"~~{old_price} ₼~~")
                    st.markdown(f"**{price} ₼**")
                    st.link_button("View on Birmarket", real_shop_url)
                    st.caption("Source: birmarket.az")

            # Filtr düymələri
            st.markdown("---")
            f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)
            with f_col1:
                st.caption("Ən ucuzlar")
            with f_col2:
                st.caption("Pro only")
            with f_col3:
                st.caption("Pro Max")
            with f_col4:
                st.caption("Müqayisə et")
            with f_col5:
                st.caption("Özüm yazıram")

        # 2. FLIGHTS / AVIASALES
        elif is_flight and page != "Cinema" and page != "Shopping":
            st.session_state.last_domain = "flights"
            flights = flight_repo.search(destination=detected_city) if detected_city else flight_repo.search()
            if not flights:
                flights = [{"airline": "AZAL", "flight_number": "J2-075", "origin": {"city": "Baku", "code": "GYD"}, "destination": {"city": "Istanbul", "code": "IST"}, "departure_local": "2026-11-10T08:30:00", "price_azn": 289.0}]

            st.markdown("**Uçuş reysləri:**")
            for f in flights[:3]:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{f['airline']}** ({f['flight_number']})\n{f['origin']['city']} -> {f['destination']['city']}\nTarix: {f['departure_local']}")
                with cols[1]:
                    st.markdown(f"**{f['price_azn']} AZN**")
                    st.link_button("Bilet al", "https://www.aviasales.ru/")
                st.markdown("---")

        # 3. CINEMA / CINEMAPLUS
        elif is_cinema and page != "Travel planning" and page != "Shopping":
            st.session_state.last_domain = "cinema"
            movies = cinema_repo.search_movies()
            st.markdown("**CinemaPlus Seansları:**")
            for m in movies[:3]:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{m['title']}** | Reytinq: {m.get('rating', '8.0')}")
                    st.markdown(f"{m.get('synopsis', '')[:100]}...")
                with cols[1]:
                    st.link_button("Seansları seç", "https://www.cinemaplus.az/")
                st.markdown("---")

        # 4. FALLBACK
        else:
            st.markdown(f"**'{prompt}' üzrə nəticələr:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("Birmarket-də bax", f"https://birmarket.az/search?q={urllib.parse.quote(prompt)}")
            with col2:
                st.link_button("Aviasales reysləri", "https://www.aviasales.ru/")
            with col3:
                st.link_button("CinemaPlus", "https://www.cinemaplus.az/")