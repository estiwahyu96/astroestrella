import streamlit as st

# 1. Set Page Config (Pakai Emoji, JANGAN gambar dulu)
st.set_page_config(page_title="Dashboard Tata Surya", page_icon="🪐", layout="wide")

# 2. Tampilkan Pesan Awal
st.write("⏳ Aplikasi mulai berjalan...")

# 3. Cek API Key
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    st.write("✅ API Key berhasil ditemukan!")
except Exception as e:
    st.error("❌ API Key GAGAL ditemukan di Secrets Streamlit. Pesan Error:", e)

# 4. Tampilkan Sidebar
st.sidebar.title("🪐 Navigasi Belajar")
menu = st.sidebar.radio("Menu:", ["🏠 Beranda", "📖 Materi", "🔭 Simulasi"])

if menu == "🏠 Beranda":
    st.title("Selamat Datang di Dashboard! 🌌")
    st.write("Ini adalah halaman beranda versi uji coba.")
elif menu == "📖 Materi":
    st.title("Ini Halaman Materi")
    st.write("Materi Tata Surya ada di sini.")
elif menu == "🔭 Simulasi":
    st.title("Ini Halaman Simulasi")
    st.write("Simulasi akan muncul di sini nanti.")
