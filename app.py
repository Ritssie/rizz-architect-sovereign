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
    page_title="Rizz Architect Sovereign v11.5", 
    page_title="Rizz Architect Sovereign v11.8", 
page_icon="👑", 
layout="wide",
initial_sidebar_state="expanded"
)

# ==============================================================================
# --- 2. MULTI-LANGUAGE DICTIONARY (EXTENDED LEGAL) ---
# --- 2. MULTI-LANGUAGE DICTIONARY ---
# ==============================================================================
translations = {
"NL": {
"header": "RIZZ<span>ARCHITECT</span>",
"tag_intake": "📥 TACTISCHE INTAKE",
"tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIEVE DIMENSIES",
        "tag_dims": "📐 TACTISCH ARSENAAL",
"tag_signals": "📡 SOCIAL SIGNALS",
"ctx_ph": "Vibe, relatie, laatste bericht, doel...",
"btn_scan": "⚡ START ANALYSE",
"dark_mode": "🌑 Dark Psychology Mode",
"reboot": "🔄 RESET SYSTEEM",
"upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "📋 Copy",
        "copy_btn": "KOPIEER",
"copied": "Gekopieerd!",
"strategy_label": "STRATEGIE",
        "legal_title": "⚖️ TERMS & LEGAL SHIELD",
        "legal_text": """
            <b>1. Geen Resultaatgarantie:</b> Sociale interactie is complex. De AI biedt suggesties, geen garanties op succes.<br><br>
            <b>2. Volledige Aansprakelijkheid:</b> Jij bent de verzender. Wij zijn niet verantwoordelijk voor afwijzingen, ruzies, juridische geschillen of emotionele schade.<br><br>
            <b>3. Geen Professioneel Advies:</b> Deze software is voor entertainment en analytische doeleinden. Het vervangt geen psychologische hulp.<br><br>
            <b>4. Data & Privacy:</b> Door gebruik te maken van deze tool stem je in dat screenshots tijdelijk worden verwerkt. Upload geen illegale of uiterst gevoelige content.<br><br>
            <b>5. Misbruik:</b> Het gebruik van de 'Dark Psychology' modus is voor eigen risico en morele verantwoording.
        """,
        "legal_title": "TERMS & LEGAL SHIELD",
        "legal_text": "<b>1. Geen Garantie:</b> AI biedt suggesties, geen zekerheid.<br><b>2. Eigen Risico:</b> Jij bent de verzender.<br><b>3. Privacy:</b> Upload geen gevoelige data.",
"idle_msg": "Systeem stand-by. Upload screenshot."
},
"EN": {
"header": "RIZZ<span>ARCHITECT</span>",
"tag_intake": "📥 TACTICAL INTAKE",
"tag_pick": "🏆 ARCHITECT'S CHOICE",
        "tag_dims": "📐 ALTERNATIVE DIMENSIONS",
        "tag_dims": "📐 TACTICAL ARSENAL",
"tag_signals": "📡 SOCIAL SIGNALS",
"ctx_ph": "Vibe, relationship, last message, goal...",
"btn_scan": "⚡ EXECUTE SCAN",
"dark_mode": "🌑 Dark Psychology Mode",
"reboot": "🔄 RESET SYSTEM",
"upload_label": "📂 DATA SOURCE (Screenshot)",
        "copy_btn": "📋 Copy",
        "copy_btn": "COPY",
"copied": "Copied!",
"strategy_label": "STRATEGY",
        "legal_title": "⚖️ TERMS & LEGAL SHIELD",
        "legal_text": """
            <b>1. No Success Guarantee:</b> Human interaction is unpredictable. AI provides suggestions, not guaranteed outcomes.<br><br>
            <b>2. Full Liability:</b> You are the sender. We are not responsible for rejections, conflicts, legal issues, or emotional distress.<br><br>
            <b>3. Not Professional Advice:</b> This tool is for entertainment and data analysis only. It is not a substitute for professional counseling.<br><br>
            <b>4. Data & Privacy:</b> By using this tool, you agree to temporary processing of screenshots. Do not upload illegal or highly sensitive content.<br><br>
            <b>5. Ethical Use:</b> Use of 'Dark Psychology' mode is at your own risk and moral discretion.
        """,
        "legal_title": "TERMS & LEGAL SHIELD",
        "legal_text": "<b>1. No Guarantee:</b> AI provides suggestions.<br><b>2. Liability:</b> You are the sender.<br><b>3. Privacy:</b> No sensitive data.",
"idle_msg": "System on standby. Upload screenshot."
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

   .brand-container { text-align: center; padding: 25px 0; }
   .brand-logo { font-family: 'Playfair Display', serif; font-size: 3rem; color: #ffffff !important; letter-spacing: -2px; }
   .brand-logo span { color: #fcd34d !important; text-shadow: 0 0 20px rgba(252, 211, 77, 0.4); }

   .section-header {
       font-family: 'JetBrains Mono', monospace; color: #fcd34d; font-size: 0.7rem;
       letter-spacing: 3px; margin: 30px 0 15px 0; display: flex; align-items: center;
       text-transform: uppercase; opacity: 0.8;
   }
   .section-header::after { content: ""; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(252, 211, 77, 0.3), transparent); margin-left: 15px; }

    /* Kaart Basis */
   .sovereign-card { 
       background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); 
        border-radius: 14px; padding: 22px; margin-bottom: 12px; position: relative; overflow: hidden;
        border-radius: 14px; padding: 20px; position: relative; overflow: hidden;
   }
    .winner-card { border: 2px solid #fcd34d; background: linear-gradient(165deg, rgba(252, 211, 77, 0.15) 0%, rgba(1, 4, 9, 1) 100%); transition: all 0.3s ease; }
    .winner-card:hover { border-color: #fbbf24; box-shadow: 0 0 30px rgba(252, 211, 77, 0.1); }

    .success-badge { 
        position: absolute; top: 15px; right: 15px; padding: 6px 14px; border-radius: 20px; 
        font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.7rem; z-index: 10;
        background: rgba(0,0,0,0.7); backdrop-filter: blur(8px); border: 1px solid rgba(252, 211, 77, 0.3);
    }

    .prob-container { margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px; }
    .prob-row { display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.75rem; margin-bottom: 8px; }
    /* Winnaar Kaart */
    .winner-card { border: 2px solid #fcd34d; background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); }
    
    /* Alternatieve Kaarten */
    .alt-card { border: 1px solid rgba(255, 255, 255, 0.1); background: rgba(255, 255, 255, 0.03); margin-bottom: 15px; }
    .alt-type { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #fcd34d; opacity: 0.7; margin-bottom: 8px; text-transform: uppercase; }

    .legal-box {
        background: rgba(248, 113, 113, 0.03); border: 1px solid rgba(248, 113, 113, 0.15); 
        border-radius: 12px; padding: 15px; color: #f87171; font-size: 0.65rem; line-height: 1.5;
    .success-badge { 
        position: absolute; top: 15px; right: 15px; padding: 4px 12px; border-radius: 20px; 
        font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.65rem;
        background: rgba(0,0,0,0.6); border: 1px solid rgba(252, 211, 77, 0.3); color: #fcd34d;
   }

    /* Button Styling */
    .stButton>button { 
        background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; 
        color: #010409 !important; font-weight: 700; border-radius: 8px; border: none !important;
        transition: transform 0.1s ease !important;
    }
    .stButton>button:active { transform: scale(0.98); }
    .prob-container { margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px; }
    .prob-row { display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.7rem; margin-bottom: 4px; opacity: 0.8; }

    /* Danger Button override */
    .danger-zone button {
        background: transparent !important; color: #f87171 !important;
        border: 1px solid rgba(248, 113, 113, 0.3) !important; margin-top: 20px;
    }
    .stButton>button { border-radius: 8px !important; font-weight: 700 !important; }
    
    /* Toast Style */
    [data-testid="stToast"] { background-color: #161b22 !important; color: #fcd34d !important; border: 1px solid #fcd34d !important; }
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

def get_analysis(client, b64, ctx, dark, lang):
lang_name = "Dutch" if lang == "NL" else "English"
    prompt = f"Role: Sovereign Architect. Respond ONLY in {lang_name}. Return JSON: success_rate(int), breakdown{{vibe, timing, subtext}}, green_flags, red_flags, options, winner_idx."
    prompt = f"Role: Sovereign Architect. Respond ONLY in {lang_name}. Return JSON: success_rate(int), breakdown{{vibe, timing, subtext}}, green_flags, red_flags, options[{{\"type\": \"str\", \"zin\": \"str\", \"psychology\": \"str\"}}], winner_idx."
try:
res = client.chat.completions.create(
model="grok-4.20-0309-non-reasoning",
response_format={"type": "json_object"},
messages=[{"role": "system", "content": prompt},
{"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
)
return json.loads(res.choices[0].message.content)
except: return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
# ==============================================================================
if 'state' not in st.session_state: st.session_state.state = None

with st.sidebar:
st.markdown("### ⚙️ SETTINGS")
lang_choice = st.selectbox("🌍 Language", options=["NL", "EN"], index=0)
t = translations[lang_choice]
    
api_key = st.text_input("Grok API Key", type="password")
is_dark = st.toggle(t["dark_mode"])

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    
    # --- DE UITGEBREIDE LEGAL SHIELD ---
    st.markdown(f"""
        <div class="legal-box">
            <b style="font-size: 0.75rem; letter-spacing: 1px;">{t['legal_title']}</b><br><br>
            <div style="max-height: 180px; overflow-y: auto; padding-right: 5px;">
                {t['legal_text']}
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander(f"⚖️ {t['legal_title']}"):
        st.markdown(f'<div style="font-size:0.65rem; color:#94a3b8;">{t["legal_text"]}</div>', unsafe_allow_html=True)

    # --- DANGER ZONE REBOOT ---
    st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
if st.button(t["reboot"], use_container_width=True):
st.session_state.clear(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

if not api_key:
    st.info("🔐 Voer je API-key in de sidebar in om te beginnen.")
    st.info("🔐 Voer je API-key in.")
else:
col_l, col_r = st.columns([1, 1.2], gap="large")

with col_l:
st.markdown(f"<div class='section-header'>{t['tag_intake']}</div>", unsafe_allow_html=True)
u_file = st.file_uploader(t["upload_label"], type=['png','jpg','jpeg'], label_visibility="collapsed")
if u_file:
st.image(u_file, width='stretch')
u_ctx = st.text_area("Context", placeholder=t["ctx_ph"], height=80)
if st.button(t["btn_scan"], use_container_width=True):
                with st.spinner("Calculating Probabilities..."):
                with st.spinner("Analyzing Architecture..."):
client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
st.session_state.state = get_analysis(client, process_img(u_file), u_ctx, is_dark, lang_choice)
st.rerun()

with col_r:
if st.session_state.state:
s = st.session_state.state

# --- SIGNALS ---
st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
sc1, sc2 = st.columns(2)
with sc1:
for gf in s.get('green_flags', []):
st.markdown(f'<div class="pill pill-green">✅ {gf if isinstance(gf, str) else gf.get("label", "Flag")}</div>', unsafe_allow_html=True)
with sc2:
for rf in s.get('red_flags', []):
st.markdown(f'<div class="pill pill-red">🚩 {rf if isinstance(rf, str) else rf.get("label", "Flag")}</div>', unsafe_allow_html=True)

# --- WINNER CARD ---
st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            options = s.get('options', [])
            opts = s.get('options', [])
w_idx = s.get('winner_idx', 0)

            if options and len(options) > w_idx:
                w = options[w_idx]
                zin = w.get('zin', str(w)) if isinstance(w, dict) else str(w)
                psych = w.get('psychology', 'N/A') if isinstance(w, dict) else "N/A"
                rate = s.get('success_rate', 0)
            if opts and len(opts) > w_idx:
                w = opts[w_idx]
                zin, psych = w.get('zin'), w.get('psychology')
                rate = s.get('success_rate', 85)
b = s.get('breakdown', {'vibe': 50, 'timing': 50, 'subtext': 50})

st.markdown(f"""
                   <div class="sovereign-card winner-card">
                       <div class="success-badge">{rate}% HIT RATE</div>
                        <div style="font-size:1.3rem; font-weight:800; margin-bottom:20px; padding-right:110px; line-height:1.4; color:white;">
                            "{zin}"
                        </div>
                        <div style="font-size:0.85rem; opacity:0.9; margin-bottom:15px; border-left: 2px solid #fcd34d; padding-left: 12px;">
                        <div style="font-size:1.3rem; font-weight:800; margin-bottom:15px; padding-right:100px; color:white;">"{zin}"</div>
                        <div style="font-size:0.85rem; opacity:0.9; border-left: 2px solid #fcd34d; padding-left: 10px; margin-bottom: 15px;">
                           <b style="color:#fcd34d;">{t['strategy_label']}:</b> {psych}
                       </div>
                       <div class="prob-container">
                            <div class="prob-row"><span>VIBE</span><span style="font-weight:700; color:#fcd34d;">{b.get('vibe', 0)}%</span></div>
                            <div class="prob-row"><span>TIMING</span><span style="font-weight:700; color:#fcd34d;">{b.get('timing', 0)}%</span></div>
                            <div class="prob-row"><span>SUBTEXT</span><span style="font-weight:700; color:#fcd34d;">{b.get('subtext', 0)}%</span></div>
                            <div class="prob-row"><span>VIBE</span><b>{b.get('vibe')}%</b></div>
                            <div class="prob-row"><span>TIMING</span><b>{b.get('timing')}%</b></div>
                            <div class="prob-row"><span>SUBTEXT</span><b>{b.get('subtext')}%</b></div>
                       </div>
                   </div>
               """, unsafe_allow_html=True)
                
                if st.button(f"{t['copy_btn']}", key="copy_win", use_container_width=True):
                if st.button(f"✨ {t['copy_btn']} PRIMARY CHOICE", key="cp_w", use_container_width=True):
st.write(f'<script>navigator.clipboard.writeText("{zin}")</script>', unsafe_allow_html=True)
st.toast(t["copied"])

            # --- ALTERNATIVES ---
            # --- ARSENAL (ALTERNATIVES AS CARDS) ---
st.markdown(f"<div class='section-header' style='margin-top:40px;'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(options):
            for i, opt in enumerate(opts):
if i != w_idx:
                    alt_zin = opt.get('zin', str(opt)) if isinstance(opt, dict) else str(opt)
                    c1, c2 = st.columns([5, 1.2])
                    with c1:
                        st.markdown(f'<div class="sovereign-card"><b>"{alt_zin}"</b></div>', unsafe_allow_html=True)
                    with c2:
                        st.write("") 
                        if st.button(t["copy_btn"], key=f"c_{i}"):
                            st.write(f'<script>navigator.clipboard.writeText("{alt_zin}")</script>', unsafe_allow_html=True)
                            st.toast(t["copied"])
                    a_zin, a_psych, a_type = opt.get('zin'), opt.get('psychology'), opt.get('type', 'ALT')
                    st.markdown(f"""
                        <div class="sovereign-card alt-card">
                            <div class="alt-type">{a_type}</div>
                            <div style="font-weight:600; font-size:1rem; margin-bottom:10px;">"{a_zin}"</div>
                            <div style="font-size:0.75rem; opacity:0.7; font-style: italic;">{a_psych}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"{t['copy_btn']} {a_type}", key=f"cp_{i}", use_container_width=True):
                        st.write(f'<script>navigator.clipboard.writeText("{a_zin}")</script>', unsafe_allow_html=True)
                        st.toast(t["copied"])
else:
st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V11.5 | IRONCLAD EDITION</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V11.8</div>", unsafe_allow_html=True)
