# SHOPPING (Məhsul axtarışı)
else:
products = product_repo.search(query=prompt)
st.markdown(f"**Birmarket üzrə nəticələr ('{prompt}'):**")

if not products:
    st.warning("Uyğun məhsul tapılmadı.")
else:
    cols = st.columns(min(len(products[:3]), 3))
    for idx, p in enumerate(products[:3]):
        with cols[idx]:
            # Dataset-dən dil strukturuna uyğun adın götürülməsi
            name_dict = p.get("name", {})
            name = name_dict.get("az") or name_dict.get("en") or str(name_dict)

            img_src = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"
            real_shop_url = f"https://birmarket.az/search?q={urllib.parse.quote(name)}"
            price = f"{p.get('price_azn', 0)} ₼"
            desc = p.get("description", "")

            st.image(img_src, use_container_width=True)
            st.markdown(f"**{name}**")
            if desc:
                st.caption(desc)
            st.markdown(f"**Qiymət: {price}** | Stok: {p.get('stock', 0)}")
            st.link_button("View on Birmarket", real_shop_url)