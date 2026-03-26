import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re
import sys

# ==============================================================================
# --- 1. SYSTEEM PROTOCOL (UTF-8 FORCING) ---
# ==============================================================================
# Forceer Python om UTF-8 te gebruiken voor alle systeem-output
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Geen emoji's in de configuratie om browser/OS errors te voorkomen
st.set_page_config(
    page_title="Rizz Architect Ultra",
    page_icon="---", 
    layout="wide"
)

if 'rizz_data' not in st.session_state:
    st.session_state.rizz_data = None

# ==============================================================================
# --- 2. TACTICAL INTERFACE (MODERN DARK UI) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    .title-banner { 
        font-weight: 900; font-size: 3.5rem; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #333 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* Success Meter Styles */
    .meter-container { position: relative; width: 260px; height: 130px; margin: 0 auto 30px auto; overflow: hidden; }
    .meter-arc {
        width: 260px; height: 260px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .meter-needle {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 100px;
        background: #fff; border-radius: 4px; transform-origin: bottom center;
        transition: transform 2s cubic-bezier(0.1, 0.8, 0.2, 1);
    }

    /* Content Cards */
    .analysis-card {
        background: #0a0a0a; border: 1px solid #1a1a1a;
        border-radius: 12px; padding: 25px; margin-bottom: 20px;
    }
    .highlight-card { border: 1px solid #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.05); }
    
    .flag-pill {
        padding: 5px 12px; border-radius: 6px; font-family: 'JetBrains Mono';
        font-size: 0.75rem; font-weight: 700; display: inline-block; margin: 5px;
    }
    .green-pill { background: rgba(0, 255, 100, 0.1); color: #00ff64; border: 1px solid #00ff6433; }
    .red-pill { background: rgba(255, 50, 50, 0.1); color: #ff3232; border: 1px solid #ff323233; }

    .stButton>button {
        background: #fff !important; color: #000 !important; font-weight: 900 !important;
        border-radius: 8px !important; height: 3.5rem !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. CORE ENGINE (FAILSAFE) ---
# ==============================================================================

def nuclear_sanitize(text):
    """
    Verwijdert ALLES wat geen standaard ASCII-karakter is.
    Dit is de definitieve oplossing voor de 'ascii' codec error.
    """
    if not text: return ""
    # Alleen karakters tussen spatie (32) en tilde (126) blijven over.
    return "".join(c for c in text if 31 < ord(c) < 127)

def process_image(uploaded_file):
    """Verwerkt de afbeelding naar een veilige base64 string."""
    try:
        img = Image.open(uploaded_file).convert('RGB')
        img.thumbnail((1000, 1000))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        # We decoderen naar ascii om er zeker van te zijn dat de string 'schoon' is
        return base64.b64encode(buffer.getvalue()).decode('ascii')
    except Exception as e:
        st.error(f"Media Error: {e}")
        return None

def run_architect_scan(api_key, b64_image, context):
    """Roept de Grok-4-1-fast-reasoning engine aan met maximale beveiliging."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Deze instructies zijn 100% gegarandeerd ASCII-veilig
    system_prompt = (
        "Role: Rizz Architect 3.0. Expert in social dynamics. "
        "Goal: Analyze the chat screenshot. "
        "Requirements: Provide success rate, Green Flags, Red Flags, and 3 reply options. "
        "Output: MUST be a valid JSON object. "
        "Fields: success_rate (int), green_flags (list), red_flags (list), "
        "options (list of {type, text}), verdict_idx (int), reasoning (str)."
    )

    try:
        # Dubbele beveiliging: sanitizen van alle inputs
        safe_system = nuclear_sanitize(system_prompt)
        safe_context = nuclear_sanitize(context)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": safe_system},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {safe_context}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]}
            ]
        )
        # Parse de response en sanitize de output ook voor de zekerheid
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Toon de error zonder de karakters die de crash veroorzaken
        clean_error = nuclear_sanitize(str(e))
        st.error(f"System Error: {clean_error}")
        return None

# ==============================================================================
# --- 4. DE WEBSITE STRUCTUUR (2026 STANDAARD) ---
# ==============================================================================

st.markdown('<div class="title-banner">RIZZ ARCHITECT 3.0</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#444; letter-spacing:5px; font-size:0.7rem; margin-top:-10px;">VERSION 19.5 - STABLE RELEASE</p>', unsafe_allow_html=True)

# Sidebar voor instellingen
with st.sidebar:
    st.markdown("### SYSTEM ACCESS")
    api_key_input = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    if st.button("RESET SYSTEM", width='stretch'):
        st.session_state.clear()
        st.rerun()
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("Secure Architecture - 2026 Ready")

# Hoofdlayout
col_l, col_r = st.columns([1, 1.2], gap="large")

with col_l:
    st.markdown("#### TACTICAL INTAKE")
    file = st.file_uploader("Upload Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if file:
        st.image(file, width='stretch', caption="Signal Source")
    
    briefing = st.text_area("MISSION CONTEXT", placeholder="Bijv: 'Match op Tinder, ze reageert enthousiast...'", height=120)
    
    if st.button("EXECUTE ANALYSIS", width='stretch'):
        if api_key_input and file:
            with st.spinner("Decoding social layers..."):
                b64 = process_image(file)
                if b64:
                    result = run_architect_scan(api_key_input, b64, briefing)
                    if result:
                        st.session_state.rizz_data = result
                        st.rerun()

with col_r:
    st.markdown("#### ARCHITECT OUTPUT")
    if st.session_state.rizz_data:
        data = st.session_state.rizz_data
        
        # Success Probablity Meter
        prob = data.get('success_rate', 0)
        rotation = (prob * 1.8) - 90
        st.markdown(f"""
            <div class="meter-container">
                <div class="meter-arc"></div>
                <div class="meter-needle" style="transform: translateX(-50%) rotate({rotation}deg);"></div>
            </div>
            <div style="text-align:center; font-weight:900; font-size:1.5rem; margin-top:-20px; color:#fff;">
                {prob}% SUCCESS RATE
            </div>
        """, unsafe_allow_html=True)

        # Health & Flags
        st.markdown("<br><b>SOCIAL HEALTH CHECK:</b>", unsafe_allow_html=True)
        st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
        for f in data.get('green_flags', []):
            st.markdown(f'<div class="flag-pill green-pill">CHECK: {nuclear_sanitize(f)}</div>', unsafe_allow_html=True)
        for f in data.get('red_flags', []):
            st.markdown(f'<div class="flag-pill red-pill">ALERT: {nuclear_sanitize(f)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Response Strategies
        st.markdown("<b>TACTICAL OPTIONS:</b>", unsafe_allow_html=True)
        opts = data.get('options', [])
        winner = data.get('verdict_idx', 0)
        
        for i, opt in enumerate(opts):
            is_best = (i == winner)
            card_style = "analysis-card highlight-card" if is_best else "analysis-card"
            label = "BEST MOVE" if is_best else opt['type'].upper()
            
            st.markdown(f"""
                <div class="{card_style}">
                    <div style="font-family:'JetBrains Mono'; font-size:0.6rem; color:#FFD700; letter-spacing:2px; margin-bottom:8px;">{label}</div>
                    <div style="font-size:1.2rem; font-weight:700;">"{nuclear_sanitize(opt['text'])}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(opt['text'], language=None)

        st.info(f"**The Verdict:** {nuclear_sanitize(data.get('reasoning', ''))}")
    else:
        st.markdown("""
            <div style="height:350px; display:flex; align-items:center; justify-content:center; border:1px dashed #222; border-radius:15px; opacity:0.3;">
                Awaiting mission data...
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><div style='text-align:center; opacity:0.2; font-size:0.6rem; font-family:\"JetBrains Mono\";'>SYSTEM-V19.5-STABLE // MAR-2026 // NO_UNICODE_PAYLOAD</div>", unsafe_allow_html=True)
