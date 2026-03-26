import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import urllib.parse

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Rizz Architect Sovereign", page_icon="⚡", layout="wide")

# --- 2. TRANSLATIONS ---
languages = {
    "NL": {
        "warning": "⚠️ Voer je API key in.",
        "tab_scan": "🔍 STRATEGISCHE SCAN",
        "tab_lab": "🥊 TRAINING LAB",
        "intake": "Tactische Intake",
        "context_label": "Context",
        "btn_scan": "⚡ EXECUTE SCAN",
        "success": "Success Rate",
        "flags": "Signal Analysis",
        "green_flags": "Green Flags",
        "red_flags": "Red Flags",
        "intel": "Field Intelligence",
        "choice_header": "ARCHITECT'S PICK",
        "logic_label": "STRATEGY & LOGIC",
        "alt_header": "STRATEGIC DIMENSIONS",
        "idle": "System stand-by...",
    },
    "EN": {
        "warning": "⚠️ Enter your API key.",
        "tab_scan": "🔍 STRATEGIC SCAN",
        "tab_lab": "🥊 TRAINING LAB",
        "intake": "Tactical Intake",
        "context_label": "Context",
        "btn_scan": "⚡ EXECUTE SCAN",
        "success": "Success Rate",
        "flags": "Signal Analysis",
        "green_flags": "Green Flags",
        "red_flags": "Red Flags",
        "intel": "Field Intelligence",
        "choice_header": "ARCHITECT'S PICK",
        "logic_label": "STRATEGY & LOGIC",
        "alt_header": "STRATEGIC DIMENSIONS",
        "idle": "System stand-by...",
    }
}

# --- 3. CSS (FULL SCREENSHOT STYLE) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&family=Inter:wght@300;500;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{ background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; }}
    
    /* Branding */
    .brand-banner {{ display: flex; align-items: center; justify-content: center; padding: 15px 0; border-bottom: 1px solid rgba(252, 211, 77, 0.1); margin-bottom: 20px; }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 800; color: #ffffff !important; letter-spacing: 1px; }}
    .logotype span {{ color: #fcd34d !important; }}

    /* Labels & Headers */
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; opacity: 0.8; }}
    
    /* ARCHITECT'S PICK CARD */
    .pick-card {{ 
        background: linear-gradient(145deg, rgba(252, 211, 77, 0.08) 0%, rgba(1, 4, 9, 1) 100%);
        border: 2px solid #fcd34d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 25px;
        position: relative;
    }}
    .pick-badge {{
        position: absolute;
        top: -12px;
        left: 20px;
        background: #fcd34d;
        color: #010409;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 0.7rem;
        padding: 2px 10px;
        border-radius: 4px;
    }}
    .pick-type {{ font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: #ffffff; font-weight: 700; margin-bottom: 10px; }}
    .logic-box {{ font-size: 0.75rem; color: #fcd34d; margin-top: 10px; border-top: 1px solid rgba(252, 211, 77, 0.2); padding-top: 10px; opacity: 0.9; }}

    /* DIMENSIONS */
    .dim-box {{ margin-bottom: 15px; padding-left: 10px; border-left: 1px solid rgba(255, 255, 255, 0.1); }}
    .dim-type {{ font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #94a3b8; font-weight: 600; margin-bottom: 5px; }}

    /* Flags */
    .flag-box {{ font-size: 0.75rem; padding: 6px 10px; border-radius: 6px; margin-bottom: 5px; font-weight: 500; border: 1px solid rgba(255,255,255,0.05); }}
    .green-f {{ background: rgba(34, 197, 94, 0.1); color: #4ade80; }}
    .red-f {{ background: rgba(239, 68, 68, 0.1); color: #f87171; }}
    
    .stButton>button {{ background: #fcd34d !important; color: #010409 !important; font-weight: 800; width: 100%; border-radius: 8px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR & STATE ---
with st.sidebar:
    lang_choice = st.radio("Language", ["🇳🇱 NL", "🇬🇧 EN"], horizontal=True)
    l_key = "NL" if "🇳🇱" in lang_choice else "EN"
    t = languages[l_key]
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["WhatsApp", "Instagram", "Hinge", "Tinder"])
    t_city = st.text_input("TARGET CITY", placeholder="Amsterdam")

if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner"><div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN ENGINE ---
if not user_api_key:
    st.warning(t["warning"])
else:
    c1, c2 = st.columns([1, 1.4], gap="medium")
    
    with c1:
        st.markdown(f"<div class='label-tag'>{t['intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            ctx = st.text_area(t["context_label"], height=70, placeholder="Wat is de vibe?")
            if st.button(t["btn_scan"]):
                with st.spinner("Analyzing..."):
                    try:
                        client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                        img_obj = Image.open(u_file).convert('RGB')
                        img_obj.thumbnail((800, 800))
                        buf = io.BytesIO(); img_obj.save(buf, format="JPEG", quality=80); b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                        
                        sys_p = f"Role: Mastermind. Language: {l_key}. Return JSON: dynamics, success_rate, green_flags, red_flags, armor, venues, options(3), verdict."
                        res = client.chat.completions.create(
                            model="grok-4.20-0309-non-reasoning",
                            response_format={"type": "json_object"},
                            messages=[{"role": "system", "content": sys_p},
                                      {"role": "user", "content": [{"type":"text","text":f"Context: {ctx}"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}]
                        )
                        st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                        st.rerun()
                    except Exception as e: st.error(str(e))

    with c2:
        if st.session_state.rizz_master:
            data = st.session_state.rizz_master
            
            # Row 1: Signals
            st.markdown(f"<div class='label-tag'>{t['success']}</div>", unsafe_allow_html=True)
            st.progress(data.get('success_rate', 50) / 100)
            
            cf1, cf2 = st.columns(2)
            with cf1:
                st.markdown(f"<div class='label-tag'>{t['green_flags']}</div>", unsafe_allow_html=True)
                for gf in data.get('green_flags', []): st.markdown(f"<div class='flag-box green-f'>✅ {gf}</div>", unsafe_allow_html=True)
            with cf2:
                st.markdown(f"<div class='label-tag'>{t['red_flags']}</div>", unsafe_allow_html=True)
                for rf in data.get('red_flags', []): st.markdown(f"<div class='flag-box red-f'>🚩 {rf}</div>", unsafe_allow_html=True)

            # ARCHITECT'S PICK SECTION
            opts = data.get('options', [])
            v_idx = data.get('verdict', {}).get('idx', 0)
            if opts:
                winner = opts[v_idx]
                st.markdown(f"""
                <div class="pick-card">
                    <div class="pick-badge">{t['choice_header']}</div>
                    <div class="pick-type">{winner.get('type')}</div>
                """, unsafe_allow_html=True)
                st.code(winner.get('zin'), language=None)
                st.markdown(f"""
                    <div class="logic-box">
                        <b>{t['logic_label']}:</b><br>{data.get('verdict', {}).get('logic')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # STRATEGIC DIMENSIONS
                st.markdown(f"<div class='label-tag'>{t['alt_header']}</div>", unsafe_allow_html=True)
                for i, o in enumerate(opts):
                    if i != v_idx:
                        st.markdown(f"<div class='dim-box'><div class='dim-type'>{o.get('type')}</div>", unsafe_allow_html=True)
                        st.code(o.get('zin'), language=None)
                        st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(t["idle"])
