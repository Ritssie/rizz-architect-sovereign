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

# Logo Handling
logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. BRUTE FORCE CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&family=Playfair+Display:wght@700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #010409 !important;
        color: #e2e8f0 !important;
    }}

    input, textarea, [data-baseweb="base-input"] {{
        background-color: #0d1117 !important;
        color: #ffffff !important;
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

# --- 3. LANGUAGE & SESSION STATE ---
lang_choice = st.sidebar.radio("🌐 Language", ["🇳🇱", "🇬🇧"], horizontal=True)
lang = "NL" if lang_choice == "🇳🇱" else "EN"

texts = {
    "NL": {
        "access": "SOVEREIGN ACCESS", "key": "xAI API KEY", "field_intel": "Field Intel",
        "m_city": "JOUW STAD", "t_city": "HAAR STAD", "reset": "REBOOT SYSTEM",
        "tab_analyze": "🔍 Analyze", "tab_spar": "🥊 Sparring",
        "intake": "Tactical Intake", "context": "Context (Vibe)", "scan": "⚡ EXECUTE SCAN",
        "wait": "Architect is analyzing patterns...", "armor": "📍 Intelligence & Armor", "weather": "Local Weather",
        "outfit": "Armor (Outfit)", "pick": "🏆 THE ARCHITECT'S PICK", "strategy": "STRATEGY",
        "warning": "⚠️ Voer je xAI API Key in de sidebar in.", "info": "Wachten op tactische data...",
        "sim_start": "START SIMULATION", "sim_end": "TERMINATE",
        "archetype": "Persona Select", "chat_placeholder": "Input message...",
        "coach": "👨‍🏫 DEBRIEF BY ARCHITECT", "coach_wait": "Reviewing performance..."
    },
    "EN": {
        "access": "SOVEREIGN ACCESS", "key": "xAI API KEY", "field_intel": "Field Intel",
        "m_city": "YOUR CITY", "t_city": "HER CITY", "reset": "REBOOT SYSTEM",
        "tab_analyze": "🔍 Analyze", "tab_spar": "🥊 Sparring",
        "intake": "Tactical Intake", "context": "Context (Vibe)", "scan": "⚡ EXECUTE SCAN",
        "wait": "Architect is analyzing patterns...", "armor": "📍 Intelligence & Armor", "weather": "Local Weather",
        "outfit": "Armor (Outfit)", "pick": "🏆 THE ARCHITECT'S PICK", "strategy": "STRATEGY",
        "warning": "⚠️ Enter your xAI API Key in the sidebar.", "info": "Waiting for tactical data...",
        "sim_start": "START SIMULATION", "sim_end": "TERMINATE",
        "archetype": "Persona Select", "chat_placeholder": "Input message...",
        "coach": "👨‍🏫 DEBRIEF BY ARCHITECT", "coach_wait": "Reviewing performance..."
    }
}
t = texts[lang]

if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'sim_active' not in st.session_state: st.session_state.sim_active = False

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((800, 800)) # Iets kleiner voor snellere API upload
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#fcd34d; text-align:center;'>{t['access']}</h3>", unsafe_allow_html=True)
    user_api_key = st.text_input(t['key'], type="password")
    st.markdown("---")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    u_city = st.text_input(t['m_city'], placeholder="e.g. Amsterdam")
    t_city = st.text_input(t['t_city'], placeholder="e.g. Utrecht")
    if st.button(t['reset']):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# --- 6. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 7. MAIN INTERFACE ---
if not user_api_key:
    st.warning(t['warning'])
else:
    tab1, tab2 = st.tabs([t['tab_analyze'], t['tab_spar']])

    with tab1:
        c1, c2 = st.columns([1, 1.4], gap="medium")
        with c1:
            st.markdown(f"<div class='label-tag'>{t['intake']}</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, use_container_width=True)
                context = st.text_area(t['context'], placeholder="Wat is de vibe?")
                if st.button(t['scan']):
                    with st.spinner(t['wait']):
                        try:
                            # FIX: Stabiele xAI Base URL en Modelnaam
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            
                            sys_msg = f"""
                            Jij bent '⚡ Rizz Architect Ultra 3.0: The Executioner Edition'. 
                            Taal: {lang}. Platform: {platform}. Locaties: {u_city}/{t_city}.
                            
                            Analyseer via het Triple-A Protocol (App, Atmosphere, Anomaly).
                            Wetten: Max 20 woorden per optie. Max 1 emoji. Geen clichés.

                            Output strikt in JSON:
                            {{
                              "weather": "string",
                              "outfit": "string",
                              "venues": [{{"naam": "string", "type": "string"}}],
                              "options": [
                                {{"type": "Playful Provocateur", "zin": "string"}},
                                {{"type": "Velvet Charmer", "zin": "string"}},
                                {{"type": "Pattern Interrupt", "zin": "string"}}
                              ],
                              "architect_pick": {{"choice": 1, "reason": "string"}}
                            }}
                            """

                            res = client.chat.completions.create(
                                model="grok-vision-beta", # STABIELE VISION NAAM
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": sys_msg},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": f"Context: {context}"},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                    ]}
                                ]
                            )
                            st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                            st.rerun()
                        except Exception as e: st.error(f"Grok Error: {e}")

        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown(f"<div class='label-tag'>{t['armor']}</div>", unsafe_allow_html=True)
                st.markdown(f'<div class="glass-card"><b>{t["weather"]} {t_city}:</b> {data.get("weather")}<br><br><b>🛡️ {t["outfit"]}:</b> {data.get("outfit")}</div>', unsafe_allow_html=True)
                
                if data.get('venues'):
                    v_cols = st.columns(3)
                    for i, v in enumerate(data.get('venues')[:3]):
                        with v_cols[i]:
                            search_url = urllib.parse.quote(f"{v.get('naam')} {t_city}")
                            st.markdown(f"**{v.get('naam')}**\n\n[MAP](https://www.google.com/maps/search/{search_url})")
                
                p = data.get('architect_pick', {})
                idx = max(0, min(int(p.get('choice', 1)) - 1, 2))
                options = data.get('options', [{}, {}, {}])
                best = options[idx] if idx < len(options) else {"zin": "Fout bij laden", "type": "Onbekend"}
                
                st.markdown(f"""
                    <div class="pick-container">
                        <div class='label-tag'>{t['pick']}</div>
                        <h2 style="margin:0; color:#fff; font-size:1.6rem;">"{best.get('zin')}"</h2>
                        <p style="font-size:0.85rem; color:#fcd34d; margin-top:15px;">
                            <b>{t['strategy']} ({best.get('type')}):</b> {p.get('reason')}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info(t['info'])

    with tab2:
        if not st.session_state.sim_active:
            if st.button(t['sim_start']):
                st.session_state.sim_active = True
                st.session_state.chat_history = [{"role": "assistant", "content": "Hey."}]
                st.rerun()
        else:
            for m in st.session_state.chat_history:
                with st.chat_message(m["role"]): st.markdown(m["content"])
            
            if pr := st.chat_input(t['chat_placeholder']):
                st.session_state.chat_history.append({"role": "user", "content": pr})
                with st.chat_message("assistant"):
                    client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                    r = client.chat.completions.create(
                        model="grok-beta", # STABIELE CHAT NAAM
                        messages=[{"role":"system","content":f"Dating sim op {platform}. Wees uitdagend. Taal:{lang}."}] + st.session_state.chat_history
                    )
                    rep = r.choices[0].message.content
                    st.markdown(rep)
                    st.session_state.chat_history.append({"role": "assistant", "content": rep})
            
            if st.button(t['sim_end']):
                st.session_state.sim_active = False
                st.session_state.chat_history = []
                st.rerun()
