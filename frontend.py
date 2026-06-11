import requests
import streamlit as st

BASE_URL= "https://gezi-rehberi-yjse.onrender.com"
STRAPI_TOKEN= "5e9f1fb49194e492af759462bb866d4edc1b9aeba13df793b350270ee35fbb1c3ff27d388b345ebb06d0e02be025d241c46f7f16db772ca7ec0fca68025c876f2322294a74cc5982510b0f92c47a5c4448612db8aba0805444b9a9d0ab19845545996007f47eae3dae13062b683ea20ed8f0ca5d613128206ebb5de82185a444"

headers={
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type":"application/json"
}

st.set_page_config(page_title="Gezi Rehberi", page_icon="🍁", layout="centered")

# --- Başlangıç dili ayarı (butonlardan ÖNCE olmalı) ---
if "dil" not in st.session_state:
    st.session_state.dil = "tr"

# --- Başlık ---
if st.session_state.dil == "tr":
    st.title("🍁 Dinamik Gezi Rehberi")
    st.markdown("Bu web sitesi **Strapi** ve **Streamlit** kullanılarak oluşturulmuştur.")
else:
    st.title("🍁 Dynamic Travel Guide")
    st.markdown("This website was built using **Strapi** and **Streamlit**.")

st.divider()

# --- Dil Seçimi ---
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    tr_type = "primary" if st.session_state.dil == "tr" else "secondary"
    if st.button("🇹🇷 Türkçe", use_container_width=True, type=tr_type):
        st.session_state.dil = "tr"
        st.rerun()
with col2:
    en_type = "primary" if st.session_state.dil == "en" else "secondary"
    if st.button("🇬🇧 English", use_container_width=True, type=en_type):
        st.session_state.dil = "en"
        st.rerun()
with col3:
    aktif_dil = "🇹🇷 Türkçe" if st.session_state.dil == "tr" else "🇬🇧 English"
    st.info(f"Aktif / Active: **{aktif_dil}**")

st.divider()

dil = st.session_state.dil

# --- Strapi'den locale'e göre içerik çek ---
@st.cache_data
def makaleleri_getir(locale: str):
    url = f"{BASE_URL}/api/yazis?populate=*&locale={locale}"
    res = requests.get(url, headers=headers)
    if res.ok:
        return res.json().get("data", [])
    return []

articles = makaleleri_getir(dil)

if not articles:
    if dil == "tr":
        st.warning("Herhangi bir içerik bulunamadı.")
    else:
        st.warning("No content found.")
else:
    for a in articles:
        baslik = a.get("Baslik", "—")
        icerik = a.get("Icerik2", "—")

        with st.expander(f"{baslik}"):
            st.write(icerik)

# --- Sidebar ---
if dil == "tr":
    st.sidebar.success("Site Durumu: Site stabil bir durumda")
    st.sidebar.info("İçerik Yönetim Dersi")
else:
    st.sidebar.success("Site Status: Site is stable")
    st.sidebar.info("Content Management Course")
