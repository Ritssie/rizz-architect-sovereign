import streamlit as st
from openai import OpenAI
import base64
import json
import time

# ==============================================================================
# --- 1. CONFIG & CYBERPUNK STYLING (Feedback 2 & 4) ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT OS", page_icon="📟", layout="wide")

# Custom CSS voor Monospace, Scherpe hoeken en Neon effecten
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    /* Forceer Dark Mode & Font */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #050505 !important;
        color: #00ff41 !important; /* Classic Matrix/Hacker Groen */
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* Hoekig Design: Geen ronde hoeken (Feedback 2) */
    div.stButton > button, div[data-testid="stTextArea"] textarea, .stSelectbox, .alpha-box {
        border-radius: 0px !important;
        border: 1px solid #1e293b !important;
        text-transform: uppercase;
    }

    /* Status Balk bovenaan (Feedback 4) */
    .status-bar {
        background: #111;
        padding: 5px 20px;
        border-bottom: 2px solid #00ff41;
        font-size: 0.7rem;
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    /* Neon Progress Bars (Feedback 2) */
    .stProgress > div > div > div > div {
        background-color: #00ff41 !important; /* Default groen */
        border-radius: 0px;
    }

    /* Custom Cards voor de moves */
    .alpha-box {
        background: #0a0a0a;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #00ff41 !important;
    }
    
    /* Verberg standaard Streamlit elementen voor meer immersie */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div class="status-bar">
        <span>STATUS: SYSTEM ACTIVE</span>
        <span>ENCRYPTION: AES-256</span>
        <span>LOCATION: [LOCAL_NODE_MOCKED]</span>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. LOGIC & SESSION STATE (Feedback 1) ---
# ==============================================================================
if 'history' not in st.session_state:
    st.session_state.history = []

def run_sovereign_scan(client, chat_b64, bio_text, vibe, plat, sarcasm):
    # Prompt aanpassing op basis van Sarcasme slider (Feedback 5)
    tone_instruction = f"Tone: {vibe}. Sarcasm level: {sarcasm}/10."
    
    prompt = f"""Role: Elite Dating Architect. Platform: {plat}. {tone_instruction}
    Return JSON ONLY: {{
        "metrics": {{"warmth": int, "tension": int, "risk": int}},
        "flags": {{"green": ["str"], "red": ["str"]}},
        "note": "str",
        "moves": [
            {{"type": "Tactical", "zin": "str", "logic": "str"}},
            {{"type": "Power", "zin": "str", "logic": "str"}}
        ]
    }}"""
    
    msg = [{"type": "text", "text": f"Context: {bio_text}"}]
    if chat_b64:
        msg.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})

    try:
        res = client.chat.completions.create(
            model="gpt-4o", # Of grok-beta/v3 indien beschikbaar
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": msg}]
        )
        data = json.loads(res.choices[0].message.content)
        # Sla op in geschiedenis (Feedback 1)
        st.session_state.history.insert(0, data)
        if len(st.session_state.history) > 3: st.session_state.history.pop()
        return data
    except Exception as e:
        st.error(f"SYSTEM ERROR: {e}")
        return None

# ==============================================================================
# --- 3. UI LAYOUT (Feedback 4: Split-Screen) ---
# ==============================================================================
st.title("RIZZ_ARCHITECT.EXE")

with st.sidebar:
    st.markdown("### 🖥️ COMMAND_INPUT")
    api_key = st.text_input("ACCESS_TOKEN (API KEY)", type="password")
    vibe_mode = st.selectbox("VIBE_PROFILE", ["Funny", "Mysterious", "Alpha", "The Flame"])
    sarcasm_level = st.slider("SARCASM_THRESHOLD", 0, 10, 5) # Feedback 5
    st.markdown("---")
    u_chat = st.file_uploader("UPLOAD_INTEL (.JPG, .PNG)", type=['png','jpg','jpeg'])
    u_bio = st.text_area("BIO_DATA", placeholder="Paste bio or profile details here...")

    if st.button("⚡ INITIALIZE_SCAN"):
        if api_key and u_chat:
            with st.spinner("DECRYPTING DATA..."):
                client = OpenAI(api_key=api_key)
                c_b64 = base64.b64encode(u_chat.getvalue()).decode()
                st.session_state.current_scan = run_sovereign_scan(client, c_b64, u_bio, vibe_mode, "Tinder", sarcasm_level)

# Hoofdvenster: Split-Screen (Feedback 4)
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown("#### [SOURCE_IMAGE]")
    if u_chat:
        st.image(u_chat, use_container_width=True)
        # Simuleer Scanning Overlay (Feedback 2 - Visueel via tekst/animatie)
        st.caption("SCANNING_ELEMENTS: DETECTED")
    else:
        st.info("Awaiting visual input...")

with col_right:
    st.markdown("#### [ANALYSIS_OUTPUT]")
    
    if 'current_scan' in st.session_state and st.session_state.current_scan:
        s = st.session_state.current_scan
        met = s.get('metrics', {})

        # Dynamische Meters (Feedback 1 & 2)
        c1, c2, c3 = st.columns(3)
        c1.metric("WARMTH", f"{met.get('warmth')}%")
        c1.progress(met.get('warmth', 0) / 100)
        
        c2.metric("TENSION", f"{met.get('tension')}%")
        c2.progress(met.get('tension', 0) / 100)
        
        c3.metric("RISK", f"{met.get('risk')}%")
        c3.progress(met.get('risk', 0) / 100)

        st.markdown("---")

        # Architect Note met Typewriter-ish feel (Feedback 3)
        st.markdown(f"**ARCHITECT_LOG:** {s.get('note')}")

        # Moves tonen met st.code (Feedback 1)
        for move in s.get('moves', []):
            with st.container():
                st.markdown(f"<div class='alpha-box'>", unsafe_allow_html=True)
                st.write(f"**{move['type']} MOVE**")
                st.code(move['zin'], language="text") # Automatische kopieerknop!
                st.caption(f"Logic: {move['logic']}")
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("SYSTEM STANDBY: Please upload data and initialize scan.")

# Geschiedenis Sectie (Feedback 1)
if st.session_state.history:
    with st.expander("📜 SCAN_HISTORY (LAST 3)"):
        for i, hist in enumerate(st.session_state.history):
            st.write(f"Scan {i+1}: {hist.get('note')[:50]}...")
