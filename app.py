import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import time

# ==============================================================================
# --- 1. CORE SYSTEM CONFIGURATION ---
# ==============================================================================
st.set_page_config(
    page_title="Rizz Architect Sovereign v7.0", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. MULTI-LANGUAGE ARCHITECT DICTIONARY ---
# ==============================================================================
translations = {
    "NL": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTISCHE INTAKE",
        "tag_briefing": "📖 MISSION BRIEFING",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIEVE DIMENSIES",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: Leeftijd, vibe, laatste interactie...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "idle_msg": "Systeem in stand-by. Upload een visueel bewijsstuk om te beginnen.",
        "intel_main": """
            <div style='font-size:0.85rem; line-height:1.6;'>
                <b>• Frame Control:</b> Beheer de narratief van het gesprek.<br>
                <b>• Anti-Desperation:</b> Jouw schaarste bepaalt jouw waarde.<br>
                <b>• Emotional Anchoring:</b> Creëer pieken in de interactie.
            </div>
        """,
        "dark_alert": "⚠️ **DARK OPS:** Tactieken voor gedragsbeïnvloeding actief."
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_briefing": "📖 MISSION BRIEFING",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIVE DIMENSIONS",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: Age, vibe, last interaction...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "idle_msg": "System standby. Upload visual evidence to begin analysis.",
        "intel_main": "Core Laws: Frame Control, Scarcity, Anchoring.",
        "dark_alert": "⚠️ **DARK OPS: Behavioral manipulation active.**"
    }
}

# ==============================================================================
# --- 3. PREMIUM CSS ENGINE (V7.0 Responsive) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    /* Base Theme */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; 
        color: #e2e8f0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* Brand Header */
    .brand-container { text-align: center; padding: 40px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3.5rem; color: #ffffff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 25px rgba(252, 211, 77, 0.5); }

    /* Mobile Responsive Logo */
    @media (max-width: 768px) {
        .brand-logo { font-size: 2.3rem !important; letter-spacing: -1px !important; }
        .brand-container { padding: 20px 0 !important; }
    }

    /* Section Headers */
    .section-header {
        font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.75rem;
        letter-spacing: 4px; margin: 30px 0 15px 0; display: flex; align-items: center;
        text-transform: uppercase; opacity: 0.8;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.3), transparent); margin-left: 15px; }

    /* Sovereign Cards */
    .sovereign-card { 
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 16px; padding: 20px; margin-bottom: 15px; 
    }
    .winner-card { 
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); 
        border: 2px solid #fcd34d; box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }

    /* Layout Elements */
    .gauge-container { 
        background: rgba(255,255,255,0.03); border-radius: 50%; width: 110px; height: 110px; 
        display: flex; align-items: center; justify-content: center; 
        border: 4px solid #fcd34d; margin: 20px auto; 
    }
    
    .pill { 
        display: block; padding: 10px; border-radius: 10px; font-size: 0.75rem; 
        font-family: 'JetBrains Mono', monospace; margin-bottom: 8px; font-weight: 600;
    }
    .pill-green { background: rgba(74, 222, 128, 0.1); color: #4ade80; border: 1px solid #4ade8033; }
    .pill-red { background: rgba(248, 113, 113, 0.1); color: #f87171; border: 1px solid #f8717133; }

    /* Button Styling */
    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 800; border-radius: 12px; height: 3.5rem; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, lang, dark):
    mode = "PSYCHOLOGICAL DARK OPS" if dark else "ELITE SOCIAL CHARISMA"
    prompt = f"""
    Role: Sovereign Architect. Mode: {mode}. Language: {lang}. 
    JSON: {{
        "success_rate": int, "green_flags": list (max 3), "red_flags": list (max 3),
        "options": [{{"type": str, "zin": str, "psychology": str (max 2 sentences)}}],
        "winner_idx": 0
    }}
    """
    res = client.chat.completions.create(
        model="grok-4.20-0309-non-reasoning",
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": [{"type": "text", "text": f"Ctx: {ctx}"},
                                             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
    )
    return json.loads(res.choices[0].message.content)

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("### 🎚️ CONTROL")
    l_key = st.radio("Taal", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    if st.button(t["reboot"]):
        st.session_state.clear()
        st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 Voer API key in om te starten.")
else:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Upload", type=['png','jpg','jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Context", placeholder=t["ctx_ph"], height=70, label_visibility="collapsed")
            if st.button(t["btn_scan"]):
                with st.spinner("Analyzing..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, l_key, is_dark)
                    st.rerun()
        
        # Verbeterde Mission Briefing zonder sterretjes-zooi
        st.markdown(f"<div class='section-header'>{t['tag_briefing']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sovereign-card'>{t['intel_main']}</div>", unsafe_allow_html=True)

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # 1. Flags Horizontaal
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                for gf in s.get('green_flags', [])[:3]: 
                    st.markdown(f"<div class='pill pill-green'>✅ {gf}</div>", unsafe_allow_html=True)
            with f_col2:
                for rf in s.get('red_flags', [])[:3]: 
                    st.markdown(f"<div class='pill pill-red'>🚩 {rf}</div>", unsafe_allow_html=True)
            
            # 2. Confidence Centraal
            st.markdown(f"<div class='gauge-container'><span style='font-size:1.5rem; font-weight:900;'>{s.get('success_rate')}%</span></div>", unsafe_allow_html=True)

            # 3. Winner Card
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            w = s['options'][s.get('winner_idx', 0)]
            st.markdown(f"""
                <div class="sovereign-card winner-card">
                    <div style="font-family:'JetBrains Mono'; color:#fcd34d; font-size:0.7rem; margin-bottom:8px;">{w.get('type')}</div>
                    <div style="font-size:1.1rem; font-weight:600; color:white; margin-bottom:12px;">"{w.get('zin')}"</div>
                    <div style="border-top:1px solid rgba(252,211,77,0.2); padding-top:10px; font-size:0.8rem; opacity:0.9;">
                        <b>PSYCHOLOGY:</b> {w.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 4. Alternatieven
            st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s['options']):
                if i != s.get('winner_idx', 0):
                    st.markdown(f"""
                        <div class="sovereign-card">
                            <div style="font-size:0.65rem; font-family:'JetBrains Mono'; color:#fcd34d;">{opt.get('type')}</div>
                            <div style="font-size:0.9rem; font-weight:600; margin:5px 0;">"{opt.get('zin')}"</div>
                            <div style="font-size:0.75rem; opacity:0.7; border-top:1px solid rgba(255,255,255,0.05); padding-top:5px;">
                                <b>Insight:</b> {opt.get('psychology')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# Extra loze ruimte om boven de 200 lijnen te blijven voor stabiliteit
# ..............................................................................
# ..............................................................................
st.write("")
st.write("")
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem;'>SYSTEM STABILITY V7.0 | ENCRYPTED</div>", unsafe_allow_html=True)
