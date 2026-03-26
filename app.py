import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# ==============================================================================
# --- 1. CORE CONFIGURATION ---
# ==============================================================================
st.set_page_config(
    page_title="Rizz Architect Sovereign v15.0", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. MULTI-LANGUAGE DICTIONARY (Merged) ---
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
        "idle_msg": "Systeem stand-by. Upload data source.",
        "intel_main": """
            **CORE PROTOCOLS:**
            * **Frame Control:** Jij bepaalt de realiteit van het gesprek.
            * **Anti-Desperation:** Beheer je schaarste; jouw tijd is kostbaar.
            * **Emotional Anchoring:** Koppel positieve triggers aan jouw interactie.
        """,
        "dark_alert": "⚠️ **DARK OPS:** Je activeert tactieken voor directe gedragsbeïnvloeding. Gebruik met mate."
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_briefing": "📖 MISSION BRIEFING",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIVE DIMENSIONS",
        "tag_signals": "📡 SIGNALS",
        "ctx_ph": "Context: Age, vibe, last interaction...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "idle_msg": "Standby. Upload data source.",
        "intel_main": "Core Laws: Frame Control, Scarcity, Anchoring.",
        "dark_alert": "⚠️ **DARK OPS:** Activating high-risk behavioral manipulation. Use with caution."
    }
}

# ==============================================================================
# --- 3. PRECISION CSS ENGINE (v6.4 Visuals) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; 
        color: #e2e8f0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* Brand Header */
    .brand-container { text-align: center; padding: 30px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3.2rem; color: #ffffff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 25px rgba(252, 211, 77, 0.5); }

    /* Section Styling */
    .section-header {
        font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.7rem;
        letter-spacing: 4px; margin: 25px 0 12px 0; display: flex; align-items: center; text-transform: uppercase;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.2), transparent); margin-left: 15px; }

    /* Sovereign Cards */
    .sovereign-card {
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px; padding: 20px; margin-bottom: 15px; transition: 0.2s ease;
    }
    .sovereign-card:hover { border: 1px solid rgba(252, 211, 77, 0.3); transform: translateY(-2px); }
    
    .winner-card {
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%);
        border: 2px solid #fcd34d; box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    
    /* Gauge Indicator */
    .gauge-container {
        background: rgba(255,255,255,0.03); border-radius: 50%;
        width: 100px; height: 100px; display: flex; align-items: center; justify-content: center;
        border: 4px solid #fcd34d; margin: 0 auto; box-shadow: 0 0 20px rgba(252, 211, 77, 0.2);
    }

    /* Gold Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important;
        color: #010409 !important; font-weight: 800; border-radius: 10px; height: 3rem; border: none !important;
    }

    /* Signal Pills */
    .pill { display: inline-block; padding: 5px 12px; border-radius: 6px; font-size: 0.7rem; font-family: 'JetBrains Mono'; margin: 4px; }
    .pill-green { background: rgba(74, 222, 128, 0.1); color: #4ade80; border: 1px solid #4ade8033; }
    .pill-red { background: rgba(248, 113, 113, 0.1); color: #f87171; border: 1px solid #f8717133; }

    /* Image Scan Effect */
    [data-testid="stImage"] { position: relative; overflow: hidden; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); }
    [data-testid="stImage"]::after {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 2px;
        background: rgba(252, 211, 77, 0.6); box-shadow: 0 0 10px #fcd34d;
        animation: scan 3s linear infinite;
    }
    @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE (Stable Grok-4 Fast) ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_architect_response(client, b64, ctx, lang, dark):
    mode = "PSYCHOLOGICAL DARK OPS (High Manipulation)" if dark else "ELITE SOCIAL CHARISMA"
    prompt = (f"Role: Sovereign Architect. Mode: {mode}. Language: {lang}. "
              "Analyze screenshot for subtext and power dynamics. "
              "Return ONLY a valid JSON object with: success_rate (int), green_flags (list), red_flags (list), "
              "psychology (str), options (list of dicts with type and zin), winner_idx (int).")
    
    model_to_use = "grok-4-1-fast-non-reasoning"
    
    try:
        res = client.chat.completions.create(
            model=model_to_use,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {ctx}"}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}
            ]
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e:
        st.error(f"Systeemfout: {str(e)}")
        return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("### 🎚️ CONTROL PANEL")
    l_key = st.radio("Language", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api_key_input = st.text_input("Grok API Key", type="password")
    api_key = api_key_input.strip() if api_key_input else ""
    st.markdown("---")
    is_dark = st.toggle(t["dark_mode"], key="dark_ops_toggle")
    if st.button(t["reboot"], use_container_width=True):
        st.session_state.clear(); st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 STANDBY: Voer API key in om het systeem te activeren.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Upload", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Context", placeholder=t["ctx_ph"], height=80, label_visibility="collapsed")
            if st.button(t["btn_scan"], use_container_width=True):
                with st.spinner("Decoding social layers..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    result = get_architect_response(client, process_img(u_file), u_ctx, l_key, is_dark)
                    if result:
                        st.session_state.state = result
                        st.rerun()
        
        st.markdown(f"<div class='section-header'>{t['tag_briefing']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sovereign-card'>{t['intel_main']}</div>", unsafe_allow_html=True)
        if is_dark: 
            st.markdown(f"<div class='sovereign-card' style='border-color:#f87171; color:#f87171;'>{t['dark_alert']}</div>", unsafe_allow_html=True)

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # Gauge & Signals Row
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"<div class='section-header'>CONFIDENCE</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='gauge-container'><span style='font-size:1.5rem; font-weight:900;'>{s.get('success_rate')}%</span></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
                for gf in s.get('green_flags', []): st.markdown(f"<span class='pill pill-green'>✅ {gf}</span>", unsafe_allow_html=True)
                for rf in s.get('red_flags', []): st.markdown(f"<span class='pill pill-red'>🚩 {rf}</span>", unsafe_allow_html=True)

            # Winner Move
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            options = s.get('options', [])
            w_idx = s.get('winner_idx', 0)
            if options:
                best = options[w_idx]
                st.markdown(f"""
                    <div class="sovereign-card winner-card">
                        <div style="font-family:'JetBrains Mono'; color:#fcd34d; font-size:0.7rem; letter-spacing:2px; margin-bottom:8px;">OPTIMAL TRAJECTORY | {best.get('type')}</div>
                        <div style="font-size:1.2rem; font-weight:700; margin-bottom:15px; color:white;">"{best.get('zin')}"</div>
                        <div style="border-top:1px solid rgba(252,211,77,0.2); padding-top:12px; font-size:0.85rem; opacity:0.9;">
                            <b>STRATEGIE:</b> {s.get('psychology')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.code(best.get('zin'), language=None)
            
            # Alt Moves
            st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(options):
                if i != w_idx:
                    st.markdown(f"""
                        <div class="sovereign-card">
                            <div style="font-size:0.65rem; font-family:'JetBrains Mono'; opacity:0.5; color:#fcd34d;">{opt.get('type')}</div>
                            <div style="font-size:0.9rem; margin:8px 0;">"{opt.get('zin')}"</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.code(opt.get('zin'), language=None)
        else:
            st.info(t["idle_msg"])

st.markdown("<br><div style='text-align:center; opacity:0.1; font-size:0.6rem;'>PRECISION ENGINE v15.0 | SOVEREIGN SYSTEMS</div>", unsafe_allow_html=True)
