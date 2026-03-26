import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import json

# ==============================================================================
# --- 1. CONFIG & SYSTEM ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v18.5", page_icon="🎯", layout="wide")

# Zorg dat de state altijd een dictionary is om KeyErrors te voorkomen
if 'state' not in st.session_state or st.session_state.state is None:
    st.session_state.state = {}

def get_color(val, reverse=False):
    if reverse: val = 100 - val
    if val < 30: return "#ef4444"
    if val < 70: return "#facc15"
    return "#22c55e"

# ==============================================================================
# --- 2. ELITE UI STYLING ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; color: #e6edf3 !important; font-family: 'Inter', sans-serif; 
    }
    
    .platform-badge {
        padding: 5px 15px; border-radius: 5px; font-family: 'Orbitron'; font-size: 0.7rem;
        text-transform: uppercase; margin-bottom: 15px; display: inline-block;
    }
    .hinge { background: #8e2de2; color: white; border: 1px solid #ffffff44; }
    .bumble { background: #ffcb37; color: black; border: 1px solid #00000022; }
    .tinder { background: #fe3c72; color: white; border: 1px solid #ffffff44; }

    .alpha-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid #fcd34d66;
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .logic-box { 
        font-size: 0.85rem; color: #fcd34d; opacity: 0.9; 
        margin-top: 10px; font-style: italic; background: rgba(252, 211, 77, 0.05);
        padding: 8px; border-radius: 5px;
    }
    .badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: bold; margin-right: 5px; margin-bottom: 5px;
        background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. ENGINE (Platform Logic) ---
# ==============================================================================
def run_analysis(client, chat_b64, bio_b64, bio_text, ctx, vibe, platform):
    prompt = f"""Role: Sovereign Dating Architect. Platform: {platform}.
    Analyze Chat + Bio. If Hinge, analyze prompts. If Bumble, focus on the opener.
    Respond in Dutch. Style: {vibe}.
    
    STRICT JSON Output:
    {{
        "detected_platform": "Hinge/Bumble/Tinder",
        "detected_interests": ["str"],
        "sentiment_label": "str",
        "ghost_risk": int,
        "success_rate": int,
        "tags": ["str"],
        "fast_move": {{"zin": "str", "logic": "str"}},
        "deep_move": {{"zin": "str", "logic": "str"}},
        "platform_tip": "str"
    }}"""
    
    msg_content = [{"type": "text", "text": f"Ctx: {ctx}. Manual Bio: {bio_text}"}]
    if chat_b64: msg_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})
    if bio_b64: msg_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{bio_b64}"}})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": msg_content}]
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# ==============================================================================
# --- 4. UI ASSEMBLY ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fcd34d;'>RIZZ<span>ARCHITECT</span> v18.5</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛰️ GLOBAL SETTINGS")
    api_key = st.text_input("Grok API Key", type="password")
    platform_hint = st.selectbox("Target Platform", ["Auto-Detect", "Hinge", "Bumble", "Tinder"])
    vibe_style = st.select_slider("Vibe", ["Playful", "Alpha", "Mysterious"])
    st.markdown("---")
    if st.button("RESET ENGINE"): 
        st.session_state.state = {}
        st.rerun()

col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("#### 📥 DATA INGESTION")
    u_chat = st.file_uploader("Upload Chat", type=['png','jpg','jpeg'])
    u_bio = st.file_uploader("Upload Bio Screenshot", type=['png','jpg','jpeg'])
    u_bio_text = st.text_area("Manual Bio Info", placeholder="e.g. She likes traveling...", height=70)
    
    if st.button("⚡ EXECUTE NEURAL SCAN"):
        if not api_key: st.error("API Key Required")
        else:
            with st.status("Analyzing Patterns...", expanded=True):
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                c_b64 = base64.b64encode(u_chat.getvalue()).decode() if u_chat else None
                b_b64 = base64.b64encode(u_bio.getvalue()).decode() if u_bio else None
                st.session_state.state = run_analysis(client, c_b64, b_b64, u_bio_text, "Dating", vibe_style, platform_hint)
                st.rerun()

with col_right:
    s = st.session_state.state
    if s and "error" not in s and s != {}:
        # Platform Display
        p_name = s.get('detected_platform', 'Tinder').lower()
        st.markdown(f"<div class='platform-badge {p_name}'>{p_name} Detected</div>", unsafe_allow_html=True)
        
        # Metrics
        c1, c2, c3 = st.columns(3)
        g_color = get_color(s.get('ghost_risk', 0), reverse=True)
        s_color = get_color(s.get('success_rate', 0))
        
        c1.metric("Sentiment", s.get('sentiment_label', 'Neutral'))
        c2.markdown(f"<small>GHOST RISK</small><br><b style='color:{g_color}; font-size:1.2rem;'>{s.get('ghost_risk', 0)}%</b>", unsafe_allow_html=True)
        c3.markdown(f"<small>HIT RATE</small><br><b style='color:{s_color}; font-size:1.2rem;'>{s.get('success_rate', 0)}%</b>", unsafe_allow_html=True)

        # Tags
        st.markdown("<div style='margin: 10px 0;'>", unsafe_allow_html=True)
        for tag in s.get('tags', []): st.markdown(f"<span class='badge'>⚡ {tag}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if s.get('platform_tip'):
            st.info(f"💡 **Platform Tip:** {s['platform_tip']}")

        # Output Cards (Bulletproofed with .get)
        fast = s.get('fast_move', {"zin": "No data", "logic": "N/A"})
        deep = s.get('deep_move', {"zin": "No data", "logic": "N/A"})

        st.markdown("### 🏆 FAST MOVE")
        st.markdown(f"""<div class='alpha-card'>
            <h2 style='color:white; margin:0;'>"{fast.get('zin')}"</h2>
            <div class='logic-box'><b>Logic:</b> {fast.get('logic')}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("📋 Copy Fast"): st.toast("Copied!")

        st.markdown("### 🧠 DEEP MOVE")
        st.markdown(f"""<div class='alpha-card' style='border-color:#8e2de2;'>
            <h2 style='color:white; margin:0;'>"{deep.get('zin')}"</h2>
            <div class='logic-box'><b>Logic:</b> {deep.get('logic')}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("📋 Copy Deep"): st.toast("Copied!")
    elif "error" in s:
        st.error(f"AI Error: {s['error']}")
    else:
        st.info("System stand-by. Initialiseer scan.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN v18.5 // BULLETPROOF ENGINE</div>", unsafe_allow_html=True)
