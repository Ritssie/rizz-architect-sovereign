import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import time

# ==============================================================================
# --- 1. CORE CONFIGURATION & STABILITY ---
# ==============================================================================
# We stellen de pagina in met een wide layout voor een dashboard-gevoel.
st.set_page_config(
    page_title="Rizz Architect Ultra 3.0 | Sovereign Systems",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiseer session state: dit voorkomt dat data verdwijnt bij interactie.
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'system_ready' not in st.session_state:
    st.session_state.system_ready = False

# ==============================================================================
# --- 2. ADVANCED SOVEREIGN UI (CSS & ANIMATIES) ---
# ==============================================================================
# Deze sectie zorgt voor de high-end, dark-mode esthetiek van de app.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Achtergrond en Basis Kleuren */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #020202 !important;
        color: #f0f0f0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Branding */
    .brand-header { text-align: center; padding: 40px 0 10px 0; }
    .main-title {
        font-weight: 900; font-size: 3.2rem; letter-spacing: -3px;
        background: linear-gradient(180deg, #FFFFFF 0%, #333333 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .version-tag {
        font-family: 'JetBrains Mono', monospace; color: #FFD700;
        font-size: 0.7rem; letter-spacing: 5px; text-transform: uppercase;
        margin-bottom: 30px; opacity: 0.8;
    }

    /* De Gauge (Succes Meter) */
    .gauge-container {
        position: relative; width: 220px; height: 110px; margin: 20px auto;
        overflow: hidden; border-bottom: 2px solid #222;
    }
    .gauge-arc {
        width: 220px; height: 220px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 68%, black 69%);
        -webkit-mask: radial-gradient(circle, transparent 68%, black 69%);
    }
    .gauge-needle {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 85px;
        background: #fff; border-radius: 4px; transform-origin: bottom center;
        transition: transform 2s cubic-bezier(0.19, 1, 0.22, 1);
        box-shadow: 0 0 10px rgba(255,255,255,0.5);
    }

    /* Flag Systeem */
    .flag-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }
    .pill {
        padding: 5px 12px; border-radius: 4px; font-family: 'JetBrains Mono';
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
    }
    .pill-green { background: rgba(0, 230, 118, 0.1); color: #00e676; border: 1px solid #00e67633; }
    .pill-red { background: rgba(248, 113, 113, 0.1); color: #f87171; border: 1px solid #f8717133; }

    /* Tactical Cards */
    .rizz-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
        transition: 0.3s ease;
    }
    .rizz-card:hover { border-color: #FFD700; background: rgba(255, 215, 0, 0.02); }
    .winner-box { border: 1px solid #FFD700 !important; background: rgba(255, 215, 0, 0.04) !important; }
    
    /* Button Styling */
    .stButton>button {
        width: 100%; background: #fff !important; color: #000 !important;
        font-weight: 800; border-radius: 8px; border: none; height: 3.2rem;
    }

    /* Verberg standaard Streamlit elementen voor cleaner uiterlijk */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. CORE LOGIC & API WRAPPERS ---
# ==============================================================================

def prepare_image(image_file):
    """Verwerkt de afbeelding naar base64 voor de vision API."""
    try:
        img = Image.open(image_file).convert('RGB')
        # We verkleinen de foto iets voor snellere API response
        img.thumbnail((1000, 1000))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.error(f"Fout bij beeldverwerking: {e}")
        return None

def call_architect_engine(api_key, b64_img, context_text):
    """Roept de Grok-4-1-fast-reasoning engine aan met strikte JSON output."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # CRITIEK: Geen emoji's in deze string om ASCII errors te voorkomen!
    system_prompt = (
        "Role: Rizz Architect Ultra 3.0. You are a strategic dating expert. "
        "Goal: Analyze the chat screenshot and provide the best move to secure a date. "
        "Analysis: Determine platform vibe, investment ratio, and psychological subtext. "
        "Safety: Identify Green Flags (engagement) and Red Flags (warning signs). "
        "Response Options: Provide 3 distinct options: Playful Provocateur, Elegant Direct, and Pattern Interrupt. "
        "Constraint: Max 20 words per message. Only 1 emoji per message. "
        "Return ONLY a JSON object with: success_rate (int), green_flags (list), red_flags (list), "
        "options (list of {type, text}), verdict_idx (int), reasoning (str)."
    )

    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning", # Gebruik van de reasoning engine
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {context_text}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Architect Engine Error: {str(e)}")
        return None

# ==============================================================================
# --- 4. APP INTERFACE ---
# ==============================================================================

# Header
st.markdown('<div class="brand-header"><div class="main-title">RIZZ ARCHITECT</div><div class="version-tag">Ultra 3.0 // Sovereign Edition</div></div>', unsafe_allow_html=True)

# Sidebar voor configuratie
with st.sidebar:
    st.markdown("### 🛠️ SYSTEM STATUS")
    api_key_input = st.text_input("Grok API Key", type="password", help="Je xAI API Sleutel")
    st.markdown("---")
    
    if st.button("🔄 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("<br><br>" * 5, unsafe_allow_html=True)
    st.caption("v19.0 Stable Build | Encrypted Protocol")

# Main Content Layout
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("#### 📥 DATA SOURCE")
    uploaded_file = st.file_uploader("Upload Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True, caption="Source Screenshot")
    
    user_context = st.text_area("MISSION BRIEFING", placeholder="Bijv: 'We hebben gematcht op Insta, ze reageert traag maar stelt wel vragen.'", height=100)
    
    if st.button("EXECUTE ANALYSIS"):
        if not api_key_input:
            st.error("Voer eerst je API key in.")
        elif not uploaded_file:
            st.error("Upload een screenshot.")
        else:
            with st.spinner("Decoding social signals..."):
                img_encoded = prepare_image(uploaded_file)
                if img_encoded:
                    result = call_architect_engine(api_key_input, img_encoded, user_context)
                    if result:
                        st.session_state.analysis_result = result
                        st.rerun()

with col_right:
    st.markdown("#### 📡 STRATEGIC OUTPUT")
    
    if st.session_state.analysis_result:
        res = st.session_state.analysis_result
        
        # 1. De Gauge (Succes Meter)
        prob = res.get('success_rate', 0)
        needle_rot = (prob * 1.8) - 90 # Bereken graden voor CSS
        
        st.markdown(f"""
            <div class="gauge-container">
                <div class="gauge-arc"></div>
                <div class="gauge-needle" style="transform: translateX(-50%) rotate({needle_rot}deg);"></div>
            </div>
            <div style="text-align:center; margin-top:-10px; font-weight:800; color:#FFD700; font-size:1.3rem;">
                {prob}% SUCCESS PROBABILITY
            </div>
        """, unsafe_allow_html=True)

        # 2. Health Check (Red & Green Flags)
        st.markdown("<br><b>SOCIAL HEALTH CHECK:</b>", unsafe_allow_html=True)
        st.markdown('<div class="flag-grid">', unsafe_allow_html=True)
        for gf in res.get('green_flags', []):
            st.markdown(f'<div class="pill pill-green">✔ {gf}</div>', unsafe_allow_html=True)
        for rf in res.get('red_flags', []):
            st.markdown(f'<div class="pill pill-red">✘ {rf}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 3. Text Opties
        st.markdown("<br><b>TACTICAL DIMENSIONS:</b>", unsafe_allow_html=True)
        opts = res.get('options', [])
        winner = res.get('verdict_idx', 0)
        
        for idx, o in enumerate(opts):
            is_win = (idx == winner)
            card_class = "rizz-card winner-box" if is_win else "rizz-card"
            title = "🏆 ARCHITECT'S CHOICE" if is_win else o['type'].upper()
            
            st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-family:'JetBrains Mono'; font-size:0.6rem; color:#FFD700; letter-spacing:2px; margin-bottom:5px;">{title}</div>
                    <div style="font-size:1.1rem; color:#fff; font-weight:600;">"{o['text']}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(o['text'], language=None)

        # 4. Psychologische Onderbouwing
        st.markdown("<br><b>ARCHITECT'S VERDICT:</b>", unsafe_allow_html=True)
        st.info(res.get('reasoning', 'Geen verdere analyse beschikbaar.'))

    else:
        st.markdown("""
            <div style="height:400px; display:flex; align-items:center; justify-content:center; border:1px dashed #333; border-radius:12px; opacity:0.4;">
                Awaiting input data...
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><div style='text-align:center; opacity:0.1; font-size:0.6rem;'>PRECISION ENGINE v19.0 PRO | NO DATA LOGGING ACTIVE</div>", unsafe_allow_html=True)
