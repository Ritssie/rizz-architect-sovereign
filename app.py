import streamlit as st
from openai import OpenAI
import base64
import json

# ==============================================================================
# --- 1. CONFIG & PREMIUM SIGNAL UI DESIGN ---
# ==============================================================================
st.set_page_config(page_title="Signal v3 — Conversatie Analyse", page_icon="📡", layout="wide")

if 'state' not in st.session_state: 
    st.session_state.state = None

# Uitgebreide, geavanceerde CSS voor een premium, futuristische uitstraling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap');
    
    /* Globale styling & Donkere Modus */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #050508 !important; 
        color: #f8fafc !important; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Verberg standaard Streamlit rommel voor een cleanere app */
    [data-testid="stHeader"], footer { visibility: hidden; }

    /* Custom labels boven invoervelden */
    .lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        color: #475569;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 8px;
        display: block;
    }

    /* Subtiele styling voor Streamlit input velden zodat ze matchen met de UI */
    .stTextArea textarea, .stTextInput input, div[data-testid="stSelectbox"] > div {
        background-color: #0b0b14 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: rgba(165, 180, 252, 0.4) !important;
        box-shadow: 0 0 10px rgba(165, 180, 252, 0.1) !important;
    }

    /* Premium Badges Bovenaan Dashboard */
    .custom-badge {
        display: inline-flex; align-items: center; gap: 6px; 
        font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 500;
        padding: 5px 12px; border-radius: 20px; border: 1px solid; 
        margin-right: 8px; margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .b-purple { background: rgba(99, 102, 241, 0.1); color: #a5b4fc; border-color: rgba(99, 102, 241, 0.3); }
    .b-teal   { background: rgba(20, 184, 166, 0.1);  color: #2dd4bf; border-color: rgba(20, 184, 166, 0.3); }
    .b-amber  { background: rgba(245, 158, 11, 0.1);  color: #fcd34d; border-color: rgba(245, 158, 11, 0.3); }

    /* Flags & Signalen Pillen */
    .pill { 
        font-size: 12px; padding: 8px 12px; border-radius: 8px; 
        margin-bottom: 8px; line-height: 1.4; border: 1px solid;
        transition: transform 0.2s ease;
    }
    .pill:hover { transform: translateX(3px); }
    .g-p { background: rgba(16, 185, 129, 0.06); color: #34d399; border-color: rgba(16, 185, 129, 0.2); }
    .r-p { background: rgba(239, 68, 68, 0.06); color: #f87171; border-color: rgba(239, 68, 68, 0.2); }
    .n-p { background: rgba(99, 102, 241, 0.06); color: #a5b4fc; border-color: rgba(99, 102, 241, 0.2); }
    .a-p { background: rgba(245, 158, 11, 0.06); color: #fbbf24; border-color: rgba(245, 158, 11, 0.2); }

    /* Eerlijke Analyse Box */
    .analysis-box {
        font-size: 13.5px; color: #cbd5e1; background: #0b0b14;
        border-left: 3px solid #6366f1; border-radius: 4px 10px 10px 4px; 
        padding: 14px; line-height: 1.6; margin-bottom: 20px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }

    /* Premium Reply Cards met Glow-effecten */
    .signal-card {
        background: #0b0b14; border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px; padding: 18px; margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .signal-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    /* Special Glow voor de 'Main Character' of high risk opties */
    .signal-card.main-char { 
        border-color: rgba(99, 102, 241, 0.4) !important; 
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
    }
    .signal-card.main-char:hover {
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2);
    }
    
    /* Card Metadata */
    .rmeta { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
    .rstyle { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #64748b; }
    .rtag { font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 2px 8px; border-radius: 20px; font-weight: 500; }
    .rl { background: rgba(16, 185, 129, 0.1); color: #34d399; }
    .rm { background: rgba(245, 158, 11, 0.1); color: #fbbf24; }
    .rh { background: rgba(239, 68, 68, 0.1); color: #f87171; }
    
    /* De daadwerkelijke openingszin */
    .rline { font-size: 17px; font-weight: 600; color: #ffffff; margin-bottom: 10px; letter-spacing: -0.01em; line-height: 1.4; }
    .rwhy {
        font-size: 12px; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 10px; line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. STRATEGIC ENGINE (Grok / OpenAI-compatibel) ---
# ==============================================================================
def run_signal_scan(api_key, chat_text, chat_b64, bio_text, vibe, platform, stage):
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    no_question = vibe in ['Delusional / Bold', 'Direct & Calm']
    constraint = "STRICT: Geen vraagtekens (?) in de reply-teksten. Gebruik statements, cold reads of teases." if no_question else ""

    sys_prompt = f"""Je bent een scherpe, eerlijke, cultureel-bewuste Gen-Z dating analyst voor de Nederlandse markt.
Platform: {platform}. Gewenste vibe: {vibe}. Fase: {stage}.
{constraint}

Analyseer de conversatie. Reply-teksten moeten in NATUURLIJK DUTCH zijn, eventueel gemixd met Gen-Z slang (low-key, cooking, yapping, ate, valid, clean, ick, main character). Geen cringe pick-uplines, geen alpha-talk, geen uitroeptekens tenzij meme-context, grotendeels lowercase, kort en punchy.

Return verplicht een valide JSON object:
{{
  "detected_stage": "Early | Mid | Late",
  "tone": "Dry | Chaotic | Soft | Avoidant | Flirty | Clingy | Mysterious | Direct",
  "metrics": {{
    "her_investment": 0-100,
    "signal_strength": 0-100,
    "try_hard_score": 0-100,
    "ghost_risk": 0-100
  }},
  "green_flags": ["max 3 korte bevindingen"],
  "red_flags": ["max 2 korte bevindingen"],
  "self_signals": ["2-3 bevindingen over de gebruiker"],
  "potential_icks": ["1-2 mogelijke icks"],
  "analysis": "Eerlijke analyse in 2 zinnen Nederlands. Geen sugarcoating.",
  "replies": [
    {{"style": "Low Effort", "text": "...", "why_it_works": "...", "risk_level": "Low", "energy": "Low"}},
    {{"style": "Playful Banter", "text": "...", "why_it_works": "...", "risk_level": "Low", "energy": "Medium"}},
    {{"style": "Curious / Warm", "text": "...", "why_it_works": "...", "risk_level": "Medium", "energy": "Medium"}},
    {{"style": "Main Character", "text": "...", "why_it_works": "...", "risk_level": "High", "energy": "High"}}
  ]
}}"""

    user_content = []
    if chat_text:
        user_content.append({"type": "text", "text": f"Chat transcript:\n{chat_text}"})
    if chat_b64:
        user_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{chat_b64}"}})
    if bio_text:
        user_content.append({"type": "text", "text": f"Extra context / Bio: {bio_text}"})

    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e:
        st.error(f"Fout tijdens de scan: {str(e)}")
        return None

# ==============================================================================
# --- 3. UI ASSEMBLY ---
# ==============================================================================
# Minimalistische premium titelontwerp
st.markdown("<h1 style='text-align:center; font-weight:700; font-size: 28px; letter-spacing: -0.02em; margin-bottom:2px; color:#ffffff;'>Signal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-family:\"JetBrains Mono\", monospace; font-size:11px; color:#475569; letter-spacing:0.05em; margin-bottom:35px;'>CONVERSATIE-INTELLIGENTIE · v3 (GROK ENGINE)</p>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<span class='lbl'>🎚️ SIGNAL CONTROLS</span>", unsafe_allow_html=True)
    api_key = st.text_input("Grok API Key", type="password", placeholder="xai-...")
    plat = st.selectbox("Platform", ["Hinge", "Tinder", "Bumble", "Instagram DMs", "TikTok DMs", "Breeze", "WhatsApp"])
    vibe = st.selectbox("Jouw Vibe", ["Low-key Banter", "Unhinged / Meme", "Delusional / Bold", "Soft Launch", "Dry / Sarcastic", "Direct & Calm"])
    stage = st.selectbox("Situationship Fase", ["Talking Stage", "Almost Dating", "DTR Zone", "Post-Sitch"])
    st.markdown("---")
    if st.button("RESET SYSTEM", use_container_width=True): 
        st.session_state.state = None
        st.rerun()

col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown("<span class='lbl'>📥 INTEL INTAKE</span>", unsafe_allow_html=True)
    u_transcript = st.text_area("Chat Transcript", placeholder="Plak hier de gekopieerde chat (WhatsApp, DMs...)", height=150, label_visibility="collapsed")
    
    st.markdown("<span class='lbl' style='margin-top:15px;'>📸 SCREENSHOT UPLOAD</span>", unsafe_allow_html=True)
    u_chat = st.file_uploader("Drop screenshot hier", type=['png','jpg','jpeg'], label_visibility="collapsed")
    
    c_b64 = None
    if u_chat: 
        st.image(u_chat, use_container_width=True, caption="Chat Preview")
        c_b64 = base64.b64encode(u_chat.getvalue()).decode()

    st.markdown("<span class='lbl' style='margin-top:15px;'>📝 CONTEXT (OPTIONEEL)</span>", unsafe_allow_html=True)
    u_bio = st.text_area("Context (Optioneel)", placeholder="Bio, interesses, wat weet je over hen...", height=70, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📡 ANALYSEER CONVERSATIE", use_container_width=True):
        if not api_key:
            st.warning("Voer eerst je Grok API key in.")
        elif not u_transcript and not u_chat:
            st.warning("Voer een transcript in of upload een screenshot.")
        else:
            with st.status("Reading the room met Grok...") as status:
                st.session_state.state = run_signal_scan(api_key, u_transcript, c_b64, u_bio, vibe, plat, stage)
                status.update(label="Analyse Compleet", state="complete")
            st.rerun()

with col_out:
    st.markdown("<span class='lbl'>📡 STRATEGIC DASHBOARD</span>", unsafe_allow_html=True)
    
    if st.session_state.state:
        s = st.session_state.state
        met = s.get('metrics', {})
        
        # Badges Bovenaan
        st.markdown(f"""
            <span class='custom-badge b-teal'>📈 {s.get('detected_stage', '—')} stage</span>
            <span class='custom-badge b-purple'>🎭 Toon: {s.get('tone', '—')}</span>
            <span class='custom-badge b-amber'>❤️ {stage}</span>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Metrics Matrix (4 cellen)
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Haar Inves.", f"{met.get('her_investment', 0)}%")
        m_col2.metric("Jouw Signaal", f"{met.get('signal_strength', 0)}%")
        m_col3.metric("Try-hard", f"{met.get('try_hard_score', 0)}%")
        m_col4.metric("Ghost Risk", f"{met.get('ghost_risk', 0)}%")
        
        st.markdown("<hr style='margin:20px 0; border:0; border-top:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        
        # Flags & Signalen Matrix (2x2 indeling)
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown("<div style='font-family:\"JetBrains Mono\", monospace; font-size:10px; color:#34d399; font-weight:600; margin-bottom:8px; letter-spacing:0.05em;'>✅ GREEN FLAGS</div>", unsafe_allow_html=True)
            for f in s.get('green_flags', []): st.markdown(f"<div class='pill g-p'>✦ {f}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='font-family:\"JetBrains Mono\", monospace; font-size:10px; color:#a5b4fc; font-weight:600; margin-top:14px; margin-bottom:8px; letter-spacing:0.05em;'>📡 JOUW SIGNALEN</div>", unsafe_allow_html=True)
            for f in s.get('self_signals', []): st.markdown(f"<div class='pill n-p'>⚡ {f}</div>", unsafe_allow_html=True)
            
        with f_col2:
            st.markdown("<div style='font-family:\"JetBrains Mono\", monospace; font-size:10px; color:#f87171; font-weight:600; margin-bottom:8px; letter-spacing:0.05em;'>🚩 RED FLAGS</div>", unsafe_allow_html=True)
            for f in s.get('red_flags', []): st.markdown(f"<div class='pill r-p'>⚠️ {f}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='font-family:\"JetBrains Mono\", monospace; font-size:10px; color:#fbbf24; font-weight:600; margin-top:14px; margin-bottom:8px; letter-spacing:0.05em;'>🍋 MOGELIJKE ICKS</div>", unsafe_allow_html=True)
            for f in s.get('potential_icks', []): st.markdown(f"<div class='pill a-p'>✕ {f}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:20px 0; border:0; border-top:1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        
        # Eerlijke Analyse Box
        st.markdown(f"<div class='analysis-box'><b>Architect Analysis:</b> {s.get('analysis', '')}</div>", unsafe_allow_html=True)
        
        # Antwoorden renderen
        st.markdown("<span class='lbl'>Voorgestelde Replies</span>", unsafe_allow_html=True)
        for idx, r in enumerate(s.get('replies', [])):
            style_name = r.get('style', 'Banter')
            is_main = "main-char" if style_name == "Main Character" else ""
            risk = r.get('risk_level', 'Low')
            rl_class = "rl" if risk == "Low" else ("rh" if risk == "High" else "rm")
            
            st.markdown(f"""
                <div class="signal-card {is_main}">
                    <div class="rmeta">
                        <span class="rstyle">{style_name}</span>
                        <span class="rtag {rl_class}">{risk} Risk</span>
                        <span style="font-family:'JetBrains Mono', monospace; font-size:10px; color:#475569;">· NRG: {r.get('energy')}</span>
                    </div>
                    <div class="rline">"{r.get('text')}"</div>
                    <div class="rwhy">
                        {r.get('why_it_works')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Prachtig minimalistisch copy-paste blokje eronder
            st.code(r.get('text'), language="text")
            
    else:
        st.markdown("<div style='text-align:center; padding:100px 0; color:#475569; font-size:13px; font-family:\"JetBrains Mono\", monospace;'>[AWAITING DATA INTAKE...]</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align:center; opacity:0.15; font-family:\"JetBrains Mono\", monospace; font-size:0.55rem; margin-top:80px; letter-spacing:0.1em;'>SIGNAL v3.0 // NO CRINGE POLICY // POWERED BY GROK ENGINE</div>", unsafe_allow_html=True)
