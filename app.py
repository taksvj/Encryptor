import streamlit as st
import base64
import random
import string
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CYBER VAULT // RED CODE",
    page_icon="🛑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- GLOBAL CSS & BACKGROUND ---
st.markdown("""
<style>
    /* 1. Reset & Font */
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    @import url('https://fonts.googleapis.com/css?family=Consolas');

    :root {
        --red-glow: #f00;
        --red-dark: #411;
        --bg-black: #111;
    }

    .stApp {
        background-color: var(--bg-black);
        font-family: 'Consolas', 'Courier', monospace;
        color: var(--red-glow);
    }

    /* 2. Matrix Canvas (Background) */
    #matrix-canvas {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0; opacity: 0.3; pointer-events: none;
    }

    /* 3. Kontainer Utama */
    .main .block-container {
        z-index: 1; position: relative;
        background: rgba(17, 0, 0, 0.8);
        border: 1px solid var(--red-dark);
        padding: 30px; 
        box-shadow: 0 0 50px rgba(255, 0, 0, 0.2);
        margin-top: 50px;
    }

    /* 4. Header Style */
    .vault-header {
        text-align: center;
        font-size: 50px; 
        font-weight: bold;
        color: var(--red-glow);
        text-shadow: 0 0 15px var(--red-glow);
        margin-bottom: 5px;
        text-transform: uppercase;
        font-family: 'Consolas', monospace;
    }
    
    .vault-sub {
        text-align: center;
        color: var(--red-dark);
        text-shadow: 0 0 5px var(--red-dark);
        font-size: 18px;
        margin-bottom: 30px;
        font-family: 'Share Tech Mono', monospace;
    }

    /* 5. Input Fields */
    .stTextArea > div > div > textarea {
        background-color: #050000 !important; 
        color: var(--red-glow) !important;
        border: 1px solid var(--red-dark) !important;
        font-family: 'Consolas', monospace;
        font-size: 1.1rem;
    }
    
    /* 6. Buttons */
    .stButton > button {
        background: #000; 
        border: 2px solid var(--red-glow); 
        color: var(--red-glow);
        font-family: 'Consolas', monospace; 
        font-weight: bold; 
        padding: 15px; 
        width: 100%;
        text-transform: uppercase; 
        transition: 0.3s;
        font-size: 18px;
        text-shadow: 0 0 5px var(--red-glow);
    }
    .stButton > button:hover {
        background: var(--red-glow); 
        color: #000; 
        box-shadow: 0 0 30px var(--red-glow);
    }
    
    /* 7. Dropdown */
    .stSelectbox > div > div {
        background-color: #050000 !important;
        color: var(--red-glow) !important;
    }

    /* HIDE UI */
    #MainMenu, footer, header {visibility: hidden;}
</style>

<canvas id="matrix-canvas"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789SYSTEMFAILURE';
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];
    for(let x = 0; x < columns; x++) drops[x] = 1;

    function draw() {
        ctx.fillStyle = 'rgba(17, 0, 0, 0.1)'; 
        ctx.fillRect(0, 0, canvas.width, canvas.height);
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
        return "FATAL ERROR"
    return text

# --- FUNGSI ANIMASI DECODE (ADAPTASI DARI KODEMU) ---
def render_red_decode(final_text, label):
    # Sanitize input untuk JS
    safe_text = final_text.replace("'", "\\'").replace("\n", " ")
    
    # HTML + JS (Vanilla Version of your jQuery code)
    html_code = f"""
    <style>
        body {{
            background: transparent;
            color: #411;
            font-family: Consolas, Courier, monospace;
            /* Font size disesuaikan agar muat di container */
            font-size: 24px; 
            text-shadow: 0 0 15px #411;
            margin: 0; padding: 0;
            text-align: center;
        }}
        .loading-container {{
            position: relative;
            text-align: center;
            margin-top: 20px;
            word-wrap: break-word;
        }}
        .glow {{
            color: #f00;
            text-shadow: 0px 0px 10px #f00;
        }}
        span {{
            display: inline-block;
            padding: 0 2px;
        }}
        .label {{
            color: #411;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
            font-weight: bold;
        }}
    </style>

    <div class="label">{label}</div>
    <div id="loading" class="loading-container">{safe_text}</div>

    <script>
    (function() {{
        var alphabet = new Array("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0");
        var letter_count = 0;
        var el = document.getElementById("loading");
        var word = el.innerText.trim();
        var finished = false;

        el.innerHTML = "";
        for (var i = 0; i < word.length; i++) {{
            var span = document.createElement("span");
            span.innerHTML = word.charAt(i);
            el.appendChild(span);
        }}

        // Fungsi mengacak huruf
        function write() {{
            var spans = el.getElementsByTagName("span");
            for (var i = letter_count; i < word.length; i++) {{
                var c = Math.floor(Math.random() * 36);
                spans[i].innerHTML = alphabet[c];
            }}
            if (!finished) {{
                setTimeout(write, 75);
            }}
        }}

        // Fungsi mengunci huruf satu per satu
        function inc() {{
            var spans = el.getElementsByTagName("span");
            spans[letter_count].innerHTML = word[letter_count];
            spans[letter_count].classList.add("glow");
            letter_count++;
            if (letter_count >= word.length) {{
                finished = true;
            }} else {{
                setTimeout(inc, 150); // Kecepatan lock huruf (ms)
            }}
        }}

        // Jalankan
        write();
        setTimeout(inc, 500); 
    }})();
    </script>
    """
    st.components.v1.html(html_code, height=300, scrolling=True)


# --- MAIN UI ---
st.markdown("<div class='vault-header'>RED CODE</div>", unsafe_allow_html=True)
st.markdown("<div class='vault-sub'>CRITICAL FAILURE // SYSTEM OVERRIDE</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("PROTOCOL", ["ENCRYPT", "DECRYPT"])
with col2:
    method = st.selectbox("ALGORITHM", ["BINARY", "HEX", "BASE64", "REVERSE"])

input_text = st.text_area("", placeholder="INSERT MALICIOUS CODE...", height=100)

if st.button("EXECUTE OVERRIDE"):
    if input_text:
        result = process_text(input_text, method, mode)
        label_text = f"// TARGET: {mode}ED_PAYLOAD"
        
        # Panggil animasi JS
        render_red_decode(result, label_text)
    else:
        st.error("NO TARGET DETECTED.")
