import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

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
    /* Styling voor de copy-box */
    .stCodeBlock {{ background-color: rgba(252, 211, 77, 0.05) !important; border: 1px dashed #fcd34d !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LANGUAGE & SESSION STATE ---
lang_choice = st.sidebar.radio("🌐 Language", ["🇳🇱", "🇬🇧"], horizontal=True)
lang = "NL" if lang_choice == "🇳🇱" else "EN"

texts = {
    "NL": {
        "warning": "⚠️ Voer je xAI API Key in de sidebar in.",
        "tab_analyze": "🔍 STRATEGISCHE SCAN",
        "tab_spar": "🥊 SPARRING SIM",
        "wait": "Architect analyseert patronen...",
        "info": "Systeem stand-by. Upload tactische data.",
        "pick": "THE EXECUTIONER'S CHOICE",
        "strategy": "STRATEGIE",
        "intake": "Tactische Intake",
        "context": "Vibe Context",
        "scan_btn": "⚡ START GROK-4 SCAN",
        "report": "Intelligence Rapport",
        "weather": "📍 Klimaat:",
        "armor": "🛡️ Aanbevolen Armor:",
        "copy_hint": "Klik hieronder om te kopiëren:"
    },
    "EN": {
        "warning": "⚠️ Waiting for Grok-4 API Credentials...",
        "tab_analyze": "🔍 STRATEGIC SCAN",
        "tab_spar": "🥊 SPARRING SIM",
        "wait": "Decoding social dynamics...",
        "info": "System Idle. Upload tactical data to begin.",
        "pick": "THE EXECUTIONER'S CHOICE",
        "strategy": "STRATEGY",
        "intake": "Tactical Intake",
        "context": "Vibe Context",
        "scan_btn": "⚡ INITIATE GROK-4 SCAN",
        "report": "Intelligence Report",
        "weather": "📍 Climate:",
        "armor": "🛡️ Recommended Armor:",
        "copy_hint": "Click below to copy:"
    }
}
t = texts[lang]

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
    st.markdown(f'<div style="text-align:center;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#fcd34d; text-align:center;'>QUANTUM ACCESS</h3>", unsafe_allow_html=True)
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    u_city = st.text_input("MY LOCATION", placeholder="Amsterdam")
    t_city = st.text_input("TARGET LOCATION", placeholder="Utrecht")
    if st.button("REBOOT CORE"):
        st.session_state.clear()
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN INTERFACE ---
if not user_api_key:
    st.warning(t['warning'])
else:
    tab1, tab2 = st.tabs([t['tab_analyze'], t['tab_spar']])

    with tab1:
        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            st.markdown(f"<div class='label-tag'>{t['intake']}</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, width='stretch')
                context = st.text_area(t['context'], placeholder="Describe the energy...")
                if st.button(t['scan_btn']):
                    with st.spinner(t['wait']):
                        try:
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            res = client.chat.completions.create(
                                model="grok-4.20-0309-non-reasoning", 
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": f"Identity: Rizz Architect Ultra 4.0. Mission: Analyze {platform}. Platform: {platform}. Context: {context}. Return ONLY JSON. Options must contain 'zin' and 'type'."},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": "Analyze target. Return JSON: weather, outfit, options (list of 3 with type and zin), architect_pick (dict with choice int and reason)."},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                    ]}
                                ]
                            )
                            st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                            st.rerun()
                        except Exception as e: st.error(f"Grok-4 Scan Error: {e}")
        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown(f"<div class='label-tag'>{t['report']}</div>", unsafe_allow_html=True)
                st.markdown(f'<div class="glass-card"><b>{t["weather"]}</b> {data.get("weather", "N/A")}<br><b>{t["armor"]}</b> {data.get("outfit", "N/A")}</div>', unsafe_allow_html=True)
                
                # --- SAFE DATA PARSING ---
                p = data.get('architect_pick', {})
                if not isinstance(p, dict): p = {"choice": 1, "reason": str(p)}
                options = data.get('options', [])
                
                if options and isinstance(options, list):
                    try: choice_int = int(p.get('choice', 1))
                    except: choice_int = 1
                    
                    idx = max(0, min(choice_int - 1, len(options) - 1))
                    best = options[idx]
                    
                    d_zin = best.get('zin', '...') if isinstance(best, dict) else str(best)
                    d_type = best.get('type', 'Strategy') if isinstance(best, dict) else 'Executioner'

                    st.markdown(f"""
                        <div class="pick-container">
                            <div class='label-tag'>{t['pick']}</div>
                            <p style="color:#fcd34d; font-size:0.8rem; margin-bottom:5px;">{t['copy_hint']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # De "Magic Copy" box
                    st.code(d_zin, language=None)
                    
                    st.markdown(f"""
                        <div style="padding: 0 25px;">
                            <div style="margin-top:10px; color:#94a3b8; font-size:0.85rem;">
                                <b>{t['strategy']} ({d_type}):</b> {p.get('reason', 'Analyzed by Grok-4.')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("System refresh required. Data structure mismatch.")
            else:
                st.info(t['info'])

    with tab2:
        st.markdown("<div class='label-tag'>Combat Simulator</div>", unsafe_allow_html=True)
        if not st.session_state.get('sim_active', False):
            if st.button("START NEURAL SIMULATION"):
                st.session_state.sim_active = True
                st.session_state.chat_history = [{"role": "assistant", "content": "Hey. What's the move?"}]
                st.rerun()
        else:
            for m in st.session_state.chat_history:
                with st.chat_message(m["role"]): st.markdown(m["content"])
            if pr := st.chat_input("Input command..."):
                st.session_state.chat_history.append({"role": "user", "content": pr})
                with st.chat_message("assistant"):
                    client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                    r = client.chat.completions.create(
                        model="grok-4-1-fast-non-reasoning", 
                        messages=[{"role":"system","content":"Dating sim match. Be challenging."}] + st.session_state.chat_history
                    )
                    rep = r.choices[0].message.content
                    st.markdown(rep)
                    st.session_state.chat_history.append({"role": "assistant", "content": rep})
            if st.button("TERMINATE SESSION"):
                st.session_state.sim_active = False
                st.session_state.chat_history = []
                st.rerun()
