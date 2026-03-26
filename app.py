import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# --- 1. CORE CONFIGURATION ---
st.set_page_config(
    page_title="Rizz Architect Sovereign", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INTELLIGENCE DICTIONARY ---
translations = {
    "NL": {
        "header_main": "RIZZ<span>ARCHITECT</span>",
        "label_intake": "📥 TACTISCHE INTAKE",
        "label_pick": "🏆 ARCHITECT'S PICK",
        "label_dims": "📐 STRATEGISCHE DIMENSIES",
        "label_signals": "📡 SIGNALEN",
        "label_intel": "📖 MISSION BRIEFING",
        "ctx_ph": "Bijv: 18j, reageert afstandelijk na date...",
        "btn_execute": "🚀 START STRATEGISCHE SCAN",
        "success_rate": "SLAGINGSPERCENTAGE",
        "psych_title": "🧠 PSYCHOLOGISCHE ANALYSE",
        "idle_msg": "Systeem stand-by. Upload screenshots voor analyse.",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEEM HERSTARTEN",
        "standard_intel": """
            ### 🛡️ Standaard Strategie
            Focus op **High-Value leadership** en charisma.
            * **Frame:** Jij bepaalt de richting van het gesprek.
            * **Tension:** Gebruik speelsheid om aantrekkingskracht te creëren.
        """,
        "dark_intel_warning": """
            ### ⚠️ WAARSCHUWING: DARK OPS GEACTIVEERD
            Dit menu bevat nu instructies voor **high-risk** beïnvloeding.
            
            **Strategische Risico's:**
            * **Scarcity Tactics:** We creëren een kunstmatig gevoel van verlies.
            * **Push-Pull Dynamics:** Extreme schommelingen in aandacht om haar investering te forceren.
            * **Frame Dominance:** Je tolereert geen enkel gebrek aan respect en straft dit direct af.
            
            *Let op: Deze modus kan contacten permanent verbreken als het verkeerd wordt toegepast.*
        """,
        "footer_text": "RIZZ ARCHITECT | SECURE OPERATIONAL INTERFACE"
    },
    "EN": {
        "header_main": "RIZZ<span>ARCHITECT</span>",
        "label_intake": "📥 TACTICAL INTAKE",
        "label_pick": "🏆 ARCHITECT'S PICK",
        "label_dims": "📐 STRATEGIC DIMENSIONS",
        "label_signals": "📡 SIGNALS",
        "label_intel": "📖 MISSION BRIEFING",
        "ctx_ph": "E.g.: 18yo, cold after date...",
        "btn_execute": "🚀 START STRATEGIC SCAN",
        "success_rate": "SUCCESS PROBABILITY",
        "psych_title": "🧠 PSYCHOLOGICAL ANALYSIS",
        "idle_msg": "System stand-by. Upload data.",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 REBOOT SYSTEM",
        "standard_intel": "Standard high-value leadership content...",
        "dark_intel_warning": "Warning: High-risk psychological tactics enabled...",
        "footer_text": "RIZZ ARCHITECT | SECURE OPERATIONAL INTERFACE"
    }
}

# --- 3. CSS DESIGN SYSTEM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; }
    
    .header-box { text-align: center; padding: 30px 0; margin-bottom: 20px; }
    .logo { font-family: 'Playfair Display', serif; font-size: 2.8rem; color: #ffffff !important; }
    .logo span { color: #fcd34d !important; text-shadow: 0 0 30px rgba(252, 211, 77, 0.4); }

    .section-tag { font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 15px; display: block; opacity: 0.8; }

    .pick-card { 
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); 
        border: 2px solid #fcd34d; border-radius: 20px; padding: 35px; position: relative; 
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5); 
    }
    .pick-badge { position: absolute; top: -16px; left: 30px; background: #fcd34d; color: #010409; font-family: 'JetBrains Mono', monospace; font-weight: 900; font-size: 0.8rem; padding: 4px 18px; border-radius: 8px; }

    .dark-warning-box {
        background: rgba(239, 68, 68, 0.05); border: 1px solid #f87171; border-radius: 12px; padding: 20px; color: #f87171; margin-top: 10px;
    }

    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 800; border-radius: 12px; height: 3.8rem; border: none !important; font-size: 1.1rem; width: 100%;
    }
    
    .stExpander { border: 1px solid rgba(252, 211, 77, 0.2) !important; background: transparent !important; border-radius: 12px !important; }
    
    .footer { text-align: center; opacity: 0.3; font-size: 0.65rem; font-family: 'JetBrains Mono', monospace; margin-top: 60px; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA PROCESSING ---
def get_b64(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

def run_scan(client, b64, ctx, lang, dark):
    mode = "DARK OPS" if dark else "STANDARD"
    prompt = f"Role: Sovereign Architect. Mode: {mode}. Language: {lang}. Provide tactical responses in JSON."
    res = client.chat.completions.create(
        model="grok-4.20-0309-non-reasoning",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": [{"type":"text","text":f"Ctx:{ctx}"},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}
        ]
    )
    return json.loads(res.choices[0].message.content)

# --- 5. UI ASSEMBLY ---
if 'res' not in st.session_state: st.session_state.res = None

with st.sidebar:
    st.markdown("### 🛠️ CONTROL")
    l_key = st.radio("Language", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    is_dark = st.toggle(t["dark_mode"])
    if st.button(t["reboot"]):
        st.session_state.clear(); st.rerun()

st.markdown(f'<div class="header-box"><div class="logo">{t["header_main"]}</div></div>', unsafe_allow_html=True)

if not api:
    st.info("System stand-by. Enter API key to begin.")
else:
    cl, cr = st.columns([1, 1.3], gap="large")

    with cl:
        st.markdown(f"<span class='section-tag'>{t['label_intake']}</span>", unsafe_allow_html=True)
        f = st.file_uploader("Upload", type=['png','jpg','jpeg'], label_visibility="collapsed")
        if f:
            st.image(f, use_container_width=True)
            u_ctx = st.text_area("Intelligence Context", placeholder=t["ctx_ph"], height=80)
            if st.button(t["btn_execute"]):
                with st.spinner("Analyzing dynamics..."):
                    try:
                        ai = OpenAI(api_key=api, base_url="https://api.x.ai/v1")
                        st.session_state.res = run_scan(ai, get_b64(f), u_ctx, l_key, is_dark)
                        st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"✨ {t['label_intel']}", expanded=is_dark):
            if is_dark:
                st.markdown(f"<div class='dark-warning-box'>{t['dark_intel_warning']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(t['standard_intel'])

    with cr:
        if st.session_state.res:
            d = st.session_state.res
            st.markdown(f"<span class='section-tag'>{t['success_rate']}</span>", unsafe_allow_html=True)
            st.progress(d.get('success_rate', 50) / 100)
            
            st.markdown(f"<span class='section-tag'>{t['label_pick']}</span>", unsafe_allow_html=True)
            best = d['options'][d.get('winner_idx', 0)]
            st.markdown(f"""
                <div class="pick-card">
                    <div class="pick-badge">OPTIMIZED MOVE</div>
                    <div style="font-family:'JetBrains Mono'; color:#94a3b8; font-size:0.8rem; margin-bottom:10px;">{best.get('type')}</div>
            """, unsafe_allow_html=True)
            st.code(best.get('zin'), language=None)
            st.markdown(f"""
                    <div style="margin-top:20px; padding-top:15px; border-top:1px solid rgba(252,211,77,0.2); font-size:0.85rem; color:#fcd34d;">
                        <b>{t['psych_title']}:</b><br>{d.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<span class='section-tag'>{t['label_signals']}</span>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                for gf in d.get('green_flags', []): st.markdown(f"<div style='color:#4ade80; font-size:0.8rem;'>✅ {gf}</div>", unsafe_allow_html=True)
            with sc2:
                for rf in d.get('red_flags', []): st.markdown(f"<div style='color:#f87171; font-size:0.8rem;'>🚩 {rf}</div>", unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# --- 6. FOOTER (CLEANED) ---
st.markdown(f"<div class='footer'>{t['footer_text']}</div>", unsafe_allow_html=True)
