import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import logging

# ==============================================================================
# --- 1. SYSTEEM CONFIGURATIE & ERROR LOGGING ---
# ==============================================================================
# We stellen logging in om eventuele dieperliggende fouten te vangen zonder de app te laten crashen.
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Rizz Architect Ultra 3.0 | Sovereign Systems",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiseer de session state voor persistentie van data
if 'analysis' not in st.session_state:
    st.session_state.analysis = None
if 'last_upload' not in st.session_state:
    st.session_state.last_upload = None

# ==============================================================================
# --- 2. SOVEREIGN UI ENGINE (GEAVANCEERDE CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Universe */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #010204 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Top Branding */
    .brand-container { text-align: center; padding: 50px 0 20px 0; }
    .main-title { 
        font-weight: 900; font-size: 3.5rem; letter-spacing: -3px; 
        background: linear-gradient(180deg, #FFFFFF 0%, #444444 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-tag { 
        font-family: 'JetBrains Mono'; color: #fcd34d; font-size: 0.7rem; 
        letter-spacing: 6px; text-transform: uppercase; opacity: 0.8;
    }

    /* Gauge & Probability Meter */
    .gauge-box { position: relative; width: 240px; height: 120px; margin: 0 auto 30px auto; overflow: hidden; }
    .gauge-arc {
        width: 240px; height: 240px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ef4444 0%, #facc15 50%, #22c55e 100%);
        mask: radial-gradient(circle, transparent 69%, black 70%);
        -webkit-mask: radial-gradient(circle, transparent 69%, black 70%);
    }
    .gauge-needle {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 95px;
        background: #fff; border-radius: 4px; transform-origin: bottom center;
        transition: transform 2s cubic-bezier(0.22, 1, 0.36, 1);
        box-shadow: 0 0 15px rgba(255,255,255,0.3);
    }
    .gauge-text { text-align: center; font-family: 'JetBrains Mono'; font-weight: 800; font-size: 1.4rem; color: #fff; margin-top: -15px; }

    /* Tactical Components: Flags */
    .flag-deck { display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }
    .status-pill {
        padding: 6px 15px; border-radius: 5px; font-family: 'JetBrains Mono';
        font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .green-zone { background: rgba(34, 197, 94, 0.1); color: #4ade80; border-color: rgba(74, 222, 128, 0.2); }
    .red-zone { background: rgba(239, 68, 68, 0.1); color: #f87171; border-color: rgba(248, 113, 113, 0.2); }

    /* The Tactical Cards */
    .strat-card {
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 15px; padding: 25px; margin-bottom: 20px; transition: 0.4s;
    }
    .strat-card:hover { border-color: #fcd34d; background: rgba(252, 211, 77, 0.02); }
    .winner-glow { border: 1px solid #fcd34d !important; box-shadow: 0 0 30px rgba(252, 211, 77, 0.1); }
    
    .label-meta { font-family: 'JetBrains Mono'; font-size: 0.6rem; color: #fcd34d; letter-spacing: 2px; margin-bottom: 10px; }
    .message-text { font-size: 1.25rem; font-weight: 700; color: #fff; line-height: 1.4; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }

    /* Buttons */
    .stButton>button {
        background: #fff !important; color: #000 !important; font-weight: 900 !important;
        border-radius: 10px !important; height: 3.5rem !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. CORE ANALYTICAL ENGINE ---
# ==============================================================================

def encode_source_image(uploaded_file):
    """Verwerkt de afbeelding veilig naar base64 voor de API."""
    try:
        img = Image.open(uploaded_file).convert('RGB')
        # Optimalisatie: Verklein voor snelheid en kosten
        img.thumbnail((1200, 1200))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        st.error(f"Media Error: {e}")
        return None

def call_grok_architect(api_key, b64_img, ctx):
    """Interface met de Grok-4-1-fast-reasoning engine."""
    # Belangrijk: Geen speciale karakters in de system_prompt variabelen!
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # We gebruiken een strikt ASCII-veilige prompt om de encoder error te voorkomen
    system_role = (
        "Role: Rizz Architect Ultra 3.0. "
        "Focus: Strategic dating analysis and psychological dominance. "
        "Task: Analyze the screenshot. Evaluate investment, flow, and subtext. "
        "Response: Provide three response options: Playful Provocateur, Elegant Direct, Pattern Interrupt. "
        "Health Check: Identify Green Flags and Red Flags for the user's social health. "
        "Output Format: Return JSON only. Fields: success_rate (int), green_flags (list), "
        "red_flags (list), options (list of {type, text}), verdict_idx (int), reasoning (str)."
    )

    try:
        completion = client.chat.completions.create(
            model="grok-4-1-fast-reasoning", # De reasoning engine voor diepere analyse
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {ctx}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ],
            temperature=0.8
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        logging.error(f"API Failure: {e}")
        st.error("Systeemfout: De Architect kon de data niet decoderen. Controleer je API key.")
        return None

# ==============================================================================
# --- 4. INTERFACE ASSEMBLY (STABLE BUILD) ---
# ==============================================================================

# Branding Section
st.markdown("""
    <div class="brand-container">
        <div class="main-title">RIZZ ARCHITECT</div>
        <div class="sub-tag">Ultra 3.0 // Tactical Intelligence</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Layout
with st.sidebar:
    st.markdown("### 🛠️ SYSTEM CONFIG")
    api_key_vault = st.text_input("Grok Access Key", type="password", help="Input your xAI API key here.")
    st.markdown("---")
    
    st.markdown("**MISSION STATUS:**")
    if api_key_vault:
        st.success("ENGINE ONLINE")
    else:
        st.info("AWAITING AUTH")
        
    st.markdown("---")
    if st.button("🔄 FULL SYSTEM REBOOT"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.caption("v19.1 Stable | No Data Persistence")

# Main Dashboard
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown("#### 📥 MISSION INTAKE")
    source_file = st.file_uploader("Upload Data Source", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if source_file:
        st.image(source_file, use_container_width=True, caption="Tactical Source")
        
    briefing = st.text_area("CONTEXT BRIEFING", placeholder="Bijv: 'We praten nu een week, ze reageert enthousiast maar we hebben nog geen date.'", height=120)
    
    if st.button("EXECUTE PRECISION SCAN"):
        if not api_key_vault:
            st.warning("Grendel geblokkeerd: Voer API key in.")
        elif not source_file:
            st.warning("Data ontbreekt: Upload een screenshot.")
        else:
            with st.spinner("Decoding social dynamics..."):
                encoded_img = encode_source_image(source_file)
                if encoded_img:
                    data = call_grok_architect(api_key_vault, encoded_img, briefing)
                    if data:
                        st.session_state.analysis = data
                        st.rerun()

with col_right:
    st.markdown("#### 📡 ARCHITECT'S OUTPUT")
    
    if st.session_state.analysis:
        res = st.session_state.analysis
        
        # --- SUCCESS GAUGE ---
        rate = res.get('success_rate', 50)
        needle_rot = (rate * 1.8) - 90
        
        st.markdown(f"""
            <div class="gauge-box">
                <div class="gauge-arc"></div>
                <div class="gauge-needle" style="transform: translateX(-50%) rotate({needle_rot}deg);"></div>
            </div>
            <div class="gauge-text">{rate}% CHANCE</div>
        """, unsafe_allow_html=True)

        # --- SOCIAL HEALTH (FLAGS) ---
        st.markdown("<br><b>SOCIAL HEALTH CHECK:</b>", unsafe_allow_html=True)
        st.markdown('<div class="flag-deck">', unsafe_allow_html=True)
        for gf in res.get('green_flags', []):
            st.markdown(f'<div class="status-pill green-zone">✔ {gf}</div>', unsafe_allow_html=True)
        for rf in res.get('red_flags', []):
            st.markdown(f'<div class="status-pill red-zone">✘ {rf}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- TACTICAL OPTIONS ---
        st.markdown("<br><b>TACTICAL DIMENSIONS:</b>", unsafe_allow_html=True)
        options = res.get('options', [])
        best_move = res.get('verdict_idx', 0)
        
        for i, opt in enumerate(options):
            is_best = (i == best_move)
            card_class = "strat-card winner-glow" if is_best else "strat-card"
            meta_label = "🏆 OPTIMAL TRAJECTORY" if is_best else opt['type'].upper()
            
            st.markdown(f"""
                <div class="{card_class}">
                    <div class="label-meta">{meta_label}</div>
                    <div class="message-text">"{opt['text']}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(opt['text'], language=None)

        # --- PSYCHOLOGICAL REASONING ---
        st.markdown("<br><b>THE ARCHITECT'S VERDICT:</b>", unsafe_allow_html=True)
        st.info(res.get('reasoning', 'Analyse voltooid.'))
        
    else:
        st.markdown("""
            <div style="height:400px; display:flex; align-items:center; justify-content:center; border:1px dashed #333; border-radius:20px; opacity:0.3;">
                <p>Waiting for data source injection...</p>
            </div>
        """, unsafe_allow_html=True)

# Footer Maintenance
st.markdown("<br><hr><div style='text-align:center; opacity:0.2; font-size:0.7rem; font-family:\"JetBrains Mono\";'>SYSTEM-V19.1-STABLE // NO_LOG_PROTOCOL_ACTIVE</div>", unsafe_allow_html=True)
