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
    page_title="Rizz Architect Sovereign v13.0", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. THE ARCHETYPE CLEANER ---
# ==============================================================================
def clean_type(t):
    if not t: return "Unknown Strategy"
    t_low = t.lower()
    if any(x in t_low for x in ["provocateur", "energy", "playful"]): return "Playful Provocateur"
    if any(x in t_low for x in ["charmer", "velvet", "leadership"]): return "Velvet Charmer"
    if any(x in t_low for x in ["interrupt", "pattern", "challenger"]): return "Pattern Interrupt"
    return t

# ==============================================================================
# --- 3. PREMIUM CSS ENGINE (The "Touch" Update) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    /* Background & Global */
    html, body, [data-testid="stAppViewContainer"] { 
        background: radial-gradient(circle at top right, #0a0f1a, #010409) !important; 
        color: #e2e8f0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* Brand Header */
    .brand-container { text-align: center; padding: 40px 0 20px 0; }
    .brand-logo { 
        font-family: 'Playfair Display', serif; 
        font-size: 3.5rem; 
        color: #ffffff !important; 
        letter-spacing: -3px;
        line-height: 1;
    }
    .brand-logo span { 
        color: #fcd34d !important; 
        text-shadow: 0 0 30px rgba(252, 211, 77, 0.5); 
    }

    /* Section Headers */
    .section-header {
        font-family: 'JetBrains Mono', monospace; 
        color: rgba(252, 211, 77, 0.8); 
        font-size: 0.65rem;
        letter-spacing: 4px; 
        margin: 30px 0 15px 0; 
        display: flex; 
        align-items: center;
        text-transform: uppercase;
    }
    .section-header::after { 
        content: ""; flex: 1; height: 1px; 
        background: linear-gradient(90deg, rgba(252, 211, 77, 0.4), transparent); 
        margin-left: 20px; 
    }

    /* Sovereign Card System */
    .sovereign-card { 
        background: rgba(255, 255, 255, 0.01); 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 16px; 
        padding: 24px; 
        position: relative; 
        overflow: hidden; 
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }

    .winner-card { 
        border: 1px solid rgba(252, 211, 77, 0.5); 
        background: linear-gradient(145deg, rgba(252, 211, 77, 0.08) 0%, rgba(0, 0, 0, 0) 100%);
        box-shadow: 0 10px 40px -10px rgba(252, 211, 77, 0.15);
    }

    .archetype-label { 
        font-family: 'JetBrains Mono', monospace; 
        font-size: 0.6rem; 
        color: #fcd34d; 
        font-weight: 700; 
        text-transform: uppercase; 
        margin-bottom: 12px; 
        letter-spacing: 2px;
        background: rgba(252, 211, 77, 0.1);
        padding: 4px 10px;
        border-radius: 4px;
        display: inline-block;
    }

    .success-badge { 
        position: absolute; top: 20px; right: 20px; padding: 5px 14px; border-radius: 30px; 
        font-family: 'JetBrains Mono'; font-size: 0.6rem; 
        background: #000; border: 1px solid #fcd34d; color: #fcd34d;
        box-shadow: 0 0 15px rgba(252, 211, 77, 0.2);
    }

    /* Signals / Pills */
    .pill { padding: 8px 14px; border-radius: 8px; font-size: 0.7rem; font-weight: 600; margin-bottom: 10px; }
    .pill-green { background: rgba(16, 185, 129, 0.08); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .pill-red { background: rgba(239, 68, 68, 0.08); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

    /* Button Styling */
    .stButton>button { 
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover { 
        border-color: #fcd34d !important;
        color: #fcd34d !important;
        background: rgba(252, 211, 77, 0.05) !important;
        box-shadow: 0 0 20px rgba(252, 211, 77, 0.1) !important;
    }

    /* Sidebar Fixes */
    [data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid rgba(255,255,255,0.05); }
    </style>
    """, unsafe_allow_html=True)

# ... (Helper functions process_img & get_analysis blijven gelijk aan v12.6) ...

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, dark, lang):
    lang_name = "Dutch" if lang == "NL" else "English"
    prompt = f"""Role: Sovereign Architect. Respond ONLY in {lang_name}. 
    Analyze the screenshot and provide 3 options based on these archetypes:
    - Playful Provocateur
    - Velvet Charmer
    - Pattern Interrupt
    Return JSON: success_rate(int), green_flags[str], red_flags[str], options[{{\"type\": \"str\", \"zin\": \"str\", \"psychology\": \"str\"}}], winner_idx."""
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
# --- 4. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("<div style='padding-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ SYSTEM CONFIG")
    lang_choice = st.selectbox("🌍 Core Language", options=["NL", "EN"], index=0)
    t = {"NL": {"header": "RIZZ<span>ARCHITECT</span>", "tag_intake": "📥 INTAKE", "tag_pick": "🏆 PRIME CHOICE", "tag_dims": "📐 ARSENAL", "tag_signals": "📡 SIGNALS", "ctx_ph": "Context...", "btn_scan": "⚡ ANALYZE", "dark_mode": "🌑 Dark Psychology", "reboot": "🔄 RESET", "upload_label": "DATA SOURCE", "copy_btn": "COPY", "copied": "Copied", "strategy_label": "PSYCHOLOGY", "legal_title": "LEGAL SHIELD", "legal_text": "Suggestions only. Use at own risk.", "idle_msg": "System Standby..."}, 
         "EN": {"header": "RIZZ<span>ARCHITECT</span>", "tag_intake": "📥 INTAKE", "tag_pick": "🏆 PRIME CHOICE", "tag_dims": "📐 ARSENAL", "tag_signals": "📡 SIGNALS", "ctx_ph": "Context...", "btn_scan": "⚡ ANALYZE", "dark_mode": "🌑 Dark Psychology", "reboot": "🔄 RESET", "upload_label": "DATA SOURCE", "copy_btn": "COPY", "copied": "Copied", "strategy_label": "PSYCHOLOGY", "legal_title": "LEGAL SHIELD", "legal_text": "Suggestions only.", "idle_msg": "Standby..."}}[lang_choice]
    
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    
    with st.expander(f"⚖️ {t['legal_title']}"):
        st.markdown(f'<div style="font-size:0.65rem; color:#64748b;">{t["legal_text"]}</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    if st.button(t["reboot"], use_container_width=True):
        st.session_state.clear(); st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 Restricted Access. Enter API Key.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'], label_visibility="collapsed")
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Live Context", placeholder=t["ctx_ph"], height=70)
            if st.button(t["btn_scan"], use_container_width=True):
                with st.spinner("Decoding Social Matrix..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, is_dark, lang_choice)
                    st.rerun()

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # SIGNALS
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                for gf in s.get('green_flags', []):
                    st.markdown(f'<div class="pill pill-green">✓ {gf}</div>', unsafe_allow_html=True)
            with sc2:
                for rf in s.get('red_flags', []):
                    st.markdown(f'<div class="pill pill-red">! {rf}</div>', unsafe_allow_html=True)
            
            # PRIME CHOICE
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            opts = s.get('options', [])
            w_idx = s.get('winner_idx', 0)
            
            if opts:
                w = opts[w_idx]
                w_type = clean_type(w.get('type'))
                st.markdown(f"""
                    <div class="sovereign-card winner-card">
                        <div class="success-badge">{s.get('success_rate', 85)}% SUCCESS</div>
                        <div class="archetype-label">{w_type}</div>
                        <div style="font-size:1.4rem; font-weight:800; margin-bottom:15px; color:#fff; line-height:1.2;">"{w.get('zin')}"</div>
                        <div style="font-size:0.75rem; color:#94a3b8; border-left: 2px solid #fcd34d; padding-left: 12px;">
                            <b style="color:#fcd34d;">STRATEGY:</b> {w.get('psychology')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"✨ USE {w_type}", key="cp_w", use_container_width=True):
                    st.write(f'<script>navigator.clipboard.writeText("{w.get("zin")}")</script>', unsafe_allow_html=True)
                    st.toast(f"{w_type} Ready.")

                # ARSENAL
                st.markdown(f"<div class='section-header' style='margin-top:40px;'>{t['tag_dims']}</div>", unsafe_allow_html=True)
                for i, opt in enumerate(opts):
                    if i != w_idx:
                        a_type = clean_type(opt.get('type'))
                        st.markdown(f"""
                            <div class="sovereign-card alt-card">
                                <div class="archetype-label" style="background:rgba(255,255,255,0.05); color:#fff;">{a_type}</div>
                                <div style="font-weight:600; font-size:1.1rem; margin-bottom:10px;">"{opt.get('zin')}"</div>
                                <div style="font-size:0.75rem; color:#64748b; font-style:italic;">{opt.get('psychology')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"⚡ USE {a_type}", key=f"cp_{i}", use_container_width=True):
                            st.write(f'<script>navigator.clipboard.writeText("{opt.get("zin")}")</script>', unsafe_allow_html=True)
                            st.toast(f"{a_type} Ready.")
        else:
            st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.2; font-size:0.5rem; margin-top:80px; letter-spacing:2px;'>SOVEREIGN ARCHITECT | PRIVILEGED ACCESS</div>", unsafe_allow_html=True)
