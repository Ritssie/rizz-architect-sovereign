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

# --- 2. TRANSLATIONS ---
languages = {
    "NL": {
        "warning": "⚠️ Voer je API key in om te starten.",
        "intake": "Tactische Intake",
        "context_label": "Context",
        "context_ph": "Doel van dit gesprek?",
        "btn_scan": "⚡ EXECUTE SCAN",
        "success": "Success Rate",
        "flags": "Signal Analysis",
        "green_flags": "Green Flags",
        "red_flags": "Red Flags",
        "intel": "Field Intelligence",
        "dynamics": "Social Dynamics",
        "armor": "Armor (Outfit)",
        "choice": "The Executioner's Choice",
        "logic": "Logica",
        "alt": "Strategic Dimensions",
        "venues": "Strategic Venues",
        "idle": "Systeem stand-by. Upload tactical data.",
        "none": "Geen"
    },
    "EN": {
        "warning": "⚠️ Enter your API key to initialize.",
        "intake": "Tactical Intake",
        "context_label": "Context",
        "context_ph": "Goal of this conversation?",
        "btn_scan": "⚡ EXECUTE SCAN",
        "success": "Success Rate",
        "flags": "Signal Analysis",
        "green_flags": "Green Flags",
        "red_flags": "Red Flags",
        "intel": "Field Intelligence",
        "dynamics": "Social Dynamics",
        "armor": "Armor (Outfit)",
        "choice": "The Executioner's Choice",
        "logic": "Logic",
        "alt": "Strategic Dimensions",
        "venues": "Strategic Venues",
        "idle": "System stand-by. Upload tactical data.",
        "none": "None"
    }
}

# --- 3. SIDEBAR & STATE ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center;">{logo_img}</div>', unsafe_allow_html=True)
    lang_choice = st.radio("Language / Taal", ["🇳🇱 NL", "🇬🇧 EN"], horizontal=True)
    l_key = "NL" if "🇳🇱" in lang_choice else "EN"
    t = languages[l_key]
    
    st.markdown("---")
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["WhatsApp", "Instagram", "Hinge", "Tinder"])
    t_city = st.text_input("TARGET CITY", placeholder="Amsterdam")
    if st.button("REBOOT"):
        st.session_state.clear()
        st.rerun()

if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None

# --- 4. CSS (ENHANCED COMPACT) ---
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
    .flag-box {{ font-size: 0.7rem; padding: 5px; border-radius: 5px; margin-bottom: 3px; }}
    .green-f {{ background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }}
    .red-f {{ background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN ---
if not user_api_key:
    st.warning(t["warning"])
else:
    c1, c2 = st.columns([1, 1.4], gap="medium")
    with c1:
        st.markdown(f"<div class='label-tag'>{t['intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            context = st.text_area(t["context_label"], placeholder=t["context_ph"], height=70)
            if st.button(t["btn_scan"]):
                with st.spinner("Analyzing Signals..."):
                    try:
                        client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                        img_obj = Image.open(u_file).convert('RGB')
                        img_obj.thumbnail((1000, 1000))
                        buf = io.BytesIO()
                        img_obj.save(buf, format="JPEG", quality=85)
                        b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                        
                        sys_prompt = f"""Role: Strategic Mastermind. Language: {l_key}. Return ONLY JSON. 
                        Platform: {platform}. City: {t_city}. 
                        Structure: {{
                            'dynamics':'',
                            'success_rate':0,
                            'green_flags':[],
                            'red_flags':[],
                            'armor':'',
                            'venues':[{{'name':'','vibe':''}}],
                            'options':[{{'type':'Playful','zin':''}}, {{'type':'Direct','zin':''}}, {{'type':'Pattern','zin':''}}],
                            'verdict':{{'idx':0,'logic':''}}
                        }}"""
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
        if st.session_state.rizz_master and isinstance(st.session_state.rizz_master, dict):
            data = st.session_state.rizz_master
            
            # Row 1: Success & Multi-Flags
            st.markdown(f"<div class='label-tag'>{t['success']}</div>", unsafe_allow_html=True)
            st.progress(data.get('success_rate', 50) / 100)
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                st.markdown(f"<div class='label-tag'>{t['green_flags']}</div>", unsafe_allow_html=True)
                g_flags = data.get('green_flags', [])
                for gf in g_flags[:3]:
                    st.markdown(f"<div class='flag-box green-f'>✅ {gf}</div>", unsafe_allow_html=True)
                if not g_flags: st.markdown(f"<div class='flag-box green-f'>{t['none']}</div>", unsafe_allow_html=True)
            with col_f2:
                st.markdown(f"<div class='label-tag'>{t['red_flags']}</div>", unsafe_allow_html=True)
                r_flags = data.get('red_flags', [])
                for rf in r_flags[:3]:
                    st.markdown(f"<div class='flag-box red-f'>🚩 {rf}</div>", unsafe_allow_html=True)
                if not r_flags: st.markdown(f"<div class='flag-box red-f'>{t['none']}</div>", unsafe_allow_html=True)

            # Row 2: Intel
            st.markdown(f"<div class='label-tag'>{t['intel']}</div>", unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card" style="font-size:0.8rem;"><b>📍 {t["dynamics"]}:</b> {data.get("dynamics")}<br><b>🛡️ {t["armor"]}:</b> {data.get("armor")}</div>', unsafe_allow_html=True)

            # Row 3: All 3 Options
            options = data.get('options', [])
            if len(options) >= 1:
                v_idx = data.get('verdict', {}).get('idx', 0)
                st.markdown(f"<div class='label-tag'>{t['choice']}</div>", unsafe_allow_html=True)
                
                # Toon de winnaar in de pick-container
                winner = options[v_idx] if v_idx < len(options) else options[0]
                st.markdown("<div class='pick-container'>", unsafe_allow_html=True)
                st.code(winner.get('zin'), language=None)
                st.markdown(f"<p style='color:#fcd34d; font-size:0.7rem; margin-top:4px;'><b>{t['logic']}:</b> {data.get('verdict', {}).get('logic')}</p></div>", unsafe_allow_html=True)

                # Toon de overige 2 opties strak onder elkaar
                st.markdown(f"<div class='label-tag'>{t['alt']}</div>", unsafe_allow_html=True)
                for i, opt in enumerate(options):
                    if i != v_idx:
                        st.markdown(f"<div style='font-size:0.6rem; color:#94a3b8; margin-bottom:-10px;'>{opt.get('type')}</div>", unsafe_allow_html=True)
                        st.code(opt.get('zin'), language=None)
            
            # Row 4: Venues
            if data.get('venues'):
                st.markdown(f"<div class='label-tag'>{t['venues']}</div>", unsafe_allow_html=True)
                vcols = st.columns(len(data['venues']))
                for i, v in enumerate(data['venues']):
                    with vcols[i]:
                        st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:8px; border-radius:8px; font-size:0.7rem;'><b>{v['name']}</b><br>{v['vibe']}</div>", unsafe_allow_html=True)
        else:
            st.info(t["idle"])
