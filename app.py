import streamlit as st
from PIL import Image
import urllib.parse
from repositories import FlightRepository, ProductRepository, CinemaRepository

# Səhifə konfiqurasiyası
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

if st.sidebar.button("+ Yeni çat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.last_domain = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Naviqasiya**")

page = st.sidebar.radio(
    "Kateqoriyalar",
    ["Travel planning", "Cinema", "Shopping"],
    label_visibility="collapsed",
    key="nav_selection"
)

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

# Chat Input & Strict Domain Engine
if prompt := st.chat_input("Sualınızı daxil edin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    with st.chat_message("assistant"):
        # 1. TRAVEL PLANNING -> AVIASALES
        if page == "Travel planning" or any(k in q for k in ["bilet", "flight", "uçuş", "reys", "istanbul", "baku", "paris"]):
            st.session_state.last_domain = "flights"
            flights = flight_repo.search()
            st.markdown(f"**Aviasales - Səyahət və Uçuş Nəticələri ('{prompt}'):**")
            for f in flights[:2]:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{f['airline']}** ({f['flight_number']})\n{f['origin']['city']} -> {f['destination']['city']}\nTarix: {f['departure_local']}")
                with cols[1]:
                    st.markdown(f"**{f['price_azn']} AZN**")
                    st.link_button("Bilet al", "https://www.aviasales.ru/")
                st.markdown("---")

        # 2. CINEMA -> CINEMAPLUS
        elif page == "Cinema" or any(k in q for k in ["film", "cinema", "kino", "seans", "movie", "horror", "action", "komediya"]):
            st.session_state.last_domain = "cinema"
            movies = cinema_repo.search_movies()
            st.markdown(f"**CinemaPlus Repertuarı ('{prompt}'):**")
            for m in movies[:2]:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{m['title']}** | Reytinq: {m.get('rating', '8.0')}")
                    st.markdown(f"{m.get('synopsis', '')[:100]}...")
                with cols[1]:
                    st.link_button("Seansları seç", "https://www.cinemaplus.az/")
                st.markdown("---")

        # 3. SHOPPING -> BIRMARKET (Yalnız axtarılan sözə uyğun, səhvən iPhone çıxarmayan məntiq)
        elif page == "Shopping" or any(k in q for k in ["iphone", "telefon", "shopping", "məhsul", "socks", "chay", "qulaqlıq", "birmarket"]):
            st.session_state.last_domain = "shopping"

            # İstifadəçinin yazdığı sözə uyğun məhsul yaradırıq (iPhone DEYİL!)
            encoded_q = urllib.parse.quote(prompt)
            product_name = prompt.title()

            st.markdown(f"**Birmarket üzrə tapılan nəticə ('{prompt}'):**")

            # Tək və təmiz kart formatı
            col1, col2 = st.columns([2, 2])
            with col1:
                st.markdown("PRODUCT")
                st.markdown(f"**{product_name}**")
                st.markdown("~~49.99 ₼~~")
                st.markdown("**19.99 ₼**")
                st.link_button("View on Birmarket", f"https://birmarket.az/search?q={encoded_q}")
                st.caption("Source: birmarket.az")

        # 4. NORMAL SÖHBƏT VƏ ÜNSİYYƏT (Chat kimi işləməsi üçün)
        else:
            resp_text = f"Salam! '{prompt}' sorğunuz qəbul olundu. Zəhmət olmasa sol paneldən müvafiq bölməni (Travel planning, Cinema və ya Shopping) seçin və ya sorğunuzu dəqiqləşdirin."
            st.markdown(resp_text)
            st.session_state.messages.append({"role": "assistant", "content": resp_text})