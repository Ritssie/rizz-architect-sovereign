import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re

# ==============================================================================
# --- 1. THE GHOST PROTOCOL (ANTIVIRUS VOOR EMOJIS) ---
# ==============================================================================

def strip_all_non_ascii(text):
    """
    FORCEERT de tekst naar ASCII. 
    Alles wat geen letter, cijfer of standaard leesteken is, wordt VERWIJDERD.
    Dit is de enige manier om die hardnekkige kroon-emoji te doden.
    """
    if not text:
        return ""
    # We gebruiken een byte-conversie die alles wat niet ASCII is simpelweg negeert.
    return str(text.encode("ascii", "ignore").decode("ascii"))

# Systeembrede configuratie zonder enige poespas
st.set_page_config(
    page_title="Architect Ultra",
    page_icon="---",
    layout="wide"
)

if 'rizz_payload' not in st.session_state:
    st.session_state.rizz_payload = None

# ==============================================================================
# --- 2. DARK ARCHITECT UI (MODERN 2026) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    .title-banner { 
        font-weight: 900; font-size: 2.5rem; text-align: center;
        color: #ffffff; letter-spacing: -1px; margin-bottom: 20px;
    }

    /* Gauge / Meter Visuals */
    .meter-container { position: relative; width: 200px; height: 100px; margin: 0 auto 20px auto; overflow: hidden; }
    .meter-bg {
        width: 200px; height: 200px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .meter-needle {
        position: absolute; bottom: 0; left: 50%; width: 3px; height: 80px;
        background: #fff; transform-origin: bottom center;
        transition: transform 2s ease-in-out;
    }

    /* Minimalist Cards */
    .info-card {
        background: #080808; border: 1px solid #1a1a1a;
        border-radius: 8px; padding: 15px; margin-bottom: 10px;
    }
    .best-card { border: 1px solid #FFD700 !important; }
    
    .stButton>button {
        background: #ffffff !important; color: #000000 !important; font-weight: 900 !important;
        border-radius: 4px !important; height: 3rem !important; width: 100%; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. THE CLEAN ENGINE ---
# ==============================================================================

def secure_image_to_b64(file):
    """Converteert afbeelding naar b64 en dwingt ASCII encoding af."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((800, 800))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        # De .decode('ascii') hier is cruciaal voor de OpenAI client
        return base64.b64encode(buf.getvalue()).decode('ascii')
    except Exception as e:
        st.error(f"Media Error: {strip_all_non_ascii(str(e))}")
        return None

def call_grok_ghost(api_key, b64_str, context_text):
    """Gepurgeerde API aanroep naar Grok-4-1."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Alleen pure ASCII karakters in de prompt
    prompt_instr = (
        "Role: Rizz Architect. Analyze dating chat. "
        "Format: JSON ONLY. "
        "Fields: success_rate (int), green_flags (list), red_flags (list), "
        "options (list of {type, text}), verdict_idx (int), reasoning (str)."
    )

    try:
        # We 'scrobben' de input van de gebruiker om verborgen emoji's te wissen
        clean_context = strip_all_non_ascii(context_text)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": strip_all_non_ascii(prompt_instr)},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {clean_context}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_str}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Zelfs de error melding wordt geschoond
        clean_err = strip_all_non_ascii(str(e))
        st.error(f"Architect Offline: {clean_err}")
        return None

# ==============================================================================
# --- 4. INTERFACE ASSEMBLY ---
# ==============================================================================

st.markdown('<div class="title-banner">RIZZ ARCHITECT 3.0</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ACCESS")
    api_key_vault = st.text_input("Grok API Key", type="password")
    if st.button("HARD RESET", width='stretch'):
        st.session_state.clear()
        st.rerun()

left, right = st.columns([1, 1.2], gap="medium")

with left:
    st.markdown("#### INPUT SIGNAL")
    img_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if img_file:
        st.image(img_file, width='stretch')
    
    briefing_txt = st.text_area("MISSION BRIEF", placeholder="Wat is de status?", height=100)
    
    if st.button("START ANALYSIS", width='stretch'):
        if api_key_vault and img_file:
            with st.spinner("Purging data & analyzing..."):
                b64_clean = secure_image_to_b64(img_file)
                if b64_clean:
                    res = call_grok_ghost(api_key_vault, b64_clean, briefing_txt)
                    if res:
                        st.session_state.rizz_payload = res
                        st.rerun()

with right:
    st.markdown("#### ANALYSIS RESULT")
    if st.session_state.rizz_payload:
        p = st.session_state.rizz_payload
        
        # Success Meter
        rate = p.get('success_rate', 0)
        rot_deg = (rate * 1.8) - 90
        st.markdown(f"""
            <div class="meter-container">
                <div class="meter-bg"></div>
                <div class="meter-needle" style="transform: translateX(-50%) rotate({rot_deg}deg);"></div>
            </div>
            <p style="text-align:center; font-weight:900;">{rate}% SUCCESS PROBABILITY</p>
        """, unsafe_allow_html=True)

        # Health Scan
        st.markdown("<b>SOCIAL SCAN:</b>", unsafe_allow_html=True)
        for gf in p.get('green_flags', []):
            st.write(f"PRO: {strip_all_non_ascii(gf)}")
        for rf in p.get('red_flags', []):
            st.write(f"CON: {strip_all_non_ascii(rf)}")

        # Options
        st.markdown("<br><b>SUGGESTED MOVES:</b>", unsafe_allow_html=True)
        opts = p.get('options', [])
        winner_idx = p.get('verdict_idx', 0)
        
        for idx, o in enumerate(opts):
            is_winner = (idx == winner_idx)
            card_class = "info-card best-card" if is_winner else "info-card"
            st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-size:0.6rem; color:#888;">{strip_all_non_ascii(o['type']).upper()}</div>
                    <div style="font-size:1.1rem; font-weight:700;">"{strip_all_non_ascii(o['text'])}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(o['text'], language=None)

        st.info(strip_all_non_ascii(p.get('reasoning', '')))
    else:
        st.markdown('<div style="height:250px; display:flex; align-items:center; justify-content:center; border:1px dashed #333; opacity:0.3;">SIGNAL IDLE</div>', unsafe_allow_html=True)

st.markdown("<br><hr><div style='text-align:center; opacity:0.1; font-size:0.5rem;'>BUILD_19.7_STABLE_NO_UNICODE</div>", unsafe_allow_html=True)
