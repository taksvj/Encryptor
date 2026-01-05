import streamlit as st
import base64
import random
import string

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER VAULT // DECODER",
    page_icon="🔓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS & JS INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    :root {
        --neon-green: #00ff41;
        --bg-black: #000;
    }

    /* BACKGROUND & RESET */
    .stApp {
        background-color: var(--bg-black);
        font-family: 'Share Tech Mono', monospace;
    }
    
    #matrix-canvas {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0; opacity: 0.8;
    }

    /* KONTAINER UTAMA (Glassmorphism) */
    .main .block-container {
        z-index: 1; position: relative;
        background: rgba(0, 10, 0, 0.85);
        border: 1px solid var(--neon-green);
        padding: 30px; border-radius: 5px;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
        margin-top: 50px;
    }

    /* HEADER */
    .vault-header {
        text-align: center; font-size: 3rem; font-weight: bold; color: var(--neon-green);
        text-shadow: 0 0 10px var(--neon-green); letter-spacing: 5px; margin-bottom: 5px;
    }

    /* INPUT STYLES */
    .stTextArea > div > div > textarea {
        background-color: #050505 !important; color: var(--neon-green) !important;
        border: 1px solid var(--neon-green) !important; font-family: 'Share Tech Mono', monospace;
    }
    .stButton > button {
        background: black; border: 2px solid var(--neon-green); color: var(--neon-green);
        font-family: 'Share Tech Mono', monospace; font-weight: bold; padding: 15px; width: 100%;
        text-transform: uppercase; letter-spacing: 2px; transition: 0.3s;
    }
    .stButton > button:hover {
        background: var(--neon-green); color: black; box-shadow: 0 0 20px var(--neon-green);
    }

    /* --- DECODE TEXT ANIMATION CSS (ADAPTED FROM YOUR REQUEST) --- */
    .decode-text {
        width: 100%;
        font-size: 24px;
        text-align: center;
        margin-top: 20px;
        min-height: 60px;
    }
    
    .text-animation {
        display: inline-block;
        position: relative;
        color: transparent; /* Awalnya transparan */
        text-transform: uppercase;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
    }

    /* Pseudo-element untuk Kursor Blok */
    .text-animation:before {
        content: "";
        color: black;
        position: absolute;
        top: 50%;
        left: 50%;
        background: var(--neon-green); /* Warna Kursor Hijau */
        width: 0;
        height: 1.2em;
        transform: translate(-50%, -55%);
    }

    /* STATE 1: Kursor Muncul Tipis */
    .text-animation.state-1:before {
        width: 1px;
    }

    /* STATE 2: Kursor Melebar (Blok Penuh) */
    .text-animation.state-2:before {
        width: 0.9em;
    }

    /* STATE 3: Teks Muncul, Kursor Hilang */
    .text-animation.state-3 {
        color: var(--neon-green); /* Teks jadi Hijau */
    }
    .text-animation.state-3:before {
        width: 0;
    }

    /* Label Hasil */
    .result-label {
        color: white; font-size: 0.9rem; text-align: center; 
        opacity: 0.7; margin-top: 20px; text-transform: uppercase;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>

<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const alphabet = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプ0123456789';
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) drops[x] = 1;

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0F0';
        ctx.font = fontSize + 'px monospace';
        for(let i = 0; i < drops.length; i++) {
            const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 33);
    window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
</script>
""", unsafe_allow_html=True)

# --- LOGIKA ENKRIPSI ---
def process_text(text, method, mode):
    try:
        if mode == "ENCRYPT":
            if method == "BINARY": return ' '.join(format(ord(char), '08b') for char in text)
            if method == "HEX": return text.encode('utf-8').hex().upper()
            if method == "BASE64": return base64.b64encode(text.encode('utf-8')).decode('utf-8')
            if method == "REVERSE": return text[::-1]
        else: # DECRYPT
            if method == "BINARY": return ''.join(chr(int(b, 2)) for b in text.split(' '))
            if method == "HEX": return bytes.fromhex(text).decode('utf-8')
            if method == "BASE64": return base64.b64decode(text.encode('utf-8')).decode('utf-8')
            if method == "REVERSE": return text[::-1]
    except:
        return "ERROR: DATA CORRUPTED"
    return text

# --- FUNGSI ANIMASI DECODE (JS INJECTION) ---
def render_decode_animation(final_text, label):
    # Kita sanitize text dulu biar aman masuk ke JS string
    safe_text = final_text.replace("'", "\\'").replace("\n", " ")
    
    # HTML + JS untuk animasi per huruf
    html_code = f"""
    <div class="result-label">{label}</div>
    <div id="decode-container" class="decode-text"></div>
    
    <script>
        (function() {{
            var textStr = '{safe_text}';
            var container = document.getElementById("decode-container");
            container.innerHTML = ''; // Reset container
            
            var splitText = textStr.split("");
            
            // 1. Buat span untuk setiap huruf (Awalnya kosong/transparan)
            splitText.forEach(function(char) {{
                var span = document.createElement("span");
                span.className = "text-animation";
                span.innerHTML = (char === " ") ? "&nbsp;" : char;
                container.appendChild(span);
            }});
            
            var spans = container.getElementsByClassName("text-animation");
            
            // 2. Fungsi Jalankan Animasi Berurutan
            var i = 0;
            function animateChar() {{
                if (i < spans.length) {{
                    var s = spans[i];
                    
                    // Tambah state-1 (Kursor tipis)
                    s.classList.add("state-1");
                    
                    setTimeout(function() {{
                        // Tambah state-2 (Kursor blok penuh)
                        s.classList.add("state-2");
                        
                        setTimeout(function() {{
                            // Tambah state-3 (Reveal huruf, kursor hilang)
                            s.classList.add("state-3");
                            
                            // Lanjut ke huruf berikutnya
                            i++;
                            animateChar();
                            
                        }}, 50); // Durasi blok penuh
                    }}, 50); // Durasi kursor tipis
                }}
            }}
            
            // Mulai animasi
            animateChar();
        }})();
    </script>
    """
    st.components.v1.html(html_code, height=200, scrolling=True)


# --- MAIN UI ---
st.markdown("<div class='vault-header'>CYBER VAULT</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("OPERATION MODE", ["ENCRYPT", "DECRYPT"])
with col2:
    method = st.selectbox("ALGORITHM", ["BINARY", "HEX", "BASE64", "REVERSE"])

input_text = st.text_area("", placeholder="ENTER DATA STREAM...", height=100)

if st.button("EXECUTE PROCESS"):
    if input_text:
        result = process_text(input_text, method, mode)
        label_text = f"// OUTPUT: {method} {mode}ED DATA"
        
        # Panggil Animasi Keren Kamu
        render_decode_animation(result, label_text)
    else:
        st.error("NO INPUT DETECTED.")
