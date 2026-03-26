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
    page_title="Rizz Architect Sovereign v7.5", 
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
        "upload_label": "📂 DATA SOURCE (Klik voor upload)",
        "idle_msg": "Systeem in stand-by. Gebruik de Data Source module om te beginnen.",
        "intel_main": """
            <div style='font-size:0.85rem; line-height:1.6; opacity:0.9;'>
                <span style='color:#fcd34d;'>•</span> <b>Frame Control:</b> Jij bepaalt de werkelijkheid.<br>
                <span style='color:#fcd34d;'>•</span> <b>Anti-Desperation:</b> Reageer nooit vanuit tekort.<br>
                <span style='color:#fcd34d;'>•</span> <b>Emotional Anchoring:</b> Word de bron van hun dopamine.
            </div>
        """,
        "dark_alert_html": """
            <div style='background: rgba(248, 113, 113, 0.1); border: 1px solid #f87171; 
                 border-radius: 12px; padding: 15px; color: #f87171; font-size: 0.85rem; 
                 box-shadow: 0 0 15px rgba(248, 113, 113, 0.1);'>
                <b style='font-family:JetBrains Mono;'>⚠️ DARK OPS GEACTIVEERD</b><br>
                Tactieken voor gedragsbeïnvloeding en emotionele manipulatie zijn actief. Gebruik deze data met volledige verantwoordelijkheid.
            </div>
        """
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
        "upload_label": "📂 DATA SOURCE (Click to upload)",
        "idle_msg": "System standby. Use the Data Source module to begin.",
        "intel_main": "Core Laws: Frame Control, Scarcity, Anchoring.",
        "dark_alert_html": "<div style='color:#f87171;'>⚠️ DARK OPS ACTIVE</div>"
    }
}

# ==============================================================================
# --- 3. PREMIUM CSS ENGINE (V7.5 Clean UI) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    .brand-container { text-align: center; padding: 45px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3.5rem; color: #ffffff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 25px rgba(252, 211, 77, 0.5); }

    @media (max-width: 768px) {
        .brand-logo { font-size: 2.3rem !important; letter-spacing: -1px !important; }
        .brand-container { padding: 25px 0 !important; }
    }

    /* File Uploader Custom Styling */
    [data-testid="stFileUploader"] { 
        background-color: rgba(255, 255, 255, 0.01); border: 1px dashed rgba(252, 211, 77, 0.15); 
        border-radius: 12px; padding: 5px; 
    }
    [data-testid="stFileUploader"] section { padding: 0 !important; }
    [data-testid="stFileUploader"] label { display: none; }

    .section-header {
        font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.75rem;
        letter-spacing: 4px; margin: 30px 0 15px 0; display: flex; align-items: center;
        text-transform: uppercase; opacity: 0.7;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.3), transparent); margin-left: 15px; }

    .sovereign-card { 
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 16px; padding: 22px; margin-bottom: 18px; 
    }
    .winner-card { 
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); 
        border: 2px solid #fcd34d; 
    }

    .gauge-container { 
        background: rgba(255,255,255,0.02); border-radius: 50%; width: 115px; height: 115px; 
        display: flex; align-items: center; justify-content: center; 
        border: 4px solid #fcd34d; margin: 25px auto;
    }
    
    .pill { display: block; padding: 12px; border-radius: 10px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; margin-bottom: 10px; font-weight: 600; }
    .pill-green { background: rgba(74, 222, 128, 0.08); color: #4ade80; border: 1px solid #4ade8022; }
    .pill-red { background: rgba(248, 113, 113, 0.08); color: #f87171; border: 1px solid #f8717122; }

    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 800; border-radius: 12px; height: 3.8rem; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, lang, dark):
    mode = "PSYCHOLOGICAL DARK OPS" if dark else "ELITE SOCIAL CHARISMA"
    prompt = f"Sovereign Architect Engine. Mode: {mode}. Lang: {lang}. Output strictly JSON: success_rate, green_flags(max3), red_flags(max3), options[type,zin,psychology], winner_idx."
    
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"},
                                                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
        )
        return json.loads(res.choices[0].message.content)
    except Exception: return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("### 🎚️ COMMAND")
    l_key = st.radio("Language", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    if st.button(t["reboot"]):
        st.session_state.clear(); st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 STANDBY: API key vereist.")
else:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        
        # Verbeterde Uploader: Klapt in als er een file is
        with st.expander(t["upload_label"], expanded=(st.session_state.state is None)):
            u_file = st.file_uploader("Upload", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Context Intel", placeholder=t["ctx_ph"], height=80, label_visibility="collapsed")
            if st.button(t["btn_scan"]):
                with st.spinner("Decoding..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, l_key, is_dark)
                    st.rerun()
        
        st.markdown(f"<div class='section-header'>{t['tag_briefing']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sovereign-card'>{t['intel_main']}</div>", unsafe_allow_html=True)
        
        # Clean Dark Ops Warning
        if is_dark:
            st.markdown(t["dark_alert_html"], unsafe_allow_html=True)

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                for gf in s.get('green_flags', [])[:3]: 
                    st.markdown(f"<div class='pill pill-green'>✅ {gf}</div>", unsafe_allow_html=True)
            with f_col2:
                for rf in s.get('red_flags', [])[:3]: 
                    st.markdown(f"<div class='pill pill-red'>🚩 {rf}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='gauge-container'><span style='font-size:1.6rem; font-weight:900;'>{s.get('success_rate')}%</span></div>", unsafe_allow_html=True)

            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            w = s['options'][s.get('winner_idx', 0)]
            st.markdown(f"""
                <div class="sovereign-card winner-card">
                    <div style="font-family:'JetBrains Mono'; color:#fcd34d; font-size:0.7rem; margin-bottom:10px;">{w.get('type')}</div>
                    <div style="font-size:1.2rem; font-weight:700; color:white; margin-bottom:15px; line-height:1.4;">"{w.get('zin')}"</div>
                    <div style="border-top:1px solid rgba(252,211,77,0.2); padding-top:12px; font-size:0.85rem; opacity:0.9;">
                        <b style="color:#fcd34d;">PSYCHOLOGY:</b> {w.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s['options']):
                if i != s.get('winner_idx', 0):
                    st.markdown(f"""
                        <div class="sovereign-card">
                            <div style="font-size:0.65rem; font-family:'JetBrains Mono'; color:#fcd34d;">{opt.get('type')}</div>
                            <div style="font-size:0.95rem; font-weight:600; margin:8px 0;">"{opt.get('zin')}"</div>
                            <div style="font-size:0.8rem; opacity:0.7; border-top:1px solid rgba(255,255,255,0.06); padding-top:8px;">
                                <b>Insight:</b> {opt.get('psychology')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# Padding & Stabiliteit
# ..............................................................................
# ..............................................................................
st.write("")
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem;'>RIZZ ARCHITECT V7.5 | SOVEREIGN SYSTEMS</div>", unsafe_allow_html=True)
