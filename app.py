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
if prompt := st.chat_input("Nə axtarırsınız? (məs: roma, iphone, mommy filmi)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    q = prompt.lower()

    with st.chat_message("assistant"):
        assistant_reply = ""

        # 1. TRAVEL / FLIGHTS (Uçuş və şəhər adları)
        if any(k in q for k in ["bilet", "flight", "uçuş", "reys", "roma", "paris", "nyc", "london", "istanbul", "dubai", "havai"]):
            flights = flight_repo.search(query=prompt)
            st.markdown(f"**Aviasales üzrə tapılan reyslər ('{prompt}'):**")

            for f in flights:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{f['airline']}** ({f['flight_number']})\n{f['origin']['city']} -> {f['destination']['city']}\nTarix: {f['departure_local']}")
                with cols[1]:
                    st.markdown(f"**{f['price_azn']}**")
                    st.link_button("Bilet al", f["url"])
                st.markdown("---")

            assistant_reply = f"Aviasales üzrə '{prompt}' istiqamətində reyslər tapıldı."

        # 2. CINEMA (Film və kino adları)
        elif any(k in q for k in ["film", "cinema", "kino", "seans", "movie", "mommy", "horror", "action", "komediya", "venom", "smile"]):
            movies = cinema_repo.search_movies(query=prompt)
            st.markdown(f"**CinemaPlus seansları ('{prompt}'):**")

            for m in movies:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**{m['title']}** | Reytinq: {m['rating']}")
                    st.markdown(f"{m['synopsis']}")
                    st.caption(f"Kinoteatr: {m['cinema']}")
                with cols[1]:
                    st.link_button("Seansları seç", m["url"])
                st.markdown("---")

            assistant_reply = f"CinemaPlus üzrə '{prompt}' seansları tapıldı."

        # 3. SHOPPING (Məhsul axtarışı)
        else:
            products = product_repo.search(query=prompt)
            st.markdown(f"**Birmarket üzrə nəticələr ('{prompt}'):**")

            cols = st.columns(min(len(products[:3]), 3))
            for idx, p in enumerate(products[:3]):
                with cols[idx]:
                    name = p.get("name", prompt.title())
                    img_src = p.get("image", "https://images.unsplash.com/photo-1556742049-0a67d5e86540?w=500")
                    real_shop_url = p.get("url", f"https://birmarket.az/search?q={urllib.parse.quote(prompt)}")
                    price = p.get("price", "49.99 ₼")
                    desc = p.get("desc", "")

                    st.image(img_src, use_container_width=True)
                    st.markdown("PRODUCT")
                    st.markdown(f"**{name}**")
                    if desc:
                        st.caption(desc)
                    st.markdown(f"**{price}**")
                    st.link_button("View on Birmarket", real_shop_url)
                    st.caption("Source: birmarket.az")

            assistant_reply = f"Birmarket üzrə '{prompt}' məhsulları tapıldı."

        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})