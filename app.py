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
    page_title="Rizz Architect Ultra 3.0", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. SOVEREIGN UI ENGINE (Custom CSS) ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
        color: #E0E0E0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Brand Header */
    .header-container { text-align: center; padding: 2rem 0; }
    .main-title { 
        font-weight: 900; font-size: 3rem; letter-spacing: -2px; 
        background: linear-gradient(135deg, #fff 30%, #555 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-family: 'JetBrains Mono'; color: #FFD700; font-size: 0.8rem; letter-spacing: 5px; text-transform: uppercase; }

    /* The Gauge (Authentic Look) */
    .gauge-wrapper {
        position: relative; width: 200px; height: 100px; margin: 0 auto;
        overflow: hidden; text-align: center;
    }
    .gauge-body {
        width: 200px; height: 200px; border-radius: 50%;
        background: conic-gradient(from 270deg, #ff4b4b 0%, #ffeb3b 50%, #00e676 100%);
        mask: radial-gradient(circle, transparent 65%, black 66%);
        -webkit-mask: radial-gradient(circle, transparent 65%, black 66%);
    }
    .gauge-needle {
        position: absolute; bottom: 0; left: 50%; width: 4px; height: 80px;
        background: white; border-radius: 2px; transform-origin: bottom center;
        transition: transform 1.5s cubic-bezier(0.17, 0.67, 0.83, 0.67);
    }
    .gauge-value { font-family: 'JetBrains Mono'; font-size: 1.5rem; font-weight: 700; margin-top: 10px; color: white; }

    /* Tactical Cards */
    .tactical-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; transition: 0.3s;
    }
    .tactical-card:hover { border-color: #FFD700; background: rgba(255, 215, 0, 0.02); }
    .card-label { font-family: 'JetBrains Mono'; color: #FFD700; font-size: 0.7rem; margin-bottom: 0.5rem; }
    
    /* Winning Move Styling */
    .winner-highlight { border: 2px solid #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.15); }

    /* Button Styling */
    .stButton>button {
        width: 100%; background: white !important; color: black !important;
        font-weight: 700; border: none; border-radius: 8px; padding: 0.6rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. ANALYSE LOGICA ---
# ==============================================================================
def encode_image(file):
    img = Image.open(file).convert('RGB')
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()

def call_grok_architect(api_key, b64_image, context):
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Gebruik van het gevraagde reasoning model voor diepe psychologische analyse
    model_name = "grok-4-1-fast-reasoning"
    
    system_prompt = """
    Role: Rizz Architect Ultra 3.0 (Strategic Mastermind)
    Goal: Analyseer screenshots voor sociaal overwicht en leid naar een date.
    
    Protocol:
    1. Analyseer platform, investment (wie typt meer?), en subtext.
    2. Genereer 3 specifieke tekstopties: 
       - Playful Provocateur (plagen/spanning)
       - Elegant Direct (zelfverzekerd/date-gericht)
       - Pattern Interrupt (onverwacht/intellectueel)
    3. Kies de 'Architect's Verdict' (beste optie).
    4. Schat een success_rate (0-100) op basis van de huidige flow.

    JSON Output format:
    {
      "success_rate": int,
      "platform": "string",
      "investment_analysis": "string",
      "options": [
        {"type": "Playful Provocateur", "text": "string"},
        {"type": "Elegant Direct", "text": "string"},
        {"type": "Pattern Interrupt", "text": "string"}
      ],
      "verdict_idx": int,
      "psychology_reasoning": "string"
    }
    """

    try:
        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {context}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Architect Error: {e}")
        return None

# ==============================================================================
# --- 4. DE INTERFACE ---
# ==============================================================================
st.markdown('<div class="header-container"><div class="sub-title">Sovereign Systems</div><div class="main-title">RIZZ ARCHITECT 3.0</div></div>', unsafe_allow_html=True)

# Sidebar voor API Key en Reset
with st.sidebar:
    api_key = st.text_input("Grok API Key", type="password")
    if st.button("System Reset"):
        st.session_state.clear()
        st.rerun()

col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.markdown('<p style="font-family:\'JetBrains Mono\'; color:#FFD700; font-size:0.8rem;">📥 INPUT DATA SOURCE</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    context = st.text_area("Extra Context (Optioneel)", placeholder="Bijv: 'We hebben 2 dagen niet gesproken' of 'Ze lacht om al mijn grappen'", height=100)
    
    if st.button("EXECUTE ANALYSIS") and uploaded_file and api_key:
        with st.spinner("Decoding social signals..."):
            img_b64 = encode_image(uploaded_file)
            result = call_grok_architect(api_key, img_b64, context)
            if result:
                st.session_state.analysis = result

with col_output:
    if 'analysis' in st.session_state:
        data = st.session_state.analysis
        
        # --- SUCCESS GAUGE ---
        st.markdown('<p style="font-family:\'JetBrains Mono\'; color:#FFD700; font-size:0.8rem; text-align:center;">PROBABILITY OF SUCCESS</p>', unsafe_allow_html=True)
        
        # De Gauge Animatie
        rate = data['success_rate']
        # Berekening van rotatie: 0% = -90deg, 100% = 90deg
        rotation = (rate * 1.8) - 90
        
        st.markdown(f"""
            <div class="gauge-wrapper">
                <div class="gauge-body"></div>
                <div class="gauge-needle" style="transform: translateX(-50%) rotate({rotation}deg);"></div>
                <div class="gauge-value">{rate}%</div>
            </div>
        """, unsafe_allow_html=True)

        # --- OPTIONS ---
        st.markdown('<p style="font-family:\'JetBrains Mono\'; color:#FFD700; font-size:0.8rem; margin-top:2rem;">STRATEGIC DIMENSIONS</p>', unsafe_allow_html=True)
        
        for i, opt in enumerate(data['options']):
            is_winner = (i == data['verdict_idx'])
            winner_class = "winner-highlight" if is_winner else ""
            winner_label = " 🏆 ARCHITECT'S CHOICE" if is_winner else ""
            
            st.markdown(f"""
                <div class="tactical-card {winner_class}">
                    <div class="card-label">{opt['type'].upper()}{winner_label}</div>
                    <div style="font-size:1.1rem; font-weight:600; color:white;">"{opt['text']}"</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(opt['text'], language=None)

        # --- VERDICT / REASONING ---
        st.markdown('<p style="font-family:\'JetBrains Mono\'; color:#FFD700; font-size:0.8rem; margin-top:1rem;">THE ARCHITECT\'S VERDICT</p>', unsafe_allow_html=True)
        st.info(data['psychology_reasoning'])
    else:
        st.markdown('<div style="text-align:center; padding-top:100px; opacity:0.3;">Systeem stand-by. Wachten op data input...</div>', unsafe_allow_html=True)
