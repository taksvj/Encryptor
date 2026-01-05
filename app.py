import streamlit as st
import base64
import time
import random
import string

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER VAULT // MATRIX",
    page_icon="matrix",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INJECT MATRIX RAIN (JS + CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    :root {
        --neon-green: #0F0;
        --dark-green: #003b00;
    }

    /* Reset Streamlit UI biar transparan */
    .stApp {
        background-color: black;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Canvas Matrix ditaruh di paling belakang */
    #matrix-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0; /* Di belakang konten */
        opacity: 0.8;
    }

    /* KONTAINER KONTEN (Supaya ada di atas matrix) */
    .main .block-container {
        z-index: 1;
        position: relative;
        background: rgba(0, 0, 0, 0.7); /* Background semi-transparan biar teks kebaca */
        border: 1px solid #003300;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 0 50px rgba(0, 255, 0, 0.1);
        margin-top: 50px;
    }

    /* HEADER */
    .vault-header {
        text-align: center;
        font-size: 3.5rem; font-weight: bold; color: var(--neon-green);
        text-shadow: 0 0 10px var(--neon-green); letter-spacing: 5px;
        margin-bottom: 5px; text-transform: uppercase;
    }
    .vault-sub {
        text-align: center; color: white; margin-bottom: 30px;
        font-size: 1rem; letter-spacing: 3px; opacity: 0.8;
    }

    /* INPUT & WIDGETS */
    .stTextArea > div > div > textarea {
        background-color: rgba(0, 20, 0, 0.8) !important; 
        color: var(--neon-green) !important;
        border: 1px solid var(--neon-green) !important;
        font-family: 'Share Tech Mono', monospace;
    }
    .stSelectbox > div > div {
        background-color: rgba(0, 20, 0, 0.8) !important;
        color: var(--neon-green) !important;
    }
    
    /* BUTTON */
    .stButton > button {
        background: black; border: 2px solid var(--neon-green); color: var(--neon-green);
        font-family: 'Share Tech Mono', monospace; font-weight: bold;
        padding: 15px; width: 100%; transition: 0.3s;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton > button:hover {
        background: var(--neon-green); color: black;
        box-shadow: 0 0 20px var(--neon-green);
    }

    /* RESULT BOX */
    .result-container {
        border-left: 5px solid var(--neon-green);
        background: rgba(0, 50, 0, 0.5);
        padding: 15px; margin-top: 20px;
    }
    .result-text {
        color: white; font-size: 1.2rem; word-break: break-all;
        font-family: 'Share Tech Mono', monospace;
    }

    /* HIDE DEFAULT UI */
    #MainMenu, footer, header {visibility: hidden;}
</style>

<canvas id="matrix-canvas"></canvas>

<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');

    // Set ukuran canvas full screen
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Karakter: Katakana + Latin + Angka
    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポ';
    const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const nums = '0123456789';
    const alphabet = katakana + latin + nums;

    const fontSize = 16;
    const columns = canvas.width / fontSize;

    const drops = [];
    // Inisialisasi posisi drop (semua mulai dari atas y=1)
    for(let x = 0; x < columns; x++) {
        drops[x] = 1;
    }

    const draw = () => {
        // Efek trail (jejak) dengan menimpa warna hitam transparansi rendah
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#0F0'; // Warna Hijau Matrix
        ctx.font = fontSize + 'px monospace';

        for(let i = 0; i < drops.length; i++) {
            const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            // Reset drop ke atas secara acak setelah keluar layar
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    };

    // Jalankan animasi (30fps)
    setInterval(draw, 33);

    // Resize handler biar gak gepeng kalau window diubah
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", unsafe_allow_html=True)

# --- PYTHON LOGIC (SAMA SEPERTI SEBELUMNYA) ---
def encrypt_message(text, method):
    if method == "BINARY": return ' '.join(format(ord(char), '08b') for char in text)
    elif method == "HEX": return text.encode('utf-8').hex().upper()
    elif method == "BASE64": return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    elif method == "REVERSE": return text[::-1]
    return text

def decrypt_message(text, method):
    try:
        if method == "BINARY": return ''.join(chr(int(b, 2)) for b in text.split(' '))
        elif method == "HEX": return bytes.fromhex(text).decode('utf-8')
        elif method == "BASE64": return base64.b64decode(text.encode('utf-8')).decode('utf-8')
        elif method == "REVERSE": return text[::-1]
    except: return "DECRYPTION ERROR"
    return text

def animate_scramble(final_text, placeholder, label):
    chars = string.ascii_letters + string.digits + "@#$%"
    length = min(len(final_text), 50)
    
    for _ in range(15):
        random_str = ''.join(random.choice(chars) for _ in range(length))
        placeholder.markdown(f"""
        <div class='result-container'>
            <div style='color:#0F0; font-size:0.8rem;'>DECODING...</div>
            <div class='result-text' style='opacity:0.5'>{random_str}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.05)

    placeholder.markdown(f"""
    <div class='result-container'>
        <div style='color:#0F0; font-size:0.8rem;'>{label}</div>
        <div class='result-text'>{final_text}</div>
    </div>
    """, unsafe_allow_html=True)

# --- UI CONTENT ---
st.markdown("<div class='vault-header'>THE MATRIX</div>", unsafe_allow_html=True)
st.markdown("<div class='vault-sub'>FOLLOW THE WHITE RABBIT.</div>", unsafe_allow_html=True)

mode = st.radio("", ["ENCRYPT", "DECRYPT"], horizontal=True)

input_text = st.text_area("", placeholder="Enter your code...", height=100)
method = st.selectbox("", ["BINARY", "HEX", "BASE64", "REVERSE"])

result_area = st.empty()

if st.button("ENTER THE MATRIX"):
    if input_text:
        if mode == "ENCRYPT":
            res = encrypt_message(input_text, method)
            lbl = "ENCRYPTED DATA"
        else:
            res = decrypt_message(input_text, method)
            lbl = "DECRYPTED DATA"
        
        animate_scramble(res, result_area, lbl)
