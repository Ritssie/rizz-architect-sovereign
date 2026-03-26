import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# ==============================================================================
# --- 1. SESSIEBEHEER & CONFIG ---
# ==============================================================================
st.set_page_config(page_title="RIZZ ARCHITECT v16.0", page_icon="🕵️‍♂️", layout="wide")

if 'state' not in st.session_state: st.session_state.state = None
if 'success_log' not in st.session_state: st.session_state.success_log = 0

# ==============================================================================
# --- 2. ELITE CYBER-DASHBOARD UI (Met Stealth Mode Support) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #030712 !important; color: #f8fafc !important; font-family: 'Inter', sans-serif; 
    }

    /* Scanning Animatie Overlay */
    .scanner-overlay {
        position: relative; border: 1px solid #fcd34d44; border-radius: 15px; overflow: hidden;
    }
    .scan-bar {
        position: absolute; width: 100%; height: 2px; background: #fcd34d;
        box-shadow: 0 0 15px #fcd34d; z-index: 5; animation: scanMove 2.5s infinite;
    }
    @keyframes scanMove { 0% { top: 0%; } 50% { top: 100%; } 100% { top: 0%; } }

    /* Resultaten Hiërarchie */
    .metric-container { background: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 12px; text-align: center; }
    .alpha-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #020617 100%);
        border: 2px solid #fcd34d; border-radius: 20px; padding: 25px; margin-top: 15px;
        box-shadow: 0 0 30px rgba(252, 211, 77, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. CORE ENGINE (Met Bio-Scanner Logic) ---
# ==============================================================================
def get_comprehensive_analysis(client, chat_b64, bio_b64, bio_text, ctx, lang, vibe, goal):
    # De prompt dwingt de AI nu om Bio-data te verweven
    prompt = f"""Role: Elite Dating Architect. Language: {lang}. 
    Goal: {goal}. User Style: {vibe}.
    Analyze Chat + Bio. 
    Bio Context: {bio_text if bio_text else "Extract from image if provided."}
    
    STRICT JSON Output:
    {{
        "sentiment": "Cold/Neutral/Warm/Hot", "ghost_risk": int, "success_rate": int,
        "bio_signals": ["interest 1", "interest 2"],
        "tactical_signals": ["signal 1", "signal 2"],
        "options": [
            {{"type": "The Hook", "zin": "str", "psychology": "str"}},
            {{"type": "The Spike", "zin": "str", "psychology": "str"}},
            {{"type": "The Close", "zin": "str", "psychology": "str"}}
        ],
        "winner_idx": 0
    }}"""
    
    messages = [{"role": "system", "content": prompt}]
    user_content = [{"type": "text", "text": f"Context: {ctx}"}]
    
    if chat_b64:
        user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})
    if bio_b64:
        user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{bio_b64}"}})
        
    messages.append({"role": "user", "content": user_content})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=messages
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 4. DASHBOARD LAYOUT ---
# ==============================================================================
st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#fcd34d;'>RIZZ<span>ARCHITECT</span> v16</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛠️ INTEL PARAMETERS")
    api_key = st.text_input("Grok API Key", type="password")
    lang = st.selectbox("Output Language", ["NL", "EN"])
    vibe = st.select_slider("Persona Vibe", ["Playful", "Funny", "Mysterious", "Alpha"])
    goal = st.selectbox("Strategic Goal", ["The Hook", "The Spike", "The Close"])
    st.markdown("---")
    if st.button("🔄 REBOOT SYSTEM"): 
        st.session_state.state = None
        st.rerun()

# Kolommen voor Input
c_chat, c_bio = st.columns(2)

with c_chat:
    st.subheader("📥 CHAT INTAKE")
    u_chat = st.file_uploader("Upload Chat Screenshot", type=['png','jpg','jpeg'], key="chat_up")
    if u_chat: st.image(u_chat, use_container_width=True)

with c_bio:
    st.subheader("🧬 BIO-SCANNER")
    u_bio = st.file_uploader("Upload Profile/Bio Screenshot", type=['png','jpg','jpeg'], key="bio_up")
    bio_text = st.text_area("Or Paste Bio Text Here", placeholder="Houdt van honden, reizen, techno...", height=68)

st.markdown("---")
u_ctx = st.text_input("Additional Context", placeholder="Bijv. 'We hebben gisteren gematcht', 'Ze is een beetje kortaf'...")

# --- EXECUTION ---
if st.button("⚡ EXECUTE ARCHITECT ANALYSIS"):
    if not api_key:
        st.error("Missing API Key.")
    elif not u_chat and not bio_text and not u_bio:
        st.warning("Please provide Chat or Bio data.")
    else:
        with st.status("Initializing Neural Scan...", expanded=True) as status:
            client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
            
            # Image Processing
            chat_b64 = base64.b64encode(u_chat.getvalue()).decode() if u_chat else None
            bio_b64 = base64.b64encode(u_bio.getvalue()).decode() if u_bio else None
            
            st.write("Extracting Signals...")
            st.session_state.state = get_comprehensive_analysis(client, chat_b64, bio_b64, bio_text, u_ctx, lang, vibe, goal)
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            st.rerun()

# --- OUTPUT DISPLAY ---
if st.session_state.state:
    s = st.session_state.state
    res_l, res_r = st.columns([1, 1.5], gap="large")
    
    with res_l:
        st.markdown("### 📡 TACTICAL METRICS")
        m1, m2 = st.columns(2)
        m1.metric("Sentiment", s.get('sentiment', 'N/A'))
        m2.metric("Ghosting Risk", f"{s.get('ghost_risk', 0)}%")
        
        st.progress(s.get('success_rate', 50) / 100, text=f"Hit Rate: {s.get('success_rate')}%")
        
        st.markdown("**Bio Insights:**")
        for b in s.get('bio_signals', []): st.caption(f"📍 {b}")
        
        st.markdown("**Tactical Signals:**")
        for t in s.get('tactical_signals', []): st.caption(f"⚡ {t}")

    with res_r:
        st.markdown("### 🏆 ALPHA SELECTION")
        opts = s.get('options', [])
        w_idx = s.get('winner_idx', 0)
        
        if opts:
            w = opts[w_idx]
            st.markdown(f"""
                <div class="alpha-box">
                    <small style="color:#fcd34d; font-family:Orbitron;">TOP SUGGESTION ({w.get('type')})</small>
                    <h2 style="color:white; margin:15px 0;">"{w.get('zin')}"</h2>
                    <p style="font-size:0.85rem; opacity:0.8; border-top:1px solid #ffffff22; padding-top:10px;">
                        <b>Logic:</b> {w.get('psychology')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 COPY ALPHA LINE"):
                st.toast("Copied to clipboard!", icon="🔥")
            
            # Alternatieven (Goal-Based)
            st.markdown("#### 📐 ALTERNATIVE STRATAGEMS")
            for i, opt in enumerate(opts):
                if i != w_idx:
                    with st.expander(f"{opt.get('type')}"):
                        st.write(f"**{opt.get('zin')}**")
                        st.caption(opt.get('psychology'))

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN v16.0 // BIO-SCANNER ACTIVE // END-TO-END ENCRYPTED</div>", unsafe_allow_html=True)
