import streamlit as st
from openai import OpenAI
import base64
import json
import time

# ==============================================================================
# --- 1. CONFIG & NEON STYLING ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v20.0", page_icon="🔥", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #05070a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    /* Neon Glow Cards */
    .glow-card {
        background: #0d1117; border: 1px solid #30363d; border-radius: 15px;
        padding: 25px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(252, 211, 77, 0.05);
        transition: 0.3s;
    }
    .flame-border { border: 1px solid #ff4b2b !important; box-shadow: 0 0 20px rgba(255, 75, 43, 0.2); }
    
    .metric-box {
        background: rgba(255,255,255,0.03); border-radius: 10px; padding: 15px;
        text-align: center; border: 1px solid #30363d;
    }
    
    .type-tag { 
        font-family: 'Orbitron'; font-size: 0.6rem; letter-spacing: 1px;
        padding: 3px 10px; border-radius: 5px; background: rgba(252, 211, 77, 0.1); color: #fcd34d;
    }
    
    .stButton>button { border-radius: 10px !important; font-family: 'Orbitron'; background: #fcd34d !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. THE FLAME ENGINE (No-Question Logic) ---
# ==============================================================================
def execute_neural_scan(client, chat_b64, bio_text, vibe, goal):
    # De prompt dwingt nu "Pattern Breaks" af
    no_question_rule = ""
    if vibe in ["Alpha", "The Flame"]:
        no_question_rule = "STRICT RULE: Do NOT use question marks (?). Make bold assumptions, teases, or observations instead."

    prompt = f"""Role: Sovereign Dating Architect. Vibe: {vibe}. Goal: {goal}.
    {no_question_rule}
    Analyze the subtext. Generate 3 types in Dutch:
    1. The Pattern Breaker (Unexpected observation, no questions)
    2. The Escalator (High sexual tension, playful/edgy)
    3. The Closer (Leading towards a date/number)
    
    Return JSON: {{
        "metrics": {{"warmth": int, "risk": int, "tension": int}},
        "analysis": "short subtext summary",
        "responses": [
            {{"type": "Pattern Breaker", "zin": "str", "logic": "str"}},
            {{"type": "The Escalator", "zin": "str", "logic": "str"}},
            {{"type": "The Closer", "zin": "str", "logic": "str"}}
        ]
    }}"""
    
    content = [{"type": "text", "text": f"Context: {bio_text}"}]
    if chat_b64: content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 3. UI LAYOUT ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fff;'>RIZZ<span style='color:#fcd34d;'>ARCHITECT</span> v20</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔥 TACTICAL CORE")
    api_key = st.text_input("Grok API Key", type="password")
    vibe = st.selectbox("Current Vibe", ["Funny", "Mysterious", "Alpha", "The Flame"])
    goal = st.selectbox("Objective", ["Building Tension", "Escalating", "Closing"])
    st.markdown("---")
    if st.button("RESET SYSTEM"): 
        st.session_state.state = None
        st.rerun()

col_left, col_right = st.columns([1, 1.5], gap="large")

with col_left:
    st.markdown("#### 📥 INTEL UPLOAD")
    u_chat = st.file_uploader("Screenshot Chat", type=['png','jpg','jpeg'])
    if u_chat: st.image(u_chat, use_container_width=True)
    u_bio = st.text_area("Bio / Prompt Intel", placeholder="Wat staat er in haar bio?", height=100)
    
    if st.button("⚡ EXECUTE NEURAL SCAN"):
        if api_key and u_chat:
            progress_text = ["Analyzing subtext...", "Detecting body language...", "Calculating tension...", "Breaking patterns...", "Generating heat..."]
            status_container = st.empty()
            
            client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
            chat_b = base64.b64encode(u_chat.getvalue()).decode()
            
            for t in progress_text:
                status_container.status(t)
                time.sleep(0.5)
                
            st.session_state.state = execute_neural_scan(client, chat_b, u_bio, vibe, goal)
            st.rerun()

with col_right:
    if st.session_state.state:
        s = st.session_state.state
        m = s.get('metrics', {})
        
        # 1. VISUAL METRICS (The Widgets)
        st.markdown("#### 📡 TACTICAL METRICS")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-box'><small>WARMTH</small><br><b style='color:#22c55e;'>{m.get('warmth')}%</b></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-box'><small>GHOST RISK</small><br><b style='color:#ef4444;'>{m.get('risk')}%</b></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-box' style='border-color:#ff4b2b;'><small>SEXUAL TENSION</small><br><b style='color:#ff4b2b;'>{m.get('tension')}%</b></div>", unsafe_allow_html=True)
        
        st.caption(f"**Architect's Note:** {s.get('analysis')}")
        st.markdown("---")

        # 2. OUTPUT CARDS (The Results)
        for resp in s.get('responses', []):
            is_flame = vibe == "The Flame"
            border_style = "flame-border" if is_flame else ""
            
            st.markdown(f"""
                <div class="glow-card {border_style}">
                    <span class="type-tag">{resp['type'].upper()}</span>
                    <h2 style="color:white; margin:15px 0;">"{resp['zin']}"</h2>
                    <p style="font-size:0.85rem; opacity:0.7; border-top: 1px solid #30363d; padding-top:10px;">
                        <b>Logic:</b> {resp['logic']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📋 Copy {resp['type']}"): st.toast(f"{resp['type']} Copied!")
            
    else:
        st.info("System Standby. Upload tactical data om de neural scan te starten.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN v20.0 // FLAME_MODE_ENABLED // NO_QUESTION_LOGIC</div>", unsafe_allow_html=True)
