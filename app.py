import streamlit as st
from openai import OpenAI
import base64
import json
import time

# ==============================================================================
# --- 1. CONFIG & NEON UI ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v21.0", page_icon="⚖️", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #030712 !important; color: #f8fafc !important; font-family: 'Inter', sans-serif; 
    }

    /* Permanente Containers voor Zero-Shift */
    .skeleton-container {
        background: rgba(255,255,255,0.02); border: 1px dashed #30363d;
        border-radius: 12px; padding: 20px; margin-bottom: 20px; min-height: 100px;
    }

    .flag-card { padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem; }
    .green-flag { background: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e; color: #4ade80; }
    .red-flag { background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #f87171; }

    .glow-card {
        background: #0f172a; border: 1px solid #1e293b; border-radius: 15px;
        padding: 25px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .flame-mode { border: 1px solid #f59e0b !important; box-shadow: 0 0 15px rgba(245, 158, 11, 0.2) !important; }
    
    .stMetric { background: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. STRATEGIC ENGINE (Logic & Constraints) ---
# ==============================================================================
def run_strategic_scan(client, chat_b64, bio_text, vibe, platform):
    # Harde limitatie op vraagtekens voor offensieve modi
    constraint = ""
    if vibe in ["Alpha", "The Flame", "Counter-Rizz"]:
        constraint = "STRICT: NO question marks (?) allowed. Use statements, teases, or cold reads."

    prompt = f"""Role: Sovereign Dating Architect. Platform: {platform}. Vibe: {vibe}.
    {constraint}
    Analyze the conversation for behavioral signals (Red/Green flags).
    Generate 2 strategic moves in Dutch:
    1. The Tactical Move (Maintenance/Bridge)
    2. The Power Move (Escalation/The Close/Counter-Rizz)
    
    Return JSON: {{
        "metrics": {{"warmth": int, "tension": int, "risk": int}},
        "green_flags": ["signal 1", "signal 2"],
        "red_flags": ["signal 1", "signal 2"],
        "note": "Analysis matching the percentages",
        "moves": [
            {{"type": "Tactical", "zin": "str", "logic": "str"}},
            {{"type": "Power", "zin": "str", "logic": "str"}}
        ]
    }}"""
    
    msg = [{"type": "text", "text": f"Bio Context: {bio_text}"}]
    if chat_b64:
        msg.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})

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
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fcd34d;'>RIZZ<span>ARCHITECT</span> v21</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎚️ STRATEGIC CONTROL")
    api_key = st.text_input("Grok API Key", type="password")
    plat = st.selectbox("Platform", ["Tinder", "Bumble", "Hinge"])
    vibe = st.selectbox("Current Vibe", ["Funny", "Alpha", "The Flame", "Counter-Rizz"])
    st.markdown("---")
    if st.button("RESET SYSTEM"): 
        st.session_state.state = None
        st.rerun()

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.markdown("#### 📥 INTEL INTAKE")
    u_chat = st.file_uploader("Chat Screenshot", type=['png','jpg','jpeg'])
    if u_chat: st.image(u_chat, use_container_width=True)
    u_bio = st.text_area("Bio / Interests", placeholder="Wat weten we over haar?", height=80)
    
    if st.button("⚡ EXECUTE NEURAL SCAN"):
        if api_key and u_chat:
            with st.status("Gathering Intelligence...") as status:
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                c_b64 = base64.b64encode(u_chat.getvalue()).decode()
                st.session_state.state = run_strategic_scan(client, c_b64, u_bio, vibe, plat)
                status.update(label="Analysis Complete", state="complete")
            st.rerun()

with col_out:
    # --- METRICS ROW (Placeholders) ---
    st.markdown("#### 📡 STRATEGIC DASHBOARD")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    # --- BEHAVIORAL SIGNALS (Placeholders) ---
    f_col1, f_col2 = st.columns(2)
    
    # --- OUTPUT AREA ---
    res_area = st.empty()

    if st.session_state.state:
        s = st.session_state.state
        met = s.get('metrics', {})
        
        # Fill Metrics
        m_col1.metric("Warmth", f"{met.get('warmth')}%")
        m_col2.metric("Tension", f"{met.get('tension')}%")
        m_col3.metric("Ghost Risk", f"{met.get('risk')}%", delta_color="inverse")
        
        # Fill Flags
        with f_col1:
            st.caption("✅ GREEN FLAGS")
            for f in s.get('green_flags', []): st.markdown(f"<div class='flag-card green-flag'>✦ {f}</div>", unsafe_allow_html=True)
        with f_col2:
            st.caption("🚩 RED FLAGS")
            for f in s.get('red_flags', []): st.markdown(f"<div class='flag-card red-flag'>⚠ {f}</div>", unsafe_allow_html=True)
        
        # Results Rendering
        with res_area.container():
            st.info(f"**Architect's Note:** {s.get('note')}")
            for move in s.get('moves', []):
                card_style = "glow-card flame-mode" if (vibe == "The Flame" or move['type'] == "Power") else "glow-card"
                st.markdown(f"""
                    <div class="{card_style}">
                        <span style="font-family:Orbitron; font-size:0.7rem; color:#fcd34d;">{move['type'].upper()} MOVE</span>
                        <h2 style="color:white; margin:10px 0;">"{move['zin']}"</h2>
                        <p style="font-size:0.85rem; opacity:0.8; border-top:1px solid #334155; padding-top:10px;">
                            <b>Logic:</b> {move['logic']}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"📋 Copy {move['type']} Line"): st.toast("Copied!")
    else:
        # Skeletons / Initial State
        m_col1.metric("Warmth", "0%")
        m_col2.metric("Tension", "0%")
        m_col3.metric("Ghost Risk", "0%")
        res_area.info("Initialiseer de scan om tactische data te laden.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN v21.0 // STRATEGIST_EDITION // COUNTER_RIZZ_ACTIVE</div>", unsafe_allow_html=True)
