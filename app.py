import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# ==============================================================================
# --- 1. CONFIG & STYLING ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v17.0", page_icon="👑", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None

def get_color(val, reverse=False):
    """Bepaalt kleur op basis van percentage (rood-geel-groen)"""
    if reverse: val = 100 - val
    if val < 30: return "#ef4444" # Rood
    if val < 70: return "#facc15" # Geel
    return "#22c55e" # Groen

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{ 
        background-color: #020617 !important; color: #f1f5f9 !important; font-family: 'Inter', sans-serif; 
    }}

    /* Vaste containers om layout shift te voorkomen */
    .main-card {{
        background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(252, 211, 77, 0.2);
        border-radius: 20px; padding: 25px; min-height: 400px;
    }}

    /* Alpha Box Styling */
    .alpha-card {{
        background: linear-gradient(145deg, #1e1b4b, #020617);
        border: 2px solid #fcd34d; border-radius: 15px; padding: 25px;
        margin-bottom: 20px; line-height: 1.6;
    }}
    
    .logic-text {{
        color: #fcd34d; font-size: 0.9rem; font-weight: 600;
        background: rgba(252, 211, 77, 0.1); padding: 10px; border-radius: 8px; margin-top: 15px;
    }}

    .badge {{
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: bold; margin-right: 5px; margin-bottom: 5px;
        background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
    }}

    .stButton>button {{ border-radius: 10px !important; font-family: 'Orbitron'; font-size: 0.8rem; }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. CORE ENGINE ---
# ==============================================================================
def execute_analysis(client, chat_b64, bio_b64, bio_text, ctx, lang, vibe, goal):
    prompt = f"""Role: Elite Dating Architect. Language: {lang}. 
    Goal: {goal}. Vibe: {vibe}. 
    Provide analysis and two distinct response types:
    1. Fast Move (Short, snappy, punchy)
    2. Deep Move (Contextual, longer, woven with bio/chat details)
    
    Return JSON: {{
        "sentiment_score": int, "ghost_risk": int, "success_rate": int,
        "sentiment_label": "Cold/Warm/Hot",
        "tags": [str], "bio_insights": [str],
        "fast_move": {{"zin": "str", "logic": "str"}},
        "deep_move": {{"zin": "str", "logic": "str"}}
    }}"""
    
    msg_content = [{"type": "text", "text": f"Context: {ctx}. Bio info: {bio_text}"}]
    if chat_b64: msg_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})
    if bio_b64: msg_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{bio_b64}"}})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": msg_content}]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 3. UI ASSEMBLY ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fff;'>RIZZ<span style='color:#fcd34d;'>ARCHITECT</span> PRO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ OPERATION COMMAND")
    api_key = st.text_input("Grok API Key", type="password")
    vibe = st.select_slider("Persona Vibe", ["Funny", "Mysterious", "Alpha"])
    goal = st.selectbox("Strategic Goal", ["The Hook", "The Bridge", "The Close"])
    st.markdown("---")
    if st.button("🔄 SYSTEM RESET"):
        st.session_state.state = None
        st.rerun()

# --- INPUT SECTION ---
col_in, col_out = st.columns([1, 1.3], gap="large")

with col_in:
    st.markdown("#### 📥 DATA INGESTION")
    u_chat = st.file_uploader("Chat Screenshot", type=['png','jpg','jpeg'])
    u_bio = st.file_uploader("Bio Screenshot (Optional)", type=['png','jpg','jpeg'])
    u_bio_text = st.text_area("Bio Text / Interests", placeholder="Sushi, Techno, Dogs...", height=68)
    u_ctx = st.text_input("Extra Context", placeholder="e.g. She's being short with me")
    
    if st.button("⚡ START NEURAL SCAN"):
        if not api_key: st.error("API Key Required")
        else:
            with st.spinner("Processing Signals..."):
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                chat_b = base64.b64encode(u_chat.getvalue()).decode() if u_chat else None
                bio_b = base64.b64encode(u_bio.getvalue()).decode() if u_bio else None
                st.session_state.state = execute_analysis(client, chat_b, bio_b, u_bio_text, u_ctx, "NL", vibe, goal)
                st.rerun()

# --- OUTPUT SECTION ---
with col_out:
    # Placeholder container om verspringing te voorkomen
    with st.container():
        if st.session_state.state:
            s = st.session_state.state
            
            # 1. Metrics & Gauges (Dynamische Kleuren)
            st.markdown("#### 📡 TACTICAL SIGNALS")
            c1, c2, c3 = st.columns(3)
            
            # Kleur-logica voor metrics
            s_color = get_color(s.get('success_rate', 0))
            g_color = get_color(s.get('ghost_risk', 0), reverse=True)
            
            c1.markdown(f"<div style='text-align:center;'><small>SENTIMENT</small><br><b style='font-size:1.2rem; color:#fcd34d;'>{s.get('sentiment_label')}</b></div>", unsafe_allow_html=True)
            c2.markdown(f"<div style='text-align:center;'><small>GHOST RISK</small><br><b style='font-size:1.2rem; color:{g_color};'>{s.get('ghost_risk')}%</b></div>", unsafe_allow_html=True)
            c3.markdown(f"<div style='text-align:center;'><small>HIT RATE</small><br><b style='font-size:1.2rem; color:{s_color};'>{s.get('success_rate')}%</b></div>", unsafe_allow_html=True)

            # 2. Visual Tags (Badges)
            st.markdown("<div style='margin-top:15px;'>", unsafe_allow_html=True)
            for tag in s.get('tags', []): st.markdown(f"<span class='badge'>⚡ {tag}</span>", unsafe_allow_html=True)
            for bio in s.get('bio_insights', []): st.markdown(f"<span class='badge' style='border-color:#fcd34d;'>📍 {bio}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # 3. The Alpha Selections (Two Variants)
            st.markdown("---")
            
            # Fast Move (Short)
            st.markdown("### 🏆 FAST MOVE (Snappy)")
            st.markdown(f"""<div class='alpha-card'>
                <h2 style='color:white; margin:0;'>"{s['fast_move']['zin']}"</h2>
                <div class='logic-text'><b>Architect's Logic:</b> {s['fast_move']['logic']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("📋 COPY FAST MOVE"): st.toast("Fast Move Copied!")

            # Deep Move (Contextual)
            st.markdown("### 🧠 DEEP MOVE (Contextual)")
            st.markdown(f"""<div class='alpha-card'>
                <h2 style='color:white; margin:0;'>"{s['deep_move']['zin']}"</h2>
                <div class='logic-text'><b>Architect's Logic:</b> {s['deep_move']['logic']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("📋 COPY DEEP MOVE"): st.toast("Deep Move Copied!")
            
        else:
            st.info("System Standby. Upload tactical data to initialize neural processing.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN v17.0 // FINAL STABLE // MOBILE OPTIMIZED</div>", unsafe_allow_html=True)
