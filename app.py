import streamlit as st
import base64

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
    /* Import Font ala Terminal/Kodingan */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    :root {
        --neon-green: #00ff41;  /* Hijau Matrix */
        --dark-green: #003b00;
        --bg-black: #020202;    /* Hitam Pekat */
    }

    /* Reset Streamlit ke Tema Hacker */
    .stApp {
        background-color: var(--bg-black);
        color: var(--neon-green);
        font-family: 'Share Tech Mono', monospace;
        /* Efek garis scan halus di background */
        background-image: repeating-linear-gradient(
            0deg,
            rgba(0, 255, 65, 0.03) 0px,
            rgba(0, 255, 65, 0.03) 1px,
            transparent 1px,
            transparent 3px
        );
        background-size: 100% 3px;
    }
    
    /* Ubah warna cursor jadi hijau */
    * { caret-color: var(--neon-green); }

    /* HEADER */
    .vault-header {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: var(--neon-green);
        text-shadow: 0 0 15px var(--neon-green); /* Efek Cahaya Neon */
        letter-spacing: 5px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    .vault-sub {
        text-align: center;
        color: rgba(0, 255, 65, 0.7);
        margin-bottom: 40px;
        font-size: 1.1rem;
        letter-spacing: 2px;
    }
    
    /* MODIFIKASI WIDGET STREAMLIT (Radio & Selectbox) */
    .stRadio > label, .stSelectbox > label, .stTextArea > label {
        color: var(--neon-green) !important;
    }
    /* Warna teks pilihan radio button */
    .stRadio div[role='radiogroup'] > label > div:first-child {
        color: var(--neon-green);
    }

    /* INPUT AREAS (Tempat ketik pesan) */
    .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important;
        color: var(--neon-green) !important;
        border: 2px solid var(--neon-green) !important;
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.1rem;
        border-radius: 0px; /* Kotak tajam ala terminal */
        box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.2);
    }
    .stTextArea > div > div > textarea:focus {
        box-shadow: 0 0 15px var(--neon-green);
    }

    /* BUTTONS */
    .stButton > button {
        background: black;
        border: 2px solid var(--neon-green);
        color: var(--neon-green);
        font-weight: bold;
        font-family: 'Share Tech Mono', monospace;
        padding: 15px;
        text-transform: uppercase;
        letter-spacing: 3px;
        width: 100%;
        transition: 0.2s;
        border-radius: 0; /* Kotak tajam */
    }
    .stButton > button:hover {
        background: var(--neon-green);
        color: black;
        box-shadow: 0 0 30px var(--neon-green);
        font-weight: 900;
    }

    /* RESULT BOX */
    .result-container {
        border: 2px solid var(--neon-green);
        background: rgba(0, 255, 65, 0.05);
        padding: 20px;
        margin-top: 20px;
        border-radius: 0px;
        position: relative;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    }
    .result-label {
        color: var(--neon-green);
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        font-weight: bold;
        border-bottom: 1px dashed var(--neon-green);
        display: inline-block;
    }
    .result-text {
        color: white;
        font-family: 'Share Tech Mono', monospace;
        word-break: break-all;
        font-size: 1.3rem;
        margin-top: 15px;
        text-shadow: 0 0 5px white;
    }

    /* HIDE UI */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- FUNGSI ENKRIPSI (LOGIKA SAMA) ---
def encrypt_message(text, method):
    if method == "BINARY (0101)":
        return ' '.join(format(ord(char), '08b') for char in text)
    elif method == "HEXADECIMAL":
        return text.encode('utf-8').hex().upper()
    elif method == "BASE64 (SECURE)":
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif method == "REVERSE (MIRROR)":
        return text[::-1]
    return text

def decrypt_message(text, method):
    try:
        if method == "BINARY (0101)":
            return ''.join(chr(int(b, 2)) for b in text.split(' '))
        elif method == "HEXADECIMAL":
            return bytes.fromhex(text).decode('utf-8')
        elif method == "BASE64 (SECURE)":
            return base64.b64decode(text.encode('utf-8')).decode('utf-8')
        elif method == "REVERSE (MIRROR)":
            return text[::-1]
    except:
        return "ERROR: INVALID CODE FORMAT - DECRYPTION FAILED"
    return text

# --- HALAMAN UTAMA ---
st.markdown("<div class='vault-header'>CYBER VAULT</div>", unsafe_allow_html=True)
st.markdown("<div class='vault-sub'>// SECURE TERMINAL UPLINK //</div>", unsafe_allow_html=True)

# Pilihan Mode
# Menggunakan st.radio dengan label yang jelas
mode = st.radio("SELECT OPERATION MODE >>", ["ENCRYPT (LOCK DATA)", "DECRYPT (UNLOCK DATA)"], horizontal=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Box
input_text = st.text_area("ENTER INPUT STREAM >>", height=150, placeholder="Awaiting command input...")

# Pilihan Metode
method = st.selectbox("SELECT ALGORITHM >>", ["BINARY (0101)", "HEXADECIMAL", "BASE64 (SECURE)", "REVERSE (MIRROR)"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("[ EXECUTE ]"):
    if input_text:
        # Efek spinner loading
        with st.spinner("PROCESSING BITSTREAM..."):
            time.sleep(0.5) # Sedikit delay biar kerasa loadingnya
            if "ENCRYPT" in mode:
                result = encrypt_message(input_text, method)
                label = "ENCRYPTED OUTPUT >>"
            else:
                result = decrypt_message(input_text, method)
                label = "DECRYPTED MESSAGE >>"
            
            st.markdown(f"""
            <div class='result-container'>
                <div class='result-label'>{label}</div>
                <div class='result-text'>{result}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("ERROR: NO INPUT DATA DETECTED.")

# Footer
st.markdown("<br><br><div style='text-align: center; color: #00ff41; opacity: 0.5; font-size: 0.8rem;'>TERMINAL V.2.2 | ENCRYPTED CONNECTION ESTABLISHED</div>", unsafe_allow_html=True)
