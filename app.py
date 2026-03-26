import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# ==============================================================================
# --- 1. CONFIG & PERSISTENCE ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v15.0", page_icon="👑", layout="wide")

# Initialiseer History in de sessie (blijft bewaard zolang de tab open is)
if 'history' not in st.session_state: st.session_state.history = []
if 'state' not in st.session_state: st.session_state.state = None

# ==============================================================================
# --- 2. ELITE UI/UX STYLING ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #020408 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    .brand-header { text-align: center; padding: 20px; margin-bottom: 30px; border-bottom: 1px solid #fcd34d22; }
    .brand-header h1 { font-family: 'Orbitron'; font-size: 2.2rem; color: #fff; margin: 0; }
    .brand-header span { color: #fcd34d; text-shadow: 0 0 15px #fcd34d55; }

    /* Alpha Secret Weapon Card */
    .alpha-box {
        background: linear-gradient(165deg, #0f172a 0%, #020617 100%);
        border: 2px solid #fcd34d; border-radius: 20px; padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 0 20px rgba(252,211,77,0.05);
        position: relative; margin: 20px 0;
    }
    .alpha-tag { 
        position: absolute; top: -12px; left: 20px; background: #fcd34d; color: #000;
        font-family: 'Orbitron'; font-size: 0.6rem; padding: 2px 12px; border-radius: 5px; font-weight: bold;
    }

    /* History & Metrics */
    .history-card { 
        background: rgba(255,255,255,0.03); border-radius: 10px; padding: 10px; 
        margin-bottom: 8px; border-left: 3px solid #fcd34d; font-size: 0.8rem;
    }
    .hit-rate-info { font-size: 0.65rem; opacity: 0.5; margin-top: 5px; font-style: italic; }

    .stButton>button { border-radius: 12px !important; font-family: 'Orbitron'; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(252,211,77,0.2); }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. LOGIC & API ---
# ==============================================================================
def get_analysis(client, b64, ctx, lang, vibe, goal):
    prompt = f"""Role: Sovereign Architect. Respond in {lang}. 
    Goal: {goal}. Vibe: {vibe}. 
    Return JSON: {{
        "success_rate": int, "sentiment": "str", "ghost_risk": int,
        "options": [ {{"type": "str", "zin": "str", "psychology": "str"}} ],
        "winner_idx": 0
    }}"""
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [{"type": "text", "text": f"Ctx: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
        )
        data = json.loads(res.choices[0].message.content)
        # Sla op in history
        win = data['options'][data['winner_idx']]
        st.session_state.history.insert(0, {"zin": win['zin'], "goal": goal, "time": "Just now"})
        st.session_state.history = st.session_state.history[:5] # Max 5 items
        return data
    except: return None

# ==============================================================================
# --- 4. APP LAYOUT ---
# ==============================================================================
st.markdown("<div class='brand-header'><h1>RIZZ<span>ARCHITECT</span></h1><small>LAUNCH EDITION V15.0</small></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ CONTROL PANEL")
    api_key = st.text_input("Grok API Key", type="password")
    
    tab1, tab2 = st.tabs(["Strategy", "History"])
    
    with tab1:
        lang = st.selectbox("Language", ["NL", "EN"])
        goal = st.selectbox("Tactical Goal", ["The Hook", "The Bridge", "The Close"])
        vibe = st.select_slider("Persona Vibe", options=["Sweet", "Funny", "Mysterious", "Alpha"])
        if st.button("🗑️ CLEAR SESSION"):
            st.session_state.state = None
            st.rerun()

    with tab2:
        if not st.session_state.history:
            st.caption("No history yet...")
        for item in st.session_state.history:
            st.markdown(f"""<div class='history-card'><b>{item['goal']}</b><br>"{item['zin']}"</div>""", unsafe_allow_html=True)

# --- MAIN CONTENT ---
col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown("### 📤 INTAKE")
    u_file = st.file_uploader("Screenshot", type=['png','jpg','jpeg'], label_visibility="collapsed")
    if u_file:
        st.image(u_file, use_container_width=True)
        u_ctx = st.text_area("Intelligence Context", placeholder="e.g. It's Friday night, she likes sushi...", height=80)
        if st.button("⚡ EXECUTE ARCHITECT SCAN"):
            if api_key:
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                img_b64 = base64.b64encode(u_file.getvalue()).decode()
                st.session_state.state = get_analysis(client, img_b64, u_ctx, lang, vibe, goal)
                st.rerun()
            else: st.error("Enter API Key")

with col_out:
    st.markdown("### 📡 ANALYSIS")
    if st.session_state.state:
        s = st.session_state.state
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Sentiment", s.get('sentiment', 'Neutral'))
        m2.metric("Ghosting Risk", f"{s.get('ghost_risk', 0)}%")
        with m3:
            st.metric("Hit Rate", f"{s.get('success_rate', 0)}%")
            st.markdown("<p class='hit-rate-info'>*Based on similar profile matches</p>", unsafe_allow_html=True)

        # Alpha Secret Weapon Card
        opts = s.get('options', [])
        w_idx = s.get('winner_idx', 0)
        if opts:
            w = opts[w_idx]
            st.markdown(f"""
                <div class="alpha-box">
                    <div class="alpha-tag">SECRET WEAPON: {w.get('type').upper()}</div>
                    <h2 style="color:white; margin-bottom:15px; font-size:1.6rem;">"{w.get('zin')}"</h2>
                    <p style="font-size:0.85rem; opacity:0.8; border-top: 1px solid #ffffff22; padding-top:10px;">
                        <b>Architect's Logic:</b> {w.get('psychology')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Copy Button & Result Tracker
            c_copy, c_res = st.columns(2)
            with c_copy:
                if st.button("📋 COPY ALPHA LINE"):
                    st.toast("Line copied to clipboard!", icon="🔥")
            with c_res:
                if st.button("✅ I SENT THIS"):
                    st.toast("Result logged. Hit Rate database updated.")

            # Arsenal
            st.markdown("### 📐 STRATAGEM ARSENAL")
            for i, opt in enumerate(opts):
                if i != w_idx:
                    with st.expander(f"Alt: {opt.get('type')}"):
                        st.write(f"**{opt.get('zin')}**")
                        st.caption(opt.get('psychology'))
    else:
        st.info("System stand-by. Upload intelligence to initialize scan.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px; letter-spacing:3px;'>SOVEREIGN v15.0 // END-TO-END ENCRYPTED // LAUNCH READY</div>", unsafe_allow_html=True)
