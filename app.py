import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# ==============================================================================
# --- 1. CORE SYSTEM & STEALTH LOGIC ---
# ==============================================================================
if 'stealth_mode' not in st.session_state: st.session_state.stealth_mode = False
if 'success_count' not in st.session_state: st.session_state.success_count = 0
if 'state' not in st.session_state: st.session_state.state = None

st.set_page_config(
    page_title="RIZZ ARCHITECT SOVEREIGN v13.5", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. PREMIUM CSS (Dynamic Stealth Styling) ---
# ==============================================================================
if st.session_state.stealth_mode:
    # "Office Mode" - Saai grijs/wit, zakelijk font
    bg_color, text_color, accent = "#ffffff", "#202124", "#1a73e8"
    font_main = "'Segoe UI', Tahoma, sans-serif"
    header_html = "<h3 style='color:#5f6368;'>Quarterly_Report_Analysis_v13.xlsx</h3>"
else:
    # "Cyber Mode" - Jouw originele stijl
    bg_color, text_color, accent = "#05070a", "#e2e8f0", "#fcd34d"
    font_main = "'Inter', sans-serif"
    header_html = "<div style='text-align:center; padding:20px;'><h1 style='font-family:Orbitron; color:#fff; letter-spacing:3px;'>RIZZ<span style='color:#fcd34d;'>ARCHITECT</span></h1></div>"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ 
        background-color: {bg_color} !important; color: {text_color} !important; font-family: {font_main}; 
    }}
    
    .stMetric {{ background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; border: 1px solid {accent}44; }}
    
    .winner-card {{ 
        background: {"linear-gradient(145deg, rgba(252, 211, 77, 0.1), #010409)" if not st.session_state.stealth_mode else "#f8f9fa"};
        border: 1px solid {accent}; border-radius: 20px; padding: 25px; margin-top: 20px;
    }}
    
    .stButton>button {{ 
        width: 100% !important; border-radius: 10px !important; 
        background: {accent} !important; color: {"#000" if not st.session_state.stealth_mode else "#fff"} !important;
        font-family: 'Orbitron', sans-serif; font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. ENGINE CORE ---
# ==============================================================================
def get_analysis(client, b64, ctx, lang, vibe, goal):
    prompt = f"""Role: Sovereign Architect. Respond in {lang}. 
    Strategy: {vibe} vibe. CURRENT GOAL: {goal}.
    STRICT JSON structure: 
    {{
        "success_rate": int, "sentiment": "str", "ghosting_risk": "str",
        "date_planner": "string (suggest a specific date activity based on info)",
        "green_flags": [str], "red_flags": [str],
        "options": [ {{"type": "str", "zin": "str", "psychology": "str"}} ],
        "winner_idx": 0
    }}"""
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}
            ]
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e:
        st.error(f"System Error: {e}")
        return None

# ==============================================================================
# --- 4. INTERFACE ---
# ==============================================================================
with st.sidebar:
    st.markdown("### 🛠️ CORE SETTINGS")
    st.session_state.stealth_mode = st.toggle("🕵️ Stealth Mode", help="Verander de app in een 'werk-document' look.")
    
    st.markdown("---")
    st.metric("🏆 SESSION SUCCESSES", st.session_state.success_count)
    if st.button("➕ LOG WIN (Date/Number)"):
        st.session_state.success_count += 1
        st.balloons()
        
    st.markdown("---")
    api_key = st.text_input("Grok API Key", type="password")
    lang = st.selectbox("Language", ["NL", "EN"])
    
    st.markdown("### 🎯 TACTICAL GOAL")
    target_goal = st.selectbox("Current Objective", 
        ["Building Tension", "Escalate to Number", "Ask on Date", "Vibe Check"])
    
    vibe = st.select_slider("Persona Vibe", options=["Sweet", "Funny", "Mysterious", "Alpha"])

# Header
st.markdown(header_html, unsafe_allow_html=True)

if not api_key:
    st.warning("🔐 INITIALIZE: Voer je API-key in de zijbalk in.")
else:
    col_l, col_r = st.columns([1, 1.2])

    with col_l:
        st.markdown("#### 📥 DATA INGESTION")
        u_file = st.file_uploader("Upload Intelligence", type=['png','jpg','jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Intelligence Context", placeholder="Vibe, relatie, doel...", height=80)
            if st.button("⚡ EXECUTE ARCHITECT SCAN"):
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                img_b64 = base64.b64encode(u_file.getvalue()).decode()
                st.session_state.state = get_analysis(client, img_b64, u_ctx, lang, vibe, target_goal)
                st.rerun()

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # Date Planner (Feedback punt 1)
            if s.get('date_planner'):
                st.success(f"📍 **DATE STRATAGEM:** {s['date_planner']}")
            
            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Sentiment", s.get('sentiment', 'N/A'))
            c2.metric("Ghost Risk", s.get('ghosting_risk', 'N/A'))
            c3.metric("Hit Rate", f"{s.get('success_rate')}%")

            # Winner Card
            opts = s.get('options', [])
            w_idx = s.get('winner_idx', 0)
            if opts:
                w = opts[w_idx]
                st.markdown(f"""
                    <div class="winner-card">
                        <small style='color:{accent};'>TOP ALPHA SELECTION</small>
                        <h2 style='margin:10px 0;'>"{w.get('zin')}"</h2>
                        <hr style='opacity:0.2;'>
                        <p style='font-size:0.85rem;'><b>Psychology:</b> {w.get('psychology')}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("📋 COPY ALPHA LINE"): 
                    st.toast("Copied to clipboard!")

            # Alternatieven
            st.markdown("#### 📐 STRATAGEM ARSENAL")
            for i, opt in enumerate(opts):
                if i != w_idx:
                    with st.expander(f"Option {i+1}: {opt.get('type', 'Alternative')}"):
                        st.write(f"**\"{opt.get('zin')}\"**")
                        st.caption(opt.get('psychology'))
        else:
            st.info("Systeem stand-by. Upload data om te beginnen.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V13.5 // STEALTH-READY</div>", unsafe_allow_html=True)
