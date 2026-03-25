import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import urllib.parse

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Rizz Architect Ultra 4.0", page_icon="⚡", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. GROK-4 NEON CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@700&family=Inter:wght@300;500;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }}
    
    .brand-banner {{ 
        display: flex; align-items: center; justify-content: center; gap: 20px; 
        padding: 20px 0; border-bottom: 2px solid rgba(252, 211, 77, 0.3); 
        margin-bottom: 25px; background: linear-gradient(180deg, rgba(252,211,77,0.05) 0%, rgba(0,0,0,1) 100%);
    }}
    
    .brand-logo {{ 
        width: 70px; height: 70px; border-radius: 15px; 
        border: 2px solid #fcd34d; box-shadow: 0 0 20px rgba(252, 211, 77, 0.4); 
    }}
    
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 800; color: #ffffff !important; letter-spacing: -1px; }}
    .logotype span {{ color: #fcd34d !important; text-shadow: 0 0 10px rgba(252, 211, 77, 0.5); }}

    .stButton>button {{ 
        width: 100%; background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #000000 !important; font-weight: 800; border-radius: 12px; border: none !important;
        transition: 0.3s; text-transform: uppercase; letter-spacing: 1px;
    }}
    .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 0 15px rgba(252, 211, 77, 0.4); }}

    .glass-card {{ 
        background: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(252, 211, 77, 0.2) !important; 
        border-radius: 20px; padding: 20px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
    }}
    
    .pick-container {{ 
        border-left: 5px solid #fcd34d; border-radius: 0 20px 20px 0; 
        padding: 25px; margin-top: 25px; background: rgba(252, 211, 77, 0.03); 
    }}
    
    .label-tag {{ 
        font-family: 'JetBrains Mono', monospace; color: #fcd34d !important; 
        font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{ color: #94a3b8 !important; }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{ color: #fcd34d !important; border-bottom-color: #fcd34d !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1000, 1000))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#fcd34d; text-align:center;'>QUANTUM ACCESS</h3>", unsafe_allow_html=True)
    user_api_key = st.text_input("GROK-4 API KEY", type="password")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    u_city = st.text_input("MY LOCATION", placeholder="Amsterdam")
    t_city = st.text_input("TARGET LOCATION", placeholder="Utrecht")
    if st.button("REBOOT CORE"):
        st.session_state.clear()
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN INTERFACE ---
if not user_api_key:
    st.warning("⚠️ Waiting for Grok-4 API Credentials...")
else:
    tab1, tab2 = st.tabs(["🔍 STRATEGIC SCAN", "🥊 SPARRING SIM"])

    with tab1:
        c1, c2 = st.columns([1, 1.4], gap="large")
        with c1:
            st.markdown("<div class='label-tag'>Tactical Intake</div>", unsafe_allow_html=True)
            u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            if u_file:
                st.image(u_file, use_container_width=True, caption="Visual Data Locked")
                context = st.text_area("Vibe Context", placeholder="Describe the current energy...")
                if st.button("⚡ INITIATE GROK-4 SCAN"):
                    with st.spinner("Decoding social dynamics..."):
                        try:
                            client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                            b64 = process_img(u_file)
                            
                            sys_msg = f"""
                            Identity: Rizz Architect Ultra 4.0.
                            Mission: Analyze {platform} screenshot in {u_city}/{t_city}.
                            Protocol: Triple-A (App, Atmosphere, Anomaly).
                            Laws: Max 20 words, Max 1 emoji, No clichés.
                            Output: STRICT JSON.
                            """

                            res = client.chat.completions.create(
                                model="grok-4.20-0309-non-reasoning", # JOUW SPECIFIEKE MODEL
                                response_format={"type": "json_object"},
                                messages=[
                                    {"role": "system", "content": sys_msg},
                                    {"role": "user", "content": [
                                        {"type": "text", "text": "Analyze target. Return JSON: weather, outfit, venues, options (3x: type, zin), architect_pick (choice int, reason)."},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                    ]}
                                ]
                            )
                            st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                            st.rerun()
                        except Exception as e: st.error(f"Grok-4 Error: {e}")

        with c2:
            if st.session_state.rizz_master:
                data = st.session_state.rizz_master
                st.markdown("<div class='label-tag'>Intelligence Report</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="glass-card">
                    <p style="margin:0;"><b>📍 Climate:</b> {data.get('weather')}</p>
                    <p style="margin:10px 0 0 0;"><b>🛡️ Recommended Armor:</b> {data.get('outfit')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                p = data.get('architect_pick', {})
                options = data.get('options', [])
                if options:
                    idx = max(0, min(int(p.get('choice', 1)) - 1, len(options)-1))
                    best = options[idx]
                    st.markdown(f"""
                        <div class="pick-container">
                            <div class='label-tag'>THE EXECUTIONER'S CHOICE</div>
                            <h1 style="margin:0; color:#ffffff; font-size:2rem; font-family:'Inter';">"{best.get('zin')}"</h1>
                            <div style="margin-top:20px; color:#fcd34d; font-size:0.9rem;">
                                <b>STRATEGY ({best.get('type')}):</b> {p.get('reason')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("System Idle. Upload tactical data to begin.")

    with tab2:
        st.markdown("<div class='label-tag'>Combat Simulator</div>", unsafe_allow_html=True)
        if not st.session_state.get('sim_active', False):
            if st.button("START NEURAL SIMULATION"):
                st.session_state.sim_active = True
                st.session_state.chat_history = [{"role": "assistant", "content": "Hey. What's on your mind?"}]
                st.rerun()
        else:
            for m in st.session_state.chat_history:
                with st.chat_message(m["role"]): st.markdown(m["content"])
            
            if pr := st.chat_input("Input command..."):
                st.session_state.chat_history.append({"role": "user", "content": pr})
                with st.chat_message("assistant"):
                    client = OpenAI(api_key=user_api_key, base_url="https://api.x.ai/v1")
                    r = client.chat.completions.create(
                        model="grok-4-1-fast-non-reasoning", # JOUW FAST MODEL
                        messages=[{"role":"system","content":"Dating sim. Challenge the user."}] + st.session_state.chat_history
                    )
                    rep = r.choices[0].message.content
                    st.markdown(rep)
                    st.session_state.chat_history.append({"role": "assistant", "content": rep})
            
            if st.button("TERMINATE SESSION"):
                st.session_state.sim_active = False
                st.session_state.chat_history = []
                st.rerun()
