import streamlit as st
from google import genai

# === KONFIGURASI API ===
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = """
Kamu adalah Astroestrella, teman belajar IPA yang asyik untuk siswa SMP kelas VII.
Tugasmu membantu mereka memahami materi "Sistem Tata Surya".

# Aturan Menjawab
1. Jawab dengan bahasa santai, akrab, dan gaul (khas anak SMP). Gunakan kata "aku" dan "kamu".
2. JAWABAN MAKSIMAL 2 PARAGRAF PENDEK. Jangan bertele-tele!
3. Gunakan analogi kehidupan sehari-hari atau benda yang ada di sekitar siswa.
4. JIKA siswa bertanya fakta dasar (contoh: "Berapa lama bumi berotasi?"), LANGSUNG berikan jawabannya di awal (contoh: "Bumi berotasi butuh waktu 24 jam lho!") baru kemudian berikan analogi.
5. JIKA pertanyaan siswa bersifat konseptual (contoh: "Kenapa planet tidak jatuh?"), berikan pertanyaan pancingan agar dia berpikir. TAPI JANGAN selalu bertanya di akhir jawaban. Cukup berikan pertanyaan pancingan 1-2 kali saja dalam satu sesi obrolan.
6. Gunakan emoji secukupnya agar menarik. 🪐
7. Jika pertanyaan di luar materi tata surya, tolak dengan sopan dan arahkan kembali ke topik.

# Topik yang boleh dibahas
- Sistem Tata Surya (Matahari, planet, satelit, asteroid, komet)
- Rotasi dan revolusi Bumi
- Gerhana
- Dampak rotasi-revolusi terhadap kehidupan sehari-hari
"""

# === TAMPILAN WEB ===
st.set_page_config(page_title="Astroestrella", page_icon="🌟")
st.title("🌟 Astroestrella")
st.caption("Teman belajar Tata Surya untuk siswa SMP")

# Simpan riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input dari pengguna
if prompt := st.chat_input("Tanya apa saja tentang Tata Surya..."):
    # 1. Tampilkan pesan user
    with st.chat_message("user"):
        st.write(prompt)
    
    # Simpan pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Dapatkan respons dari Gemini
    with st.chat_message("assistant"):
        try:
            # Panggil model dengan system prompt
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                )
            )
            st.write(response.text)
            
            # Simpan respons AI ke riwayat
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
