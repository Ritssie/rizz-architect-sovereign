import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import os

# --- UNICODE & SYSTEM FIX ---
os.environ["PYTHONIOENCODING"] = "utf-8"

st.set_page_config(
    page_title="Rizz Architect Sovereign v8.5", 
    page_icon="👑", 
    layout="wide"
)

# --- TRANSLATIONS ---
translations = {
    "NL": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_briefing": "📖 MISSION BRIEFING",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: Leeftijd, vibe, laatste interactie...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "upload_label": "📂 DATA SOURCE",
        "idle_msg": "Systeem in stand-by. Upload een screenshot."
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_briefing": "📖 MISSION BRIEFING",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: Age, vibe, etc...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "upload_label": "📂 DATA SOURCE",
        "idle_msg": "System standby. Upload a screenshot."
    }
}

# --- STYLING ---
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #010409 !important; color: #e2e8f0 !important; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3rem; text-align: center; padding: 20px; color: white; }
    .brand-logo span { color: #fcd34d; }
    .sovereign-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
    .stButton>button { background: #fcd34d !important; color: black !important; font-weight: bold; width: 100%; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((800, 800)) # Iets kleiner voor snellere upload
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(api_key, b64, ctx, dark):
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    mode = "DARK PSYCHOLOGY" if dark else "CHARISMA"
    
    prompt = f"Role: Sovereign Architect. Mode: {mode}. Analyze dating chat. Output JSON: success_rate(int 0-100), green_flags(list), red_flags(list), options(list of {{'type':str, 'zin':str, 'psychology':str}}), winner_idx(int)."

    try:
        # GEBRUIK DE STABIELE 2026 VISION ENGINE
        res = client.chat.completions.create(
            model="grok-2-vision-1212", 
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {ctx}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e:
        st.error(f"⚠️ API ERROR: {str(e)}")
        return None

# --- UI ASSEMBLY ---
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    lang = st.radio("Language", ["NL", "EN"], horizontal=True)
    t = translations[lang]
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    if st.button("SYSTEM REBOOT"):
        st.session_state.clear()
        st.rerun()

st.markdown(f'<div class="brand-logo">{t["header"]}</div>', unsafe_allow_html=True)

if not api_key:
    st.warning("Voer je API Key in de sidebar in.")
else:
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader(t["tag_intake"])
        u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'])
        if u_file:
            st.image(u_file)
            u_ctx = st.text_area("Context", placeholder=t["ctx_ph"])
            if st.button(t["btn_scan"]):
                with st.spinner("Connecting to Grok Sovereign..."):
                    encoded = process_img(u_file)
                    result = get_analysis(api_key, encoded, u_ctx, is_dark)
                    if result:
                        st.session_state.state = result
                        st.rerun()

    with col2:
        if st.session_state.state:
            s = st.session_state.state
            st.subheader(t["tag_signals"])
            st.write(f"Success Rate: {s.get('success_rate')}%")
            st.progress(s.get('success_rate') / 100)
            
            st.subheader(t["tag_pick"])
            w = s['options'][s.get('winner_idx', 0)]
            st.success(f"**{w['type']}**")
            st.info(f"\"{w['zin']}\"")
            st.write(f"Reasoning: {w['psychology']}")
        else:
            st.info(t["idle_msg"])
