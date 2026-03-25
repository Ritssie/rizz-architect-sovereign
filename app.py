import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import urllib.parse

# --- 1. CONFIG ---
st.set_page_config(page_title="Rizz Architect: Sovereign", page_icon="⚡", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except: return None

# Logo inladen (zorg dat dit bestand in je GitHub repo staat)
logo_b64 = get_base64("Gemini_Generated_Image_ch8eerch8eerch8e.jpg")
logo_img = f'<img src="data:image/jpeg;base64,{logo_b64}" class="brand-logo">' if logo_b64 else '<div class="brand-logo-fallback">⚡</div>'

# --- 2. CSS (Huisstijl op basis van logo) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&family=Playfair+Display:wght@700&display=swap');
    
    .stApp {{ background-color: #010409; color: #e2e8f0; font-family: 'Space Grotesk', sans-serif; }}
    
    .brand-banner {{ display: flex; align-items: center; justify-content: center; gap: 25px; padding: 40px 0; border-bottom: 1px solid rgba(252, 211, 77, 0.1); }}
    .brand-logo {{ width: 90px; height: 90px; border-radius: 20px; border: 2px solid #fcd34d; box-shadow: 0 0 30px rgba(252, 211, 77, 0.25); }}
    .logotype {{ font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 700; }}
    .logotype span {{ color: #fcd34d; }}

    .glass-card {{ background: rgba(13, 17, 23, 0.8); border: 1px solid rgba(252, 211, 77, 0.1); border-radius: 15px; padding: 20px; margin-bottom: 20px; }}
    .label-tag {{ font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 10px; display: block; }}
    
    .stButton>button {{ width: 100%; background: #fcd34d; color: #010409; font-weight: 800; border-radius: 12px; padding: 18px; transition: 0.3s; border: none; }}
    .stButton>button:hover {{ box-shadow: 0 0 40px rgba(252, 211, 77, 0.5); transform: translateY(-2px); }}
    
    .pick-container {{ 
        background: linear-gradient(135deg, rgba(252, 211, 77, 0.15), #010409); 
        border: 2px solid #fcd34d; border-radius: 20px; padding: 35px; margin-top: 25px; 
        box-shadow: 0 15px 50px rgba(0,0,0,0.5);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1100, 1100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

if 'rizz_master' not in st.session_state: st.session_state.rizz_master = None

# --- 4. SIDEBAR (The Command Center) ---
with st.sidebar:
    st.markdown(f'<div style="text-align:center; margin-bottom:20px;">{logo_img}</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#fcd34d; text-align:center;'>SYSTEM ACCESS</h3>", unsafe_allow_html=True)
    
    # Hier vul je de key in
    user_api_key = st.text_input("OPENAI API KEY", type="password", help="Je key wordt niet opgeslagen op de server.")
    
    st.markdown("---")
    platform = st.selectbox("PLATFORM", ["Hinge", "Tinder", "Instagram", "WhatsApp", "Bumble", "Real Life"])
    
    st.markdown("<div class='label-tag'>Logistiek</div>", unsafe_allow_html=True)
    u_city = st.text_input("JOUW STAD", placeholder="Bijv. Amsterdam")
    t_city = st.text_input("HAAR STAD", placeholder="Bijv. Utrecht")
    
    if st.button("🔄 RESET ARCHITECT"):
        st.session_state.rizz_master = None
        st.rerun()

# --- 5. HEADER ---
st.markdown(f'<div class="brand-banner">{logo_img}<div class="logotype">RIZZ<span>ARCHITECT</span></div></div>', unsafe_allow_html=True)

# --- 6. MAIN INTERFACE ---
if not user_api_key:
    st.warning("⚠️ Voer je OpenAI API Key in de sidebar in om het systeem te activeren.")
else:
    c1, c2 = st.columns([1, 1.4], gap="large")

    with c1:
        st.markdown("<div class='label-tag'>Tactical Intake</div>", unsafe_allow_html=True)
        u_file = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            context = st.text_area("Extra Context", placeholder="Wat is de vibe? Wat wil je bereiken?")
            
            if st.button("⚡ EXECUTE SOVEREIGN SCAN"):
                with st.spinner("Decoding social engineering patterns..."):
                    try:
                        client = OpenAI(api_key=user_api_key)
                        b64 = process_img(u_file)
                        
                        sys_msg = f"""
                        Jij bent '⚡ Rizz Architect'. Platform: {platform}. Locaties: {u_city} & {t_city}.
                        
                        PROTOCOL:
                        1. TRIPLE-A: Analyseer screenshot & context ({context}).
                        2. WEATHER: Geef weersvoorspelling voor {t_city}.
                        3. VENUES: 3 trendy hotspots in {t_city} (1x drinken, 1x diner, 1x activiteit).
                        4. OUTFIT: Adviseer de perfecte 'Armor' voor dit weer en deze steden.
                        5. OPTIONS: 3 zinnen (Playful, Velvet, Pattern Interrupt).
                        
                        OUTPUT (JSON):
                        {{
                          "analysis": {{"investment": "...", "status": "...", "anomaly": "..."}},
                          "weather": "...",
                          "venues": [{{"naam": "...", "type": "...", "waarom": "..."}}],
                          "outfit": "...",
                          "options": [{{"type": "...", "zin": "...", "psych": "..."}}],
                          "architect_pick": {{"choice": 1, "reason": "..."}}
                        }}
                        WETTEN: Max 20 woorden per zin. Wees specifiek over {t_city}.
                        """
                        res = client.chat.completions.create(
                            model="gpt-4o-mini", response_format={"type": "json_object"},
                            messages=[{"role": "system", "content": sys_msg},
                                      {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
                        )
                        st.session_state.rizz_master = json.loads(res.choices[0].message.content)
                        st.rerun()
                    except Exception as e: st.error(f"Fout bij scan: {e}")

    with c2:
        if st.session_state.rizz_master:
            data = st.session_state.rizz_master
            
            # Logistics & Weather
            st.markdown("<div class='label-tag'>📍 Logistics & Armor</div>", unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card"><b>Weer in {t_city}:</b> {data.get("weather")}<br><br><b>🛡️ Outfit:</b> {data.get("outfit")}</div>', unsafe_allow_html=True)
            
            if data.get('venues'):
                v_cols = st.columns(3)
                for i, v in enumerate(data.get('venues')[:3]):
                    with v_cols[i]:
                        search_url = urllib.parse.quote(f"{v.get('naam')} {t_city}")
                        st.markdown(f"**{v.get('type')}**\n\n{v.get('naam')}")
                        st.markdown(f"[MAP](https://www.google.com/maps/search/{search_url})", unsafe_allow_html=True)

            # The Result
            p = data.get('architect_pick', {})
            idx = max(0, min(int(p.get('choice', 1)) - 1, 2))
            best = data.get('options', [{}])[idx]
            
            st.markdown(f"""
                <div class="pick-container">
                    <div class="label-tag">🏆 THE ARCHITECT'S PICK</div>
                    <h2 style="margin:0; color:#fff; line-height:1.2;">"{best.get('zin')}"</h2>
                    <p style="font-size:0.9rem; color:#fcd34d; margin-top:20px;"><b>STRATEGIE:</b> {p.get('reason')}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Systeem geactiveerd. Wachten op tactische data...")