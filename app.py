import streamlit as st
from openai import OpenAI
import base64
import json
import time

# ==============================================================================
# --- 1. CONFIG & SOVEREIGN STYLING ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT", page_icon="👑", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #020617 !important; color: #f8fafc !important; font-family: 'Inter', sans-serif; 
    }

    /* Signal Center Styling */
    .signal-card {
        padding: 12px; border-radius: 8px; font-size: 0.8rem; font-weight: 600;
        margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05);
        display: flex; align-items: center; gap: 10px;
    }
    .green-zone { background: rgba(34, 197, 94, 0.1); color: #4ade80; border-color: #22c55e33; }
    .red-zone { background: rgba(239, 68, 68, 0.1); color: #f87171; border-color: #ef444433; }

    /* Alpha Output Styling */
    .alpha-box {
        background: linear-gradient(160deg, #0f172a 0%, #020617 100%);
        border: 1px solid #1e293b; border-radius: 15px; padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6); margin-bottom: 25px;
    }
    .flame-glow { border: 1px solid #f59e0b !important; box-shadow: 0 0 25px rgba(245, 158, 11, 0.2) !important; }

    /* Share Card Mockup */
    .share-preview {
        background: #000; border: 2px solid #fcd34d; padding: 30px; border-radius: 10px;
        text-align: center; font-family: 'Orbitron'; color: white; margin-top: 20px;
    }

    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #1e293b, #fcd34d) !important; }
    h1 { font-family: 'Orbitron'; letter-spacing: 3px; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. THE SOVEREIGN CORE ---
# ==============================================================================
def run_sovereign_scan(client, chat_b64, bio_text, vibe, plat):
    # Harde uitsluiting van vraagtekens voor offensieve modi
    q_rule = "STRICT: NO question marks (?) allowed. Use bold statements or playful assumptions." if vibe in ["Alpha", "The Flame"] else ""

    prompt = f"""Role: Elite Dating Architect. Platform: {plat}. Vibe: {vibe}. {q_rule}
    Scan chat for investment markers. Identify 2 Green Flags (🎯) and 2 Red Flags (⚠️).
    Generate 2 strategic moves in Dutch: 'Tactical' and 'Power'.
    
    Return JSON: {{
        "metrics": {{"warmth": int, "tension": int, "risk": int}},
        "flags": {{"green": ["str"], "red": ["str"]}},
        "note": "str",
        "moves": [
            {{"type": "Tactical", "zin": "str", "logic": "str"}},
            {{"type": "Power", "zin": "str", "logic": "str"}}
        ]
    }}"""
    
    msg = [{"type": "text", "text": f"Context: {bio_text}"}]
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
# --- 3. DASHBOARD ASSEMBLY ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; color:#fff;'>RIZZ<span style='color:#fcd34d;'>ARCHITECT</span></h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛰️ SYSTEM CONTROL")
    api_key = st.text_input("Grok API Key", type="password")
    vibe_mode = st.selectbox("Vibe", ["Funny", "Mysterious", "Alpha", "The Flame"])
    plat_mode = st.selectbox("Platform", ["Tinder", "Bumble", "Hinge"])
    st.markdown("---")
    if st.button("🔄 FULL SYSTEM REBOOT"): 
        st.session_state.state = None
        st.rerun()

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.markdown("#### 📥 INTEL DATA")
    u_chat = st.file_uploader("Upload Context Screenshot", type=['png','jpg','jpeg'], label_visibility="collapsed")
    if u_chat: st.image(u_chat, use_container_width=True)
    u_bio = st.text_area("Profile Insights", placeholder="Interesses, prompts, vibe...", height=80)
    
    if st.button("⚡ EXECUTE SOVEREIGN SCAN"):
        if api_key and u_chat:
            with st.status("Performing Neural Analysis...") as status:
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                c_b64 = base64.b64encode(u_chat.getvalue()).decode()
                st.session_state.state = run_sovereign_scan(client, c_b64, u_bio, vibe_mode, plat_mode)
                status.update(label="Target Analyzed.", state="complete")
            st.rerun()

with col_out:
    st.markdown("#### 📡 TACTICAL MONITOR")
    
    # Permanent Meters (Zero Shift)
    s = st.session_state.state if st.session_state.state else {}
    met = s.get('metrics', {})
    
    m1, m2, m3 = st.columns(3)
    m1.write(f"**WARMTH** ({met.get('warmth', 0)}%)")
    m1.progress(met.get('warmth', 0) / 100)
    m2.write(f"**TENSION** ({met.get('tension', 0)}%)")
    m2.progress(met.get('tension', 0) / 100)
    m3.write(f"**RISK** ({met.get('risk', 0)}%)")
    m3.progress(met.get('risk', 0) / 100)

    st.markdown("---")

    if s:
        # Signal Center
        f_left, f_right = st.columns(2)
        with f_left:
            for g in s.get('flags', {}).get('green', []):
                st.markdown(f"<div class='signal-card green-zone'>🎯 {g}</div>", unsafe_allow_html=True)
        with f_right:
            for r in s.get('flags', {}).get('red', []):
                st.markdown(f"<div class='signal-card red-zone'>⚠️ {r}</div>", unsafe_allow_html=True)
        
        st.info(f"**Architect's Note:** {s.get('note')}")

        # Alpha Moves
        for i, move in enumerate(s.get('moves', [])):
            card_style = "alpha-box flame-glow" if (vibe_mode == "The Flame" or move['type'] == "Power") else "alpha-box"
            st.markdown(f"""
                <div class="{card_style}">
                    <small style="font-family:Orbitron; color:#fcd34d;">{move['type'].upper()} MOVE</small>
                    <h2 style="color:white; margin:10px 0;">"{move['zin']}"</h2>
                    <p style="font-size:0.85rem; opacity:0.7; border-top:1px solid #334155; padding-top:10px;">
                        <b>Logic:</b> {move['logic']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            c_btn, s_btn = st.columns([1, 1])
            if c_btn.button(f"📋 Copy Move {i+1}", key=f"cp_{i}"): st.toast("Line Copied!")
            
            # De "Share Win" Logica (Visueel Component)
            if s_btn.button(f"🖼️ Generate Share Card {i+1}", key=f"sh_{i}"):
                st.markdown(f"""
                    <div class="share-preview">
                        <p style="font-size:0.6rem; opacity:0.5; margin-bottom:10px;">TACTICAL REPORT // {plat_mode.upper()}</p>
                        <h4 style="color:#fcd34d; margin-bottom:20px;">TARGET ANALYZED</h4>
                        <p style="font-family:'Inter'; font-style:italic; font-size:1.2rem; margin-bottom:25px;">"{move['zin']}"</p>
                        <div style="display:flex; justify-content:space-around; font-size:0.7rem; border-top:1px solid #334155; padding-top:15px;">
                            <span>TENSION: {met.get('tension')}%</span>
                            <span>WARMTH: {met.get('warmth')}%</span>
                        </div>
                        <p style="margin-top:20px; font-size:0.5rem; color:#fcd34d;">CALCULATED BY RIZZ ARCHITECT AI</p>
                    </div>
                """, unsafe_allow_html=True)
                st.download_button("💾 Download Report (Mockup)", "Fake Image Data", file_name="rizz_report.txt")
    else:
        st.info("System Standby. Upload tactical data om de neural scan te starten.")

st.markdown("<div style='text-align:center; opacity:0.2; font-size:0.6rem; margin-top:80px; font-family:Orbitron; letter-spacing:2px;'>PROJECT SOVEREIGN // ASCENDED STATUS // BEYOND THE INTERVIEW</div>", unsafe_allow_html=True)
