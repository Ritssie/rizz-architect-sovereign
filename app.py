import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import logging
import re
import sys

# ==============================================================================
# --- 1. SYSTEM UTF-8 ENFORCEMENT ---
# ==============================================================================
# Dit dwingt Python om UTF-8 te gebruiken, zelfs als de server op ASCII staat.
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Rizz Architect Ultra 3.0",
    page_icon="---", # Geen emoji hier!
    layout="wide"
)

if 'analysis' not in st.session_state:
    st.session_state.analysis = None

# ==============================================================================
# --- 2. SOVEREIGN UI (CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #030303 !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }

    .header-text { 
        font-weight: 900; font-size: 3rem; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #334155 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* Gauge / Meter Visuals */
    .gauge-container { position: relative; width: 240px; height: 120px; margin: 0 auto; overflow: hidden; }
    .gauge-bg {
        width: 240px; height: 240px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ef4444 0%, #fbbf24 50%, #10b981 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .needle-element {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 95px;
        background: #fff; border-radius: 4px; transform-origin: bottom center;
        transition: transform 2s cubic-bezier(0.1, 0.7, 0.1, 1);
    }

    /* Components */
    .rizz-panel {
        background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
    }
    .best-move { border: 1.5px solid #fbbf24 !important; }
    
    .status-badge {
        padding: 4px 10px; border-radius: 4px; font-family: 'JetBrains Mono';
        font-size: 0.7rem; font-weight: 700; margin: 5px; display: inline-block;
    }
    .badge-pos { background: rgba(16, 185, 129, 0.1); color: #34d399; }
    .badge-neg { background: rgba(239, 68, 68, 0.1); color: #f87171; }

    .stButton>button {
        background: #fff !important; color: #000 !important; font-weight: 900 !important;
        border-radius: 8px !important; height: 3.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. THE ATOMIC SANITIZER (NO EMOJIS ALLOWED) ---
# ==============================================================================

def nuclear_sanitize(text):
    """Verwijdert ALLES behalve letters, cijfers en basis leestekens."""
    if not text: return ""
    # Regex die alleen ASCII 32 t/m 126 toelaat (basis tekst)
    return "".join(c for c in text if 31 < ord(c) < 127)

def encode_media(file):
    """Verwerkt de afbeelding zonder metadata."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((1000, 1000))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=80)
        return base64.b64encode(buf.getvalue()).decode('ascii') # Forceer ascii output voor b64
    except Exception as e:
        st.error(f"Media Error: {e}")
        return None

def call_grok_engine(api_key, b64_img, context):
    """Aanroep naar Grok-4-1-fast-reasoning met maximale beveiliging."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Strikt ASCII instructies
    instr = (
        "Role: Rizz Architect 3.0. Dating strategist. "
        "Task: Analyze screenshot for success. Provide 3 options: "
        "Playful Provocateur, Elegant Direct, Pattern Interrupt. "
        "List Green and Red Flags. "
        "Return ONLY JSON: {success_rate: int, green_flags: [], red_flags: [], "
        "options: [{type: str, text: str}], verdict_idx: int, reasoning: str}"
    )

    try:
        # Dubbele sanitization op alle input strings
        safe_instr = nuclear_sanitize(instr)
        safe_ctx = nuclear_sanitize(context)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": safe_instr},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {safe_ctx}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Zelfs de error message sanitizen we voor de zekerheid
        err = nuclear_sanitize(str(e))
        st.error(f"Critical System Error: {err}")
        return None

# ==============================================================================
# --- 4. MAIN INTERFACE ---
# ==============================================================================

st.markdown('<div class="header-text">RIZZ ARCHITECT 3.0</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#475569; letter-spacing:5px; font-size:0.7rem; margin-top:-15px;">TITANIUM BUILD v19.4</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### SYSTEM ACCESS")
    api_key = st.text_input("Grok Key", type="password")
    if st.button("SYSTEM RESET", width='stretch'):
        st.session_state.clear()
        st.rerun()

left, right = st.columns([1, 1.3], gap="large")

with left:
    st.markdown("#### INPUT")
    uploaded = st.file_uploader("Upload Chat", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if uploaded:
        st.image(uploaded, width='stretch')
    
    brief = st.text_area("BRIEFING", placeholder="Wat is de status?", height=100)
    
    if st.button("ANALYZE SIGNAL", width='stretch'):
        if api_key and uploaded:
            with st.spinner("Processing..."):
                b64 = encode_media(uploaded)
                data = call_grok_engine(api_key, b64, brief)
                if data:
                    st.session_state.analysis = data
                    st.rerun()

with right:
    st.markdown("#### ARCHITECT VERDICT")
    if st.session_state.analysis:
        res = st.session_state.analysis
        
        # Success Gauge
        p = res.get('success_rate', 0)
        rot = (p * 1.8) - 90
        st.markdown(f"""
            <div class="gauge-container">
                <div class="gauge-bg"></div>
                <div class="needle-element" style="transform: translateX(-50%) rotate({rot}deg);"></div>
            </div>
            <div style="text-align:center; font-weight:900; font-size:1.4rem; margin-top:-10px;">{p}% SUCCESS</div>
        """, unsafe_allow_html=True)

        # Health Scan
        st.markdown("<br><b>HEALTH SCAN:</b>", unsafe_allow_html=True)
        for f in res.get('green_flags', []):
            st.markdown(f'<div class="status-badge badge-pos">CHECK: {nuclear_sanitize(f)}</div>', unsafe_allow_html=True)
        for f in res.get('red_flags', []):
            st.markdown(f'<div class="status-badge badge-neg">ALERT: {nuclear_sanitize(f)}</div>', unsafe_allow_html=True)

        # Strategic Moves
        st.markdown("<br><b>STRATEGY:</b>", unsafe_allow_html=True)
        opts = res.get('options', [])
        best = res.get('verdict_idx', 0)
        for i, o in enumerate(opts):
            is_best = (i == best)
            css = "rizz-panel best-move" if is_best else "rizz-panel"
            st.markdown(f"""
                <div class="{css}">
                    <div style="font-size:0.6rem; color:#fbbf24;">{o['type'].upper()}</div>
                    <div style="font-size:1.1rem; font-weight:700;">"{nuclear_sanitize(o['text'])}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(o['text'], language=None)

        st.info(f"Reasoning: {nuclear_sanitize(res.get('reasoning', ''))}")
    else:
        st.markdown('<div style="height:300px; display:flex; align-items:center; justify-content:center; border:1px dashed #222; border-radius:15px; opacity:0.2;">SIGNAL IDLE</div>', unsafe_allow_html=True)
