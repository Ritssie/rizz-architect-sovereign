import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# --- 1. CORE CONFIGURATION ---
st.set_page_config(
    page_title="Rizz Architect Sovereign v6.3.1", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MULTI-LANGUAGE DICTIONARY ---
translations = {
    "NL": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "TACTISCHE INTAKE",
        "tag_briefing": "STRATEGISCHE BRIEFING",
        "tag_pick": "ARCHITECT'S CHOICE",
        "tag_dims": "DIMENSIES",
        "tag_signals": "ANALYSE",
        "ctx_ph": "Bijv: 18j, ontmoet via Hinge, ze reageert kortaf...",
        "btn_scan": "⚡ EXECUTE STRATEGIC SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEEM REBOOT",
        "intel_main": """
            **DE GOUDEN REGELS:**
            * **Frame Control:** Jij bepaalt de realiteit van het gesprek.
            * **Effort Ratio:** Investeer nooit meer dan 70% van haar energie.
            * **The Hook:** Eindig altijd op een emotionele piek.
        """,
        "dark_alert": """
            **⚠️ DARK OPS PROTOCOL GEACTIVEERD**
            Je betreedt nu het terrein van gedragsbeïnvloeding. 
            Focus: *Emotional Spikes* & *Strategic Coldness*.
            *Risico: Contactbreuk bij verkeerde timing.*
        """
    },
    "EN": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "TACTICAL INTAKE",
        "tag_briefing": "STRATEGIC BRIEFING",
        "tag_pick": "ARCHITECT'S CHOICE",
        "tag_dims": "DIMENSIONS",
        "tag_signals": "ANALYSIS",
        "ctx_ph": "E.g.: 18yo, met on Hinge, dry texter...",
        "btn_scan": "⚡ EXECUTE STRATEGIC SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "intel_main": "Core Laws: Frame Control, Effort Ratio, The Hook.",
        "dark_alert": "Warning: High-risk psychological tactics active."
    }
}

# --- 3. POLISHED CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; 
        color: #e2e8f0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    .brand-container { text-align: center; padding: 40px 0 20px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3rem; color: #ffffff !important; letter-spacing: -1px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 30px rgba(252, 211, 77, 0.4); }

    .section-header {
        font-family: 'JetBrains Mono', monospace;
        color: #fcd34d;
        font-size: 0.75rem;
        letter-spacing: 3px;
        margin: 30px 0 15px 0;
        display: flex;
        align-items: center;
        opacity: 0.8;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: rgba(252, 211, 77, 0.15); margin-left: 15px; }

    .sovereign-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .winner-card {
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.1) 0%, rgba(1, 4, 9, 1) 100%);
        border: 2px solid #fcd34d;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }
    
    .badge-gold {
        background: #fcd34d;
        color: #010409;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 800;
        font-size: 0.7rem;
        padding: 4px 12px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 12px;
    }

    .danger-card {
        background: rgba(239, 68, 68, 0.05);
        border: 1px solid rgba(248, 113, 113, 0.4);
        color: #f87171;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
        font-size: 0.85rem;
    }

    /* Fix voor afgeronde hoeken bij afbeeldingen */
    [data-testid="stImage"] img {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .stButton>button {
        background: #fcd34d !important;
        color: #010409 !important;
        font-weight: 800;
        border-radius: 12px;
        height: 4rem;
        border: none !important;
        width: 100%;
        font-size: 1rem;
        letter-spacing: 1px;
    }
    
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid rgba(255,255,255,0.1) !important; color: white !important; border-radius: 12px; }
    
    .flag-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        margin: 0 8px 8px 0;
        font-weight: 600;
    }
    .pill-green { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
    .pill-red { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE CORE FUNCTIONS ---
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

def get_architect_response(client, b64, ctx, lang, dark):
    mode = "PSYCHOLOGICAL DARK OPS" if dark else "ELITE SOCIAL CHARISMA"
    prompt = f"Role: Sovereign Architect. Mode: {mode}. Language: {lang}. Output JSON only."
    
    res = client.chat.completions.create(
        model="grok-4.20-0309-non-reasoning",
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

# --- 5. INTERFACE ASSEMBLY ---
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("### 🎚️ CONTROL PANEL")
    l_key = st.radio("Language", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api_key = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    is_dark = st.toggle(t["dark_mode"], key="dt_toggle")
    if st.button(t["reboot"]):
        st.session_state.clear()
        st.rerun()

# Branding
st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 SYSTEM LOCKED. Please initialize with API Key.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Screenshot", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("Intelligence Context", placeholder=t["ctx_ph"], height=90, label_visibility="collapsed")
            if st.button(t["btn_scan"]):
                with st.spinner("Decoding social layers..."):
                    try:
                        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                        st.session_state.state = get_architect_response(client, process_img(u_file), u_ctx, l_key, is_dark)
                        st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
        
        # Briefing Card
        st.markdown(f"<div class='section-header'>{t['tag_briefing']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sovereign-card'>{t['intel_main']}</div>", unsafe_allow_html=True)
        
        if is_dark:
            st.markdown(f"<div class='danger-card'>{t['dark_alert']}</div>", unsafe_allow_html=True)

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # Probability Card
            st.markdown(f"<div class='section-header'>SLAGINGSKANS</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='sovereign-card' style='padding: 15px 24px;'><div style='font-size:1.5rem; font-weight:800; color:#fcd34d;'>{s.get('success_rate', 50)}%</div></div>", unsafe_allow_html=True)
            
            # Winner Card
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            best = s['options'][s.get('winner_idx', 0)]
            st.markdown(f"""
                <div class="sovereign-card winner-card">
                    <div class="badge-gold">OPTIMAL TRAJECTORY</div>
                    <div style="font-family:'JetBrains Mono'; color:#94a3b8; font-size:0.75rem; margin-bottom:8px;">{best.get('type')}</div>
            """, unsafe_allow_html=True)
            st.code(best.get('zin'), language=None)
            st.markdown(f"""
                    <div style="margin-top:20px; padding-top:15px; border-top:1px solid rgba(252,211,77,0.2); font-size:0.85rem; color:#fcd34d;">
                        <b>PSYCHOLOGISCHE LOGICA:</b><br>{s.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Flags & Dims Split
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.markdown(f"<div class='section-header'>SIGNALEN</div>", unsafe_allow_html=True)
                for gf in s.get('green_flags', []): st.markdown(f"<div class='flag-pill pill-green'>✅ {gf}</div>", unsafe_allow_html=True)
                for rf in s.get('red_flags', []): st.markdown(f"<div class='flag-pill pill-red'>🚩 {rf}</div>", unsafe_allow_html=True)
            
            with f_col2:
                st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
                for i, opt in enumerate(s['options']):
                    if i != s.get('winner_idx', 0):
                        st.markdown(f"""
                            <div class="sovereign-card" style="padding:15px; margin-bottom:10px;">
                                <div style="font-size:0.7rem; font-family:'JetBrains Mono'; opacity:0.6;">{opt.get('type')}</div>
                                <div style="font-size:0.85rem; margin-top:5px;">{opt.get('zin')}</div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("System stand-by. Waiting for tactical input.")

# --- 6. FOOTER ---
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE v6.3.1 | STABLE RELEASE</div>", unsafe_allow_html=True)
