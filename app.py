import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import urllib.parse

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Rizz Architect Ultra 3.0", page_icon="⚡", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. THE EXECUTIONER CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #010409 !important;
        color: #e2e8f0 !important;
    }}
    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 15px; padding: 10px 0; border-bottom: 1px solid rgba(252, 211, 77, 0.2); margin-bottom: 15px; }}
    .brand-logo {{ width: 55px; height: 55px; border-radius: 12px; border: 2px solid #fcd34d; object-fit: cover; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #e2e8f0 !important; }}
    .logotype span {{ color: #fcd34d !important; }}
    .stButton>button {{ width: 100%; background: #fcd34d !important; color: #010409 !important; font-weight: 800; border-radius: 15px; border: none !important; }}
    .glass-card {{ background: rgba(30, 41, 59, 0.5) !important; border: 1px solid rgba(252, 211, 77, 0.1) !important; border-radius: 18px; padding: 18px; }}
    .pick-container {{ border: 2px solid #fcd34d; border-radius: 20px; padding: 20px; margin-top: 20px; background: rgba(252, 211, 77, 0.05); }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d !important; font-size: 0.75rem; letter-spacing: 2px; text-transform: uppercase; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'sim_active' not in st.session_state: st.session_state.sim_active = False

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#fcd34d; text-align:center;'>ACCESS GRANTED</h3>", unsafe_allow_html=True)
    user_api_key = st.text_input("GROK API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    u_city = st.text_input("YOUR CITY", placeholder="e.g. Amsterdam")
    t_city = st.text_input("HER CITY", placeholder="e.g. Utrecht")
    if st.button("REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN INTERFACE ---
if not user_api_key:
    st.warning("⚠️ Enter your xAI API Key to initialize the Architect.")
else:
    tab1, tab2 = st.tabs(["🔍 Analyze", "🥊 Sparring"])

    with tab1:
        c1, c2 = st.columns([1, 1.4], gap="medium")
        with c1:
            st.markdown("<div class='label-tag'>Tactical Intake</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, use_container_width=True)
                context = st.text_area("Context", placeholder="Current vibe?")
                if st.button("⚡ EXECUTE SCAN"):
                    with st.spinner("Analyzing patterns..."):
                        try:
                            # Gebruik Grok-2-Vision
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            
                            sys_msg = f"""
                            Jij bent '⚡ Rizz Architect Ultra 3.0: The Executioner Edition'. 
                            Platform: {platform}. Locaties: {u_city}/{t_city}.
                            Protocol: Triple-A Analyse. Wetten: Max 20 woorden, Max 1 emoji. 
                            Antwoord EXCLUSIEF in JSON formaat.
                            """

                            res = client.chat.completions.create(
                                model="grok-2-vision-latest", # Beste model voor screenshots
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": sys_msg},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": f"Context: {context}. Geef JSON met weather, outfit, venues (list), options (3x: type, zin), architect_pick (choice int, reason)."},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                    ]}
                                ]
                            )
                            # Parsing & Error Handling
                            content = res.choices[0].message.content
                            st.session_state.rizz_master = json.loads(content)
                            st.rerun()
                        except Exception as e: st.error(f"Scan Error: {e}")

        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown("<div class='label-tag'>Intelligence & Armor</div>", unsafe_allow_html=True)
                st.markdown(f'<div class="glass-card"><b>Weather:</b> {data.get("weather")}<br><b>Armor:</b> {data.get("outfit")}</div>', unsafe_allow_html=True)
                
                p = data.get('architect_pick', {})
                options = data.get('options', [])
                if options:
                    idx = max(0, min(int(p.get('choice', 1)) - 1, len(options)-1))
                    best = options[idx]
                    st.markdown(f"""
                        <div class="pick-container">
                            <div class='label-tag'>THE ARCHITECT'S PICK</div>
                            <h2 style="margin:0; color:#fff; font-size:1.6rem;">"{best.get('zin')}"</h2>
                            <p style="font-size:0.85rem; color:#fcd34d; margin-top:10px;"><b>Strategy:</b> {p.get('reason')}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Waiting for tactical data...")

    with tab2:
        st.markdown("<div class='label-tag'>Sparring Session</div>", unsafe_allow_html=True)
        if not st.session_state.sim_active:
            if st.button("START SIMULATION"):
                st.session_state.sim_active = True
                st.session_state.chat_history = [{"role": "assistant", "content": "Hey."}]
                st.rerun()
        else:
            for m in st.session_state.chat_history:
                with st.chat_message(m["role"]): st.markdown(m["content"])
            
            if pr := st.chat_input("Your move..."):
                st.session_state.chat_history.append({"role": "user", "content": pr})
                with st.chat_message("assistant"):
                    client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                    r = client.chat.completions.create(
                        model="grok-2-latest", # Beste model voor chat
                        messages=[{"role":"system","content":f"Dating sim op {platform}. Wees een uitdagende match."}] + st.session_state.chat_history
                    )
                    rep = r.choices[0].message.content
                    st.markdown(rep)
                    st.session_state.chat_history.append({"role": "assistant", "content": rep})
            
            if st.button("TERMINATE"):
                st.session_state.sim_active = False
                st.session_state.chat_history = []
                st.rerun()
