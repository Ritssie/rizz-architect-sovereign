import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import time

# --- 1. CORE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Rizz Architect Sovereign v5.8", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MULTI-LAYER TRANSLATIONS & INTELLIGENCE ---
translations = {
    "NL": {
        "header_1": "TACTISCHE INTAKE",
        "header_2": "ARCHITECT'S PICK",
        "header_3": "STRATEGIC DIMENSIONS",
        "header_4": "SYSTEM ANALYSIS",
        "intel_briefing": "STRATEGISCHE UITLEG",
        "context_ph": "Bijv: 18 jaar, ontmoet op Tinder, reageert koud...",
        "btn_execute": "⚡ EXECUTE STRATEGY",
        "success_label": "SUCCESS PROBABILITY",
        "psych_label": "🧠 PSYCHOLOGIE & LOGICA",
        "idle_msg": "Systeem stand-by. Upload data voor analyse.",
        "dark_mode_label": "Dark Psychology Mode",
        "reboot_btn": "VOLLEDIGE SYSTEEM REBOOT",
        "status_console": "SYSTEM STATUS: OPERATIONAL",
        "intel_main": """
            **De Kern-Analyse:**
            * **Frame Analysis:** Wie bepaalt de richting? De Architect herstelt jouw leiderschap.
            * **Investment Balance:** We analyseren de 'effort ratio' om te voorkomen dat je te veel investeert.
        """,
        "intel_dark": """
            **⚠️ Dark Ops Actief:**
            * **Push-Pull:** Creëer emotionele pieken en dalen.
            * **Scarcity:** Maak jouw aandacht een schaars goed.
            * **Pattern Break:** Stop met het zijn van de 'voorspelbare' man.
        """,
        "intel_standard": """
            **🛡️ Standaard Modus:**
            Focus op charisma, humor en hoog-status gedrag zonder onnodige manipulatie.
        """
    },
    "EN": {
        "header_1": "TACTICAL INTAKE",
        "header_2": "ARCHITECT'S PICK",
        "header_3": "STRATEGIC DIMENSIONS",
        "header_4": "SYSTEM ANALYSIS",
        "intel_briefing": "STRATEGIC BRIEFING",
        "context_ph": "E.g.: 18 y/o, met on Tinder, reply is cold...",
        "btn_execute": "⚡ EXECUTE STRATEGY",
        "success_label": "SUCCESS PROBABILITY",
        "psych_label": "🧠 PSYCHOLOGY & LOGIC",
        "idle_msg": "System stand-by. Waiting for tactical data.",
        "dark_mode_label": "Dark Psychology Mode",
        "reboot_btn": "FULL SYSTEM REBOOT",
        "status_console": "SYSTEM STATUS: ACTIVE",
        "intel_main": "Core analysis focuses on frame control and effort ratios.",
        "intel_dark": "Dark Ops: Focus on scarcity, tension, and emotional spikes.",
        "intel_standard": "Standard: High-value charisma and social leadership."
    }
}

# --- 3. ARCHITECT VISUAL ENGINE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; }
    
    .main-header { text-align: center; padding: 25px 0; border-bottom: 1px solid rgba(252, 211, 77, 0.15); margin-bottom: 30px; }
    .logo-text { font-family: 'Playfair Display', serif; font-size: 2.2rem; color: #ffffff !important; letter-spacing: -0.5px; }
    .logo-text span { color: #fcd34d !important; text-shadow: 0 0 20px rgba(252, 211, 77, 0.4); }

    .label-tag { font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.65rem; letter-spacing: 2.5px; text-transform: uppercase; margin: 25px 0 10px 0; display: flex; align-items: center; }
    .label-tag::after { content: ""; flex: 1; height: 1px; background: rgba(252, 211, 77, 0.2); margin-left: 15px; }
    
    .pick-card { background: linear-gradient(165deg, rgba(252, 211, 77, 0.1) 0%, rgba(1, 4, 9, 1) 100%); border: 2px solid #fcd34d; border-radius: 16px; padding: 30px; position: relative; margin-bottom: 35px; box-shadow: 0 15px 45px rgba(0,0,0,0.6); }
    .pick-badge { position: absolute; top: -14px; left: 25px; background: #fcd34d; color: #010409; font-family: 'JetBrains Mono', monospace; font-weight: 900; font-size: 0.75rem; padding: 3px 12px; border-radius: 4px; }
    
    .console-box { background: #0d1117; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #4ade80; margin-bottom: 20px; }
    .intel-box { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(252, 211, 77, 0.1); border-radius: 12px; padding: 20px; font-size: 0.85rem; line-height: 1.6; }
    
    .dim-box { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 18px; margin-bottom: 15px; }
    .dim-type { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #94a3b8; font-weight: 700; margin-bottom: 8px; }

    .stButton>button { background: #fcd34d !important; color: #010409 !important; font-weight: 800; border-radius: 10px; height: 3.5rem; text-transform: uppercase; border: none !important; width: 100%; transition: 0.4s; }
    .stButton>button:hover { box-shadow: 0 0 25px rgba(252, 211, 77, 0.4); transform: translateY(-2px); }
    
    .stProgress > div > div > div > div { background-color: #fcd34d !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE FUNCTIONS ---
def encode_img_to_b64(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((900, 900))
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode()

def run_rizz_analysis(client, b64_img, context, lang, dark_ops):
    style = "High-status charisma."
    if dark_ops: style = "Dark psychology, tension, scarcity, push-pull."
    
    sys_msg = f"""Role: Sovereign Rizz Architect. Style: {style}. Language: {lang}.
    JSON structure only:
    {{
      "success_rate": 0-100,
      "green_flags": [], "red_flags": [],
      "psychology": "Detailed analysis.",
      "options": [
        {{"type": "🎭 Playful Provocation", "zin": ""}},
        {{"type": "♟️ Strategic Directness", "zin": ""}},
        {{"type": "⚡ The Pattern Breaker", "zin": ""}}
      ],
      "winner_idx": 0
    }}"""
    
    response = client.chat.completions.create(
        model="grok-4.20-0309-non-reasoning",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": [
                {"type": "text", "text": f"Context: {context}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
            ]}
        ]
    )
    return json.loads(response.choices[0].message.content)

# --- 5. INTERFACE ASSEMBLY ---
if 'rizz_state' not in st.session_state: st.session_state.rizz_state = None

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM PARAMETERS")
    lang_choice = st.radio("Systeem Taal", ["NL", "EN"], horizontal=True)
    t = translations[lang_choice]
    
    user_api = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    dark_ops = st.toggle(t["dark_mode_label"], value=False)
    
    if st.button(t["reboot_btn"]):
        st.session_state.clear()
        st.rerun()

# Branding Header
st.markdown(f'<div class="main-header"><div class="logo-text">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# Main Grid Logic
if not user_api:
    st.info("System Lockdown. Please enter your API Key in the sidebar.")
else:
    c_left, c_right = st.columns([1, 1.4], gap="large")
    
    with c_left:
        # Status Console
        st.markdown(f"<div class='console-box'>[SYSTEM] {t['status_console']}<br>[USER] Authorized<br>[MODE] {'DARK OPS' if dark_ops else 'STANDARD'}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='label-tag'>{t['header_1']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Upload Data", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Intelligence Context", placeholder=t["context_ph"], height=80)
            if st.button(t["btn_execute"]):
                with st.spinner("Decoding social layers..."):
                    try:
                        ai = OpenAI(api_key=user_api, base_url="https://api.x.ai/v1")
                        b64 = encode_img_to_b64(u_file)
                        st.session_state.rizz_state = run_rizz_analysis(ai, b64, u_ctx, lang_choice, dark_ops)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # UITLEG SECTIE
        st.markdown(f"<div class='label-tag'>{t['intel_briefing']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"<div class='intel-box'>{t['intel_main']}</div>", unsafe_allow_html=True)
            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            if dark_ops:
                st.markdown(f"<div class='intel-box' style='border-color:#f87171;'>{t['intel_dark']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='intel-box' style='border-color:#4ade80;'>{t['intel_standard']}</div>", unsafe_allow_html=True)

    with c_right:
        if st.session_state.rizz_state:
            data = st.session_state.rizz_state
            
            # success
            st.markdown(f"<div class='label-tag'>{t['success_label']}</div>", unsafe_allow_html=True)
            st.progress(data.get('success_rate', 50) / 100)
            
            # Flags Row
            f1, f2 = st.columns(2)
            with f1:
                for gf in data.get('green_flags', []): st.markdown(f"<div style='color:#4ade80; font-size:0.8rem;'>✅ {gf}</div>", unsafe_allow_html=True)
            with f2:
                for rf in data.get('red_flags', []): st.markdown(f"<div style='color:#f87171; font-size:0.8rem;'>🚩 {rf}</div>", unsafe_allow_html=True)

            # Architect's Pick
            st.markdown(f"<div class='label-tag'>{t['header_2']}</div>", unsafe_allow_html=True)
            w_idx = data.get('winner_idx', 0)
            winner = data['options'][w_idx]
            
            st.markdown(f"""
                <div class="pick-card">
                    <div class="pick-badge">OPTIMIZED PATH</div>
                    <div class="dim-type" style="color:#fcd34d;">{winner.get('type')}</div>
            """, unsafe_allow_html=True)
            st.code(winner.get('zin'), language=None)
            st.markdown(f"""
                    <div style="background:rgba(252,211,77,0.05); padding:15px; border-radius:8px; margin-top:15px; border-left:2px solid #fcd34d; font-size:0.85rem; color:#fcd34d;">
                        <b>{t['psych_label']}:</b><br>{data.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Other Dimensions
            st.markdown(f"<div class='label-tag'>{t['header_3']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(data['options']):
                if i != w_idx:
                    st.markdown(f"""<div class="dim-box"><div class="dim-type">{opt.get('type')}</div>""", unsafe_allow_html=True)
                    st.code(opt.get('zin'), language=None)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# --- 6. FOOTER ---
st.markdown("<br><div style='text-align:center; opacity:0.2; font-size:0.7rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top:20px;'>CORE VERSION 5.8.1 | STABILITY & LOGIC ACTIVE</div>", unsafe_allow_html=True)
