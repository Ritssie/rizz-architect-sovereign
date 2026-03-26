import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import time

# --- 1. CORE CONFIGURATION ---
st.set_page_config(
    page_title="Rizz Architect Sovereign", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL TRANSLATION TABLE ---
translations = {
    "NL": {
        "header_1": "TACTISCHE INTAKE",
        "header_2": "ARCHITECT'S PICK",
        "header_3": "STRATEGIC DIMENSIONS",
        "header_4": "SIGNAL ANALYSIS",
        "context_ph": "Leeftijd, vibe, eerdere interacties...",
        "btn_execute": "⚡ EXECUTE STRATEGY",
        "success_label": "SUCCESS PROBABILITY",
        "psych_label": "🧠 PSYCHOLOGIE & LOGICA",
        "idle_msg": "Systeem stand-by. Upload tactical data.",
        "dark_mode_label": "Dark Psychology Mode",
        "platform_label": "PLATFORM SELECTIE",
        "reboot_btn": "VOLLEDIGE SYSTEEM REBOOT"
    },
    "EN": {
        "header_1": "TACTICAL INTAKE",
        "header_2": "ARCHITECT'S PICK",
        "header_3": "STRATEGIC DIMENSIONS",
        "header_4": "SIGNAL ANALYSIS",
        "context_ph": "Age, vibe, previous interactions...",
        "btn_execute": "⚡ EXECUTE STRATEGY",
        "success_label": "SUCCESS PROBABILITY",
        "psych_label": "🧠 PSYCHOLOGY & LOGIC",
        "idle_msg": "System stand-by. Waiting for data.",
        "dark_mode_label": "Dark Psychology Mode",
        "platform_label": "PLATFORM SELECTION",
        "reboot_btn": "FULL SYSTEM REBOOT"
    }
}

# --- 3. ADVANCED CSS ENGINE (VIBE & STABILITY) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    /* Base Theme Override */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #010409 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* Animated Header */
    .main-header {
        text-align: center;
        padding: 30px 0;
        border-bottom: 1px solid rgba(252, 211, 77, 0.1);
        margin-bottom: 30px;
        background: linear-gradient(to right, transparent, rgba(252, 211, 77, 0.05), transparent);
    }
    .logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: #ffffff !important;
        letter-spacing: -1px;
    }
    .logo-text span {
        color: #fcd34d !important;
        text-shadow: 0 0 15px rgba(252, 211, 77, 0.3);
    }

    /* Section Labels */
    .label-tag {
        font-family: 'JetBrains Mono', monospace;
        color: #fcd34d;
        font-size: 0.7rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 25px 0 12px 0;
        display: flex;
        align-items: center;
    }
    .label-tag::after {
        content: "";
        flex: 1;
        height: 1px;
        background: rgba(252, 211, 77, 0.2);
        margin-left: 15px;
    }
    
    /* Architect's Pick - Screenshot Style */
    .pick-card {
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 60%);
        border: 2px solid #fcd34d;
        border-radius: 16px;
        padding: 30px;
        position: relative;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        transition: transform 0.3s ease;
    }
    .pick-card:hover { transform: scale(1.01); }
    
    .pick-badge {
        position: absolute;
        top: -15px;
        left: 30px;
        background: #fcd34d;
        color: #010409;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 0.8rem;
        padding: 4px 16px;
        border-radius: 6px;
        letter-spacing: 1px;
    }
    
    /* Psychology & Logic Box */
    .psych-box {
        background: rgba(252, 211, 77, 0.03);
        border-radius: 12px;
        padding: 20px;
        border-left: 3px solid #fcd34d;
        margin-top: 20px;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #cbd5e1;
    }
    
    /* Dimension Cards */
    .dim-box {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        transition: all 0.2s ease;
    }
    .dim-box:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(252, 211, 77, 0.4);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid rgba(255,255,255,0.05); }
    
    /* Buttons */
    .stButton>button {
        background: #fcd34d !important;
        color: #010409 !important;
        font-weight: 900;
        border-radius: 10px;
        height: 3.5rem;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CORE ENGINE FUNCTIONS ---
def process_image(file):
    """Resizes and encodes image to base64 for vision model."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((1000, 1000))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=90)
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Image Error: {e}")
        return None

def trigger_analysis(client, b64_img, ctx, platform, lang, dark_mode):
    """Main API call logic with specialized prompting."""
    mode_instruction = "Focus on high-status, playful, and charming moves."
    if dark_mode:
        mode_instruction = "Use advanced persuasion, frame control, and push-pull dynamics. Be bold."

    sys_prompt = f"""
    You are the Sovereign Rizz Architect. 
    Platform: {platform}. Language: {lang}. 
    Instruction: {mode_instruction}
    
    Analyze the chat screenshot and return a JSON object:
    {{
      "success_rate": int,
      "green_flags": [str, str],
      "red_flags": [str, str],
      "psychology": "Explain the social pressure, frame control, or subtext here.",
      "options": [
        {{"type": "😏 Bold Play", "zin": "text"}},
        {{"type": "🎯 Direct Value", "zin": "text"}},
        {{"type": "🃏 Chaos/Pattern Interrupt", "zin": "text"}}
      ],
      "winner_idx": 0
    }}
    """
    
    response = client.chat.completions.create(
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
    return json.loads(response.choices[0].message.content)

# --- 5. INTERFACE ASSEMBLY ---
if 'master_state' not in st.session_state:
    st.session_state.master_state = None

# Sidebar Content
with st.sidebar:
    st.markdown("### ⚡ SOVEREIGN CONTROL")
    lang_key = st.radio("Systeem Taal", ["NL", "EN"], horizontal=True)
    t = translations[lang_key]
    
    api_key = st.text_input("Grok API Key", type="password")
    plat = st.selectbox(t["platform_label"], ["Tinder", "WhatsApp", "Instagram", "Hinge"])
    
    st.markdown("---")
    dark_mode = st.toggle(t["dark_mode_label"], value=False)
    
    if st.button(t["reboot_btn"]):
        st.session_state.clear()
        st.rerun()

# Branding Header
st.markdown(f'<div class="main-header"><div class="logo-text">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# Main Application Logic
if not api_key:
    st.info("⚡ Voer je API key in om het Sovereign systeem te initialiseren.")
else:
    left_col, right_col = st.columns([1, 1.5], gap="large")
    
    with left_col:
        st.markdown(f"<div class='label-tag'>{t['header_1']}</div>", unsafe_allow_html=True)
        img_upload = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if img_upload:
            st.image(img_upload, use_container_width=True)
            u_context = st.text_area("Field Intelligence", placeholder=t["context_ph"], height=100)
            
            if st.button(t["btn_execute"]):
                with st.spinner("Synchronizing Trajectories..."):
                    try:
                        ai_client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                        encoded_img = process_image(img_upload)
                        if encoded_img:
                            st.session_state.master_state = trigger_analysis(
                                ai_client, encoded_img, u_context, plat, lang_key, dark_mode
                            )
                            st.rerun()
                    except Exception as e:
                        st.error(f"Execution Error: {str(e)}")

    with right_col:
        if st.session_state.master_state and isinstance(st.session_state.master_state, dict):
            data = st.session_state.master_state
            
            # Probability Bar
            st.markdown(f"<div class='label-tag'>{t['success_label']}</div>", unsafe_allow_html=True)
            st.progress(data.get('success_rate', 50) / 100)
            
            # Flags Row
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                for gf in data.get('green_flags', []): 
                    st.markdown(f"<div class='flag-pill green-pill'>✅ {gf}</div>", unsafe_allow_html=True)
            with f_col2:
                for rf in data.get('red_flags', []): 
                    st.markdown(f"<div class='flag-pill red-pill'>🚩 {rf}</div>", unsafe_allow_html=True)

            # Architect's Choice
            st.markdown(f"<div class='label-tag'>{t['header_2']}</div>", unsafe_allow_html=True)
            win_idx = data.get('winner_idx', 0)
            best_move = data['options'][win_idx]
            
            st.markdown(f"""
                <div class="pick-card">
                    <div class="pick-badge">OPTIMIZED PATHWAY</div>
                    <div class="dim-header" style="color:#fcd34d;">{best_move.get('type')}</div>
            """, unsafe_allow_html=True)
            st.code(best_move.get('zin'), language=None)
            st.markdown(f"""
                    <div class="psych-box">
                        <b>{t['psych_label']}:</b><br>{data.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Remaining Dimensions
            st.markdown(f"<div class='label-tag'>{t['header_3']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(data['options']):
                if i != win_idx:
                    st.markdown(f"""
                        <div class="dim-box">
                            <div class="dim-header">{opt.get('type')}</div>
                    """, unsafe_allow_html=True)
                    st.code(opt.get('zin'), language=None)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# --- 6. SYSTEM FOOTER ---
st.markdown("<br><br><div style='text-align:center; opacity:0.2; font-size:0.7rem; border-top: 1px solid rgba(255,255,255,0.05); padding-top:20px;'>CORE VERSION 5.6.2 | STABILITY MODE ACTIVE</div>", unsafe_allow_html=True)
