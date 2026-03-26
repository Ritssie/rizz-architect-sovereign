import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# ==============================================================================
# --- 1. CORE SYSTEM CONFIGURATION ---
# ==============================================================================
st.set_page_config(
    page_title="RIZZ ARCHITECT SOVEREIGN v12.5", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. MULTI-LANGUAGE DICTIONARY ---
# ==============================================================================
translations = {
    "NL": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 DATA INGESTION",
        "tag_pick": "🏆 ALPHA SELECTION",
        "tag_dims": "📐 STRATAGEM ARSENAL",
        "tag_signals": "📡 TACTICAL SIGNALS",
        "ctx_ph": "Vibe, relatie, laatste bericht, doel...",
        "btn_scan": "⚡ EXECUTE ARCHITECT SCAN",
        "reboot": "🔄 SYSTEM REBOOT",
        "upload_label": "📂 UPLOAD SCREENSHOT",
        "copy_btn": "KOPIEER",
        "copied": "Gekopieerd naar klembord!",
        "strategy_label": "PSYCHOLOGIE",
        "vibe_label": "DOELWIT VIBE",
        "sentiment_label": "SENTIMENT",
        "ghost_label": "GHOSTING RISICO",
        "idle_msg": "Systeem stand-by. Upload screenshot om te initialiseren."
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_pick": "🏆 ALPHA SELECTION",
        "tag_dims": "📐 STRATAGEM ARSENAL",
        "tag_signals": "📡 TACTICAL SIGNALS",
        "ctx_ph": "Vibe, relationship, last message, goal...",
        "btn_scan": "⚡ EXECUTE SCAN",
        "reboot": "🔄 SYSTEM REBOOT",
        "upload_label": "📂 UPLOAD SCREENSHOT",
        "copy_btn": "COPY",
        "copied": "Copied to clipboard!",
        "strategy_label": "PSYCHOLOGY",
        "vibe_label": "TARGET VIBE",
        "sentiment_label": "SENTIMENT",
        "ghost_label": "GHOSTING RISK",
        "idle_msg": "System standby. Upload screenshot to initialize."
    }
}

# ==============================================================================
# --- 3. PREMIUM CSS (Optimized for Mobile & Depth) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #05070a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    .status-box { padding: 12px; border-radius: 10px; font-family: 'Orbitron', sans-serif; font-size: 0.65rem; text-align: center; margin-bottom: 20px; letter-spacing: 1px; font-weight: 700; }
    .status-online { background: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e; color: #4ade80; box-shadow: 0 0 15px rgba(34, 197, 94, 0.3); }
    .status-offline { background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #f87171; box-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }

    .brand-container { text-align: center; padding: 30px 0; border-bottom: 1px solid rgba(252, 211, 77, 0.1); margin-bottom: 25px; }
    .brand-logo { font-family: 'Orbitron', sans-serif; font-size: clamp(1.8rem, 8vw, 3rem); color: #fff !important; font-weight: 800; letter-spacing: 3px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 20px rgba(252, 211, 77, 0.5); }

    .section-header {
        font-family: 'Orbitron', sans-serif; color: #fcd34d; font-size: 0.7rem;
        letter-spacing: 3px; margin: 30px 0 15px 0; display: flex; align-items: center;
        text-transform: uppercase; opacity: 0.8;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.3), transparent); margin-left: 15px; }

    .winner-card { 
        background: linear-gradient(145deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 0.9) 100%);
        border: 1px solid rgba(252, 211, 77, 0.5); border-radius: 20px; padding: 25px; position: relative;
    }
    
    .stButton>button { 
        width: 100% !important; background: linear-gradient(135deg, #fcd34d 0%, #d97706 100%) !important; 
        color: #000 !important; font-weight: 800 !important; border-radius: 10px !important; 
        border: none !important; font-family: 'Orbitron', sans-serif; padding: 12px !important;
    }
    
    .signal-pill { padding: 10px; border-radius: 10px; margin-bottom: 8px; font-size: 0.75rem; font-weight: 600; border: 1px solid transparent; display: flex; align-items: center; gap: 8px; }
    .pill-green { background: rgba(34, 197, 94, 0.1); border-color: rgba(34, 197, 94, 0.3); color: #4ade80; }
    .pill-red { background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3); color: #f87171; }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .brand-logo { font-size: 2rem; }
        .winner-card { padding: 15px; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE ---
# ==============================================================================
def check_api_connection(api_key):
    if not api_key: return False
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    try:
        client.models.list()
        return True
    except: return False

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, lang, vibe_choice):
    lang_name = "Dutch" if lang == "NL" else "English"
    prompt = f"""Role: Sovereign Architect. Respond ONLY in {lang_name}. 
    User Persona Strategy: {vibe_choice}.
    STRICT JSON structure: 
    {{
        "success_rate": int,
        "sentiment": "string",
        "ghosting_risk": "string",
        "breakdown": {{
            "vibe": {{"val": int, "desc": "short analysis"}},
            "timing": {{"val": int, "desc": "short analysis"}},
            "subtext": {{"val": int, "desc": "short analysis"}}
        }},
        "green_flags": [str], "red_flags": [str], 
        "options": [ {{"type": "str", "zin": "str", "psychology": "str"}} ], 
        "winner_idx": 0
    }}"""
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}
            ]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("<h2 style='font-family:Orbitron; color:#fcd34d; font-size:1rem;'>CORE SYSTEMS</h2>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌍 Language", options=["NL", "EN"], index=0)
    t = translations[lang_choice]
    api_key = st.text_input("Grok API Key", type="password")
    
    if api_key:
        if check_api_connection(api_key):
            st.markdown('<div class="status-box status-online">● SYSTEM ONLINE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box status-offline">○ INVALID KEY</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p style='font-family:Orbitron; font-size:0.7rem; color:#fcd34d;'>{t['vibe_label']}</p>", unsafe_allow_html=True)
    vibe_style = st.select_slider(
        "Vibe", options=["Sweet", "Funny", "Mysterious", "Alpha"], value="Alpha", label_visibility="collapsed"
    )

    if st.button(t["reboot"]):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    with st.expander("🛡️ PRIVACY PROTOCOL"):
        st.caption("Screenshots worden in-memory verwerkt en NIET opgeslagen. Geen training op data.")

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 INITIALIZE SYSTEM: Voer je API-key in.")
else:
    col_l, col_r = st.columns([1, 1.2])

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Intelligence Context", placeholder=t["ctx_ph"], height=80)
            if st.button(t["btn_scan"]):
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, lang_choice, vibe_style)
                st.rerun()

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # TACTICAL SIGNALS (Sentiment & Ghosting)
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            m1.metric(t["sentiment_label"], s.get('sentiment', 'Normal'))
            m2.metric(t["ghost_label"], s.get('ghosting_risk', 'Low'))

            sc1, sc2 = st.columns(2)
            with sc1:
                for gf in s.get('green_flags', []): st.markdown(f'<div class="signal-pill pill-green">✔ {gf}</div>', unsafe_allow_html=True)
            with sc2:
                for rf in s.get('red_flags', []): st.markdown(f'<div class="signal-pill pill-red">✘ {rf}</div>', unsafe_allow_html=True)

            # ALPHA SELECTION
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            opts = s.get('options', [])
            w_idx = s.get('winner_idx', 0)
            
            if opts and len(opts) > w_idx:
                w, b = opts[w_idx], s.get('breakdown', {})
                st.markdown(f"""
                    <div class="winner-card">
                        <div style="text-align:right;"><span style="color:#fcd34d; font-size:0.6rem; border:1px solid #fcd34d; padding:3px 10px; border-radius:15px;">{s.get('success_rate', 85)}% HIT RATE</span></div>
                        <div style="font-size:1.5rem; font-weight:800; color:white; margin:15px 0;">"{w.get('zin')}"</div>
                        <div style="border-left: 3px solid #fcd34d; padding-left: 15px;">
                            <span style="font-family:'Orbitron'; font-size:0.6rem; color:#fcd34d;">{t['strategy_label']}</span><br>
                            <span style="font-size:0.8rem; opacity:0.8;">{w.get('psychology')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"✨ {t['copy_btn']} ALPHA LINE"): st.toast(t["copied"])

            # ALTERNATIVE ARSENAL
            st.markdown(f"<div class='section-header' style='margin-top:40px;'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(opts):
                if i != w_idx:
                    st.markdown(f"""<div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:15px; padding:15px; margin-bottom:10px;">
                        <div style="font-family:'Orbitron'; font-size:0.55rem; color:#fcd34d;">{opt.get('type','ALT')}</div>
                        <div style="font-weight:600;">"{opt.get('zin')}"</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px; letter-spacing:5px;'>SOVEREIGN ENGINE V12.5 // GROK-4.20 STABLE</div>", unsafe_allow_html=True)
