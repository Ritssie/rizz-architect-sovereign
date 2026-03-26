# --- 1. CORE SYSTEM CONFIGURATION ---
# ==============================================================================
st.set_page_config(
    page_title="Rizz Architect Sovereign v10.8", 
    page_title="Rizz Architect Sovereign v10.9", 
page_icon="👑", 
layout="wide",
initial_sidebar_state="expanded"
@@ -32,7 +32,6 @@
"upload_label": "📂 DATA SOURCE (Screenshot)",
"copy_btn": "📋",
"idle_msg": "Systeem stand-by. Upload screenshot.",
        "lang_label": "🌍 Taal / Language",
"strategy_label": "STRATEGIE",
"legal_title": "⚖️ JURIDISCHE DISCLAIMER"
},
@@ -49,7 +48,6 @@
"upload_label": "📂 DATA SOURCE (Screenshot)",
"copy_btn": "📋",
"idle_msg": "System on standby. Upload screenshot.",
        "lang_label": "🌍 Language / Taal",
"strategy_label": "STRATEGY",
"legal_title": "⚖️ LEGAL DISCLOSURE"
}
@@ -79,35 +77,27 @@

   .sovereign-card { 
       background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); 
        border-radius: 14px; padding: 22px; margin-bottom: 20px; position: relative;
        border-radius: 14px; padding: 22px; margin-bottom: 20px; position: relative; overflow: hidden;
   }
   .winner-card { border: 2px solid #fcd34d; background: linear-gradient(165deg, rgba(252, 211, 77, 0.12) 0%, rgba(1, 4, 9, 1) 100%); }

   .success-badge { 
       position: absolute; top: 15px; right: 15px; padding: 6px 14px; border-radius: 20px; 
       font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.7rem; z-index: 10;
        background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
   }

   .prob-container { margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px; }
   .prob-row { display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.75rem; margin-bottom: 8px; }

   .legal-box {
       background: rgba(248, 113, 113, 0.05); border: 1px solid rgba(248, 113, 113, 0.2); 
        border-radius: 10px; padding: 12px; color: #f87171; font-size: 0.7rem; line-height: 1.4;
        border-radius: 10px; padding: 12px; color: #f87171; font-size: 0.7rem;
   }

   .stButton>button { background: linear-gradient(90deg, #fcd34d 0%, #fbbf24 100%) !important; color: #010409 !important; font-weight: 700; border-radius: 8px; border: none !important; }
   
    /* Gevaarlijke Reboot Knop */
    .reboot-btn > div > button {
        background: transparent !important;
        color: #f87171 !important;
        border: 1px solid rgba(248, 113, 113, 0.3) !important;
    }
    .reboot-btn > div > button:hover {
        background: rgba(248, 113, 113, 0.1) !important;
        border-color: #f87171 !important;
    }
    .reboot-container { margin-top: 100px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); }
   </style>
   """, unsafe_allow_html=True)

@@ -121,8 +111,17 @@ def process_img(file):
return base64.b64encode(buf.getvalue()).decode()

def get_analysis(client, b64, ctx, dark, lang):
    lang_instr = "Dutch" if lang == "NL" else "English"
    prompt = f"Role: Sovereign Architect. Respond entirely in {lang_instr}. Output JSON: success_rate(int), breakdown{{vibe, timing, subtext}}, green_flags(list of strings or objects), red_flags, options, winner_idx."
    lang_name = "Dutch" if lang == "NL" else "English"
    prompt = f"""Role: Sovereign Architect. Respond ONLY in {lang_name}. 
    Return JSON format: 
    {{
      "success_rate": int, 
      "breakdown": {{"vibe": int, "timing": int, "subtext": int}},
      "green_flags": ["string"], 
      "red_flags": ["string"], 
      "options": [{{"type": "str", "zin": "str", "psychology": "str"}}], 
      "winner_idx": 0
    }}"""
try:
res = client.chat.completions.create(
model="grok-4.20-0309-non-reasoning",
@@ -131,7 +130,9 @@ def get_analysis(client, b64, ctx, dark, lang):
{"role": "user", "content": [{"type": "text", "text": f"Context: {ctx}"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}]
)
return json.loads(res.choices[0].message.content)
    except: return None
    except Exception as e:
        st.error(f"Engine Error: {e}")
        return None

# ==============================================================================
# --- 5. INTERFACE ASSEMBLY ---
@@ -146,23 +147,15 @@ def get_analysis(client, b64, ctx, dark, lang):
api_key = st.text_input("Grok API Key", type="password")
is_dark = st.toggle(t["dark_mode"])

    # --- JURIDISCHE SECTIE ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
    st.markdown(f"""
        <div class="legal-box">
            <b>{t['legal_title']}</b><br><br>
            Gebruik op eigen risico. Je bent zelf verantwoordelijk voor je verzonden berichten.
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="legal-box"><b>{t["legal_title"]}</b><br><br>Eigen risico. Jij bent de verzender.</div>', unsafe_allow_html=True)

    # --- REBOOT ONDERAAN ---
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='reboot-btn'>", unsafe_allow_html=True)
    st.markdown('<div class="reboot-container">', unsafe_allow_html=True)
if st.button(t["reboot"], use_container_width=True):
st.session_state.clear()
st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="brand-container"><div class="brand-logo">{t["header"]}</div></div>', unsafe_allow_html=True)

@@ -187,61 +180,71 @@ def get_analysis(client, b64, ctx, dark, lang):
if st.session_state.state:
s = st.session_state.state

            # --- SOCIAL SIGNALS (Fix voor AttributeError) ---
            # --- SIGNALS ---
st.markdown(f"<div class='section-header'>{t['tag_signals']}</div>", unsafe_allow_html=True)
sc1, sc2 = st.columns(2)
with sc1:
for gf in s.get('green_flags', []):
                    # Check of het een dict is of een string
                    label = gf.get('label', gf) if isinstance(gf, dict) else gf
                    st.markdown(f'<div class="pill pill-green">✅ {label}</div>', unsafe_allow_html=True)
                    txt = gf if isinstance(gf, str) else gf.get('label', 'Flag')
                    st.markdown(f'<div class="pill pill-green">✅ {txt}</div>', unsafe_allow_html=True)
with sc2:
for rf in s.get('red_flags', []):
                    label = rf.get('label', rf) if isinstance(rf, dict) else rf
                    st.markdown(f'<div class="pill pill-red">🚩 {label}</div>', unsafe_allow_html=True)
                    txt = rf if isinstance(rf, str) else rf.get('label', 'Flag')
                    st.markdown(f'<div class="pill pill-red">🚩 {txt}</div>', unsafe_allow_html=True)

            # --- WINNER CARD ---
            # --- WINNER CARD (REPAIRED REGEL 216) ---
st.markdown(f"<div class='section-header'>{t['tag_pick']}</div>", unsafe_allow_html=True)
            w = s['options'][s.get('winner_idx', 0)]
            b = s.get('breakdown', {'vibe': 50, 'timing': 50, 'subtext': 50})
            rate = s.get('success_rate', 0)
            color = "#fcd34d" if rate > 75 else "#f87171"

            st.markdown(f"""
                <div class="sovereign-card winner-card">
                    <div class="success-badge" style="border:1px solid {color}; color:{color}; background:rgba(0,0,0,0.5);">
                        {rate}% HIT RATE
                    </div>
                    <div style="font-size:1.25rem; font-weight:700; margin-bottom:18px; padding-right:115px; line-height:1.4; color:white;">
                        "{w.get('zin')}"
                    </div>
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:15px; border-left: 2px solid {color}; padding-left: 10px;">
                        <b>{t['strategy_label']}:</b> {w.get('psychology')}
                    </div>
                    <div class="prob-container">
                        <div class="prob-row"><span style="opacity:0.6;">VIBE</span><span style="font-weight:700; color:{color}">{b.get('vibe', 0)}%</span></div>
                        <div class="prob-row"><span style="opacity:0.6;">TIMING</span><span style="font-weight:700; color:{color}">{b.get('timing', 0)}%</span></div>
                        <div class="prob-row"><span style="opacity:0.6;">SUBTEXT</span><span style="font-weight:700; color:{color}">{b.get('subtext', 0)}%</span></div>
            
            options = s.get('options', [])
            w_idx = s.get('winner_idx', 0)
            
            if options and len(options) > w_idx:
                w = options[w_idx]
                # Veiligheidscheck: is 'w' een dictionary?
                if isinstance(w, dict):
                    zin = w.get('zin', 'Error parsing message')
                    psych = w.get('psychology', 'Strategy unavailable')
                    type_txt = w.get('type', 'CHOICE')
                else:
                    zin = str(w)
                    psych = "N/A"
                    type_txt = "CHOICE"

                b = s.get('breakdown', {'vibe': 50, 'timing': 50, 'subtext': 50})
                rate = s.get('success_rate', 0)
                color = "#fcd34d" if rate > 75 else "#f87171"

                st.markdown(f"""
                    <div class="sovereign-card winner-card">
                        <div class="success-badge" style="border:1px solid {color}; color:{color};">
                            {rate}% HIT RATE
                        </div>
                        <div style="font-size:1.25rem; font-weight:700; margin-bottom:18px; padding-right:110px; line-height:1.4; color:white;">
                            "{zin}"
                        </div>
                        <div style="font-size:0.85rem; opacity:0.8; margin-bottom:15px; border-left: 2px solid {color}; padding-left: 10px;">
                            <b style="color:{color};">{t['strategy_label']}:</b> {psych}
                        </div>
                        <div class="prob-container">
                            <div class="prob-row"><span style="opacity:0.6;">VIBE</span><span style="font-weight:700; color:{color}">{b.get('vibe', 0)}%</span></div>
                            <div class="prob-row"><span style="opacity:0.6;">TIMING</span><span style="font-weight:700; color:{color}">{b.get('timing', 0)}%</span></div>
                            <div class="prob-row"><span style="opacity:0.6;">SUBTEXT</span><span style="font-weight:700; color:{color}">{b.get('subtext', 0)}%</span></div>
                        </div>
                   </div>
                </div>
            """, unsafe_allow_html=True)
            st.code(w.get('zin'), language=None)
                """, unsafe_allow_html=True)
                st.code(zin, language=None)

# --- ALTERNATIVES ---
st.markdown(f"<div class='section-header' style='margin-top:40px;'>{t['tag_dims']}</div>", unsafe_allow_html=True)
            for i, opt in enumerate(s.get('options', [])):
                if i != s.get('winner_idx', 0):
            for i, opt in enumerate(options):
                if i != w_idx:
                    alt_zin = opt.get('zin', str(opt)) if isinstance(opt, dict) else str(opt)
c1, c2 = st.columns([5, 1])
with c1:
                        st.markdown(f"""
                            <div class="sovereign-card" style="margin-bottom:12px;">
                                <div style="font-size:0.6rem; opacity:0.5; font-family:JetBrains Mono;">{opt.get('type', 'ALT')}</div>
                                <b>"{opt.get('zin')}"</b>
                            </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f'<div class="sovereign-card" style="margin-bottom:12px;"><b>"{alt_zin}"</b></div>', unsafe_allow_html=True)
with c2:
st.write(""); st.button(t["copy_btn"], key=f"c_{i}")
else:
st.info(t["idle_msg"])

st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V10.8 | TYPE-SAFE</div>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; opacity:0.1; font-size:0.6rem; margin-top:50px;'>SOVEREIGN ENGINE V10.9 | FINAL STABILITY</div>", unsafe_allow_html=True)
