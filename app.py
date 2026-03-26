import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import logging
import re

# ==============================================================================
# --- 1. SYSTEEM REPAIR & LOGGING ---
# ==============================================================================
logging.basicConfig(level=logging.INFO)

# VERWIJDER EMOJI UIT TITEL: Voorkomt encoder errors in de browser/header
st.set_page_config(
    page_title="Rizz Architect Ultra 3.0",
    page_icon="---", 
    layout="wide"
)

# Initialiseer session state
if 'analysis' not in st.session_state:
    st.session_state.analysis = None

# ==============================================================================
# --- 2. THE ARCHITECT UI (CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
        color: #eeeeee !important;
        font-family: 'Inter', sans-serif;
    }

    .main-title { 
        font-weight: 900; font-size: 3rem; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #444 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* Gauge / Meter Visuals */
    .gauge-wrapper { position: relative; width: 240px; height: 120px; margin: 0 auto 20px auto; overflow: hidden; }
    .gauge-arc {
        width: 240px; height: 240px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .gauge-needle {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 90px;
        background: #fff; border-radius: 4px; transform-origin: bottom center;
        transition: transform 1.5s ease-out;
    }

    /* Tactical Components */
    .rizz-card {
        background: #111; border: 1px solid #222;
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
    }
    .winner-highlight { border: 1.5px solid #FFD700 !important; }
    
    .pill {
        padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono';
        font-size: 0.7rem; font-weight: 700; display: inline-block; margin-right: 5px;
    }
    .pill-g { background: rgba(0, 255, 0, 0.1); color: #00ff00; }
    .pill-r { background: rgba(255, 0, 0, 0.1); color: #ff4b4b; }

    .stButton>button {
        background: #fff !important; color: #000 !important; font-weight: 900 !important;
        border-radius: 8px !important; height: 3.5rem !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. HARDCORE ASCII SAFETY ENGINE ---
# ==============================================================================

def sanitize_for_api(text):
    """
    Verwijdert ALLES wat geen standaard ASCII karakter is.
    Dit stript emoji's (zoals de kroon) die de crash veroorzaken.
    """
    if not text: return ""
    # Alleen letters, cijfers, spaties en basis leestekens toegestaan
    clean = re.sub(r'[^\x20-\x7E]', '', text)
    return clean

def encode_image_safely(file):
    """Beeldverwerking met kwaliteitscontrole."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((1000, 1000))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    except Exception as e:
        st.error(f"Media Fout: {e}")
        return None

def call_grok_architect(api_key, b64_img, context):
    """Failsafe call naar Grok-4-1-fast-reasoning."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # GEEN emoji's in deze tekst!
    system_instruction = (
        "Role: Rizz Architect 3.0. Dating strategist. "
        "Task: Analyze screenshot for dating success. Provide 3 options: "
        "Playful Provocateur, Elegant Direct, Pattern Interrupt. "
        "Identify Green Flags and Red Flags. "
        "Output ONLY JSON: {success_rate: int, green_flags: [], red_flags: [], "
        "options: [{type: str, text: str}], verdict_idx: int, reasoning: str}"
    )

    try:
        # We sanitizen ALLES: systeem-instructie, context en de API call zelf
        safe_system = sanitize_for_api(system_instruction)
        safe_user_context = sanitize_for_api(context)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": safe_system},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {safe_user_context}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Hier vangen we de error en tonen hem zonder de emoji die de crash veroorzaakte
        err_msg = sanitize_for_api(str(e))
        logging.error(f"Critical API Fail: {err_msg}")
        st.error(f"Architect Engine Offline: {err_msg}")
        return None

# ==============================================================================
# --- 4. DASHBOARD INTERFACE ---
# ==============================================================================

st.markdown('<div class="main-title">RIZZ ARCHITECT 3.0</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#555; letter-spacing:3px; font-size:0.7rem;">STABLE BUILD v19.3 // MAR-2026</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔑 ACCESS")
    api_key_input = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    if st.button("REBOOT SYSTEM", width='stretch'):
        st.session_state.clear()
        st.rerun()

col_l, col_r = st.columns([1, 1.2], gap="large")

with col_l:
    st.markdown("#### 📥 INTAKE")
    file = st.file_uploader("Upload Chat", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if file:
        st.image(file, width='stretch')
    
    ctx = st.text_area("MISSION CONTEXT", placeholder="Bijv: 'Ze stuurt korte berichten...'", height=100)
    
    if st.button("RUN ANALYSIS", width='stretch'):
        if api_key_input and file:
            with st.spinner("Decoding social matrix..."):
                b64 = encode_image_safely(file)
                data = call_grok_architect(api_key_input, b64, ctx)
                if data:
                    st.session_state.analysis = data
                    st.rerun()

with col_r:
    st.markdown("#### 📡 OUTPUT")
    if st.session_state.analysis:
        res = st.session_state.analysis
        
        # Success Gauge
        p = res.get('success_rate', 0)
        rot = (p * 1.8) - 90
        st.markdown(f"""
            <div class="gauge-wrapper">
                <div class="gauge-arc"></div>
                <div class="gauge-needle" style="transform: translateX(-50%) rotate({rot}deg);"></div>
            </div>
            <div style="text-align:center; font-weight:800; font-size:1.2rem; margin-top:-15px;">
                {p}% SUCCESS CHANCE
            </div>
        """, unsafe_allow_html=True)

        # Flags
        st.markdown("<br><b>HEALTH CHECK:</b>", unsafe_allow_html=True)
        for f in res.get('green_flags', []):
            st.markdown(f'<div class="pill pill-g">✔ {sanitize_for_api(f)}</div>', unsafe_allow_html=True)
        for f in res.get('red_flags', []):
            st.markdown(f'<div class="pill pill-r">✘ {sanitize_for_api(f)}</div>', unsafe_allow_html=True)

        # Options
        st.markdown("<br><b>STRATEGY:</b>", unsafe_allow_html=True)
        opts = res.get('options', [])
        win = res.get('verdict_idx', 0)
        for i, o in enumerate(opts):
            is_best = (i == win)
            card_class = "rizz-card winner-highlight" if is_best else "rizz-card"
            st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-size:0.6rem; color:#FFD700;">{o['type'].upper()}</div>
                    <div style="font-size:1.1rem; font-weight:700;">"{sanitize_for_api(o['text'])}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(o['text'], language=None)

        st.info(f"**Verdict:** {sanitize_for_api(res.get('reasoning', ''))}")
    else:
        st.markdown('<div style="height:300px; display:flex; align-items:center; justify-content:center; border:1px dashed #222; border-radius:15px; opacity:0.3;">Awaiting Signal...</div>', unsafe_allow_html=True)
