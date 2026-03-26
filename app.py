import streamlit as st
from openai import OpenAI
import base64
import json
import time

# ==============================================================================
# --- 1. CONFIG & SYSTEM UI ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v22.0", page_icon="👑", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None
if 'history' not in st.session_state: st.session_state.history = []

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #020617 !important; color: #f8fafc !important; font-family: 'Inter', sans-serif; 
    }

    /* Badge & Card Styling */
    .signal-badge {
        padding: 6px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;
        margin-bottom: 8px; display: block; border: 1px solid rgba(255,255,255,0.1);
    }
    .green-bg { background: rgba(34, 197, 94, 0.15); color: #4ade80; border-color: #22c55e44; }
    .red-bg { background: rgba(239, 68, 68, 0.15); color: #f87171; border-color: #ef444444; }

    .alpha-card {
        background: linear-gradient(145deg, #0f172a, #020617);
        border: 1px solid #1e293b; border-radius: 15px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    .flame-mode { border: 1px solid #f59e0b !important; box-shadow: 0 0 20px rgba(245, 158, 11, 0.2) !important; }
    
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #1e293b, #fcd34d) !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. THE SOVEREIGN ENGINE (Final Logic) ---
# ==============================================================================
def run_sovereign_scan(client, chat_b64, bio_text, vibe, plat):
    # Harde uitsluiting van vraagtekens voor offensieve modi
    question_constraint = ""
    if vibe in ["Alpha", "The Flame"]:
        question_constraint = "CRITICAL RULE: You are forbidden from using question marks (?). Use bold statements, cold reads, or commands."

    prompt = f"""Role: Master Dating Architect. Platform: {plat}. Vibe: {vibe}.
    {question_constraint}
    1. Scan for Investment Markers (Response speed, length, questions asked).
    2. Identify 2 Green Flags and 2 Red Flags.
    3. Generate a 'Tactical Move' and a 'Power Move' in Dutch.
    
    Return JSON ONLY: {{
        "metrics": {{"warmth": int, "tension": int, "risk": int}},
        "signals": {{"green": ["str"], "red": ["str"]}},
        "note": "Context-aware strategy based on flags",
        "moves": [
            {{"type": "Tactical", "zin": "str", "logic": "str"}},
            {{"type": "Power", "zin": "str", "logic": "str"}}
        ]
    }}"""
    
    msg = [{"type": "text", "text": f"Bio/Context: {bio_text}"}]
    if chat_b64: msg.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": msg}]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 3. UI ASSEMBLY ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fcd34d;'>RIZZ<span>ARCHITECT</span> v22</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🕹️ COMMAND CENTER")
    api_key = st.text_input("Grok API Key", type="password")
    vibe = st.selectbox("Vibe Profile", ["Funny", "Mysterious", "Alpha", "The Flame"])
    plat = st.selectbox("Platform Tuner", ["Tinder", "Bumble", "Hinge"])
    st.markdown("---")
    if st.button("🔄 REBOOT SYSTEM"): 
        st.session_state.state = None
        st.rerun()

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.markdown("#### 📥 INTEL INPUT")
    u_chat = st.file_uploader("Upload Chat", type=['png','jpg','jpeg'], label_visibility="collapsed")
    if u_chat: st.image(u_chat, use_container_width=True)
    u_bio = st.text_area("Manual Context / Bio", placeholder="Wat weten we over haar?", height=80)
    
    if st.button("⚡ EXECUTE SOVEREIGN SCAN"):
        if api_key and u_chat:
            with st.status("Initializing Neural Scan...") as status:
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                c_b64 = base64.b64encode(u_chat.getvalue()).decode()
                st.session_state.state = run_sovereign_scan(client, c_b64, u_bio, vibe, plat)
                status.update(label="Signals Extracted.", state="complete")
            st.rerun()

with col_out:
    st.markdown("#### 📡 SIGNAL CENTER")
    
    # Pre-load Meters (Zero Shift)
    m1, m2, m3 = st.columns(3)
    s = st.session_state.state if st.session_state.state else {}
    met = s.get('metrics', {})
    
    m1.write(f"**Warmth**")
    m1.progress(met.get('warmth', 0) / 100)
    m2.write(f"**Tension**")
    m2.progress(met.get('tension', 0) / 100)
    m3.write(f"**Ghost Risk**")
    m3.progress(met.get('risk', 0) / 100)

    st.markdown("---")

    # Flags Row
    f_left, f_right = st.columns(2)
    
    if s:
        # Render Signals
        with f_left:
            for g in s.get('signals', {}).get('green', []):
                st.markdown(f"<div class='signal-badge green-bg'>✅ {g}</div>", unsafe_allow_html=True)
        with f_right:
            for r in s.get('signals', {}).get('red', []):
                st.markdown(f"<div class='signal-badge red-bg'>🚩 {r}</div>", unsafe_allow_html=True)
        
        st.info(f"**Architect's Note:** {s.get('note')}")

        # Render Output Cards
        for i, move in enumerate(s.get('moves', [])):
            card_class = "alpha-card flame-mode" if (vibe == "The Flame" or move['type'] == "Power") else "alpha-card"
            st.markdown(f"""
                <div class="{card_class}">
                    <small style="font-family:Orbitron; color:#fcd34d;">{move['type'].upper()} MOVE</small>
                    <h2 style="color:white; margin:10px 0;">"{move['zin']}"</h2>
                    <p style="font-size:0.85rem; opacity:0.7; border-top:1px solid #334155; padding-top:10px;">
                        <b>Logic:</b> {move['logic']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Copy & Feedback Row
            c_btn, f_btn = st.columns([1, 1])
            if c_btn.button(f"📋 Copy Line {i+1}", key=f"copy_{i}"): st.toast("Copied!")
            with f_btn:
                sub_c1, sub_c2 = st.columns(2)
                if sub_c1.button("🔥", key=f"fire_{i}"): st.toast("Data Saved: Fire")
                if sub_c2.button("❄️", key=f"ice_{i}"): st.toast("Data Saved: Ice")

    else:
        st.info("System Standby. Upload tactical data om de neural scan te starten.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN v22.0 // FINAL STABLE // ANTI_INTERVIEW_PROTOCOL</div>", unsafe_allow_html=True)
