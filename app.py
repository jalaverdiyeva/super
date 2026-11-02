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

# Sidebar
st.sidebar.title("bir chat")
st.sidebar.markdown("Səyahət, kino və alış-veriş platforması")
st.sidebar.markdown("---")

if st.sidebar.button("+ Yeni çat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
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
st.write("Birmarket, Aviasales & CinemaPlus Ağıllı Axtarış Sistemi")

# Display Active Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Çat Girişi və Ağıllı İdentifikasiya (Smart Routing)
if prompt := st.chat_input("Nə axtarırsınız? (məs: istanbul, laptop, orbit zero)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    with st.chat_message("assistant"):
        assistant_reply = ""

        # 1. TRAVEL / FLIGHTS
        if any(k in q for k in ["bilet", "flight", "uçuş", "reys", "istanbul", "dubai", "moscow", "tbilisi", "tashkent"]):
            flights = flight_repo.search(query=prompt)
            st.markdown(f"**Aviasales üzrə tapılan reyslər ('{prompt}'):**")

            if not flights:
                st.warning("Uyğun reys tapılmadı.")
            else:
                for f in flights:
                    with st.container(border=True):
                        cols = st.columns([3, 1])
                        with cols[0]:
                            st.markdown(f"✈️ **{f['airline']}** ({f['flight_number']})")
                            st.markdown(f"**{f['origin']['city']} ({f['origin']['code']}) ➔ {f['destination']['city']} ({f['destination']['code']})**")
                            st.caption(f"Uçuş vaxtı: {f['departure_local']} | Baqaj: {f['baggage_kg']}kg")
                        with cols[1]:
                            st.markdown(f"### {f['price_azn']} AZN")
                            st.link_button("Bilet al", f"https://www.aviasales.ru/search/GYD{f['destination']['code']}1")

            assistant_reply = f"Aviasales üzrə '{prompt}' istiqamətində reyslər göstərildi."

        # 2. CINEMA
        elif any(k in q for k in ["film", "cinema", "kino", "seans", "movie", "orbit", "caravan", "laugh", "archive", "kites", "ledger", "spring", "signal", "sci-fi", "horror", "comedy", "action"]):
            movies = cinema_repo.search_movies(query=prompt)
            st.markdown(f"**CinemaPlus seansları ('{prompt}'):**")

            if not movies:
                st.warning("Uyğun film tapılmadı.")
            else:
                for m in movies:
                    with st.container(border=True):
                        cols = st.columns([3, 1])
                        with cols[0]:
                            genres = ", ".join(m.get("genre", []))
                            st.markdown(f"🎬 **{m['title']}** | ⭐ `{m['rating']}` | Janr: *{genres}*")
                            st.write(f"{m['synopsis']}")
                            st.caption(f"Müddət: {m.get('duration_min')} dəq | Dil: {m.get('language')}")
                        with cols[1]:
                            st.link_button("Seansları seç", f"https://cinemaplus.az/az/search?q={urllib.parse.quote(m['title'])}")

            assistant_reply = f"CinemaPlus üzrə '{prompt}' seansları göstərildi."

        # 3. SHOPPING
        else:
            products = product_repo.search(query=prompt)
            st.markdown(f"**Birmarket üzrə nəticələr ('{prompt}'):**")

            if not products:
                st.warning("Uyğun məhsul tapılmadı.")
            else:
                cols = st.columns(min(len(products[:3]), 3))
                for idx, p in enumerate(products[:3]):
                    with cols[idx]:
                        name_dict = p.get("name", {})
                        name = name_dict.get("az") or name_dict.get("en") or str(name_dict)
                        category = p.get("category", "").lower()

                        icon = "🛍️"
                        if "audio" in category: icon = "🎧"
                        elif "computer" in category: icon = "💻"
                        elif "phone" in category: icon = "📱"
                        elif "wearable" in category: icon = "⌚"
                        elif "sport" in category: icon = "👟"
                        elif "accessor" in category: icon = "🎒"
                        elif "home" in category: icon = "☕"
                        elif "gift" in category: icon = "🎲"

                        real_shop_url = f"https://birmarket.az/search?q={urllib.parse.quote(name)}"
                        price = f"{p.get('price_azn', 0)} ₼"
                        desc = p.get("description", "")
                        rating = p.get("rating", "4.0")
                        stock = p.get("stock", 0)

                        with st.container(border=True):
                            st.markdown(f"### {icon} {name}")
                            st.caption(f"Brend: **{p.get('brand', 'Birmarket')}** | Kateqoriya: {category.title()}")
                            if desc:
                                st.write(desc)
                            st.markdown(f"**Qiymət:** `{price}` &nbsp;|&nbsp; ⭐ `{rating}` &nbsp;|&nbsp; Stok: `{stock}` ədəd")
                            st.link_button("Birmarket-də bax", real_shop_url)

            assistant_reply = f"Birmarket üzrə '{prompt}' məhsulları göstərildi."

        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})