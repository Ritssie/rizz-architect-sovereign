import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re
import urllib.parse

# --- 1. CONFIG & SYSTEM SETUP ---
st.set_page_config(page_title="Rizz Architect Sovereign 4.0", page_icon="⚡", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. BRUTE FORCE COMPACT CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&family=Inter:wght@300;500;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background-color: #010409 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }}
    header[data-testid="stHeader"] {{ background: #010409 !important; }}

    /* Kill Whitespace */
    div[data-testid="stVerticalBlock"] > div {{ padding-top: 0rem !important; padding-bottom: 0.2rem !important; margin-top: 0rem !important; }}
    .stCodeBlock {{ margin-bottom: 0.4rem !important; }}
    
    /* Branding */
    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 15px; padding: 15px 0; border-bottom: 2px solid rgba(252, 211, 77, 0.2); margin-bottom: 15px; }}
    .brand-logo {{ width: 50px; height: 50px; border-radius: 10px; border: 1px solid #fcd34d; object-fit: cover; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 800; color: #ffffff !important; }}
    .logotype span {{ color: #fcd34d !important; }}

    /* Components */
    .stButton>button {{ width: 100%; background: #fcd34d !important; color: #010409 !important; font-weight: 800; border-radius: 8px; border: none !important; }}
    .glass-card {{ background: rgba(15, 23, 42, 0.9) !important; border: 1px solid rgba(252, 211, 77, 0.1) !important; border-radius: 10px; padding: 10px; margin-bottom: 8px; }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d !important; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px; }}
    .pick-container {{ border-left: 3px solid #fcd34d; padding: 10px 15px !important; background: rgba(252, 211, 77, 0.04); border-radius: 0 10px 10px 0; margin-bottom: 12px; }}
    .venue-box {{ background: rgba(255,255,255,0.03); padding: 8px; border-radius: 8px; border: 1px solid rgba(252,211,77,0.1); font-size: 0.7rem; }}
    
    /* Chat Styling */
    [data-testid="stChatMessage"] {{ background: rgba(15, 23, 42, 0.5) !important; border-radius: 10px !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
for key in ['rizz_master', 'chat_history', 'sim_active', 'coach_feedback']:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ['chat_history', 'coach_feedback'] else (False if key == 'sim_active' else None)

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#fcd34d;'>COMMAND CENTER</h4>", unsafe_allow_html=True)
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["WhatsApp", "Instagram", "Hinge", "Tinder", "Real Life"])
    target_city = st.text_input("TARGET CITY", placeholder="e.g. Amsterdam")
    if st.button("REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. TABS ---
tab1, tab2 = st.tabs(["🔍 STRATEGIC SCAN", "🥊 TRAINING LAB"])

with tab1:
    if not user_api_key:
        st.warning("⚠️ Enter API Key in Sidebar.")
    else:
        c1, c2 = st.columns([1, 1.4], gap="medium")
        with c1:
            st.markdown("<div class='label-tag'>Tactical Intake</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, use_container_width=True)
                context = st.text_area("Vibe Context", placeholder="Wat is het doel?", height=70)
                if st.button("⚡ EXECUTE SCAN"):
                    with st.spinner("Decoding..."):
                        try:
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            sys_prompt = f"Identity: Rizz Architect. Platform: {platform}. Target City: {target_city}. Return JSON with dynamics, success_rate, red_flags, armor, venues, options, verdict."
                            res = client.chat.completions.create(
                                model="grok-4.20-0309-non-reasoning",
                                response_format={"type": "json_object"},
                                messages=[{"role": "system", "content": sys_prompt},
                                          {"role": "user", "content": [{"type":"text","text":f"Context: {context}"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}]
                            )
                            st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                            st.rerun()
                        except Exception as e: st.error(f"Error: {e}")

        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown("<div class='label-tag'>Success Rate</div>", unsafe_allow_html=True)
                st.progress(data.get('success_rate', 50) / 100)
                
                st.markdown("<div class='label-tag'>Field Intelligence</div>", unsafe_allow_html=True)
                st.markdown(f'<div class="glass-card" style="font-size:0.8rem;"><b>📍 Dynamics:</b> {data.get("dynamics")}<br><b>🛡️ Armor:</b> {data.get("armor")}</div>', unsafe_allow_html=True)

                st.markdown("<div class='label-tag'>The Executioner's Choice</div>", unsafe_allow_html=True)
                winner = data.get('options', [{}])[data.get('verdict', {}).get('idx', 0)]
                st.markdown("<div class='pick-container'>", unsafe_allow_html=True)
                st.code(winner.get('zin'), language=None)
                st.markdown(f"<p style='color:#fcd34d; font-size:0.7rem; margin-top:4px;'><b>Logic:</b> {data.get('verdict', {}).get('logic')}</p></div>", unsafe_allow_html=True)

                st.markdown("<div class='label-tag'>Alternatives</div>", unsafe_allow_html=True)
                for opt in data.get('options', []):
                    if opt.get('zin') != winner.get('zin'):
                        st.markdown(f"<div style='font-size:0.6rem; color:#94a3b8; margin-bottom:-10px;'>{opt.get('type')}</div>", unsafe_allow_html=True)
                        st.code(opt.get('zin'), language=None)

with tab2:
    st.markdown("<div class='label-tag'>Combat Simulator & Coaching</div>", unsafe_allow_html=True)
    if not st.session_state.sim_active:
        col_s1, col_s2 = st.columns(2)
        with col_s1: archetype = st.selectbox("Persona Target", ["Spicy/Hard to get", "Cold/Corporate", "High Energy/Party"])
        with col_s2: difficulty = st.select_slider("Difficulty", ["Easy", "Normal", "Executioner"])
        
        if st.button("🚀 INITIALIZE TRAINING"):
            st.session_state.sim_active = True
            st.session_state.chat_history = [{"role": "assistant", "content": "Hoi."}]
            st.rerun()
    else:
        sc1, sc2 = st.columns([1.5, 1])
        with sc1:
            for m in st.session_state.chat_history:
                with st.chat_message(m["role"]): st.markdown(m["content"])
            
            if prompt := st.chat_input("Type je antwoord..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.spinner("Target is typing..."):
                    client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                    # Target Response
                    r = client.chat.completions.create(
                        model="grok-4.20-0309-non-reasoning",
                        messages=[{"role":"system","content":f"Dating sim. Jij bent een vrouw, type: {archetype}."}] + st.session_state.chat_history
                    )
                    # Coach Feedback
                    f = client.chat.completions.create(
                        model="grok-4.20-0309-non-reasoning",
                        messages=[{"role":"system","content":"Jij bent de Rizz Architect Coach. Geef korte, brute feedback op het laatste bericht van de user. Focus op status en frame."}] + st.session_state.chat_history
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": r.choices[0].message.content})
                    st.session_state.coach_feedback.append(f.choices[0].message.content)
                    st.rerun()
        
        with sc2:
            st.markdown("<div class='label-tag'>👨‍🏫 Architect Coaching</div>", unsafe_allow_html=True)
            if st.session_state.coach_feedback:
                st.markdown(f"<div class='glass-card' style='border:1px solid #fcd34d;'>{st.session_state.coach_feedback[-1]}</div>", unsafe_allow_html=True)
            if st.button("TERMINATE SESSION"):
                st.session_state.sim_active = False
                st.session_state.chat_history = []
                st.session_state.coach_feedback = []
                st.rerun()
