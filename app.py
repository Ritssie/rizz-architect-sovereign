import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Rizz Architect Ultra 4.0", page_icon="⚡", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. GROK-4 NEON CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&family=Inter:wght@300;500;800&display=swap');
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }}
    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 20px; padding: 20px 0; border-bottom: 2px solid rgba(252, 211, 77, 0.3); margin-bottom: 25px; }}
    .brand-logo {{ width: 70px; height: 70px; border-radius: 15px; border: 2px solid #fcd34d; box-shadow: 0 0 20px rgba(252, 211, 77, 0.4); object-fit: cover; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 800; color: #ffffff !important; }}
    .logotype span {{ color: #fcd34d !important; text-shadow: 0 0 10px rgba(252, 211, 77, 0.5); }}
    .stButton>button {{ width: 100%; background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; color: #000000 !important; font-weight: 800; border-radius: 12px; border: none !important; text-transform: uppercase; }}
    .glass-card {{ background: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(252, 211, 77, 0.2) !important; border-radius: 20px; padding: 20px; }}
    .pick-container {{ border-left: 5px solid #fcd34d; padding: 25px; margin-top: 25px; background: rgba(252, 211, 77, 0.03); border-radius: 0 20px 20px 0; }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d !important; font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px; }}
    .stCodeBlock {{ background-color: rgba(252, 211, 77, 0.05) !important; border: 1px dashed #fcd34d !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
for key in ['rizz_master', 'chat_history', 'sim_active']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'chat_history' else (False if key == 'sim_active' else None)

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: return json.loads(match.group())
        return json.loads(text)
    except: return None

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center;">{logo_img}</div>', unsafe_allow_html=True)
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    if st.button("REBOOT CORE"):
        st.session_state.clear()
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN INTERFACE ---
if not user_api_key:
    st.warning("⚠️ Voer je xAI API Key in.")
else:
    tab1, tab2 = st.tabs(["🔍 STRATEGISCHE SCAN", "🥊 SPARRING SIM"])

    with tab1:
        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            st.markdown("<div class='label-tag'>Tactische Intake</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, width='stretch')
                context = st.text_area("Vibe Context", placeholder="Describe the energy...")
                if st.button("⚡ START GROK-4 SCAN"):
                    with st.spinner("Architect analyseert patronen..."):
                        try:
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            
                            # DE SYSTEM ROLE INSTRUCTIE VOOR GROK
                            system_prompt = f"""
                            Identity: Rizz Architect Ultra 3.0. Role: Strategic Mastermind.
                            Focus: Psychological dominance & natural charisma. 
                            Goal: Move dynamics towards a physical meeting.
                            
                            Protocol:
                            1. Platform Nuance ({platform}).
                            2. Investment & Flow analysis.
                            3. Subtext Hook identification.
                            
                            Output: You MUST return a JSON object with:
                            - 'weather': Current vibe description.
                            - 'outfit': Stylistic advice.
                            - 'options': A list of EXACTLY 3 objects:
                                1. {{'type': 'Playful Provocateur', 'zin': '...'}}
                                2. {{'type': 'Elegant Direct', 'zin': '...'}}
                                3. {{'type': 'Pattern Interrupt', 'zin': '...'}}
                            - 'architect_pick': {{'choice': 1, 'reason': 'Why this works based on social psychology'}}
                            """
                            
                            res = client.chat.completions.create(
                                model="grok-4.20-0309-non-reasoning", 
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": f"Context: {context}"},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                    ]}
                                ]
                            )
                            parsed = extract_json(res.choices[0].message.content)
                            if parsed:
                                st.session_state.rizz_master = parsed
                                st.rerun()
                        except Exception as e: st.error(f"Error: {e}")
        
        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown("<div class='label-tag'>Intelligence Rapport</div>", unsafe_allow_html=True)
                
                # Weer & Outfit
                st.markdown(f'<div class="glass-card"><b>📍 Klimaat:</b> {data.get("weather", "N/A")}<br><b>🛡️ Armor:</b> {data.get("outfit", "N/A")}</div>', unsafe_allow_html=True)
                
                options = data.get('options', [])
                p = data.get('architect_pick', {})
                
                if options and isinstance(options, list):
                    # --- WINNAAR TONEN ---
                    try: c_idx = int(p.get('choice', 1)) - 1
                    except: c_idx = 0
                    c_idx = max(0, min(c_idx, len(options) - 1))
                    
                    best = options[c_idx]
                    st.markdown("<div class='pick-container'><div class='label-tag'>THE EXECUTIONER'S CHOICE</div><p style='color:#fcd34d; font-size:0.8rem;'>Klik om te kopiëren:</p></div>", unsafe_allow_html=True)
                    st.code(best.get('zin', str(best)), language=None)
                    st.markdown(f"<div style='padding:0 25px; color:#94a3b8; font-size:0.85rem; margin-bottom:20px;'><b>Strategie ({best.get('type')}):</b> {p.get('reason', 'Analyzed.')}</div>", unsafe_allow_html=True)

                    # --- OVERIGE OPTIES TONEN ---
                    st.markdown("<div class='label-tag' style='margin-top:30px;'>Alternatieve Tactieken</div>", unsafe_allow_html=True)
                    for i, opt in enumerate(options):
                        if i != c_idx:
                            with st.expander(f"🔹 {opt.get('type', 'Tactiek')}"):
                                st.code(opt.get('zin', str(opt)), language=None)
            else:
                st.info("System stand-by. Upload tactische data.")

    with tab2:
        # Sparring Sim code blijft gelijk...
        st.markdown("<div class='label-tag'>Combat Simulator</div>")
        # [Rest van de sim code]
