import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# --- 1. SYSTEEM CONFIGURATIE ---
st.set_page_config(
    page_title="Rizz Architect Sovereign v6.2", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TRANSLATIONS & INTELLIGENCE DATA ---
translations = {
    "NL": {
        "header_main": "RIZZ<span>ARCHITECT</span>",
        "label_intake": "📥 TACTISCHE INTAKE",
        "label_pick": "🏆 ARCHITECT'S PICK",
        "label_dims": "📐 STRATEGISCHE DIMENSIES",
        "label_signals": "📡 SIGNALEN",
        "label_intel": "📖 MISSION BRIEFING",
        "ctx_ph": "Bijv: 18j, ontmoet in club, ze stuurt gemixte signalen...",
        "btn_execute": "🚀 START STRATEGISCHE SCAN",
        "success_rate": "SLAGINGSPERCENTAGE",
        "psych_title": "🧠 PSYCHOLOGISCHE ANALYSE",
        "idle_msg": "Systeem stand-by. Upload een screenshot om de dynamiek te ontleden.",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEEM HERSTARTEN",
        "intel_main_body": """
            **De Strategische Basis:**
            * **Frame Control:** Behoud de leiding. Wie de vragen stelt, bepaalt de richting van het gesprek.
            * **Value Retention:** Reageer nooit sneller of uitgebreider dan zij. Beheer je schaarste.
            * **The Hook:** Elk bericht moet een reden geven om te reageren, zonder wanhopig te lijken.
        """,
        "dark_intel_alert": """
            ### ⚠️ DARK OPS PROTOCOL
            **GEVAAR:** Je activeert nu tactieken die de emotionele staat van de ander direct beïnvloeden.
            
            * **Push-Pull Extremen:** Creëer intense pieken van interesse gevolgd door koude desinteresse.
            * **Pattern Interrupts:** Verbreek haar sociale verwachtingen op een verwarrende manier.
            * **Risk:** Dit kan leiden tot een volledige blokkade als het frame niet sterk genoeg is.
        """
    },
    "EN": {
        "header_main": "RIZZ<span>ARCHITECT</span>",
        "label_intake": "📥 TACTICAL INTAKE",
        "label_pick": "🏆 ARCHITECT'S PICK",
        "label_dims": "📐 STRATEGIC DIMENSIONS",
        "label_signals": "📡 SIGNALS",
        "label_intel": "📖 MISSION BRIEFING",
        "ctx_ph": "E.g.: 18yo, met at club, mixed signals...",
        "btn_execute": "🚀 START STRATEGISCHE SCAN",
        "success_rate": "SUCCESS PROBABILITY",
        "psych_title": "🧠 PSYCHOLOGICAL ANALYSIS",
        "idle_msg": "System stand-by. Upload data to begin.",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 REBOOT SYSTEM",
        "intel_main_body": "Core strategic principles...",
        "dark_intel_alert": "Danger: Dark Ops active..."
    }
}

# --- 3. PREMIUM CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; }
    
    /* Branding */
    .header-box { text-align: center; padding: 30px 0; margin-bottom: 20px; }
    .logo { font-family: 'Playfair Display', serif; font-size: 2.8rem; color: #ffffff !important; letter-spacing: -1px; }
    .logo span { color: #fcd34d !important; text-shadow: 0 0 30px rgba(252, 211, 77, 0.4); }

    .section-tag { font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.75rem; letter-spacing: 2px; margin-bottom: 15px; display: block; opacity: 0.8; }

    /* Architect's Pick Card */
    .pick-card { 
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); 
        border: 2px solid #fcd34d; border-radius: 20px; padding: 35px; position: relative; 
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5); 
    }
    .pick-badge { position: absolute; top: -16px; left: 30px; background: #fcd34d; color: #010409; font-family: 'JetBrains Mono', monospace; font-weight: 900; font-size: 0.8rem; padding: 4px 18px; border-radius: 8px; }

    /* Intelligence Boxes */
    .briefing-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 211, 77, 0.1);
        border-radius: 12px;
        padding: 20px;
        font-size: 0.85rem;
        line-height: 1.6;
        margin-top: 10px;
    }

    .dark-alert-box {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid #f87171;
        border-radius: 12px;
        padding: 20px;
        color: #f87171;
        margin-top: 15px;
        animation: border-glow 2s infinite;
    }
    
    @keyframes border-glow {
        0% { box-shadow: 0 0 5px rgba(248, 113, 113, 0.2); }
        50% { box-shadow: 0 0 20px rgba(248, 113, 113, 0.4); }
        100% { box-shadow: 0 0 5px rgba(248, 113, 113, 0.2); }
    }

    /* Buttons */
    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 800; border-radius: 12px; height: 3.8rem; border: none !important; font-size: 1.1rem; width: 100%;
    }
    
    /* Input Styling */
    .stTextArea textarea { background-color: #0d1117 !important; border: 1px solid rgba(255,255,255,0.1) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CORE ENGINE FUNCTIONS ---
def get_b64(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

def run_architect_scan(client, b64, ctx, lang, dark):
    mode = "AGGRESSIVE DARK PSYCHOLOGY" if dark else "STANDARD HIGH-VALUE"
    sys_p = f"Role: Sovereign Architect. Mode: {mode}. Language: {lang}. Return JSON only."
    
    res = client.chat.completions.create(
        model="grok-4.20-0309-non-reasoning",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": sys_p},
            {"role": "user", "content": [
                {"type": "text", "text": f"Context: {ctx}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]}
        ]
    )
    return json.loads(res.choices[0].message.content)

# --- 5. UI LAYOUT ---
if 'data' not in st.session_state: st.session_state.data = None

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM SETTINGS")
    l_key = st.radio("Language", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    is_dark = st.toggle(t["dark_mode"], key="dark_toggle")
    if st.button(t["reboot"]):
        st.session_state.clear()
        st.rerun()

# Header
st.markdown(f'<div class="header-box"><div class="logo">{t["header_main"]}</div></div>', unsafe_allow_html=True)

if not api:
    st.info("🔐 Systeem in stand-by. Voer je API key in.")
else:
    c_left, c_right = st.columns([1, 1.3], gap="large")

    with c_left:
        # Input Sectie
        st.markdown(f"<span class='section-tag'>{t['label_intake']}</span>", unsafe_allow_html=True)
        file = st.file_uploader("Upload", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if file:
            st.image(file, use_container_width=True)
            u_ctx = st.text_area("Context Intelligence", placeholder=t["ctx_ph"], height=80)
            if st.button(t["btn_execute"]):
                with st.spinner("Decoding social battlefield..."):
                    try:
                        client = OpenAI(api_key=api, base_url="https://api.x.ai/v1")
                        st.session_state.data = run_architect_scan(client, get_b64(file), u_ctx, l_key, is_dark)
                        st.rerun()
                    except Exception as e: st.error(f"Scan Error: {e}")
        
        # --- BRIEFING & ALERTS (Hier gebeurt de magie) ---
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<span class='section-tag'>{t['label_intel']}</span>", unsafe_allow_html=True)
        
        # Vast paneel met de algemene briefing
        st.markdown(f"<div class='briefing-box'>{t['intel_main_body']}</div>", unsafe_allow_html=True)
        
        # Apart paneel dat alleen bij Dark Mode verschijnt
        if is_dark:
            st.markdown(f"<div class='dark-alert-box'>{t['dark_intel_alert']}</div>", unsafe_allow_html=True)

    with c_right:
        if st.session_state.data:
            d = st.session_state.data
            st.markdown(f"<span class='section-tag'>{t['success_rate']}</span>", unsafe_allow_html=True)
            st.progress(d.get('success_rate', 50) / 100)
            
            # Architect's Pick
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
            
            # Additional Signals
            st.markdown("<br>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"<span class='section-tag'>✅ POSITIEF</span>", unsafe_allow_html=True)
                for gf in d.get('green_flags', []): st.markdown(f"<div style='color:#4ade80; font-size:0.8rem; margin-bottom:5px;'>• {gf}</div>", unsafe_allow_html=True)
            with sc2:
                st.markdown(f"<span class='section-tag'>🚩 RISICO'S</span>", unsafe_allow_html=True)
                for rf in d.get('red_flags', []): st.markdown(f"<div style='color:#f87171; font-size:0.8rem; margin-bottom:5px;'>• {rf}</div>", unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# --- 6. FOOTER ---
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN v6.2 | DUAL LAYER INTELLIGENCE ACTIVE</div>", unsafe_allow_html=True)
