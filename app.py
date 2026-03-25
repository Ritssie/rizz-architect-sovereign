import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re
import urllib.parse

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Rizz Architect Sovereign", page_icon="⚡", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. BRUTE FORCE CSS (Dark Mode Perfection) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&family=Inter:wght@300;500;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background-color: #010409 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }}

    header[data-testid="stHeader"] {{ background: #010409 !important; }}

    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 20px; padding: 20px 0; border-bottom: 2px solid rgba(252, 211, 77, 0.3); margin-bottom: 25px; }}
    .brand-logo {{ width: 65px; height: 65px; border-radius: 15px; border: 2px solid #fcd34d; box-shadow: 0 0 20px rgba(252, 211, 77, 0.4); object-fit: cover; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 800; color: #ffffff !important; }}
    .logotype span {{ color: #fcd34d !important; }}

    .stButton>button {{ width: 100%; background: #fcd34d !important; color: #010409 !important; font-weight: 800; border-radius: 12px; border: none !important; }}
    .glass-card {{ background: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(252, 211, 77, 0.2) !important; border-radius: 20px; padding: 20px; margin-bottom: 15px; }}
    .pick-container {{ border-left: 5px solid #fcd34d; padding: 25px; margin-top: 25px; background: rgba(252, 211, 77, 0.05); border-radius: 0 20px 20px 0; }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d !important; font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px; }}
    .stCodeBlock {{ background-color: rgba(252, 211, 77, 0.05) !important; border: 1px dashed #fcd34d !important; }}
    
    /* Input Fixes */
    input, textarea {{ background-color: #0d1117 !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LANGUAGE & STATE ---
lang_choice = st.sidebar.radio("🌐 Language", ["🇳🇱", "🇬🇧"], horizontal=True)
lang = "NL" if lang_choice == "🇳🇱" else "EN"

texts = {
    "NL": {
        "scan": "⚡ START GROK-4 SCAN", "wait": "Architect analyseert patronen...",
        "armor": "📍 Intelligence & Armor", "pick": "THE EXECUTIONER'S CHOICE",
        "strategy": "Strategie", "tab_spar": "🥊 Sparring Sim", "tab_analyze": "🔍 Strategische Scan",
        "info": "Systeem stand-by. Upload tactische data.", "copy_hint": "Klik om te kopiëren:",
        "context": "Context (Vibe)", "reset": "REBOOT CORE"
    },
    "EN": {
        "scan": "⚡ START GROK-4 SCAN", "wait": "Decoding social dynamics...",
        "armor": "📍 Intelligence & Armor", "pick": "THE EXECUTIONER'S CHOICE",
        "strategy": "Strategy", "tab_spar": "🥊 Sparring Sim", "tab_analyze": "🔍 Strategic Scan",
        "info": "System Idle. Upload tactical data.", "copy_hint": "Click to copy:",
        "context": "Context (Vibe)", "reset": "REBOOT CORE"
    }
}
t = texts[lang]

for key in ['rizz_master', 'chat_history', 'sim_active']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'chat_history' else (False if key == 'sim_active' else None)

# --- 4. HELPERS ---
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: return json.loads(match.group())
        return json.loads(text)
    except: return None

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center;">{logo_img}</div>', unsafe_allow_html=True)
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    if st.button(t['reset']):
        st.session_state.clear()
        st.rerun()

# --- 6. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 7. MAIN INTERFACE ---
if not user_api_key:
    st.warning("⚠️ Voer je xAI API Key in.")
else:
    tab1, tab2 = st.tabs([t['tab_analyze'], t['tab_spar']])

    with tab1:
        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            st.markdown("<div class='label-tag'>Tactische Intake</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, use_container_width=True)
                context = st.text_area(t['context'], placeholder="Beschrijf de flow...")
                if st.button(t['scan']):
                    with st.spinner(t['wait']):
                        try:
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            
                            system_prompt = f"""
                            Identity: Rizz Architect Ultra 3.0. Role: Strategic Mastermind. 
                            Taal: {lang}. Platform: {platform}.
                            
                            Return EXACTLY this JSON structure:
                            {{
                                "weather": "Vibe beschrijving",
                                "outfit": "Armor advies",
                                "options": [
                                    {{"type": "Playful Provocateur", "zin": "..."}},
                                    {{"type": "Elegant Direct", "zin": "..."}},
                                    {{"type": "Pattern Interrupt", "zin": "..."}}
                                ],
                                "architect_pick": {{"choice_idx": 0, "reason": "Psychologische reden"}}
                            }}
                            """
                            
                            res = client.chat.completions.create(
                                model="grok-4.20-0309-non-reasoning", 
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": f"Analyseer dit gesprek. Context: {context}"},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                    ]}
                                ]
                            )
                            st.session_state.rizz_master = extract_json(res.choices[0].message.content)
                            st.rerun()
                        except Exception as e: st.error(f"Grok Error: {e}")

        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown(f"<div class='label-tag'>{t['armor']}</div>", unsafe_allow_html=True)
                
                # Weer & Outfit
                st.markdown(f'<div class="glass-card"><b>📍 Klimaat:</b> {data.get("weather", "N/A")}<br><b>🛡️ Armor:</b> {data.get("outfit", "N/A")}</div>', unsafe_allow_html=True)
                
                options = data.get('options', [])
                pick = data.get('architect_pick', {})
                v_idx = pick.get('choice_idx', 0)

                # --- THE VERDICT (WINNAAR) ---
                if options:
                    winner = options[v_idx] if v_idx < len(options) else options[0]
                    st.markdown(f"<div class='pick-container'><div class='label-tag'>{t['pick']}</div><p style='color:#fcd34d; font-size:0.8rem;'>{t['copy_hint']}</p></div>", unsafe_allow_html=True)
                    st.code(winner.get('zin'), language=None)
                    st.markdown(f"<div style='padding:10px 25px; color:#94a3b8; font-size:0.85rem;'><b>{t['strategy']} ({winner.get('type')}):</b> {pick.get('reason')}</div>", unsafe_allow_html=True)

                    # --- OVERIGE OPTIES ---
                    st.markdown("<div class='label-tag' style='margin-top:30px;'>Strategische Dimensies</div>", unsafe_allow_html=True)
                    for i, opt in enumerate(options):
                        if i != v_idx:
                            with st.expander(f"🔹 {opt.get('type')}"):
                                st.code(opt.get('zin'), language=None)
            else:
                st.info(t['info'])

    with tab2:
        st.markdown("<div class='label-tag'>Combat Simulator</div>", unsafe_allow_html=True)
        # Hier komt je Sparring Sim logica (vergelijkbaar met tab2 in je code)...
