import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json

# --- 1. SYSTEEM CONFIGURATIE ---
st.set_page_config(
    page_title="Rizz Architect Sovereign v6.0", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. TRANSLATIONS & EMOJI MAPPING ---
translations = {
    "NL": {
        "header_main": "RIZZ<span>ARCHITECT</span>",
        "label_intake": "📥 TACTISCHE INTAKE",
        "label_pick": "🏆 ARCHITECT'S PICK",
        "label_dims": "📐 STRATEGISCHE DIMENSIES",
        "label_signals": "📡 SIGNALEN",
        "label_intel": "📖 MISSION BRIEFING",
        "ctx_ph": "Context: Leeftijd, vibe, laatste interactie...",
        "btn_execute": "🚀 START SCAN",
        "success_rate": "SLAGINGSPERCENTAGE",
        "psych_title": "🧠 PSYCHOLOGISCHE ANALYSE",
        "idle_msg": "Wachten op data... Upload een screenshot om te beginnen.",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEEM HERSTARTEN",
        "console_msg": "SYSTEEM STATUS: ONLINE",
        "intel_summary": "Klik voor strategische basisprincipes",
        "intel_body": """
            ### 🏛️ De Fundamenten
            * **Frame Control:** Wie leidt de dans? We buigen het frame terug naar jou.
            * **Value Balancing:** Zorg dat jouw 'waarde' in het gesprek altijd hoog blijft.
            
            ### 🔍 De 3 Dimensies
            1.  **Playful (Speels):** Spanning opbouwen zonder serieus te worden.
            2.  **Direct (Krachtig):** Heldere intentie tonen en de leiding nemen.
            3.  **Pattern Interrupt:** Haar uit haar routine halen met iets onverwachts.
        """
    },
    "EN": {
        "header_main": "RIZZ<span>ARCHITECT</span>",
        "label_intake": "📥 TACTICAL INTAKE",
        "label_pick": "🏆 ARCHITECT'S PICK",
        "label_dims": "📐 STRATEGIC DIMENSIONS",
        "label_signals": "📡 SIGNALS",
        "label_intel": "📖 MISSION BRIEFING",
        "ctx_ph": "Context: Age, vibe, last interaction...",
        "btn_execute": "🚀 START SCAN",
        "success_rate": "SUCCESS PROBABILITY",
        "psych_title": "🧠 PSYCHOLOGICAL ANALYSIS",
        "idle_msg": "Waiting for data... Upload a screenshot to begin.",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 REBOOT SYSTEM",
        "console_msg": "SYSTEM STATUS: OPERATIONAL",
        "intel_summary": "Click for strategic principles",
        "intel_body": "Strategic briefing content..."
    }
}

# --- 3. PREMIUM CSS ENGINE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; 
        color: #e2e8f0 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* Branding */
    .header-box { text-align: center; padding: 40px 0; margin-bottom: 20px; }
    .logo { font-family: 'Playfair Display', serif; font-size: 2.8rem; color: #ffffff !important; letter-spacing: -1px; }
    .logo span { color: #fcd34d !important; text-shadow: 0 0 30px rgba(252, 211, 77, 0.4); }

    /* Tags & Labels */
    .section-tag { 
        font-family: 'JetBrains Mono', monospace; 
        color: #fcd34d; 
        font-size: 0.75rem; 
        letter-spacing: 2px; 
        margin-bottom: 15px; 
        display: block;
        opacity: 0.9;
    }

    /* Architect's Pick Card (Premium) */
    .pick-card { 
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.15) 0%, rgba(1, 4, 9, 1) 100%); 
        border: 2px solid #fcd34d; 
        border-radius: 20px; 
        padding: 35px; 
        position: relative; 
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    .pick-badge { 
        position: absolute; 
        top: -16px; 
        left: 30px; 
        background: #fcd34d; 
        color: #010409; 
        font-family: 'JetBrains Mono', monospace; 
        font-weight: 900; 
        font-size: 0.8rem; 
        padding: 4px 18px; 
        border-radius: 8px; 
    }

    /* Info Boxes */
    .info-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-top: 10px;
    }

    /* Flags */
    .flag-item { font-size: 0.85rem; padding: 8px 12px; border-radius: 8px; margin-bottom: 8px; background: rgba(255,255,255,0.02); }

    /* Button Styling */
    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; 
        font-weight: 800; 
        border-radius: 12px; 
        height: 3.8rem; 
        border: none !important;
        font-size: 1.1rem;
    }
    
    /* Clean Expanders */
    .stExpander { border: 1px solid rgba(252, 211, 77, 0.2) !important; background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ENGINE CORE ---
def prepare_vision_data(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

def analyze_conversation(client, b64_img, ctx, lang, dark):
    sys_prompt = f"""You are the Sovereign Architect. 
    Mode: {'DARK OPS' if dark else 'STANDARD'}. 
    Language: {lang}. 
    Analyze chat dynamics and return JSON only.
    Structure: {{
      "success": 0-100,
      "positives": [], "negatives": [],
      "logic": "Psychological breakdown.",
      "moves": [
        {{"type": "🎭 Playful", "zin": ""}},
        {{"type": "🎯 Direct", "zin": ""}},
        {{"type": "⚡ Pattern Break", "zin": ""}}
      ],
      "best_idx": 0
    }}"""
    
    res = client.chat.completions.create(
        model="grok-4.20-0309-non-reasoning",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": f"Context: {ctx}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
            ]}
        ]
    )
    return json.loads(res.choices[0].message.content)

# --- 5. UI ASSEMBLY ---
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
    st.markdown("### 🛠️ CONFIG")
    l_key = st.radio("Taal", ["NL", "EN"], horizontal=True)
    t = translations[l_key]
    api_val = st.text_input("Grok Key", type="password")
    st.markdown("---")
    is_dark = st.toggle(t["dark_mode"])
    if st.button(t["reboot"]):
        st.session_state.clear()
        st.rerun()

# Header
st.markdown(f'<div class="header-box"><div class="logo">{t["header_main"]}</div></div>', unsafe_allow_html=True)

if not api_val:
    st.info("🔐 Systeem vergrendeld. Voer API key in.")
else:
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown(f"<span class='section-tag'>{t['label_intake']}</span>", unsafe_allow_html=True)
        file = st.file_uploader("Screenshot", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if file:
            st.image(file, use_container_width=True)
            u_ctx = st.text_area("Context", placeholder=t["ctx_ph"], height=80, label_visibility="collapsed")
            if st.button(t["btn_execute"]):
                with st.spinner("Analyseert social cues..."):
                    try:
                        client = OpenAI(api_key=api_val, base_url="https://api.x.ai/v1")
                        b64 = prepare_vision_data(file)
                        st.session_state.state = analyze_conversation(client, b64, u_ctx, l_key, is_dark)
                        st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
        
        # UITLEG IN EXPANDER (Zorgt voor rust)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"✨ {t['label_intel']}", expanded=False):
            st.markdown(t['intel_body'])

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            
            # Probability
            st.markdown(f"<span class='section-tag'>{t['success_rate']}</span>", unsafe_allow_html=True)
            st.progress(s.get('success', 50) / 100)
            
            # Architect's Pick
            st.markdown(f"<span class='section-tag'>{t['label_pick']}</span>", unsafe_allow_html=True)
            best = s['moves'][s['best_idx']]
            st.markdown(f"""
                <div class="pick-card">
                    <div class="pick-badge">OPTIMIZED MOVE</div>
                    <div style="font-family:'JetBrains Mono'; color:#94a3b8; font-size:0.8rem; margin-bottom:10px;">{best['type']}</div>
            """, unsafe_allow_html=True)
            st.code(best['zin'], language=None)
            st.markdown(f"""
                    <div style="margin-top:20px; padding-top:15px; border-top:1px solid rgba(252,211,77,0.2); font-size:0.85rem; color:#fcd34d;">
                        <b>{t['psych_title']}:</b><br>{s.get('logic')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Signals & Others
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<span class='section-tag'>{t['label_signals']}</span>", unsafe_allow_html=True)
                for p in s.get('positives', []): st.markdown(f"<div class='flag-item' style='border-left:2px solid #4ade80;'>✅ {p}</div>", unsafe_allow_html=True)
                for n in s.get('negatives', []): st.markdown(f"<div class='flag-item' style='border-left:2px solid #f87171;'>🚩 {n}</div>", unsafe_allow_html=True)
            
            with c2:
                st.markdown(f"<span class='section-tag'>{t['label_dims']}</span>", unsafe_allow_html=True)
                for i, m in enumerate(s['moves']):
                    if i != s['best_idx']:
                        st.markdown(f"""
                            <div style="background:rgba(255,255,255,0.02); padding:10px; border-radius:10px; margin-bottom:10px; border:1px solid rgba(255,255,255,0.05);">
                                <div style="font-size:0.7rem; font-family:'JetBrains Mono'; opacity:0.6;">{m['type']}</div>
                                <div style="font-size:0.85rem; margin-top:5px;">{m['zin']}</div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# --- 6. FOOTER ---
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE v6.0.4 | PROTOTYPE BY AI</div>", unsafe_allow_html=True)
