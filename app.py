import streamlit as st
import base64
import time
import random
import string

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER VAULT // TERMINAL",
    page_icon="📟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS HACKER GREEN THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    :root {
        --neon-green: #00ff41;
        --dark-green: #003b00;
        --bg-black: #020202;
    }

    .stApp {
        background-color: var(--bg-black);
        color: var(--neon-green);
        font-family: 'Share Tech Mono', monospace;
        background-image: repeating-linear-gradient(
            0deg, rgba(0, 255, 65, 0.03) 0px, rgba(0, 255, 65, 0.03) 1px, transparent 1px, transparent 3px
        );
        background-size: 100% 3px;
    }
    
    * { caret-color: var(--neon-green); }

    /* HEADER */
    .vault-header {
        text-align: center;
        font-size: 3rem; font-weight: bold; color: var(--neon-green);
        text-shadow: 0 0 15px var(--neon-green); letter-spacing: 5px;
        margin-bottom: 10px; text-transform: uppercase;
    }
    .vault-sub {
        text-align: center; color: rgba(0, 255, 65, 0.7); margin-bottom: 40px;
        font-size: 1.1rem; letter-spacing: 2px;
    }
    
    /* WIDGETS */
    .stRadio > label, .stSelectbox > label, .stTextArea > label { color: var(--neon-green) !important; }
    .stRadio div[role='radiogroup'] > label > div:first-child { color: var(--neon-green); }

    /* INPUT AREAS */
    .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important; color: var(--neon-green) !important;
        border: 2px solid var(--neon-green) !important; font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem; border-radius: 0px; box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stTextArea > div > div > textarea:focus { box-shadow: 0 0 15px var(--neon-green); }

    /* BUTTONS */
    .stButton > button {
        background: black; border: 2px solid var(--neon-green); color: var(--neon-green);
        font-weight: bold; font-family: 'Share Tech Mono', monospace; padding: 15px;
        text-transform: uppercase; letter-spacing: 3px; width: 100%; transition: 0.2s; border-radius: 0;
    }
    .stButton > button:hover {
        background: var(--neon-green); color: black; box-shadow: 0 0 30px var(--neon-green); font-weight: 900;
    }

    /* RESULT BOX */
    .result-container {
        border: 2px solid var(--neon-green); background: rgba(0, 255, 65, 0.05);
        padding: 20px; margin-top: 20px; border-radius: 0px; position: relative;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }
    .result-label {
        color: var(--neon-green); font-size: 1rem; text-transform: uppercase;
        letter-spacing: 2px; margin-bottom: 10px; font-weight: bold;
        border-bottom: 1px dashed var(--neon-green); display: inline-block;
    }
    .result-text {
        color: white; font-family: 'Share Tech Mono', monospace; word-break: break-all;
        font-size: 1.3rem; margin-top: 15px; text-shadow: 0 0 5px white;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- FUNGSI ENKRIPSI ---
def encrypt_message(text, method):
    if method == "BINARY (0101)": return ' '.join(format(ord(char), '08b') for char in text)
    elif method == "HEXADECIMAL": return text.encode('utf-8').hex().upper()
    elif method == "BASE64 (SECURE)": return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif method == "REVERSE (MIRROR)": return text[::-1]
    return text

def decrypt_message(text, method):
    try:
        if method == "BINARY (0101)": return ''.join(chr(int(b, 2)) for b in text.split(' '))
        elif method == "HEXADECIMAL": return bytes.fromhex(text).decode('utf-8')
        elif method == "BASE64 (SECURE)": return base64.b64decode(text.encode('utf-8')).decode('utf-8')
        elif method == "REVERSE (MIRROR)": return text[::-1]
    except: return "ERROR: INVALID CODE FORMAT"
    return text

# --- FUNGSI ANIMASI SCRAMBLE (HACKER EFFECT) ---
def animate_scramble(final_text, placeholder, label_text):
    # Karakter acak untuk efek glitch (Huruf + Angka + Simbol)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    
    # Tentukan panjang teks animasi (max 50 biar gak kepanjangan di layar)
    display_len = len(final_text)
    if display_len > 50: display_len = 50 
    
    # Loop animasi sebanyak 15 frame
    for _ in range(15):
        # Bikin teks acak
        random_str = ''.join(random.choice(chars) for _ in range(display_len))
        
        # Tampilkan di placeholder
        placeholder.markdown(f"""
        <div class='result-container'>
            <div class='result-label'>DECODING DATA STREAM...</div>
            <div class='result-text' style='opacity: 0.7; color: #00ff41;'>{random_str}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Kecepatan animasi (0.05 detik per frame)
        time.sleep(0.05)

    # Tampilkan hasil akhir yang benar
    placeholder.markdown(f"""
    <div class='result-container'>
        <div class='result-label'>{label_text}</div>
        <div class='result-text'>{final_text}</div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN APP ---
st.markdown("<div class='vault-header'>CYBER VAULT</div>", unsafe_allow_html=True)
st.markdown("<div class='vault-sub'>// SECURE TERMINAL UPLINK //</div>", unsafe_allow_html=True)

mode = st.radio("SELECT OPERATION MODE >>", ["ENCRYPT (LOCK DATA)", "DECRYPT (UNLOCK DATA)"], horizontal=True)
st.markdown("<br>", unsafe_allow_html=True)

input_text = st.text_area("ENTER INPUT STREAM >>", height=150, placeholder="Awaiting command input...")
method = st.selectbox("SELECT ALGORITHM >>", ["BINARY (0101)", "HEXADECIMAL", "BASE64 (SECURE)", "REVERSE (MIRROR)"])

st.markdown("<br>", unsafe_allow_html=True)

# Placeholder kosong untuk tempat hasil animasi
result_area = st.empty()

if st.button("[ EXECUTE ]"):
    if input_text:
        # 1. Hitung hasil dulu di belakang layar
        if "ENCRYPT" in mode:
            final_result = encrypt_message(input_text, method)
            final_label = "ENCRYPTED OUTPUT >>"
        else:
            final_result = decrypt_message(input_text, method)
            final_label = "DECRYPTED MESSAGE >>"
        
        # 2. Jalankan Animasi Scramble di area result
        animate_scramble(final_result, result_area, final_label)
        
    else:
        st.error("ERROR: NO INPUT DATA DETECTED.")

st.markdown("<br><br><div style='text-align: center; color: #00ff41; opacity: 0.5; font-size: 0.8rem;'>TERMINAL V.2.3 | ENCRYPTED CONNECTION ESTABLISHED</div>", unsafe_allow_html=True)
