import requests
import streamlit as st

BASE_URL= "https://gezi-rehberi-yjse.onrender.com"
STRAPI_TOKEN= "5e9f1fb49194e492af759462bb866d4edc1b9aeba13df793b350270ee35fbb1c3ff27d388b345ebb06d0e02be025d241c46f7f16db772ca7ec0fca68025c876f2322294a74cc5982510b0f92c47a5c4448612db8aba0805444b9a9d0ab19845545996007f47eae3dae13062b683ea20ed8f0ca5d613128206ebb5de82185a444"

headers={
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type":"application/json"
}

st.set_page_config(page_title="Gezi Rehberi", page_icon="🍁", layout="centered")

st.title("Dinamik Gezi Rehberi")
st.markdown("Bu web site Strapi ve Streamlit kullanılarak oluşturulmuştur.")

st.divider()

# Dil Seçimi
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🇹🇷 Türkçe", use_container_width=True):
        st.session_state.dil = "TR"
with col2:
    if st.button("🇬🇧 English", use_container_width=True):
        st.session_state.dil = "EN"

# Başlangıç dili ayarı
if "dil" not in st.session_state:
    st.session_state.dil = "TR"

dil = st.session_state.dil
st.divider()

@st.cache_data
def makaleleri_getir():
    url=f"{BASE_URL}/api/yazis?populate=*"

    res=requests.get(url, headers=headers)

    if res.ok:
        ham_veri=res.json().get("data",[])
        return ham_veri
    return []

articles=makaleleri_getir()

if not articles:
    st.warning("Herhangi bir içerik bulunamadı")
else:
    for a in articles:
        # Dile göre başlık ve içerik seçimi
        if dil == "TR":
            baslik = a.get("Baslik", "Başlıksız Makale")
            icerik = a.get("Icerik2", "İçeriksiz makale")
        else:  # English
            baslik = a.get("Title", a.get("Baslik", "Untitled Article"))
            icerik = a.get("Content", a.get("Icerik2_EN", a.get("Icerik2", "No content available")))

        with st.expander(f"{baslik}"):
            st.write(icerik)

st.sidebar.success("Site Durumu: Site stabil bir durumda")
st.sidebar.info("İçerik Yönetim Dersi")
