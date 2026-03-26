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
    page_title="Rizz Architect Sovereign v10.1", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. MULTI-LANGUAGE ARCHITECT DICTIONARY ---
# ==============================================================================
translations = {
    "NL": {
        "header": "RIZZ<span>ARCHITECT</span>",
        "tag_intake": "📥 TACTISCHE INTAKE",
        "tag_briefing": "📖 MISSION BRIEFING",
        "tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIEVE DIMENSIES",
        "tag_signals": "📡 SOCIAL SIGNALS",
        "ctx_ph": "Context: vibe, laatste bericht, doel...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "📋",
        "idle_msg": "Systeem stand-by. Upload screenshot.",
        "dark_warning": """
            <div style='background: rgba(248, 113, 113, 0.08); border: 2px solid #f87171; 
                 border-radius: 12px; padding: 15px; color: #f87171; font-size: 0.75rem; line-height: 1.4; margin-top: 15px;'>
                <div style='font-size: 1.5rem; margin-bottom: 5px;'>⚖️</div>
                <b style='font-family:JetBrains Mono; letter-spacing:1px;'>LEGAL DISCLOSURE: DARK OPS</b><br><br>
                Rizz Architect is een adviserend instrument. Het gebruik is <b>geheel op eigen risico</b>. 
                Wij zijn niet aansprakelijk voor resultaten of emotionele schade. 
                De gebruiker kiest en verzendt altijd zelf; wij adviseren slechts (vaak gebrekkig).
            </div>
        """
    }
}

# ==============================================================================
# --- 3. PREMIUM CSS ENGINE ---
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Playfair+Display:wght@900&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #010409 !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif; 
    }

    .brand-container { text-align: center; padding: 35px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3rem; color: #ffffff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 20px rgba(252, 211, 77, 0.4); }

    .pill { 
        display: block; padding: 10px; border-radius: 8px; font-size: 0.7rem; 
        font-family: 'JetBrains Mono', monospace; margin-bottom: 8px; position: relative; cursor: help;
    }
    .pill-green { background: rgba(74, 222, 128, 0.05); color: #4ade80; border: 1px solid #4ade8022; }
    .pill-red { background: rgba(248, 113, 113, 0.05); color: #f87171; border: 1px solid #f8717122; }
    .pill:hover::after {
        content: attr(data-reason); position: absolute; left: 0; bottom: 120%;
        background: #161b22; color: white; padding: 8px 12px; border-radius: 6px; 
        font-size: 0.65rem; width: 200px; border: 1px solid rgba(255,255,255,0.1); z-index: 99;
    }

    .prob-container { margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; }
    .prob-row { display: flex; justify-content: space-between; font-size: 0.65rem; font-family: 'JetBrains Mono'; margin-bottom: 4px; }
    .prob-bar-bg { background: rgba(255,255,255,0.05); height: 4px; border-radius: 2px; width: 100%; margin-bottom: 8px; }
    .prob-bar-fill { height: 100%; border-radius: 2px; transition: width 0.5s; }

    .success-badge {
        position: absolute; top: 20px; right: 20px;
        padding: 5px 12px; border-radius: 20px;
        font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.75rem;
    }

    .sovereign-card { 
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); 
        border-radius: 14px; padding: 20px; margin-bottom: 15px; position: relative;
    }
    .winner-card { border: 2px solid #fcd34d; background: linear-gradient(165deg, rgba(252, 211, 77, 0.08) 0%, rgba(1, 4, 9, 1) 100%); }

    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 700; border-radius: 10px; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE (FIXED ERROR HANDLING) ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, dark):
    mode = "DARK OPS" if dark else "CHARISMA"
    prompt = f"""
    Role: Sovereign Architect ({mode}). Focus on conversation flow.
    Return ONLY a JSON object:
    {{
      "success_rate": int, 
      "breakdown": {{"vibe": int, "timing": int, "subtext": int}},
      "green_flags": [{{"label": "string", "reason": "string"}}], 
      "red_flags": [{{"label": "string", "reason": "string"}}], 
      "options": [{{"type": "string", "zin": "string", "psychology": "string"}}], 
      "winner_idx": int
    }}
    """
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [
                          {"type": "text", "text": f"Context: {ctx}"},
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                      ]}]
        )
        # Veilig parsen van de JSON
        content = res.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        st.error(f"Engine Error: {str(e)}")
        return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None
t = translations["NL"]

with st.sidebar:
    st.markdown("### ⚙️ SYSTEM")
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    if is_dark: st.markdown(t["dark_warning"], unsafe_allow_html=True)
    if st.button(t["reboot"]): st.session_state.clear(); st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 Voer API-sleutel in.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        with st.expander(t["upload_label"], expanded=(st.session_state.state is None)):
            u_file = st.file_uploader("U", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, width='stretch') # FIX: width='stretch' ipv use_container_width
            u_ctx = st.text_area("C", placeholder=t["ctx_ph"], height=70, label_visibility="collapsed")
            if st.button(t["btn_scan"]):
                with st.spinner("Decoding Architecture..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, is_dark)
                    st.rerun()

    with col_r:
        if st.session_state.state and isinstance(st.session_state.state, dict):
            s = st.session_state.state
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            f_c1, f_c2 = st.columns(2)
            with f_c1:
                for gf in s.get('green_flags', []): 
                    st.markdown(f'<div class="pill pill-green" data-reason="{gf.get("reason", "Geen reden")} Barb">✅ {gf.get("label", "Flag")}</div>', unsafe_allow_html=True)
            with f_c2:
                for rf in s.get('red_flags', []): 
                    st.markdown(f'<div class="pill pill-red" data-reason="{rf.get("reason", "Geen reden")}">🚩 {rf.get("label", "Flag")}</div>', unsafe_allow_html=True)
            
            rate = int(s.get('success_rate', 0))
            color = "#fcd34d" if rate > 80 else ("#fbbf24" if rate > 60 else "#f87171")
            
            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            w_idx = s.get('winner_idx', 0)
            # Veiligheid tegen index errors
            if w_idx < len(s['options']):
                w = s['options'][w_idx]
                b = s.get('breakdown', {'vibe': 50, 'timing': 50, 'subtext': 50})
                
                st.markdown(f"""
                    <div class="sovereign-card winner-card">
                        <div class="success-badge" style="border:1px solid {color}; color:{color};">{rate}% HIT RATE</div>
                        <div style="font-size:1.2rem; font-weight:700; color:white; margin-bottom:15px; padding-right:85px;">"{w.get('zin')}"</div>
                        <div class="prob-container">
                            <div class="prob-row"><span>VIBE</span><span>{b['vibe']}%</span></div>
                            <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{b['vibe']}%; background:{color};"></div></div>
                            <div class="prob-row"><span>TIMING</span><span>{b['timing']}%</span></div>
                            <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{b['timing']}%; background:{color};"></div></div>
                            <div class="prob-row"><span>SUBTEXT</span><span>{b['subtext']}%</span></div>
                            <div class="prob-bar-bg"><div class="prob-bar-fill" style="width:{b['subtext']}%; background:{color};"></div></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.code(w.get('zin'), language=None)
            
            st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s.get('options', [])):
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f'<div class="sovereign-card"><div style="font-size:0.6rem; opacity:0.5; font-family:JetBrains Mono;">{opt["type"]}</div><b>"{opt["zin"]}"</b></div>', unsafe_allow_html=True)
                with c2:
                    st.write(""); st.button(t["copy_btn"], key=f"c_{i}")
        else:
            if st.session_state.state is not None:
                st.error("Data corrupt. Probeer de scan opnieuw.")
            st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V10.1 | STABLE REBUILD</div>", unsafe_allow_html=True)
