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
    page_title="Rizz Architect Sovereign v10.8", 
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
        "tag_intake": "📥 TACTISCHE INTAKE",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIEVE DIMENSIES",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: vibe, laatste bericht, doel...",
        "btn_scan": "⚡ START ANALYSE",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 RESET SYSTEEM",
        "upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "📋",
        "idle_msg": "Systeem stand-by. Upload screenshot.",
        "lang_label": "🌍 Taal / Language",
        "strategy_label": "STRATEGIE",
        "legal_title": "⚖️ JURIDISCHE DISCLAIMER"
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIVE DIMENSIONS",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: vibe, last message, goal...",
        "btn_scan": "⚡ EXECUTE SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 RESET SYSTEM",
        "upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "📋",
        "idle_msg": "System on standby. Upload screenshot.",
        "lang_label": "🌍 Language / Taal",
        "strategy_label": "STRATEGY",
        "legal_title": "⚖️ LEGAL DISCLOSURE"
    }
}

# ==============================================================================
# --- 3. PREMIUM CSS ENGINE ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    .brand-container { text-align: center; padding: 25px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3rem; color: #ffffff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 20px rgba(252, 211, 77, 0.4); }

    .section-header {
        font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.7rem;
        letter-spacing: 3px; margin: 30px 0 15px 0; display: flex; align-items: center;
        text-transform: uppercase; opacity: 0.8;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.3), transparent); margin-left: 15px; }

    .sovereign-card { 
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); 
        border-radius: 14px; padding: 22px; margin-bottom: 20px; position: relative;
    }
    .winner-card { border: 2px solid #fcd34d; background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); }

    .success-badge { 
        position: absolute; top: 15px; right: 15px; padding: 6px 14px; border-radius: 20px; 
        font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.7rem; z-index: 10;
    }

    .prob-container { margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px; }
    .prob-row { display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.75rem; margin-bottom: 8px; }

    .legal-box {
        background: rgba(248, 113, 113, 0.05); border: 1px solid rgba(248, 113, 113, 0.2); 
        border-radius: 10px; padding: 12px; color: #f87171; font-size: 0.7rem; line-height: 1.4;
    }

    .stButton>button { background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; color: #010409 !important; font-weight: 700; border-radius: 8px; border: none !important; }
    
    /* Gevaarlijke Reboot Knop */
    .reboot-btn > div > button {
        background: transparent !important;
        color: #f87171 !important;
        border: 1px solid rgba(248, 113, 113, 0.3) !important;
    }
    .reboot-btn > div > button:hover {
        background: rgba(248, 113, 113, 0.1) !important;
        border-color: #f87171 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, dark, lang):
    lang_instr = "Dutch" if lang == "NL" else "English"
    prompt = f"Role: Sovereign Architect. Respond entirely in {lang_instr}. Output JSON: success_rate(int), breakdown{{vibe, timing, subtext}}, green_flags(list of strings or objects), red_flags, options, winner_idx."
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("### ⚙️ SETTINGS")
    lang_choice = st.selectbox("🌍 Language", options=["NL", "EN"], index=0)
    t = translations[lang_choice]
    
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    
    # --- JURIDISCHE SECTIE ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    st.markdown(f"""
        <div class="legal-box">
            <b>{t['legal_title']}</b><br><br>
            Gebruik op eigen risico. Je bent zelf verantwoordelijk voor je verzonden berichten.
        </div>
    """, unsafe_allow_html=True)
    
    # --- REBOOT ONDERAAN ---
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='reboot-btn'>", unsafe_allow_html=True)
    if st.button(t["reboot"], use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 Please enter API Key in sidebar.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, width='stretch')
            u_ctx = st.text_area("Context", placeholder=t["ctx_ph"], height=80)
            if st.button(t["btn_scan"], use_container_width=True):
                with st.spinner("Analyzing Architecture..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, is_dark, lang_choice)
                    st.rerun()

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # --- SOCIAL SIGNALS (Fix voor AttributeError) ---
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                for gf in s.get('green_flags', []):
                    # Check of het een dict is of een string
                    label = gf.get('label', gf) if isinstance(gf, dict) else gf
                    st.markdown(f'<div class="pill pill-green">✅ {label}</div>', unsafe_allow_html=True)
            with sc2:
                for rf in s.get('red_flags', []):
                    label = rf.get('label', rf) if isinstance(rf, dict) else rf
                    st.markdown(f'<div class="pill pill-red">🚩 {label}</div>', unsafe_allow_html=True)
            
            # --- WINNER CARD ---
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            w = s['options'][s.get('winner_idx', 0)]
            b = s.get('breakdown', {'vibe': 50, 'timing': 50, 'subtext': 50})
            rate = s.get('success_rate', 0)
            color = "#fcd34d" if rate > 75 else "#f87171"

            st.markdown(f"""
                <div class="sovereign-card winner-card">
                    <div class="success-badge" style="border:1px solid {color}; color:{color}; background:rgba(0,0,0,0.5);">
                        {rate}% HIT RATE
                    </div>
                    <div style="font-size:1.25rem; font-weight:700; margin-bottom:18px; padding-right:115px; line-height:1.4; color:white;">
                        "{w.get('zin')}"
                    </div>
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:15px; border-left: 2px solid {color}; padding-left: 10px;">
                        <b>{t['strategy_label']}:</b> {w.get('psychology')}
                    </div>
                    <div class="prob-container">
                        <div class="prob-row"><span style="opacity:0.6;">VIBE</span><span style="font-weight:700; color:{color}">{b.get('vibe', 0)}%</span></div>
                        <div class="prob-row"><span style="opacity:0.6;">TIMING</span><span style="font-weight:700; color:{color}">{b.get('timing', 0)}%</span></div>
                        <div class="prob-row"><span style="opacity:0.6;">SUBTEXT</span><span style="font-weight:700; color:{color}">{b.get('subtext', 0)}%</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.code(w.get('zin'), language=None)
            
            # --- ALTERNATIVES ---
            st.markdown(f"<div class='section-header' style='margin-top:40px;'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s.get('options', [])):
                if i != s.get('winner_idx', 0):
                    c1, c2 = st.columns([5, 1])
                    with c1:
                        st.markdown(f"""
                            <div class="sovereign-card" style="margin-bottom:12px;">
                                <div style="font-size:0.6rem; opacity:0.5; font-family:JetBrains Mono;">{opt.get('type', 'ALT')}</div>
                                <b>"{opt.get('zin')}"</b>
                            </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.write(""); st.button(t["copy_btn"], key=f"c_{i}")
        else:
            st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V10.8 | TYPE-SAFE</div>", unsafe_allow_html=True)
