import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re

# ==============================================================================
# --- 1. DE "PURGE" PROTOCOLLEN (ASCII FORCE) ---
# ==============================================================================

def absolute_ascii_only(text):
    """
    DE KERNOPLOSSING: Deze functie stript ELK karakter dat geen standaard 
    toetsenbordteken is. De kroon-emoji (\U0001f451) overleeft dit niet.
    """
    if not text:
        return ""
    # We coderen naar ascii en negeren alles wat niet lukt, daarna decoderen we terug.
    return text.encode("ascii", "ignore").decode("ascii")

# Geen enkel speciaal teken in de configuratie
st.set_page_config(
    page_title="Rizz Architect Ultra",
    page_icon="---",
    layout="wide"
)

if 'rizz_result' not in st.session_state:
    st.session_state.rizz_result = None

# ==============================================================================
# --- 2. TACTICAL VISUALS (CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    .title-text { 
        font-weight: 900; font-size: 3rem; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #333 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    /* Gauge / Success Meter */
    .meter-box { position: relative; width: 240px; height: 120px; margin: 0 auto 20px auto; overflow: hidden; }
    .meter-arc {
        width: 240px; height: 240px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .meter-needle {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 90px;
        background: #fff; border-radius: 4px; transform-origin: bottom center;
        transition: transform 1.5s ease-in-out;
    }

    /* Cards */
    .tactical-panel {
        background: #0a0a0a; border: 1px solid #222;
        border-radius: 10px; padding: 20px; margin-bottom: 15px;
    }
    .win-panel { border: 1px solid #FFD700 !important; }
    
    .stButton>button {
        background: #fff !important; color: #000 !important; font-weight: 900 !important;
        border-radius: 5px !important; height: 3.5rem !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. FAILSAFE ARCHITECT ENGINE ---
# ==============================================================================

def prepare_image_b64(image_file):
    """Verwerkt foto naar een schone ASCII base64 string."""
    try:
        img = Image.open(image_file).convert('RGB')
        img.thumbnail((1000, 1000))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=80)
        return base64.b64encode(buffered.getvalue()).decode('ascii')
    except Exception as e:
        st.error(f"Media Error: {absolute_ascii_only(str(e))}")
        return None

def execute_grok_call(api_key, b64_data, user_text):
    """De aanroep naar Grok-4-1-fast-reasoning, volledig gestript van emoji's."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Deze instructie is puur ASCII
    core_instruction = (
        "Role: Rizz Architect 3.0. Dating expert. Analyze the chat. "
        "Provide: success_rate (int), green_flags (list), red_flags (list), "
        "options (list with type and text), verdict_idx (int), reasoning (str). "
        "Output MUST be valid JSON. No emojis in response."
    )

    try:
        # We 'purgen' de instructies en de gebruikersinput voor de zekerheid
        clean_system = absolute_ascii_only(core_instruction)
        clean_user_input = absolute_ascii_only(user_text)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": clean_system},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {clean_user_input}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Toon de error alleen in veilige ASCII
        error_msg = absolute_ascii_only(str(e))
        st.error(f"System Error: {error_msg}")
        return None

# ==============================================================================
# --- 4. DE INTERFACE (2026 STANDAARD) ---
# ==============================================================================

st.markdown('<div class="title-text">RIZZ ARCHITECT 3.0</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#333; font-size:0.7rem; letter-spacing:4px;">STABLE BUILD v19.6 // MAR-2026</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### SYSTEM ACCESS")
    key = st.text_input("Grok Key", type="password")
    if st.button("REBOOT CORE", width='stretch'):
        st.session_state.clear()
        st.rerun()

left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("#### INTAKE")
    uploaded = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if uploaded:
        st.image(uploaded, width='stretch')
    
    briefing = st.text_area("MISSION BRIEFING", placeholder="Wat is de situatie?", height=100)
    
    if st.button("EXECUTE SCAN", width='stretch'):
        if key and uploaded:
            with st.spinner("Analyzing signal..."):
                b64 = prepare_image_b64(uploaded)
                if b64:
                    data = execute_grok_call(key, b64, briefing)
                    if data:
                        st.session_state.rizz_result = data
                        st.rerun()

with right_col:
    st.markdown("#### ARCHITECT VERDICT")
    if st.session_state.rizz_result:
        res = st.session_state.rizz_result
        
        # Meter
        val = res.get('success_rate', 0)
        deg = (val * 1.8) - 90
        st.markdown(f"""
            <div class="meter-box">
                <div class="meter-arc"></div>
                <div class="meter-needle" style="transform: translateX(-50%) rotate({deg}deg);"></div>
            </div>
            <div style="text-align:center; font-weight:900; font-size:1.4rem; margin-top:-10px;">{val}% SUCCESS</div>
        """, unsafe_allow_html=True)

        # Flags
        st.markdown("<br><b>SOCIAL HEALTH:</b>", unsafe_allow_html=True)
        for f in res.get('green_flags', []):
            st.write(f"PRO: {absolute_ascii_only(f)}")
        for f in res.get('red_flags', []):
            st.write(f"CON: {absolute_ascii_only(f)}")

        # Options
        st.markdown("<br><b>STRATEGY:</b>", unsafe_allow_html=True)
        opts = res.get('options', [])
        best_idx = res.get('verdict_idx', 0)
        
        for i, o in enumerate(opts):
            is_win = (i == best_idx)
            panel_css = "tactical-panel win-panel" if is_win else "tactical-panel"
            st.markdown(f"""
                <div class="{panel_css}">
                    <div style="font-size:0.6rem; color:#FFD700;">{absolute_ascii_only(o['type']).upper()}</div>
                    <div style="font-size:1.1rem; font-weight:700;">"{absolute_ascii_only(o['text'])}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(o['text'], language=None)

        st.info(f"Verdict: {absolute_ascii_only(res.get('reasoning', ''))}")
    else:
        st.markdown('<div style="height:300px; display:flex; align-items:center; justify-content:center; border:1px dashed #222; border-radius:10px; opacity:0.2;">SIGNAL IDLE</div>', unsafe_allow_html=True)

st.markdown("<br><hr><div style='text-align:center; opacity:0.1; font-size:0.6rem;'>TITANIUM-v19.6-STABLE // NO_EMOJI_PROTOCOL</div>", unsafe_allow_html=True)
