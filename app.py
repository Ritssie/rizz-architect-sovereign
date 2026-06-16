import streamlit as st
from openai import OpenAI
import base64
import json

# ==============================================================================
# --- 1. CONFIG & SIGNAL UI DESIGN ---
# ==============================================================================
st.set_page_config(page_title="Signal v3 — Conversatie Analyse", page_icon="📡", layout="wide")

if 'state' not in st.session_state: 
    st.session_state.state = None

# Minimalistische, strakke CSS-styling gebaseerd op de HTML-versie
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0a0a0f !important; 
        color: #f1f5f9 !important; 
        font-family: 'Inter', sans-serif; 
    }

    /* Badge & Card Styles */
    .custom-badge {
        display: inline-flex; align-items: center; gap: 4px; font-size: 11px;
        padding: 4px 10px; border-radius: 20px; border: 0.5px solid; margin-right: 5px; margin-bottom: 5px;
    }
    .b-purple { background: #EEEDFE; color: #3C3489; border-color: #CECBF6; }
    .b-teal   { background: #E1F5EE;  color: #085041;  border-color: #9FE1CB; }
    .b-amber  { background: #FAEEDA;  color: #854F0B;  border-color: #FAC775; }

    /* Custom Signal Card Grid */
    .signal-card {
        background: #111118; border: 0.5px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 15px; margin-bottom: 12px;
    }
    .signal-card.main-char { border-color: #AFA9EC !important; }
    
    .rmeta { display: flex; align-items: center; gap: 6px; margin-bottom: 8px; }
    .rstyle { font-size: 10px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: #94a3b8; }
    .rtag { font-size: 10px; padding: 2px 7px; border-radius: 10px; }
    .rl { background: #E1F5EE; color: #085041; }
    .rm { background: #FAEEDA; color: #854F0B; }
    .rh { background: #FAECE7; color: #993C1D; }
    
    /* Flags Pillen */
    .pill { font-size: 11px; padding: 6px 10px; border-radius: 6px; margin-bottom: 6px; line-height: 1.4; border: 0.5px solid; }
    .g-p { background: #E1F5EE; color: #085041; border-color: #9FE1CB; }
    .r-p { background: #FAECE7; color: #993C1D; border-color: #F5C4B3; }
    .n-p { background: #EEEDFE; color: #3C3489; border-color: #CECBF6; }
    .a-p { background: #FAEEDA; color: #854F0B; border-color: #FAC775; }

    .analysis-box {
        font-size: 13px; color: #94a3b8; background: #111118;
        border-radius: 8px; padding: 12px; line-height: 1.6; margin-bottom: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 2. STRATEGIC ENGINE (Grok / OpenAI-compatibel) ---
# ==============================================================================
def run_signal_scan(api_key, chat_text, chat_b64, bio_text, vibe, platform, stage):
    # Initialiseer de OpenAI client met de Grok URL
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

    # Gebruikers invoer combineren voor Grok Vision / Text
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
st.markdown("<h1 style='text-align:center; font-weight:500; margin-bottom:0;'>Signal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:13px; color:#475569; margin-bottom:30px;'>Conversatie-intelligentie · v3 (Grok Edition)</p>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎚️ SIGNAL CONTROLS")
    api_key = st.text_input("Grok API Key", type="password", placeholder="xai-...")
    plat = st.selectbox("Platform", ["Hinge", "Tinder", "Bumble", "Instagram DMs", "TikTok DMs", "Breeze", "WhatsApp"])
    vibe = st.selectbox("Jouw Vibe", ["Low-key Banter", "Unhinged / Meme", "Delusional / Bold", "Soft Launch", "Dry / Sarcastic", "Direct & Calm"])
    stage = st.selectbox("Situationship Fase", ["Talking Stage", "Almost Dating", "DTR Zone", "Post-Sitch"])
    st.markdown("---")
    if st.button("RESET SYSTEM"): 
        st.session_state.state = None
        st.rerun()

col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown("#### 📥 INTEL INTAKE")
    u_transcript = st.text_area("Chat Transcript", placeholder="Plak hier de gekopieerde chat (WhatsApp, DMs...)", height=150)
    
    u_chat = st.file_uploader("Drop screenshot hier", type=['png','jpg','jpeg'])
    
    c_b64 = None
    if u_chat: 
        st.image(u_chat, use_container_width=True, caption="Chat Preview")
        c_b64 = base64.b64encode(u_chat.getvalue()).decode()

    u_bio = st.text_area("Context (Optioneel)", placeholder="Bio, interesses, wat weet je over hen...", height=70)
    
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
    st.markdown("#### 📡 STRATEGIC DASHBOARD")
    
    if st.session_state.state:
        s = st.session_state.state
        met = s.get('metrics', {})
        
        # Badges Bovenaan
        st.markdown(f"""
            <span class='custom-badge b-teal'>📈 {s.get('detected_stage', '—')} stage</span>
            <span class='custom-badge b-purple'>🎭 Toon: {s.get('tone', '—')}</span>
            <span class='custom-badge b-amber'>❤️ {stage}</span>
        """, unsafe_allow_html=True)
        
        # Metrics Matrix (4 cellen)
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Haar Inves.", f"{met.get('her_investment', 0)}%")
        m_col2.metric("Jouw Signaal", f"{met.get('signal_strength', 0)}%")
        m_col3.metric("Try-hard", f"{met.get('try_hard_score', 0)}%")
        m_col4.metric("Ghost Risk", f"{met.get('ghost_risk', 0)}%")
        
        st.markdown("<hr style='margin:15px 0; border:0; border-top:0.5px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
        
        # Flags & Signalen Matrix (2x2 indeling)
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown("<div style='font-size:10px; color:#1D9E75; font-weight:600; margin-bottom:6px;'>GREEN FLAGS</div>", unsafe_allow_html=True)
            for f in s.get('green_flags', []): st.markdown(f"<div class='pill g-p'>{f}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='font-size:10px; color:#534AB7; font-weight:600; margin-top:10px; margin-bottom:6px;'>JOUW SIGNALEN</div>", unsafe_allow_html=True)
            for f in s.get('self_signals', []): st.markdown(f"<div class='pill n-p'>{f}</div>", unsafe_allow_html=True)
            
        with f_col2:
            st.markdown("<div style='font-size:10px; color:#D85A30; font-weight:600; margin-bottom:6px;'>RED FLAGS</div>", unsafe_allow_html=True)
            for f in s.get('red_flags', []): st.markdown(f"<div class='pill r-p'>{f}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='font-size:10px; color:#854F0B; font-weight:600; margin-top:10px; margin-bottom:6px;'>MOGELIJKE ICKS</div>", unsafe_allow_html=True)
            for f in s.get('potential_icks', []): st.markdown(f"<div class='pill a-p'>{f}</div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:15px 0; border:0; border-top:0.5px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
        
        # Eerlijke Analyse Box
        st.markdown(f"<div class='analysis-box'>{s.get('analysis', '')}</div>", unsafe_allow_html=True)
        
        # Antwoorden renderen
        st.markdown("<span class='lbl'>Voorgestelde Replies</span>", unsafe_allow_html=True)
        for idx, r in enumerate(s.get('replies', [])):
            is_main = "main-char" if r.get('style') == "Main Character" else ""
            risk = r.get('risk_level', 'Low')
            rl_class = "rl" if risk == "Low" else ("rh" if risk == "High" else "rm")
            
            st.markdown(f"""
                <div class="signal-card {is_main}">
                    <div class="rmeta">
                        <span class="rstyle">{r.get('style')}</span>
                        <span class="rtag {rl_class}">{risk} Risk</span>
                        <span style="font-size:10px; color:#475569;">· Energy: {r.get('energy')}</span>
                    </div>
                    <div style="font-size:16px; font-weight:500; margin-bottom:8px;">"{r.get('text')}"</div>
                    <div style="font-size:12px; color:#94a3b8; border-top:0.5px solid rgba(255,255,255,0.08); padding-top:8px;">
                        {r.get('why_it_works')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Gemakkelijke copy-box
            st.code(r.get('text'), language="text")
            
    else:
        st.info("Voer een chat in of upload een screenshot om te beginnen.")

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.5rem; margin-top:50px;'>SIGNAL v3.0 · NO CRINGE POLICY · POWERED BY GROK ENGINE</div>", unsafe_allow_html=True)
