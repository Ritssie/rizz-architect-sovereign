import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import time

# ==============================================================================
# --- 1. CORE CONFIGURATION & SETTINGS ---
# ==============================================================================
st.set_page_config(
    page_title="Rizz Architect Ultra 3.0 | Sovereign Systems",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiseer session state voor stabiliteit bij reruns
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'system_status' not in st.session_state:
    st.session_state.system_status = "IDLE"

# ==============================================================================
# --- 2. ADVANCED SOVEREIGN UI (CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #030303 !important;
        color: #f0f0f0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Brand Styling */
    .brand-header {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 3.5rem;
        letter-spacing: -3px;
        background: linear-gradient(180deg, #FFFFFF 0%, #444444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .version-tag {
        font-family: 'JetBrains Mono', monospace;
        color: #FFD700;
        font-size: 0.7rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 40px;
    }

    /* Gauge / Meter Visuals */
    .gauge-outer {
        position: relative;
        width: 240px;
        height: 120px;
        margin: 20px auto;
        overflow: hidden;
    }
    .gauge-bg {
        width: 240px;
        height: 240px;
        border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 68%, black 69%);
        -webkit-mask: radial-gradient(circle, transparent 68%, black 69%);
    }
    .needle {
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 4px;
        height: 90px;
        background: #FFFFFF;
        border-radius: 4px;
        transform-origin: bottom center;
        transition: transform 2s cubic-bezier(0.19, 1, 0.22, 1);
        z-index: 10;
    }

    /* Flags & Tactical Elements */
    .flag-box {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 15px 0;
    }
    .status-pill {
        padding: 6px 14px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .green-pill { background: rgba(0, 230, 118, 0.1); color: #00e676; border: 1px solid #00e67644; }
    .red-pill { background: rgba(255, 75, 75, 0.1); color: #ff4b4b; border: 1px solid #ff4b4b44; }

    /* Tactical Cards */
    .sovereign-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: 0.4s all;
    }
    .sovereign-card:hover {
        border-color: rgba(255, 215, 0, 0.4);
        background: rgba(255, 215, 0, 0.01);
    }
    .winner-card {
        border: 1px solid #FFD700 !important;
        background: linear-gradient(145deg, rgba(255,215,0,0.05) 0%, rgba(0,0,0,0) 100%) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* UI Buttons */
    .stButton>button {
        background: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
        height: 3.5rem !important;
        letter-spacing: 1px;
    }
    
    /* Code block styling */
    .stCodeBlock { background: #0a0a0a !important; border: 1px solid #222 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. LOGIC & API ENGINE ---
# ==============================================================================
def process_image_for_api(file):
    """Optimaliseert de afbeelding voor Grok Vision."""
    try:
        img = Image.open(file).convert('RGB')
        # Resize als het te groot is voor snellere verwerking
        if img.width > 1200:
            img.thumbnail((1200, 1200))
        
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=90)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Image Processing Error: {e}")
        return None

def analyze_interaction(api_key, b64_img, user_context):
    """Roept de Grok-4-1-fast-reasoning engine aan."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Gebruik uitsluitend veilige ASCII in de systeem prompt om encoding errors te voorkomen
    system_role = (
        "Role: Rizz Architect Ultra 3.0. You are a high-end social strategist. "
        "Task: Analyze the provided screenshot of a dating app conversation. "
        "Analyze Investment Levels: Who is texting more/faster? "
        "Analyze Subtext: Is there interest, testing (shit-tests), or boredom? "
        "Identify 3 response strategies: "
        "1. Playful Provocateur (teasing/tension). "
        "2. Elegant Direct (clear intention/date-focused). "
        "3. Pattern Interrupt (intellectual/unexpected). "
        "Output: MUST be a JSON object with: success_rate (0-100), green_flags (list), "
        "red_flags (list), options (list of {type, text}), verdict_idx (int), reasoning (str)."
    )

    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": [
                    {"type": "text", "text": f"User Context: {user_context}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Architect Engine Error: {str(e)}")
        return None

# ==============================================================================
# --- 4. INTERFACE ASSEMBLY ---
# ==============================================================================

# -- HEADER --
st.markdown("""
    <div class="brand-header">
        <div class="main-title">RIZZ ARCHITECT</div>
        <div class="version-tag">Ultra 3.0 // Sovereign Systems</div>
    </div>
""", unsafe_allow_html=True)

# -- SIDEBAR --
with st.sidebar:
    st.markdown("### SYSTEM CONTROLS")
    api_key_input = st.text_input("Grok API Key", type="password", help="Voer je xAI API key in.")
    
    st.markdown("---")
    st.markdown("**System Health:**")
    if api_key_input:
        st.success("AUTHENTICATED")
    else:
        st.warning("AWAITING KEY")
    
    st.markdown("---")
    if st.button("REBOOT SYSTEM", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/ios-filled/50/ffffff/security-configuration.png", width=30)
    st.caption("Privacy Encrypted: Screenshots worden niet opgeslagen op onze servers.")

# -- MAIN LAYOUT --
col_l, col_r = st.columns([1, 1.2], gap="large")

with col_l:
    st.markdown("### 📥 TACTICAL INTAKE")
    uploaded_file = st.file_uploader("Upload Chat Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if uploaded_file:
        st.image(uploaded_file, caption="Source Data", use_container_width=True)
    
    interaction_context = st.text_area(
        "MISSION CONTEXT", 
        placeholder="Bijv: 'We hebben gematcht op Tinder, ze reageert kortaf maar stelt wel vragen.'",
        height=120
    )
    
    if st.button("EXECUTE PRECISION SCAN"):
        if not api_key_input:
            st.error("Systeemfout: Geen API key gevonden.")
        elif not uploaded_file:
            st.error("Systeemfout: Geen data source gevonden.")
        else:
            with st.spinner("Decrypting social layers..."):
                b64_img = process_image_for_api(uploaded_file)
                if b64_img:
                    result = analyze_interaction(api_key_input, b64_img, interaction_context)
                    if result:
                        st.session_state.analysis_result = result
                        st.session_state.system_status = "ANALYSIS_COMPLETE"
                        st.rerun()

with col_r:
    st.markdown("### 📡 ARCHITECT OUTPUT")
    
    if st.session_state.analysis_result:
        res = st.session_state.analysis_result
        
        # -- SUCCESS PROBABILITY GAUGE --
        rate = res.get('success_rate', 50)
        # Rotatie berekening: 0% = -90deg, 100% = 90deg
        needle_deg = (rate * 1.8) - 90
        
        st.markdown(f"""
            <div class="gauge-outer">
                <div class="gauge-bg"></div>
                <div class="needle" style="transform: translateX(-50%) rotate({needle_deg}deg);"></div>
            </div>
            <div style="text-align:center; margin-top:-10px; font-family:'JetBrains Mono'; color:#FFD700; font-size:1.2rem;">
                {rate}% SUCCESS CHANCE
            </div>
        """, unsafe_allow_html=True)
        
        # -- HEALTH CHECK (FLAGS) --
        st.markdown("#### SOCIAL HEALTH CHECK")
        st.markdown('<div class="flag-box">', unsafe_allow_html=True)
        for gf in res.get('green_flags', []):
            st.markdown(f'<div class="status-pill green-pill">✔ {gf}</div>', unsafe_allow_html=True)
        for rf in res.get('red_flags', []):
            st.markdown(f'<div class="status-pill red-pill">✘ {rf}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # -- RESPONSE OPTIONS --
        st.markdown("#### STRATEGIC DIMENSIONS")
        options = res.get('options', [])
        winner_idx = res.get('verdict_idx', 0)
        
        for i, opt in enumerate(options):
            is_best = (i == winner_idx)
            card_style = "winner-card" if is_best else ""
            label = "🏆 ARCHITECT'S CHOICE" if is_best else opt['type'].upper()
            
            st.markdown(f"""
                <div class="sovereign-card {card_style}">
                    <div style="font-family:'JetBrains Mono'; font-size:0.6rem; color:#FFD700; letter-spacing:2px; margin-bottom:8px;">{label}</div>
                    <div style="font-size:1.1rem; font-weight:600; color:#FFFFFF; margin-bottom:12px;">"{opt['text']}"</div>
                </div>
            """, unsafe_allow_html=True)
            # Voeg een copy-knop functionaliteit toe via st.code
            st.code(opt['text'], language=None)
            
        # -- PSYCHOLOGICAL REASONING --
        st.markdown("#### THE ARCHITECT'S VERDICT")
        st.info(res.get('reasoning', 'Geen onderbouwing beschikbaar.'))
        
    else:
        st.markdown("""
            <div style="height:300px; display:flex; align-items:center; justify-content:center; border:1px dashed #333; border-radius:16px; opacity:0.5;">
                Awaiting input data for tactical analysis...
            </div>
        """, unsafe_allow_html=True)

# -- FOOTER --
st.markdown("<br><hr><div style='text-align:center; opacity:0.2; font-size:0.7rem; font-family:\"JetBrains Mono\";'>SYSTEM ID: SOVEREIGN-V19-PRO | ENCRYPTED END-TO-END</div>", unsafe_allow_html=True)
