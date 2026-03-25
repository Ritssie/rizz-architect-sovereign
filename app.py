import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import urllib.parse

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Rizz Architect: Code 1.1", page_icon="⚔️", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚔️</div>'

# --- 2. ENHANCED CSS (Soft Edges & Sovereign Styling) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&family=Playfair+Display:wght@700&display=swap');
    
    .stApp {{ background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: #0d1117 !important; border-right: 1px solid rgba(252, 211, 77, 0.1); }}
    
    /* Soft Edges for Tabs */
    .stTabs [data-baseweb="tab"] {{
        background-color: #0d1117; border: 1px solid rgba(252, 211, 77, 0.1);
        color: #e2e8f0 !important; border-radius: 12px 12px 0 0; padding: 10px 20px;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: #fcd34d !important; color: #010409 !important; font-weight: 700; border-radius: 12px 12px 0 0;
    }}

    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 15px; padding: 10px 0; border-bottom: 1px solid rgba(252, 211, 77, 0.15); margin-bottom: 15px; }}
    .brand-logo {{ width: 55px; height: 55px; border-radius: 12px; border: 2px solid #fcd34d; box-shadow: 0 0 15px rgba(252, 211, 77, 0.1); object-fit: cover; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: #e2e8f0 !important; margin: 0; }}
    .logotype span {{ color: #fcd34d !important; }}

    .glass-card {{ background: rgba(30, 41, 59, 0.3) !important; border: 1px solid rgba(252, 211, 77, 0.1) !important; border-radius: 18px; padding: 18px; margin-bottom: 15px; }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d !important; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px; }}
    
    /* Soft Edges for Inputs & Selectboxes */
    input, textarea, [data-baseweb="select"], .stNumberInput input, .stTextInput input {{ 
        background-color: #0d1117 !important; 
        color: white !important; 
        border: 1px solid rgba(252, 211, 77, 0.2) !important; 
        border-radius: 12px !important; /* Soft Edges */
        padding: 10px !important;
    }}
    
    .stButton>button {{ width: 100%; background: #fcd34d !important; color: #010409 !important; font-weight: 800; border-radius: 12px; padding: 10px; border: none !important; text-transform: uppercase; }}
    .pick-container {{ background: linear-gradient(135deg, rgba(252, 211, 77, 0.1), #010409) !important; border: 2px solid #fcd34d !important; border-radius: 20px; padding: 25px; margin-top: 20px; }}
    h1, h2, h3, p, label, .stMarkdown {{ color: #e2e8f0 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LANGUAGE & SESSION STATE ---
lang_choice = st.sidebar.radio("🌐 System Language", ["🇳🇱", "🇬🇧"], horizontal=True)
lang = "NL" if lang_choice == "🇳🇱" else "EN"

texts = {
    "NL": {
        "access": "SOVEREIGN ACCESS", "key": "OPENAI API KEY", "field_intel": "Field Intelligence",
        "m_city": "JOUW STAD", "t_city": "HAAR STAD", "reset": "REBOOT SYSTEM",
        "tab_analyze": "🔍 Analyze", "tab_spar": "🥊 Sparring",
        "intake": "Tactical Intake", "context": "Context (Vibe)", "scan": "⚡ EXECUTE SCAN",
        "wait": "Analyzing patterns...", "armor": "📍 Intelligence & Armor", "weather": "Local Weather",
        "outfit": "Armor (Outfit)", "pick": "🏆 THE ARCHITECT'S PICK", "strategy": "STRATEGY",
        "warning": "⚠️ Activate system via sidebar.", "info": "Waiting for tactical data...",
        "sim_start": "START SIMULATION", "sim_end": "TERMINATE",
        "archetype": "Persona Select", "chat_placeholder": "Input message...",
        "coach": "👨‍🏫 DEBRIEF BY ARCHITECT", "coach_wait": "Reviewing performance...",
        "bot_cold": "Ice Cold", "bot_spicy": "Spicy", "bot_professional": "Professional"
    },
    "EN": {
        "access": "SOVEREIGN ACCESS", "key": "OPENAI API KEY", "field_intel": "Field Intelligence",
        "m_city": "YOUR CITY", "t_city": "HER CITY", "reset": "REBOOT SYSTEM",
        "tab_analyze": "🔍 Analyze", "tab_spar": "🥊 Sparring",
        "intake": "Tactical Intake", "context": "Context (Vibe)", "scan": "⚡ EXECUTE SCAN",
        "wait": "Analyzing patterns...", "armor": "📍 Intelligence & Armor", "weather": "Local Weather",
        "outfit": "Armor (Outfit)", "pick": "🏆 THE ARCHITECT'S PICK", "strategy": "STRATEGY",
        "warning": "⚠️ Activate system via sidebar.", "info": "Waiting for tactical data...",
        "sim_start": "START SIMULATION", "sim_end": "TERMINATE",
        "archetype": "Persona Select", "chat_placeholder": "Input message...",
        "coach": "👨‍🏫 DEBRIEF BY ARCHITECT", "coach_wait": "Reviewing performance...",
        "bot_cold": "Ice Cold", "bot_spicy": "Spicy", "bot_professional": "Professional"
    }
}
t = texts[lang]

if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'sim_active' not in st.session_state: st.session_state.sim_active = False

# --- 4. CORE LOGIC ---
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center; margin-bottom:15px;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#fcd34d; text-align:center;'>{t['access']}</h3>", unsafe_allow_html=True)
    user_api_key = st.text_input(t['key'], type="password")
    st.markdown("---")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    st.markdown(f"<div class='label-tag'>{t['field_intel']}</div>", unsafe_allow_html=True)
    u_city = st.text_input(t['m_city'], placeholder="e.g. Amsterdam")
    t_city = st.text_input(t['t_city'], placeholder="e.g. Utrecht")
    if st.button(t['reset']):
        st.session_state.rizz_master = None
        st.session_state.chat_history = []
        st.session_state.sim_active = False
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
                context = st.text_area(t['context'], placeholder="...")
                if st.button(t['scan']):
                    with st.spinner(t['wait']):
                        try:
                            client = OpenAI(api_key=user_api_key)
                            b64 = process_img(u_file)
                            sys_msg = f"Jij bent '⚡ Rizz Architect'. Taal: {lang}. Platform: {platform}. Locaties: {u_city}/{t_city}. Protocol: Triple-A, Weather, Venues, Outfit, 3 Tactical Lines. Focus op statusbehoud. JSON output."
                            res = client.chat.completions.create(
                                model="gpt-4o-mini", response_format={"type": "json_object"},
                                messages=[{"role": "system", "content": sys_msg},
                                          {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
                            )
                            st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                            st.rerun()
                        except Exception as e: st.error(f"Error: {e}")

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
                best = data.get('options', [{}])[idx]
                st.markdown(f"""<div class="pick-container"><div class='label-tag'>{t['pick']}</div><h2 style="margin:0; color:#fff; font-size:1.8rem;">"{best.get('zin')}"</h2><p style="font-size:0.85rem; color:#fcd34d; margin-top:15px;"><b>{t['strategy']}:</b> {p.get('reason')}</p></div>""", unsafe_allow_html=True)
            else:
                st.info(t['info'])

    with tab2:
        st.markdown(f"<div class='label-tag'>{t['tab_spar']}</div>", unsafe_allow_html=True)
        if not st.session_state.sim_active:
            arc = st.selectbox(t['archetype'], [t['bot_spicy'], t['bot_cold'], t['bot_professional']])
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
                    client = OpenAI(api_key=user_api_key)
                    r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":f"Dating sim. Lang:{lang}."}]+st.session_state.chat_history)
                    rep = r.choices[0].message.content
                    st.markdown(rep)
                st.session_state.chat_history.append({"role": "assistant", "content": rep})
            if st.button(t['coach']):
                with st.spinner(t['coach_wait']):
                    client = OpenAI(api_key=user_api_key)
                    c_res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":f"Feedback on social status in {lang}."}]+st.session_state.chat_history)
                    st.markdown(f"<div class='glass-card' style='border: 2px solid #fcd34d;'><div class='label-tag'>👨‍🏫 Architect Debrief</div>{c_res.choices[0].message.content}</div>", unsafe_allow_html=True)
            if st.button(t['sim_end']):
                st.session_state.sim_active = False
                st.session_state.chat_history = []
                st.rerun()
