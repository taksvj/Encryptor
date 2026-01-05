import streamlit as st
import base64

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER VAULT // ENCRYPTOR",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS FUTURISTIC STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');

    :root {
        --primary: #00e5ff;   /* Cyan Neon */
        --secondary: #7000ff; /* Purple Neon */
        --bg: #050510;
        --card-bg: rgba(255, 255, 255, 0.05);
    }

    .stApp {
        background-color: var(--bg);
        color: white;
        font-family: 'Rajdhani', sans-serif;
        background-image: radial-gradient(circle at 50% 50%, rgba(112, 0, 255, 0.1) 0%, transparent 50%);
    }

    /* HEADER */
    .vault-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(0deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 5px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    .vault-sub {
        text-align: center;
        color: rgba(255,255,255,0.6);
        margin-bottom: 40px;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }

    /* INPUT AREAS */
    .stTextArea > div > div > textarea {
        background-color: var(--card-bg) !important;
        color: var(--primary) !important;
        border: 1px solid var(--secondary) !important;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        border-radius: 5px;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(90deg, var(--secondary), var(--primary));
        border: none;
        color: white;
        font-weight: bold;
        padding: 15px;
        text-transform: uppercase;
        letter-spacing: 3px;
        width: 100%;
        transition: 0.3s;
        border-radius: 0;
        clip-path: polygon(10% 0, 100% 0, 100% 70%, 90% 100%, 0 100%, 0 30%);
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px var(--secondary);
    }

    /* RESULT BOX */
    .result-container {
        border: 1px dashed var(--primary);
        background: rgba(0, 229, 255, 0.05);
        padding: 20px;
        margin-top: 20px;
        border-radius: 10px;
        position: relative;
    }
    .result-label {
        color: var(--secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .result-text {
        color: white;
        font-family: 'Courier New', monospace;
        word-break: break-all;
        font-size: 1.2rem;
    }

    /* HIDE UI */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- FUNGSI ENKRIPSI ---
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
        return "ERROR: INVALID CODE FORMAT"
    return text

# --- HALAMAN UTAMA ---
st.markdown("<div class='vault-header'>CYBER VAULT</div>", unsafe_allow_html=True)
st.markdown("<div class='vault-sub'>// SECURE DATA TRANSMISSION PROTOCOL //</div>", unsafe_allow_html=True)

# Pilihan Mode (Encrypt / Decrypt)
mode = st.radio("SELECT OPERATION MODE:", ["ENCRYPT (LOCK)", "DECRYPT (UNLOCK)"], horizontal=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Box
input_text = st.text_area("INPUT DATA STREAM:", height=150, placeholder="Type your secret message here...")

# Pilihan Metode
method = st.selectbox("ENCRYPTION ALGORITHM:", ["BINARY (0101)", "HEXADECIMAL", "BASE64 (SECURE)", "REVERSE (MIRROR)"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("EXECUTE PROCESS"):
    if input_text:
        with st.spinner("PROCESSING DATA..."):
            if "ENCRYPT" in mode:
                result = encrypt_message(input_text, method)
                label = "ENCRYPTED OUTPUT:"
            else:
                result = decrypt_message(input_text, method)
                label = "DECRYPTED MESSAGE:"
            
            st.markdown(f"""
            <div class='result-container'>
                <div class='result-label'>{label}</div>
                <div class='result-text'>{result}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("ERROR: NO DATA DETECTED.")

# Footer
st.markdown("<br><br><div style='text-align: center; color: #555; font-size: 0.8rem;'>SYSTEM V.2.0 | SECURE CONNECTION</div>", unsafe_allow_html=True)
