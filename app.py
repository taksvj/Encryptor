import streamlit as st
import base64
import random
import string

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER VAULT // RED ALERT",
    page_icon="🛑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS & JS INJECTION ---
st.markdown("""
<style>
    /* CSS DARI REQUEST KAMU (DIADAPTASI UNTUK STREAMLIT) */
    
    /* 1. Background & Font Utama */
    .stApp {
        background-color: #111; /* Sesuai request */
        color: #f00;            /* Default text jadi merah terang */
        font-family: Consolas, Courier, monospace; /* Sesuai request */
    }

    /* 2. Matrix Canvas di Belakang */
    #matrix-canvas {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0; opacity: 0.6; pointer-events: none;
    }

    /* 3. Kontainer Utama (Biar tulisan kebaca di atas matrix) */
    .main .block-container {
        z-index: 1; position: relative;
        background: rgba(17, 17, 17, 0.9); /* #111 dengan transparansi */
        border: 1px solid #411; /* Merah gelap */
        padding: 30px; 
        box-shadow: 0 0 30px #411; /* Shadow merah gelap */
        margin-top: 50px;
    }

    /* 4. Header Style (Mengikuti style .glow kamu) */
    .vault-header {
        text-align: center;
        font-size: 60px; /* Sesuai request */
        font-weight: bold;
        color: #f00;
        text-shadow: 0 0 15px #f00; /* Glow Effect sesuai request */
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    .vault-sub {
        text-align: center;
        color: #411; /* Merah gelap */
        text-shadow: 0 0 5px #411;
        font-size: 20px;
        margin-bottom: 30px;
    }

    /* 5. Input Fields */
    .stTextArea > div > div > textarea {
        background-color: #050505 !important; 
        color: #f00 !important;
        border: 1px solid #411 !important;
        font-family: Consolas, Courier, monospace;
        font-size: 1.2rem;
    }
    
    /* 6. Buttons */
    .stButton > button {
        background: #111; 
        border: 2px solid #f00; 
        color: #f00;
        font-family: Consolas, Courier, monospace; 
        font-weight: bold; 
        padding: 15px; 
        width: 100%;
        text-transform: uppercase; 
        transition: 0.3s;
        font-size: 20px;
        text-shadow: 0 0 5px #f00;
    }
    .stButton > button:hover {
        background: #f00; 
        color: #111; 
        box-shadow: 0 0 30px #f00;
    }

    /* 7. Dropdown & Selectbox */
    .stSelectbox > div > div {
        background-color: #111 !important;
        color: #f00 !important;
        border-color: #411 !important;
    }

    /* --- ANIMASI DECODE (Sesuai Request Sebelumnya tapi Merah) --- */
    .decode-text {
        width: 100%;
        font-size: 30px; /* Sesuai request */
        text-align: center;
        margin-top: 30px;
        min-height: 80px;
        font-family: Consolas, Courier, monospace;
    }
    
    .text-animation {
        display: inline-block;
        position: relative;
        color: transparent;
        text-transform: uppercase;
    }
    
    /* Kursor Blok Merah */
    .text-animation:before {
        content: "";
        position: absolute;
        top: 50%; left: 50%;
        background: #f00; /* Kursor Merah */
        width: 0; height: 1.2em;
        transform: translate(-50%, -55%);
        box-shadow: 0 0 10px #f00; /* Glow kursor */
    }

    /* State Animasi */
    .text-animation.state-1:before { width: 1px; }
    .text-animation.state-2:before { width: 0.9em; }
    
    /* State Akhir: Teks Muncul Merah Terang */
    .text-animation.state-3 { 
        color: #f00; 
        text-shadow: 0 0 10px #f00; /* Glow text */
    }
    .text-animation.state-3:before { width: 0; }
    
    /* Label */
    .result-label {
        color: #411; /* Merah Gelap */
        font-size: 1rem; text-align: center; 
        margin-top: 20px; text-transform: uppercase;
        font-weight: bold;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>

<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Karakter Acak
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789SYSTEMFAILURE';
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) drops[x] = 1;

    function draw() {
        // Background hitam dengan jejak transparansi
        ctx.fillStyle = 'rgba(17, 17, 17, 0.1)'; 
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // WARNA HUJAN: MERAH
        ctx.fillStyle = '#F00'; 
        ctx.font = fontSize + 'px Consolas';
        
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
        return "SYSTEM FAILURE" # Pesan Error sesuai tema
    return text

# --- FUNGSI ANIMASI DECODE (RED EDITION) ---
def render_decode_animation(final_text, label):
    safe_text = final_text.replace("'", "\\'").replace("\n", " ")
    
    html_code = f"""
    <div class="result-label">{label}</div>
    <div id="decode-container" class="decode-text"></div>
    
    <script>
        (function() {{
            var textStr = '{safe_text}';
            var container = document.getElementById("decode-container");
            container.innerHTML = '';
            
            var splitText = textStr.split("");
            
            splitText.forEach(function(char) {{
                var span = document.createElement("span");
                span.className = "text-animation";
                span.innerHTML = (char === " ") ? "&nbsp;" : char;
                container.appendChild(span);
            }});
            
            var spans = container.getElementsByClassName("text-animation");
            
            var i = 0;
            function animateChar() {{
                if (i < spans.length) {{
                    var s = spans[i];
                    s.classList.add("state-1");
                    setTimeout(function() {{
                        s.classList.add("state-2");
                        setTimeout(function() {{
                            s.classList.add("state-3");
                            i++;
                            animateChar();
                        }}, 50);
                    }}, 50);
                }}
            }}
            animateChar();
        }})();
    </script>
    """
    st.components.v1.html(html_code, height=200, scrolling=True)


# --- MAIN UI ---
st.markdown("<div class='vault-header'>RED CODE</div>", unsafe_allow_html=True)
st.markdown("<div class='vault-sub'>Unauthorized Access Detected</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("PROTOCOL", ["ENCRYPT", "DECRYPT"])
with col2:
    method = st.selectbox("ALGORITHM", ["BINARY", "HEX", "BASE64", "REVERSE"])

input_text = st.text_area("", placeholder="Inject payload...", height=100)

if st.button("INITIATE SEQUENCE"):
    if input_text:
        result = process_text(input_text, method, mode)
        label_text = f"// OUTPUT: {mode}ED_DATA"
        render_decode_animation(result, label_text)
    else:
        st.error("NO PAYLOAD DETECTED.")
