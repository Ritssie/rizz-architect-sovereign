import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
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

# --- 2. CSS (COMPACT & CLEAN) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&family=Inter:wght@300;500;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {{ background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; }}
    div[data-testid="stVerticalBlock"] > div {{ padding-top: 0rem !important; padding-bottom: 0.2rem !important; }}
    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 15px; padding: 15px 0; border-bottom: 2px solid rgba(252, 211, 77, 0.2); margin-bottom: 15px; }}
    .brand-logo {{ width: 50px; height: 50px; border-radius: 10px; border: 1px solid #fcd34d; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 800; color: #ffffff !important; }}
    .logotype span {{ color: #fcd34d !important; }}
    .stButton>button {{ background: #fcd34d !important; color: #010409 !important; font-weight: 800; border-radius: 8px; border: none; }}
    .glass-card {{ background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(252, 211, 77, 0.1); border-radius: 10px; padding: 10px; margin-bottom: 8px; }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px; }}
    .pick-container {{ border-left: 3px solid #fcd34d; padding: 10px 15px; background: rgba(252, 211, 77, 0.04); border-radius: 0 10px 10px 0; margin-bottom: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None

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
    platform = st.selectbox("PLATFORM", ["WhatsApp", "Instagram", "Hinge", "Tinder"])
    t_city = st.text_input("TARGET CITY", placeholder="Amsterdam")
    if st.button("REBOOT"):
        st.session_state.clear()
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN INTERFACE ---
if not user_api_key:
    st.warning("⚠️ Voer je API key in om te starten.")
else:
    c1, c2 = st.columns([1, 1.4], gap="medium")
    
    with c1:
        st.markdown("<div class='label-tag'>Tactical Intake</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            context = st.text_area("Context", placeholder="Doel van dit gesprek?", height=70)
            if st.button("⚡ EXECUTE SCAN"):
                with st.spinner("Decoding..."):
                    try:
                        client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                        b64 = process_img(u_file)
                        sys_prompt = f"Role: Strategic Mastermind. Return ONLY JSON. Platform: {platform}. City: {t_city}. Structure: {{'dynamics':'','success_rate':0,'red_flags':[],'armor':'','venues':[{{'name':'','vibe':''}}],'options':[{{'type':'','zin':''}}],'verdict':{{'idx':0,'logic':''}}}}"
                        
                        res = client.chat.completions.create(
                            model="grok-4.20-0309-non-reasoning",
                            response_format={"type": "json_object"},
                            messages=[{"role": "system", "content": sys_prompt},
                                      {"role": "user", "content": [{"type":"text","text":f"Context: {context}"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}]
                        )
                        # Veilig parsen van JSON
                        st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                        st.rerun()
                    except Exception as e: st.error(f"Error: {e}")

    with c2:
        if st.session_state.rizz_master and isinstance(st.session_state.rizz_master, dict):
            data = st.session_state.rizz_master
            
            # Row 1: Success & Flags
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("<div class='label-tag'>Success Rate</div>", unsafe_allow_html=True)
                st.progress(data.get('success_rate', 50) / 100)
            with col_b:
                st.markdown("<div class='label-tag'>Red Flags</div>", unsafe_allow_html=True)
                for flag in data.get('red_flags', ['Geen']):
                    st.markdown(f"<span style='color:#ff4b4b; font-size:0.7rem;'>🚩 {flag}</span>", unsafe_allow_html=True)

            # Row 2: Dynamics
            st.markdown("<div class='label-tag'>Field Intelligence</div>", unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card" style="font-size:0.8rem;"><b>📍 Social Dynamics:</b> {data.get("dynamics")}<br><b>🛡️ Armor:</b> {data.get("armor")}</div>', unsafe_allow_html=True)

            # Row 3: The Choice
            options = data.get('options', [])
            if options:
                v_idx = data.get('verdict', {}).get('idx', 0)
                st.markdown("<div class='label-tag'>The Executioner's Choice</div>", unsafe_allow_html=True)
                winner = options[v_idx] if v_idx < len(options) else options[0]
                st.markdown("<div class='pick-container'>", unsafe_allow_html=True)
                st.code(winner.get('zin'), language=None)
                st.markdown(f"<p style='color:#fcd34d; font-size:0.7rem; margin-top:4px;'><b>Logic:</b> {data.get('verdict', {}).get('logic')}</p></div>", unsafe_allow_html=True)

                # Row 4: Alternatives
                st.markdown("<div class='label-tag'>Strategic Dimensions</div>", unsafe_allow_html=True)
                for i, opt in enumerate(options):
                    if i != v_idx:
                        st.markdown(f"<div style='font-size:0.6rem; color:#94a3b8; margin-bottom:-10px;'>{opt.get('type')}</div>", unsafe_allow_html=True)
                        st.code(opt.get('zin'), language=None)
        else:
            st.info("System Ready. Upload tactical data.")
