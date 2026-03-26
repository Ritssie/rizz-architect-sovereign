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
    page_title="Rizz Architect Sovereign v13.6", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. ARCHETYPE & STYLE ENGINE ---
# ==============================================================================
def clean_type(t):
    t_low = t.lower() if t else ""
    if any(x in t_low for x in ["provocateur", "energy", "playful"]): return "Playful Provocateur"
    if any(x in t_low for x in ["charmer", "velvet", "leadership"]): return "Velvet Charmer"
    if any(x in t_low for x in ["interrupt", "pattern", "challenger"]): return "Pattern Interrupt"
    return "Strategic Move"

# ==============================================================================
# --- 3. MULTI-LANGUAGE DICTIONARY (Hersteld & Uitgebreid) ---
# ==============================================================================
translations = {
    "NL": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTISCHE INTAKE",
        "tag_pick": "🏆 PRIME CHOICE",
        "tag_dims": "📐 TACTISCH ARSENAAL",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Vibe, relatie, laatste bericht, doel...",
        "btn_scan": "⚡ START DEEP SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 RESET SYSTEEM",
        "upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "KOPIEER",
        "copied": "Gekopieerd!",
        "strategy_label": "ANALYSE",
        "legal_title": "TERMS & LEGAL SHIELD",
        "legal_text": "<b>1. Geen Garantie:</b> AI biedt suggesties.<br><b>2. Eigen Risico:</b> Jij bent de verzender.<br><b>3. Privacy:</b> Geen gevoelige data.",
        "idle_msg": "Systeem stand-by. Upload screenshot voor diepte-analyse.",
        "restricted": "🔐 Beperkte Toegang. Voer API Key in."
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTICAL INTAKE",
        "tag_pick": "🏆 PRIME CHOICE",
        "tag_dims": "📐 TACTICAL ARSENAL",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Vibe, relationship, last message, goal...",
        "btn_scan": "⚡ EXECUTE DEEP SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 RESET SYSTEM",
        "upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "COPY",
        "copied": "Copied!",
        "strategy_label": "ANALYSIS",
        "legal_title": "TERMS & LEGAL SHIELD",
        "legal_text": "<b>1. No Guarantee:</b> AI suggestions only.<br><b>2. Liability:</b> User-led messaging.<br><b>3. Privacy:</b> No sensitive data.",
        "idle_msg": "System on standby. Upload screenshot for deep analysis.",
        "restricted": "🔐 Restricted Access. Enter API Key."
    }
}

# ==============================================================================
# --- 4. SOVEREIGN UI CSS (Grid & Depth) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background: #010409 !important;
        background-image: linear-gradient(rgba(252, 211, 77, 0.03) 1px, transparent 1px), 
                          linear-gradient(90deg, rgba(252, 211, 77, 0.03) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    .brand-container { text-align: center; padding: 30px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3.2rem; color: #fff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 25px rgba(252, 211, 77, 0.4); }

    .section-header {
        font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.6rem;
        letter-spacing: 4px; margin: 25px 0 15px 0; display: flex; align-items: center; text-transform: uppercase;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.3), transparent); margin-left: 15px; }

    .sovereign-card { 
        background: rgba(13, 17, 23, 0.8); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 22px; margin-bottom: 15px;
    }
    .winner-card { border: 1px solid #fcd34d; box-shadow: 0 0 30px rgba(252, 211, 77, 0.05); }

    .archetype-tag { 
        font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #fcd34d; 
        border: 1px solid rgba(252, 211, 77, 0.3); padding: 2px 8px; border-radius: 4px; margin-bottom: 10px; display: inline-block;
    }

    .pill { padding: 6px 12px; border-radius: 4px; font-size: 0.7rem; font-family: 'JetBrains Mono'; margin-bottom: 8px; border: 1px solid transparent; }
    .pill-green { background: rgba(16, 185, 129, 0.1); color: #34d399; border-color: rgba(16, 185, 129, 0.2); }
    .pill-red { background: rgba(239, 68, 68, 0.1); color: #f87171; border-color: rgba(239, 68, 68, 0.2); }

    .stButton>button { 
        background: transparent !important; border: 1px solid rgba(252, 211, 77, 0.4) !important; color: #fcd34d !important;
        font-family: 'JetBrains Mono' !important; font-size: 0.7rem !important; text-transform: uppercase !important;
    }
    .stButton>button:hover { background: rgba(252, 211, 77, 0.1) !important; border-color: #fcd34d !important; }
    
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 5. ENGINE CORE ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, lang):
    lang_name = "Dutch" if lang == "NL" else "English"
    prompt = f"""Role: Sovereign Architect. Respond ONLY in {lang_name}.
    Analyze the screenshot with extreme precision.
    1. Identify hidden subtext and power dynamics.
    2. Provide 3 distinct options: Playful Provocateur, Velvet Charmer, Pattern Interrupt.
    3. For EACH option, explain the 'Social Engineering' behind it (why it works, what it triggers).
    Return JSON: 
    {{
      "success_rate": int,
      "green_flags": [str],
      "red_flags": [str],
      "options": [
        {{"type": "str", "zin": "str", "psychology": "DEEP ANALYSIS"}}
      ],
      "winner_idx": 0
    }}"""
    try:
        res = client.chat.completions.create(
            model="grok-2-vision-latest",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
        )
        return json.loads(res.choices[0].message.content)
    except: return None

# ==============================================================================
# --- 6. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ SYSTEM")
    lang_choice = st.selectbox("Language", options=["NL", "EN"])
    t = translations[lang_choice]
    
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    
    with st.expander(f"⚖️ {t['legal_title']}"):
        st.markdown(f'<div style="font-size:0.65rem; color:#64748b; line-height:1.4;">{t["legal_text"]}</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    if st.button(t["reboot"], use_container_width=True):
        st.session_state.clear(); st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info(t["restricted"])
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Live Context", placeholder=t["ctx_ph"], height=70)
            if st.button(t["btn_scan"], use_container_width=True):
                with st.spinner("Analyzing Matrix..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, lang_choice)
                    st.rerun()

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # SIGNALS
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                for gf in s.get('green_flags', []): st.markdown(f'<div class="pill pill-green">✓ {gf}</div>', unsafe_allow_html=True)
            with sc2:
                for rf in s.get('red_flags', []): st.markdown(f'<div class="pill pill-red">! {rf}</div>', unsafe_allow_html=True)
            
            # OPTIONS
            st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s.get('options', [])):
                is_winner = (i == s.get('winner_idx', 0))
                card_class = "winner-card" if is_winner else ""
                a_type = clean_type(opt.get('type'))
                
                st.markdown(f"""
                    <div class="sovereign-card {card_class}">
                        <div class="archetype-tag">{"⭐ " if is_winner else ""}{a_type}</div>
                        <div style="font-size:1.2rem; font-weight:800; margin-bottom:12px; color:#fff;">"{opt.get('zin')}"</div>
                        <div style="font-size:0.8rem; color:#94a3b8; line-height:1.5;">
                            <b style="color:#fcd34d;">{t['strategy_label']}:</b> {opt.get('psychology')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"{t['copy_btn']} {a_type}", key=f"btn_{i}", use_container_width=True):
                    st.write(f'<script>navigator.clipboard.writeText("{opt.get("zin")}")</script>', unsafe_allow_html=True)
                    st.toast(f"{a_type} {t['copied']}")
        else:
            st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SOVEREIGN ARCHITECT V13.6</div>", unsafe_allow_html=True)
