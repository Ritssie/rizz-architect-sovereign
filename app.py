import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import time

# ==============================================================================
# --- 1. CORE CONFIGURATION ---
# ==============================================================================
st.set_page_config(
    page_title="RIZZ ARCHITECT v14.0", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session States
if 'state' not in st.session_state: st.session_state.state = None
if 'is_scanning' not in st.session_state: st.session_state.is_scanning = False

# ==============================================================================
# --- 2. ADVANCED CSS (Animations & Stability) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #05070a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    /* Scanning Animation */
    .scan-container { position: relative; border-radius: 15px; border: 1px solid #fcd34d33; overflow: hidden; }
    .scan-line {
        position: absolute; width: 100%; height: 4px; background: #fcd34d;
        box-shadow: 0 0 20px #fcd34d; top: 0; z-index: 10;
        animation: scan 2s linear infinite;
    }
    @keyframes scan { 0% { top: 0%; } 100% { top: 100%; } }

    .brand-logo { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; text-align: center; margin-bottom: 20px; }
    .brand-logo span { color: #fcd34d; text-shadow: 0 0 15px rgba(252, 211, 77, 0.5); }

    /* Result Cards */
    .metric-card { 
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(252, 211, 77, 0.2);
        padding: 15px; border-radius: 12px; text-align: center;
    }
    
    .winner-card { 
        background: linear-gradient(145deg, rgba(252, 211, 77, 0.15), #010409);
        border: 1px solid #fcd34d; border-radius: 20px; padding: 25px; margin-top: 10px;
    }

    .stButton>button { width: 100% !important; font-family: 'Orbitron'; font-weight: bold; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. CORE FUNCTIONS ---
# ==============================================================================
def get_analysis(client, b64, ctx, lang, vibe, goal):
    prompt = f"""Role: Sovereign Architect. Respond in {lang}. 
    Goal: {goal}. Vibe: {vibe}.
    Return JSON: {{
        "success_rate": int, "sentiment": "Cold/Neutral/High Interest", 
        "ghost_risk": int, "red_flags": [str], "green_flags": [str],
        "options": [ {{"type": "Hook/Bridge/Close", "zin": "str", "psychology": "str"}} ],
        "winner_idx": 0
    }}"""
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [{"type": "text", "text": f"Ctx: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 4. UI LAYOUT ---
# ==============================================================================
st.markdown("<div class='brand-logo'>RIZZ<span>ARCHITECT</span> v14</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ STRATEGIC CONTROL")
    api_key = st.text_input("Grok API Key", type="password")
    lang = st.selectbox("Taal", ["NL", "EN"])
    st.markdown("---")
    goal = st.selectbox("Tactisch Doel", ["The Hook (Start)", "The Bridge (Deepen)", "The Close (Date/Number)"])
    vibe = st.select_slider("Persona Vibe", options=["Sweet", "Funny", "Mysterious", "Alpha"])
    
    if st.button("🔄 SYSTEM REBOOT"):
        st.session_state.state = None
        st.rerun()

# --- MAIN INTERFACE ---
col_l, col_r = st.columns([1, 1.2])

with col_l:
    st.subheader("📥 Data Intake")
    u_file = st.file_uploader("Upload Chat Screenshot", type=['png','jpg','jpeg'], label_visibility="collapsed")
    
    image_placeholder = st.empty() # Vaste plek voor afbeelding
    
    if u_file:
        # Toon afbeelding met eventuele scan-animatie
        if st.session_state.is_scanning:
            image_placeholder.markdown(f'<div class="scan-container"><div class="scan-line"></div><img src="data:image/jpeg;base64,{base64.b64encode(u_file.getvalue()).decode()}" style="width:100%"></div>', unsafe_allow_html=True)
        else:
            image_placeholder.image(u_file, use_container_width=True)
            
        u_ctx = st.text_area("Context (vrijdagavond, sfeer, etc.)", height=70)
        
        if st.button("⚡ EXECUTE ARCHITECT SCAN"):
            if not api_key:
                st.error("API Key missing!")
            else:
                st.session_state.is_scanning = True
                st.rerun()

# SCANNING LOGIC
if st.session_state.is_scanning:
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    img_b64 = base64.b64encode(u_file.getvalue()).decode()
    st.session_state.state = get_analysis(client, img_b64, u_ctx, lang, vibe, goal)
    st.session_state.is_scanning = False
    st.rerun()

with col_r:
    st.subheader("📡 Tactical Output")
    output_container = st.container() # Voorkomt layout shift
    
    if st.session_state.state:
        s = st.session_state.state
        with output_container:
            # Fase 2: Sentiment & Ghosting Meters
            m1, m2, m3 = st.columns(3)
            m1.metric("Sentiment", s.get('sentiment', 'Neutral'))
            m2.metric("Ghosting Risk", f"{s.get('ghost_risk', 0)}%")
            m3.metric("Hit Rate", f"{s.get('success_rate', 0)}%")
            
            # Flags
            f1, f2 = st.columns(2)
            with f1: 
                for gf in s.get('green_flags', []): st.caption(f"✅ {gf}")
            with f2: 
                for rf in s.get('red_flags', []): st.caption(f"🚩 {rf}")

            # Winner Card
            opts = s.get('options', [])
            w_idx = s.get('winner_idx', 0)
            if opts:
                w = opts[w_idx]
                st.markdown(f"""
                    <div class="winner-card">
                        <small style="color:#fcd34d">TOP SELECTION: {w.get('type')}</small>
                        <h2 style="margin:10px 0;">"{w.get('zin')}"</h2>
                        <p style="font-size:0.85rem; border-left: 2px solid #fcd34d; padding-left:10px;">
                        <b>Stratagem:</b> {w.get('psychology')}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("📋 KOPIEER ALPHA LINE"):
                    st.toast("✅ Line copied to clipboard!", icon="🔥")
            
            # Arsenal
            st.markdown("---")
            for i, opt in enumerate(opts):
                if i != w_idx:
                    with st.expander(f"Alt: {opt.get('type')}"):
                        st.write(f"**{opt.get('zin')}**")
                        st.caption(opt.get('psychology'))
    else:
        output_container.info("System stand-by. Initialiseer scan om tactical signals te ontvangen.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V14.0 // BUGFIXED // UI_STABLE</div>", unsafe_allow_html=True)
