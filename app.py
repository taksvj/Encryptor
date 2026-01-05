import streamlit as st
import base64
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="~/vault",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- HYPRLAND THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --base: #1e1e2e;
        --mantle: #181825;
        --surface0: #313244;
        --text: #cdd6f4;
        --blue: #89b4fa;
        --mauve: #cba6f7;
        --overlay: rgba(30, 30, 46, 0.7);
    }

    .stApp {
        background-color: var(--base);
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        background-size: cover;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text);
    }

    /* GLASS CONTAINER */
    .main .block-container {
        background: var(--overlay);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(137, 180, 250, 0.2);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        margin-top: 50px;
    }

    /* HEADER */
    .waybar-header {
        display: flex; justify-content: space-between; align-items: center;
        background: var(--surface0); padding: 10px 20px; border-radius: 15px;
        margin-bottom: 30px; border: 1px solid rgba(255,255,255,0.05);
    }
    .arch-logo { color: var(--blue); font-weight: bold; font-size: 1.2rem; }
    .window-title { color: var(--text); font-size: 0.9rem; opacity: 0.8; }
    .dots { display: flex; gap: 8px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background: #f38ba8; } .dot-yellow { background: #f9e2af; } .dot-green { background: #a6e3a1; }

    /* INPUTS & BUTTONS */
    .stTextArea > div > div > textarea {
        background-color: var(--mantle) !important; color: var(--text) !important;
        border: 2px solid var(--surface0) !important; border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--blue), var(--mauve)); color: var(--base);
        border: none; border-radius: 12px; padding: 12px; font-weight: bold;
        transition: 0.3s all; width: 100%;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(137, 180, 250, 0.4); color: white; }
    .stSelectbox > div > div { background-color: var(--mantle) !important; color: var(--text) !important; border-radius: 10px; border: none; }

    /* OUTPUT BOX STYLE */
    .hyprland-box {
        background: #11111b;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid var(--surface0);
        position: relative;
        font-family: 'JetBrains Mono', monospace;
        min-height: 80px;
    }
    .hyprland-label {
        position: absolute; top: -10px; left: 15px;
        background: var(--mauve); color: var(--base);
        padding: 2px 10px; border-radius: 5px;
        font-size: 0.7rem; font-weight: bold;
    }
    .typed-text {
        color: var(--blue);
        font-size: 1.1rem;
        word-wrap: break-word;
        white-space: pre-wrap;
    }
    .cursor {
        display: inline-block; width: 8px; height: 1em;
        background: var(--mauve); animation: blink 1s step-end infinite;
    }
    @keyframes blink { 50% { opacity: 0; } }

    /* SOCIAL BAR STYLE */
    .social-bar {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px dashed rgba(255,255,255,0.1);
    }
    .social-link {
        text-decoration: none;
        display: inline-block;
        transition: 0.3s transform;
    }
    /* Style untuk Gambar Base64 */
    .social-icon-img {
        width: 24px;
        height: 24px;
        opacity: 0.6;
        transition: 0.3s all;
        filter: invert(86%) sepia(6%) saturate(1393%) hue-rotate(194deg) brightness(98%) contrast(92%); /* Warna text Hyprland */
    }
    .social-link:hover .social-icon-img {
        opacity: 1;
        transform: scale(1.2);
        filter: invert(76%) sepia(35%) saturate(544%) hue-rotate(213deg) brightness(101%) contrast(93%); /* Warna Mauve saat hover */
        drop-shadow(0 0 5px rgba(203, 166, 247, 0.8));
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="waybar-header">
    <div class="dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
    <div class="window-title"> ~/arch/vault/encryptor.sh</div>
    <div class="arch-logo">HYPR</div>
</div>
""", unsafe_allow_html=True)

# --- LOGIC ---
def process_text(text, method, mode):
    try:
        if mode == "encrypt":
            if method == "binary": return ' '.join(format(ord(char), '08b') for char in text)
            if method == "hex": return text.encode('utf-8').hex()
            if method == "base64": return base64.b64encode(text.encode('utf-8')).decode('utf-8')
            if method == "reverse": return text[::-1]
        else:
            if method == "binary":
                clean_text = text.replace(" ", "").replace("\n", "")
                byte_chunks = [clean_text[i:i+8] for i in range(0, len(clean_text), 8)]
                return ''.join(chr(int(b, 2)) for b in byte_chunks)
            if method == "hex": return bytes.fromhex(text).decode('utf-8')
            if method == "base64": return base64.b64decode(text.encode('utf-8')).decode('utf-8')
            if method == "reverse": return text[::-1]
    except: return "error: segmentation fault"
    return text

# --- UI CONTENT ---
col1, col2 = st.columns([1, 2])
with col1: mode = st.selectbox("mode", ["encrypt", "decrypt"])
with col2: method = st.selectbox("algorithm", ["binary", "hex", "base64", "reverse"])

input_text = st.text_area("", placeholder="echo 'insert_text_here'...", height=120)

result_placeholder = st.empty()

if st.button("sh run_process.sh"):
    if input_text:
        result_text = process_text(input_text, method, mode)
        label_txt = f"stdout >> {method}"
        
        displayed_text = ""
        result_placeholder.markdown(f"""
        <div class="hyprland-box">
            <div class="hyprland-label">{label_txt}</div>
            <span class="typed-text"></span><span class="cursor"></span>
        </div>
        """, unsafe_allow_html=True)
        
        for char in result_text:
            displayed_text += char
            result_placeholder.markdown(f"""
            <div class="hyprland-box">
                <div class="hyprland-label">{label_txt}</div>
                <span class="typed-text">{displayed_text}</span><span class="cursor"></span>
            </div>
            """, unsafe_allow_html=True)
            delay = 0.02 if len(result_text) > 50 else 0.05
            time.sleep(delay)
            
    else:
        st.error("stdin is empty")

# --- SVG ICONS (ENCODED AGAR AMAN) ---
# Saya encode SVG ke Base64 supaya parser markdown tidak bingung baca kode panjang

# Icon X (Twitter)
x_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>"""
x_b64 = base64.b64encode(x_svg.encode('utf-8')).decode('utf-8')

# Icon GitHub
gh_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775
