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
    page_title="RIZZ ARCHITECT SOVEREIGN v12.0", 
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
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "upload_label": "📂 UPLOAD SCREENSHOT",
        "copy_btn": "KOPIEER",
        "copied": "Gekopieerd naar klembord!",
        "strategy_label": "PSYCHOLOGIE",
        "legal_title": "LEGAL SHIELD & TERMS",
        "legal_text": "<b>1. Geen Garantie:</b> AI biedt suggesties.<br><b>2. Eigen Risico:</b> Jij bent de verzender.<br><b>3. Privacy:</b> Geen gevoelige data.",
        "idle_msg": "Wachten op data... Upload een screenshot om te beginnen."
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 DATA INGESTION",
        "tag_pick": "🏆 ALPHA SELECTION",
        "tag_dims": "📐 STRATAGEM ARSENAL",
        "tag_signals": "📡 TACTICAL SIGNALS",
        "ctx_ph": "Vibe, relationship, last message, goal...",
        "btn_scan": "⚡ EXECUTE ARCHITECT SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "upload_label": "📂 UPLOAD SCREENSHOT",
        "copy_btn": "COPY",
        "copied": "Copied to clipboard!",
        "strategy_label": "PSYCHOLOGY",
        "legal_title": "LEGAL SHIELD & TERMS",
        "legal_text": "<b>1. No Guarantee:</b> AI provides suggestions.<br><b>2. Liability:</b> You are the sender.<br><b>3. Privacy:</b> No sensitive data.",
        "idle_msg": "System standby. Upload screenshot to initialize."
    }
}

# ==============================================================================
# --- 3. ULTRA-PREMIUM CSS (V12 PLATINUM) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    /* Base Theme */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #05070a !important; 
        color: #e2e8f0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* Header & Branding */
    .brand-container { text-align: center; padding: 40px 0; background: linear-gradient(180deg, rgba(252, 211, 77, 0.05) 0%, transparent 100%); border-bottom: 1px solid rgba(252, 211, 77, 0.1); margin-bottom: 30px; }
    .brand-logo { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; color: #ffffff !important; letter-spacing: 4px; font-weight: 800; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 30px rgba(252, 211, 77, 0.6); }

    /* Section Headers */
    .section-header {
        font-family: 'Orbitron', sans-serif; color: #fcd34d; font-size: 0.75rem;
        letter-spacing: 4px; margin: 40px 0 20px 0; display: flex; align-items: center;
        text-transform: uppercase; opacity: 0.9;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.4), transparent); margin-left: 20px; }

    /* Cards (Glassmorphism) */
    .sovereign-card { 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 20px; padding: 25px; position: relative; 
        backdrop-filter: blur(10px); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .sovereign-card:hover { transform: translateY(-5px); border-color: rgba(252, 211, 77, 0.3); box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
    
    .winner-card { 
        border: 1px solid rgba(252, 211, 77, 0.5); 
        background: linear-gradient(145deg, rgba(252, 211, 77, 0.08) 0%, rgba(1, 4, 9, 0.4) 100%); 
    }

    .success-badge { 
        position: absolute; top: 20px; right: 20px; padding: 6px 16px; border-radius: 30px; 
        font-family: 'Orbitron', sans-serif; font-weight: 700; font-size: 0.6rem;
        background: rgba(252, 211, 77, 0.1); border: 1px solid #fcd34d; color: #fcd34d;
        box-shadow: 0 0 15px rgba(252, 211, 77, 0.2);
    }

    /* Buttons */
    .stButton>button { 
        background: linear-gradient(135deg, #fcd34d 0%, #d97706 100%) !important; 
        color: #000 !important; font-weight: 800 !important; border-radius: 12px !important; 
        border: none !important; padding: 15px 25px !important;
        text-transform: uppercase; letter-spacing: 2px; font-family: 'Orbitron', sans-serif;
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4) !important;
    }
    
    /* Stats Bar */
    .prob-container { margin-top: 25px; }
    .prob-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .prob-label { font-family: 'Orbitron', sans-serif; font-size: 0.65rem; opacity: 0.6; }
    .prob-bar-bg { background: rgba(255,255,255,0.05); height: 4px; width: 60%; border-radius: 2px; overflow: hidden; }
    .prob-bar-fill { background: #fcd34d; height: 100%; border-radius: 2px; box-shadow: 0 0 10px #fcd34d; }

    /* Custom Signal Pills */
    .signal-pill {
        padding: 8px 15px; border-radius: 10px; margin-bottom: 10px; font-size: 0.8rem; font-weight: 600;
        display: flex; align-items: center; gap: 10px; border: 1px solid transparent;
    }
    .pill-green { background: rgba(34, 197, 94, 0.1); border-color: rgba(34, 197, 94, 0.3); color: #4ade80; }
    .pill-red { background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3); color: #f87171; }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #020408 !important; border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, dark, lang):
    lang_name = "Dutch" if lang == "NL" else "English"
    prompt = f"Role: Sovereign Architect. Respond ONLY in {lang_name}. Return JSON: success_rate(int), breakdown{{vibe, timing, subtext}}, green_flags[str], red_flags[str], options[{{\"type\": \"str\", \"zin\": \"str\", \"psychology\": \"str\"}}], winner_idx."
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
    except Exception as e:
        st.error(f"ENGINE ERROR: {e}")
        return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: 
    st.session_state.state = None

with st.sidebar:
    st.markdown("<h2 style='font-family:Orbitron; color:#fcd34d; font-size:1.2rem;'>CONTROL CENTER</h2>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌍 Language", options=["NL", "EN"], index=0)
    t = translations[lang_choice]
    
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"], value=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); padding:15px; border-radius:10px; font-size:0.7rem; border:1px solid rgba(255,255,255,0.05);">
            <b style="color:#fcd34d;">{t['legal_title']}</b><br><br>
            {t['legal_text']}
        </div>
    """, unsafe_allow_html=True)

    if st.button(t["reboot"], use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- MAIN UI ---
st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.warning("🔐 ARCHITECT ACCESS DENIED. PLEASE PROVIDE API KEY IN CONTROL CENTER.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Contextual Intelligence", placeholder=t["ctx_ph"], height=100)
            
            if st.button(t["btn_scan"], use_container_width=True):
                with st.spinner("INITIALIZING SOVEREIGN ENGINE..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, is_dark, lang_choice)
                    st.rerun()

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # --- TACTICAL SIGNALS ---
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                for gf in s.get('green_flags', []):
                    st.markdown(f'<div class="signal-pill pill-green">✔ {gf}</div>', unsafe_allow_html=True)
            with sc2:
                for rf in s.get('red_flags', []):
                    st.markdown(f'<div class="signal-pill pill-red">✘ {rf}</div>', unsafe_allow_html=True)

            # --- ALPHA SELECTION (WINNER) ---
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            opts = s.get('options', [])
            w_idx = s.get('winner_idx', 0)

            if opts and len(opts) > w_idx:
                w = opts[w_idx]
                zin = w.get('zin')
                psych = w.get('psychology')
                rate = s.get('success_rate', 85)
                b = s.get('breakdown', {'vibe': 50, 'timing': 50, 'subtext': 50})

                st.markdown(f"""
                    <div class="sovereign-card winner-card">
                        <div class="success-badge">{rate}% HIT RATE</div>
                        <div style="font-size:1.5rem; font-weight:800; margin-bottom:20px; color:white; font-family:'Inter'; line-height:1.4;">"{zin}"</div>
                        <div style="font-size:0.85rem; opacity:0.8; border-left: 3px solid #fcd34d; padding-left: 15px; margin-bottom: 25px; font-style: italic;">
                            <b style="color:#fcd34d; font-family:'Orbitron'; letter-spacing:1px;">STRATAGEM:</b> {psych}
                        </div>
                        <div class="prob-container">
                            <div class="prob-row">
                                <span class="prob-label">VIBE STRENGTH</span>
                                <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{b.get('vibe')}%"></div></div>
                                <span style="font-family:'Orbitron'; font-size:0.7rem; color:#fcd34d;">{b.get('vibe')}%</span>
                            </div>
                            <div class="prob-row">
                                <span class="prob-label">TEMPORAL TIMING</span>
                                <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{b.get('timing')}%"></div></div>
                                <span style="font-family:'Orbitron'; font-size:0.7rem; color:#fcd34d;">{b.get('timing')}%</span>
                            </div>
                            <div class="prob-row">
                                <span class="prob-label">SUBTEXT DEPTH</span>
                                <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{b.get('subtext')}%"></div></div>
                                <span style="font-family:'Orbitron'; font-size:0.7rem; color:#fcd34d;">{b.get('subtext')}%</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"✨ {t['copy_btn']} ALPHA LINE", key="cp_w", use_container_width=True):
                    st.toast(t["copied"])

            # --- ARSENAL (ALTERNATIVES) ---
            st.markdown(f"<div class='section-header' style='margin-top:50px;'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(opts):
                if i != w_idx:
                    a_zin, a_psych, a_type = opt.get('zin'), opt.get('psychology'), opt.get('type', 'ALT')
                    st.markdown(f"""
                        <div class="sovereign-card" style="margin-bottom:15px; padding: 20px;">
                            <div style="font-family:'Orbitron'; font-size:0.6rem; color:#fcd34d; margin-bottom:10px; opacity:0.6;">{a_type}</div>
                            <div style="font-weight:600; font-size:1.1rem; margin-bottom:12px; color:#e2e8f0;">"{a_zin}"</div>
                            <div style="font-size:0.75rem; opacity:0.6;">{a_psych}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"COPY {a_type}", key=f"cp_{i}", use_container_width=True):
                        st.toast(t["copied"])
        else:
            st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:80px; letter-spacing:5px;'>SOVEREIGN ENGINE V12.0 // PLATINUM EDITION</div>", unsafe_allow_html=True)
