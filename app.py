import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import logging
import re

# ==============================================================================
# --- 1. Systeem & Logging Configuraties ---
# ==============================================================================
logging.basicConfig(level=logging.INFO)

# We halen de emoji uit de page_title voor de zekerheid tegen browser-encoding errors
st.set_page_config(
    page_title="Rizz Architect Ultra 3.0",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'analysis' not in st.session_state:
    st.session_state.analysis = None

# ==============================================================================
# --- 2. Ultra-Sovereign UI (CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #020408 !important;
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif;
    }

    .main-title { 
        font-weight: 900; font-size: 3.5rem; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #475569 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0; letter-spacing: -2px;
    }

    /* Gauge Visuals */
    .gauge-wrapper { position: relative; width: 260px; height: 130px; margin: 0 auto 30px auto; overflow: hidden; }
    .gauge-bg-arc {
        width: 260px; height: 260px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ef4444 0%, #f59e0b 50%, #10b981 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .gauge-pointer {
        position: absolute; bottom: 0; left: 50%; width: 5px; height: 100px;
        background: #fff; border-radius: 5px; transform-origin: bottom center;
        transition: transform 2.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 0 15px rgba(255,255,255,0.4);
    }

    /* Cards & Components */
    .tactical-card {
        background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px; padding: 25px; margin-bottom: 20px; transition: 0.5s;
    }
    .winner-glow { border: 1.5px solid #fbbf24 !important; box-shadow: 0 0 40px rgba(251, 191, 36, 0.1); }
    
    .pill-box { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0; }
    .pill-tag {
        padding: 5px 12px; border-radius: 6px; font-family: 'JetBrains Mono';
        font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(255,255,255,0.1);
    }
    .g-pill { background: rgba(16, 185, 129, 0.1); color: #34d399; }
    .r-pill { background: rgba(239, 68, 68, 0.1); color: #f87171; }

    /* Buttons */
    .stButton>button {
        background: #fff !important; color: #000 !important; font-weight: 900 !important;
        border-radius: 12px !important; height: 3.8rem !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. Backend Engine (ASCII-Safe) ---
# ==============================================================================

def clean_ascii(text):
    """Verwijdert alle non-ASCII tekens om 'codec' errors te voorkomen."""
    return re.sub(r'[^\x00-\x7F]+', '', text)

def process_media(file):
    """Bereidt de afbeelding voor zonder metadata te lekken."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((1100, 1100))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.error(f"Media Fout: {e}")
        return None

def call_grok_engine(api_key, b64_img, ctx):
    """High-reasoning Grok-4-1 call met strikte ASCII filtering."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # De prompt is nu 100% gegarandeerd ASCII-veilig
    system_instr = (
        "Role: Rizz Architect 3.0. Strategist for dating dynamics. "
        "Task: Analyze chat screenshot. Identify 3 options: Playful Provocateur, "
        "Elegant Direct, Pattern Interrupt. "
        "Health: List Green and Red Flags. "
        "Return JSON only: {success_rate: int, green_flags: [], red_flags: [], "
        "options: [{type: str, text: str}], verdict_idx: int, reasoning: str}"
    )

    try:
        # We cleanen de gebruikerscontext ook voor de zekerheid
        safe_ctx = clean_ascii(ctx)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": clean_ascii(system_instr)},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {safe_ctx}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Critical API Fail: {e}")
        st.error(f"Systeemfout (API): {clean_ascii(str(e))}")
        return None

# ==============================================================================
# --- 4. Main Application Interface ---
# ==============================================================================

st.markdown('<div class="main-title">RIZZ ARCHITECT 3.0</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#64748b; letter-spacing:4px; font-size:0.7rem;">PRECISION SOCIAL INTELLIGENCE</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔒 AUTHENTICATION")
    api_key_v = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    if st.button("RESET CORE", width='stretch'):
        st.session_state.clear()
        st.rerun()

col_a, col_b = st.columns([1, 1.3], gap="large")

with col_a:
    st.markdown("#### 📥 INTAKE")
    u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if u_file:
        st.image(u_file, width='stretch', caption="Input Data")
    
    u_ctx = st.text_area("MISSION BRIEFING", placeholder="Bijv: 'We praten nu 3 dagen, hoe krijg ik haar op date?'", height=120)
    
    if st.button("EXECUTE ANALYSIS", width='stretch'):
        if api_key_v and u_file:
            with st.spinner("Analyzing social matrix..."):
                b64 = process_media(u_file)
                data = call_grok_engine(api_key_v, b64, u_ctx)
                if data:
                    st.session_state.analysis = data
                    st.rerun()

with col_b:
    st.markdown("#### 📡 OUTPUT")
    if st.session_state.analysis:
        res = st.session_state.analysis
        
        # Success Gauge
        p = res.get('success_rate', 0)
        rot = (p * 1.8) - 90
        st.markdown(f"""
            <div class="gauge-wrapper">
                <div class="gauge-bg-arc"></div>
                <div class="gauge-pointer" style="transform: translateX(-50%) rotate({rot}deg);"></div>
            </div>
            <div style="text-align:center; font-family:'JetBrains Mono'; font-weight:800; font-size:1.3rem; margin-top:-20px;">
                {p}% SUCCESS CHANCE
            </div>
        """, unsafe_allow_html=True)

        # Health Flags
        st.markdown("<br><b>SOCIAL HEALTH SCAN:</b>", unsafe_allow_html=True)
        st.markdown('<div class="pill-box">', unsafe_allow_html=True)
        for f in res.get('green_flags', []):
            st.markdown(f'<div class="pill-tag g-pill">✔ {clean_ascii(f)}</div>', unsafe_allow_html=True)
        for f in res.get('red_flags', []):
            st.markdown(f'<div class="pill-tag r-pill">✘ {clean_ascii(f)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Response Dimensions
        st.markdown("<br><b>STRATEGIC DIMENSIONS:</b>", unsafe_allow_html=True)
        opts = res.get('options', [])
        win = res.get('verdict_idx', 0)
        for i, o in enumerate(opts):
            is_best = (i == win)
            style = "winner-glow" if is_best else ""
            label = "🏆 ARCHITECT'S CHOICE" if is_best else o['type'].upper()
            st.markdown(f"""
                <div class="tactical-card {style}">
                    <div style="font-family:'JetBrains Mono'; font-size:0.6rem; color:#f59e0b; letter-spacing:2px; margin-bottom:8px;">{label}</div>
                    <div style="font-size:1.2rem; font-weight:700;">"{clean_ascii(o['text'])}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(o['text'], language=None)

        st.info(f"**The Verdict:** {clean_ascii(res.get('reasoning', ''))}")
    else:
        st.markdown('<div style="height:350px; display:flex; align-items:center; justify-content:center; border:1px dashed #334155; border-radius:20px; opacity:0.3;">Awaiting Signal Injection...</div>', unsafe_allow_html=True)

st.markdown("<br><hr><div style='text-align:center; opacity:0.2; font-size:0.6rem; font-family:\"JetBrains Mono\";'>ENGINE v19.2-STABLE // MAR-2026 // NO_LOGS_ENABLED</div>", unsafe_allow_html=True)
