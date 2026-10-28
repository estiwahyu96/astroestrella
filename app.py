import streamlit as st
import google.generativeai as genai

API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

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

model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    system_instruction=SYSTEM_PROMPT
)

st.set_page_config(page_title="Astroestrella", page_icon="🌟")
st.title("🌟 Astroestrella")
st.caption("Teman belajar Tata Surya untuk siswa SMP")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.write(message.parts[0].text)

if prompt := st.chat_input("Tanya apa saja tentang Tata Surya..."):
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.write(response.text)