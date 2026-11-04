import streamlit as st
from google import genai
import streamlit.components.v1 as components

# === KONFIGURASI HALAMAN ===
st.set_page_config(page_title="Dashboard Tata Surya", page_icon="logo.png", layout="wide")

# === KONFIGURASI API AI ===
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
Kamu adalah Astroestrella, teman belajar IPA untuk siswa SMP kelas VII.
Tugasmu membantu mereka memahami materi "Sistem Tata Surya".

# Aturan
1. Jawab dengan bahasa sederhana, cocok untuk anak SMP.
2. JANGAN langsung memberi jawaban akhir. Berikan pertanyaan pancingan agar siswa berpikir.
3. Jelaskan konsep dengan analogi kehidupan sehari-hari.
4. Gunakan emoji sesekali agar menarik. 🪐
5. Jika pertanyaan di luar materi tata surya, arahkan kembali ke topik dengan sopan.
6. Jawab maksimal 3 paragraf pendek.

# Topik yang boleh dibahas
- Sistem Tata Surya (Matahari, planet, satelit, asteroid, komet)
- Rotasi dan revolusi Bumi
- Gerhana
- Dampak rotasi-revolusi terhadap kehidupan sehari-hari
"""

# === SIDEBAR MENU ===
st.sidebar.title("🪐 Navigasi Belajar")
st.sidebar.markdown("Pilih menu di bawah ini untuk mulai belajar:")
menu = st.sidebar.radio(
    "Menu:",
    ["🏠 Beranda", "📖 Materi", "🔭 Simulasi", "🤖 Tanya Astro (AI)"]
)

# ==========================================
# KONTEN MENU 1: BERANDA
# ==========================================
if menu == "🏠 Beranda":
    st.title("Selamat Datang di Dashboard Tata Surya! 🌌")
    st.write("Halo para astronom muda! Di sini kamu bisa belajar tentang Tata Surya dengan cara yang seru.")
    
    st.info("""
    **Cara Menggunakan Dashboard Ini:**
    1. Buka menu **Materi** untuk membaca konsep dasar Tata Surya.
    2. Buka menu **Simulasi** untuk melihat langsung bagaimana planet bergerak.
    3. Jika kamu bingung atau punya pertanyaan, tanyakan saja ke **Astroestrella** di menu AI!
    """)
    
    st.write("Yuk, mulai petualanganmu dengan memilih menu di sebelah kiri! 🚀")


# ==========================================
# KONTEN MENU 2: MATERI
# ==========================================
elif menu == "📖 Materi":
    st.title("📖 Materi Sistem Tata Surya")
    
    st.header("1. Apa itu Tata Surya?")
    st.write("Sistem Tata Surya adalah kumpulan benda langit yang terdiri dari Matahari sebagai pusatnya, serta semua objek yang terikat oleh gaya gravitasinya. Anggota Tata Surya meliputi 8 planet, satelit alami (seperti Bulan), planet katai, asteroid, komet, dan meteoroid.")
    
    st.header("2. Rotasi dan Revolusi Bumi")
    st.write("**Rotasi Bumi** adalah perputaran Bumi pada porosnya (butuh waktu 24 jam). Ini menyebabkan terjadinya siang dan malam.")
    st.write("**Revolusi Bumi** adalah pergerakan Bumi mengelilingi Matahari (butuh waktu 365 hari / 1 tahun). Ini menyebabkan perubahan musim.")
    
    st.success("💡 **Ingat!** Kamu juga bisa bertanya lebih dalam tentang materi ini ke menu 'Tanya Astro (AI)'.")


# ==========================================
# KONTEN MENU 3: SIMULASI
# ==========================================
elif menu == "🔭 Simulasi":
    st.title("🔭 Simulasi Tata Surya Interaktif")
    st.write("Gunakan simulasi di bawah ini untuk melihat pergerakan planet secara langsung. Kamu bisa memutar, memperbesar, dan melihat orbit planet-planet!")
    
    # Menampilkan Solar System Scope secara langsung di dalam web (Embed Iframe)
    components.iframe("https://www.solarsystemscope.com/iframe", height=600, scrolling=True)
    
    st.caption("Sumber Simulasi: Solar System Scope (INOVE)")


# ==========================================
# KONTEN MENU 4: AI ASTROESTRELLA
# ==========================================
elif menu == "🤖 Tanya Astro (AI)":
    st.title("🤖 Tanya Astroestrella")
    st.write("Hai! Aku Astroestrella. Punya pertanyaan tentang planet, bintang, atau gerhana? Tanya saja ke aku!")

    # Inisialisasi riwayat chat di session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat percakapan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input dari pengguna
    if prompt := st.chat_input("Ketik pertanyaanmu di sini..."):
        # 1. Tampilkan dan simpan pesan user
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Dapatkan respons dari Gemini
        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model='gemini-3.5-flash-lite', # Model stabil
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                    )
                )
                st.write(response.text)
                # Simpan respons AI
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Ups, Astro sedang sibuk. Coba tanya lagi ya! (Error: {e})")
