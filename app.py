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
    page_title="Rizz Architect Sovereign v8.5", 
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
        "ctx_ph": "Context: Leeftijd, vibe, laatste interactie...",
        "btn_scan": "⚡ EXECUTE PRECISION SCAN",
        "dark_mode": "🌑 Dark Psychology Mode",
        "reboot": "🔄 SYSTEM REBOOT",
        "upload_label": "📂 DATA SOURCE (Klik voor upload)",
        "copy_btn": "📋 Kopieer Antwoord",
        "idle_msg": "Systeem in stand-by. Upload intel om de architectuur te starten.",
        "dark_alert_html": """
            <div style='background: rgba(248, 113, 113, 0.05); border: 1px solid rgba(248, 113, 113, 0.3); 
                 border-radius: 12px; padding: 15px; color: #f87171; font-size: 0.8rem; 
                 box-shadow: 0 0 15px rgba(248, 113, 113, 0.05); margin-top: 15px;'>
                <b style='font-family:JetBrains Mono; letter-spacing:1px;'>⚠️ DARK OPS GEACTIVEERD</b><br>
                Gevorderde beïnvloedingstechnieken en 'The Takeaway' strategieën geladen.
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

    .brand-container { text-align: center; padding: 40px 0; }
    .brand-logo { font-family: 'Playfair Display', serif; font-size: 3.2rem; color: #ffffff !important; letter-spacing: -2px; }
    .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 20px rgba(252, 211, 77, 0.4); }

    .archetype-label {
        font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; text-transform: uppercase;
        letter-spacing: 1.5px; padding: 3px 10px; border-radius: 4px;
        background: rgba(252, 211, 77, 0.1); color: #fcd34d; border: 1px solid rgba(252, 211, 77, 0.2);
        margin-bottom: 10px; display: inline-block;
    }

    .section-header {
        font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.7rem;
        letter-spacing: 3px; margin: 25px 0 12px 0; display: flex; align-items: center;
        text-transform: uppercase; opacity: 0.6;
    }
    .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.2), transparent); margin-left: 15px; }

    .sovereign-card { 
        background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); 
        border-radius: 14px; padding: 20px; margin-bottom: 15px; 
    }
    .winner-card { 
        background: linear-gradient(165deg, rgba(252, 211, 77, 0.08) 0%, rgba(1, 4, 9, 1) 100%); 
        border: 1px solid #fcd34d; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .gauge-container { 
        background: rgba(255,255,255,0.01); border-radius: 50%; width: 100px; height: 100px; 
        display: flex; align-items: center; justify-content: center; 
        border: 3px solid #fcd34d; margin: 10px auto;
    }
    
    .pill { display: block; padding: 10px; border-radius: 8px; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; margin-bottom: 8px; }
    .pill-green { background: rgba(74, 222, 128, 0.05); color: #4ade80; border: 1px solid #4ade8011; }
    .pill-red { background: rgba(248, 113, 113, 0.05); color: #f87171; border: 1px solid #f8717111; }

    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 700; border-radius: 10px; height: 3.2rem; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 4. ENGINE CORE ---
# ==============================================================================
def process_img(file):
    img = Image.open(file).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO(); img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, dark):
    mode = "DARK OPS" if dark else "CHARISMA"
    prompt = f"Role: Sovereign Architect ({mode}). Output JSON: success_rate(int), green_flags(max3), red_flags(max3), options[type(Playful Provocateur/Velvet Charmer/Pattern Interrupt), zin, psychology], winner_idx."
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt},
                      {"role": "user", "content": [{"type": "text", "text": ctx},
                                                 {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
        )
        data = json.loads(res.choices[0].message.content)
        if data.get('success_rate', 0) < 1.0: data['success_rate'] = int(data['success_rate'] * 100)
        return data
    except Exception: return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None
t = translations["NL"]

with st.sidebar:
    st.markdown("### ⚙️ SETTINGS")
    api_key = st.text_input("Grok API Key", type="password")
    is_dark = st.toggle(t["dark_mode"])
    if st.button(t["reboot"]): st.session_state.clear(); st.rerun()

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 Toegang geweigerd. Voer API-sleutel in.")
else:
    col_l, col_r = st.columns([1, 1.2], gap="large")

    with col_l:
        st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
        with st.expander(t["upload_label"], expanded=(st.session_state.state is None)):
            u_file = st.file_uploader("U", type=['png','jpg','jpeg'], label_visibility="collapsed")
        
        if u_file:
            st.image(u_file, use_container_width=True)
            u_ctx = st.text_area("C", placeholder=t["ctx_ph"], height=70, label_visibility="collapsed")
            if st.button(t["btn_scan"]):
                with st.spinner("Analyzing Architecture..."):
                    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                    st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, is_dark)
                    st.rerun()
        
        # --- DYNAMISCHE MISSION BRIEFING ---
        tip_5 = "<b>The Takeaway:</b> Bereidheid om weg te lopen is macht." if is_dark else "<b>Value Offering:</b> Toon een boeiend leven zonder validatie te zoeken."
        
        intel_html = f"""
            <div style='font-size:0.85rem; line-height:1.7; opacity:0.95;'>
                <div style='margin-bottom:8px;'><span style='color:#fcd34d;'>🎯</span> <b>Frame Control:</b> Jij bepaalt de narratief.</div>
                <div style='margin-bottom:8px;'><span style='color:#fcd34d;'>💎</span> <b>Anti-Desperation:</b> Schaarste bepaalt jouw waarde.</div>
                <div style='margin-bottom:8px;'><span style='color:#fcd34d;'>⚓</span> <b>Emotional Anchoring:</b> Word de bron van dopamine.</div>
                <div style='margin-bottom:8px;'><span style='color:#fcd34d;'>⚖️</span> <b>Push-Pull:</b> Wissel plagen af met oprechte interesse.</div>
                <div style='margin-bottom:2px;'><span style='color:#fcd34d;'>🚀</span> {tip_5}</div>
            </div>
        """
        st.markdown(f"<div class='section-header'>{t['tag_briefing']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sovereign-card'>{intel_html}</div>", unsafe_allow_html=True)
        if is_dark: st.markdown(t["dark_alert_html"], unsafe_allow_html=True)

    with col_r:
        if st.session_state.state:
            s = st.session_state.state
            st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
            f_c1, f_c2 = st.columns(2)
            with f_c1:
                for gf in s.get('green_flags', []): st.markdown(f"<div class='pill pill-green'>✅ {gf}</div>", unsafe_allow_html=True)
            with f_c2:
                for rf in s.get('red_flags', []): st.markdown(f"<div class='pill pill-red'>🚩 {rf}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='gauge-container'><span style='font-size:1.4rem; font-weight:900;'>{int(s.get('success_rate', 0))}%</span></div>", unsafe_allow_html=True)

            st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            w = s['options'][s.get('winner_idx', 0)]
            st.markdown(f"""
                <div class="sovereign-card winner-card">
                    <div class="archetype-label">{w.get('type')}</div>
                    <div style="font-size:1.1rem; font-weight:700; color:white; margin-bottom:12px;">"{w.get('zin')}"</div>
                    <div style="font-size:0.8rem; opacity:0.8; border-top:1px solid rgba(252,211,77,0.2); padding-top:10px;">
                        <b>ARCHITECT'S NOTE:</b> {w.get('psychology')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.code(w.get('zin'), language=None)

            st.markdown(f"<div class='section-header'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s['options']):
                if i != s.get('winner_idx', 0):
                    st.markdown(f"""
                        <div class="sovereign-card">
                            <div class="archetype-label" style="opacity:0.7;">{opt.get('type')}</div>
                            <div style="font-size:0.9rem; font-weight:600; margin:5px 0;">"{opt.get('zin')}"</div>
                            <div style="font-size:0.75rem; opacity:0.6;"><i>Insight: {opt.get('psychology')}</i></div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(t["idle_msg"])

# ..............................................................................
# ..............................................................................
# ..............................................................................
st.write("")
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; letter-spacing:2px;'>SOVEREIGN ENGINE V8.5 | ANTI-DARK OPS SHIELD</div>", unsafe_allow_html=True)
