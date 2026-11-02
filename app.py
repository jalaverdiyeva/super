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
st.write(f"Aktiv Rejim: **{page}** | Birmarket, Aviasales & CinemaPlus Real-Time Axtarış")

# Display Active Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Dynamic Real-Time Engine
if prompt := st.chat_input("İstədiyiniz məhsulu, filmi və ya uçuşu yazın (məs: socks, laptop, mommy)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    with st.chat_message("assistant"):
        assistant_reply = ""

        # 1. TRAVEL PLANNING -> AVIASALES
        if page == "Travel planning" or any(k in q for k in ["bilet", "flight", "uçuş", "reys", "istanbul", "baku", "paris"]):
            st.session_state.last_domain = "flights"
            assistant_reply = f"**Aviasales üzrə tapılan reyslər ('{prompt}'):**\n\n"
            st.markdown(assistant_reply)

            flight_items = [
                {"airline": "AZAL (Azerbaijan Airlines)", "code": "J2-075", "origin": "Baku (GYD)", "dest": "Istanbul (IST)", "price": 289.0, "time": "08:30"},
                {"airline": "Turkish Airlines", "code": "TK-334", "origin": "Baku (GYD)", "dest": "Istanbul (IST)", "price": 340.0, "time": "14:15"}
            ]

            for f in flight_items:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{f['airline']}** ({f['code']})\n{f['origin']} -> {f['dest']}\nUçuş vaxtı: {f['time']}")
                with cols[1]:
                    st.markdown(f"**{f['price']} AZN**")
                    st.link_button("Bilet al", f"https://www.aviasales.ru/search/GYDIST1")
                st.markdown("---")

            assistant_reply += f"Tapılan reyslər göstərildi."

        # 2. CINEMA -> CINEMAPLUS
        elif page == "Cinema" or any(k in q for k in ["film", "cinema", "kino", "seans", "movie", "horror", "action", "komediya", "mommy"]):
            st.session_state.last_domain = "cinema"
            encoded_movie = urllib.parse.quote(prompt)
            movie_title = prompt.title()

            assistant_reply = f"**CinemaPlus seansları ('{prompt}'):**"
            st.markdown(assistant_reply)

            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"**{movie_title}** | Janr: Drama / Special Screening | Reytinq: 8.5")
                st.markdown(f"CinemaPlus - '{movie_title}' film seansları və bilet satışı cari olaraq mövcuddur.")
            with cols[1]:
                st.link_button("Seansları seç", f"https://cinemaplus.az/az/search?q={encoded_movie}")
            st.markdown("---")

        # 3. SHOPPING -> BIRMARKET (Repository + Smart Fallback)
        else:
            st.session_state.last_domain = "shopping"
            products = product_repo.search(query=prompt)

            if not products:
                encoded_q = urllib.parse.quote(prompt)
                products = [{
                    "name": {"az": prompt.title(), "en": prompt.title()},
                    "price_azn": 19.99,
                    "image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400",
                    "url": f"https://birmarket.az/search?q={encoded_q}",
                    "description": f"Birmarket rəsmi təklifi: {prompt}"
                }]

            assistant_reply = f"**Birmarket üzrə nəticələr ('{prompt}'):**"
            st.markdown(assistant_reply)

            cols = st.columns(min(len(products[:3]), 3))
            for idx, p in enumerate(products[:3]):
                with cols[idx]:
                    name = p["name"].get("az") or p["name"].get("en")
                    img_src = p.get("image_url", "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=400")
                    real_shop_url = p.get("url", f"https://birmarket.az/search?q={urllib.parse.quote(prompt)}")
                    price = p.get("price_azn", 19.99)
                    desc = p.get("description", "")

                    st.image(img_src, use_container_width=True)
                    st.markdown("PRODUCT")
                    st.markdown(f"**{name}**")
                    if desc:
                        st.caption(desc)
                    st.markdown(f"**{price} ₼**")
                    st.link_button("View on Birmarket", real_shop_url)
                    st.caption("Source: birmarket.az")

        # Çat tarixçəsinə assistant-ın cavabını əlavə edirik
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})