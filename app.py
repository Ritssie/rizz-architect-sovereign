import streamlit as st
from openai import OpenAI
import base64
import json

# ==============================================================================
# --- 1. CONFIG & PERSISTENT STATE ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v19.0", page_icon="🕵️", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None

# ==============================================================================
# --- 2. ADVANCED UI STYLING (Zero Shift) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0d1117 !important; color: #c9d1d9 !important; font-family: 'Inter', sans-serif; 
    }
    
    /* Result Cards met vaste padding om shift te minimaliseren */
    .res-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; min-height: 120px;
    }
    .type-tag { 
        font-family: 'Orbitron'; font-size: 0.6rem; color: #fcd34d; 
        border: 1px solid #fcd34d33; padding: 2px 8px; border-radius: 4px;
    }
    .logic-sub { font-size: 0.8rem; opacity: 0.6; margin-top: 8px; font-style: italic; }
    
    .img-preview { border: 2px solid #30363d; border-radius: 10px; position: sticky; top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. ARCHITECT ENGINE v19 (The Rule of Three) ---
# ==============================================================================
def run_neural_scan(client, chat_b64, bio_b64, bio_text, vibe, platform):
    prompt = f"""Role: Sovereign Dating Architect. Platform: {platform}.
    Detect UI Anchors (Hinge Prompts, Bumble Openers). 
    Generate 3 response types in Dutch. Vibe: {vibe}.
    
    STRICT JSON Output:
    {{
        "platform": "Hinge/Bumble/Tinder",
        "anchors_found": ["str"],
        "metrics": {{"sentiment": "str", "ghost_risk": int}},
        "punchy": {{"zin": "max 7 words", "logic": "str"}},
        "contextualist": {{"zin": "medium length", "logic": "str"}},
        "questioner": {{"zin": "open question", "logic": "str"}}
    }}"""
    
    content = [{"type": "text", "text": f"Bio: {bio_text}"}]
    if chat_b64: content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})
    if bio_b64: content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{bio_b64}"}})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": content}]
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e: return {"error": str(e)}

# ==============================================================================
# --- 4. APP LAYOUT (Sticky Preview & Skeleton) ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fcd34d;'>RIZZ<span>ARCHITECT</span> v19</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM CONFIG")
    api_key = st.text_input("Grok API Key", type="password")
    vibe = st.select_slider("Vibe", ["Funny", "Mysterious", "Alpha"])
    platform_mode = st.selectbox("Detection Mode", ["Auto-Detect Anchors", "Hinge", "Bumble", "Tinder"])
    if st.button("CLEAN STATE"): 
        st.session_state.state = None
        st.rerun()

# Hoofdindeling: Links de Foto, Rechts de Analyse
col_img, col_main = st.columns([1, 2], gap="medium")

with col_img:
    st.markdown("#### 🖼️ CONTEXT PREVIEW")
    u_chat = st.file_uploader("Upload Chat", type=['png','jpg','jpeg'], label_visibility="collapsed")
    if u_chat:
        st.markdown('<div class="img-preview">', unsafe_allow_html=True)
        st.image(u_chat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    u_bio = st.file_uploader("Upload Bio/Prompt", type=['png','jpg','jpeg'])
    u_text = st.text_area("Manual Context", placeholder="Interesses, sfeer...", height=100)

with col_main:
    # --- PLACEHOLDERS (Skeleton) ---
    st.markdown("#### 📡 ARCHITECT OUTPUT")
    header_placeholder = st.empty()
    metric_placeholder = st.empty()
    result_placeholder = st.empty()

    if st.button("⚡ EXECUTE NEURAL SCAN"):
        if api_key and u_chat:
            with st.status("Scanning UI Anchors & Patterns..."):
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                c_b64 = base64.b64encode(u_chat.getvalue()).decode()
                b_b64 = base64.b64encode(u_bio.getvalue()).decode() if u_bio else None
                st.session_state.state = run_neural_scan(client, c_b64, b_b64, u_text, vibe, platform_mode)
                st.rerun()
        else: st.warning("Zorg voor een API Key en een Chat Screenshot.")

    # --- RENDER OUTPUT ---
    if st.session_state.state:
        s = st.session_state.state
        
        # Header & Platform
        with header_placeholder:
            plat = s.get('platform', 'Detecting...')
            st.markdown(f"**Platform:** `{plat}` | **Anchors:** `{', '.join(s.get('anchors_found', ['None']))}`")
        
        # Metrics Row
        with metric_placeholder:
            m1, m2 = st.columns(2)
            m1.metric("Sentiment", s.get('metrics', {}).get('sentiment', 'N/A'))
            risk = s.get('metrics', {}).get('ghost_risk', 0)
            m2.metric("Ghost Risk", f"{risk}%", delta=f"{risk}%", delta_color="inverse")

        # The Rule of Three Results
        with result_placeholder:
            # 1. The Punchy One
            p = s.get('punchy', {})
            st.markdown(f"""<div class="res-card">
                <span class="type-tag">THE PUNCHY ONE</span>
                <h3 style="margin:10px 0; color:white;">"{p.get('zin')}"</h3>
                <div class="logic-sub"><b>Logic:</b> {p.get('logic')}</div>
            </div>""", unsafe_allow_html=True)
            
            # 2. The Contextualist
            c = s.get('contextualist', {})
            st.markdown(f"""<div class="res-card" style="border-left: 3px solid #fcd34d;">
                <span class="type-tag" style="background:#fcd34d; color:black;">THE CONTEXTUALIST</span>
                <h3 style="margin:10px 0; color:white;">"{c.get('zin')}"</h3>
                <div class="logic-sub"><b>Logic:</b> {c.get('logic')}</div>
            </div>""", unsafe_allow_html=True)
            
            # 3. The Questioner
            q = s.get('questioner', {})
            st.markdown(f"""<div class="res-card">
                <span class="type-tag">THE QUESTIONER</span>
                <h3 style="margin:10px 0; color:white;">"{q.get('zin')}"</h3>
                <div class="logic-sub"><b>Logic:</b> {q.get('logic')}</div>
            </div>""", unsafe_allow_html=True)

    else:
        result_placeholder.info("Awaiting Tactical Ingestion. Gebruik de knop hierboven om te scannen.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:100px;'>SOVEREIGN v19.0 // RULE OF THREE // STICKY_CONTEXT</div>", unsafe_allow_html=True)
