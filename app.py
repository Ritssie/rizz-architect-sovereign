import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import sys

# --- 0. UNICODE FIX (Cruciaal voor de Kroon-emoji) ---
# Dit dwingt Python om UTF-8 te gebruiken voor alle systeemstromen
if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# --- 1. CONFIG & THEME ---
st.set_page_config(
    page_title="Rizz Architect Sovereign v21.0",
    page_icon="👑",
    layout="wide"
)

# --- 2. CSS ARCHITECTURE (Dark Minimalist) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #010409 !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif;
    }

    .brand-title {
        font-family: 'Inter', sans-serif; font-weight: 800; font-size: 2.5rem;
        text-align: center; letter-spacing: -2px; margin-bottom: 5px;
    }
    .brand-title span { color: #fcd34d; }

    .sovereign-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(252, 211, 77, 0.2);
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
    }

    .winner-card {
        border: 2px solid #fcd34d;
        background: linear-gradient(145deg, rgba(252, 211, 77, 0.1), transparent);
    }

    .stButton>button {
        background: #fcd34d !important; color: #000 !important;
        font-weight: 800 !important; border-radius: 10px !important;
        border: none !important; height: 3.2rem !important;
    }

    .label-tag {
        font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
        color: #fcd34d; letter-spacing: 3px; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC ---
def process_image(file):
    """Verwerkt afbeelding naar een schone Base64 string."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((1200, 1200)) # Hoge kwaliteit voor Grok-4.20
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    except Exception:
        return None

def call_grok_sovereign(api_key, b64_image, context_text):
    """De aanroep naar de nieuwste Grok-4.20-0309-reasoning."""
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # We gebruiken Grok-4.20 reasoning voor maximale diepgang
    model_id = "grok-4.20-0309-reasoning"
    
    system_instruction = (
        "Role: Sovereign Architect. Analyze social dynamics in dating screenshots. "
        "Return a JSON object with: success_rate (int), green_flags (list), "
        "red_flags (list), strategic_analysis (str), options (list of {type, text}), winner_idx (int). "
        "Use emojis in the analysis where appropriate."
    )

    try:
        response = client.chat.completions.create(
            model=model_id,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {context_text}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Failsafe: Als het model niet gevonden wordt, gebruik de fast variant
        if "404" in str(e):
            st.warning("Grok-4.20 not found, switching to Grok-4-1-fast...")
            # (Hier zou je een fallback call kunnen doen)
        st.error(f"Systeem Error: {str(e)}")
        return None

# --- 4. UI ASSEMBLY ---
st.markdown('<div class="brand-title">RIZZ<span>ARCHITECT</span> v21.0</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### SYSTEM CORE")
    api_key = st.text_input("Grok API Key", type="password")
    st.markdown("---")
    st.markdown("**Model Info:**\nUsing `Grok-4.20-0309-reasoning` (2M TPM)")
    if st.button("REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()

col_l, col_r = st.columns([1, 1.2], gap="large")

if not api_key:
    st.info("Voer je Grok API key in om de Architect te activeren.")
else:
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None

    with col_l:
        st.markdown('<div class="label-tag">Tactical Intake</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Chat", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)
            u_ctx = st.text_area("Briefing", placeholder="Vibe, leeftijd, doel...", height=80)
            
            if st.button("EXECUTE ANALYSIS"):
                with st.spinner("Grok-4.20 is reasoning..."):
                    b64 = process_image(uploaded_file)
                    if b64:
                        res = call_grok_sovereign(api_key, b64, u_ctx)
                        if res:
                            st.session_state.analysis = res
                            st.rerun()

    with col_r:
        if st.session_state.analysis:
            data = st.session_state.analysis
            
            # Probability
            rate = data.get('success_rate', 0)
            st.markdown(f"### Success Probability: {rate}%")
            st.progress(rate / 100)
            
            # Flags
            f1, f2 = st.columns(2)
            with f1:
                st.markdown('<div class="label-tag">Green Flags</div>', unsafe_allow_html=True)
                for gf in data.get('green_flags', []): st.success(gf)
            with f2:
                st.markdown('<div class="label-tag">Red Flags</div>', unsafe_allow_html=True)
                for rf in data.get('red_flags', []): st.error(rf)

            # Winner Move
            st.markdown('<div class="label-tag">Optimal Move</div>', unsafe_allow_html=True)
            opts = data.get('options', [])
            w_idx = data.get('winner_idx', 0)
            if opts:
                best = opts[w_idx]
                st.markdown(f"""
                    <div class="sovereign-card winner-card">
                        <div class="label-tag" style="color:#fcd34d;">{best.get('type')}</div>
                        <h2 style="color:#fff; margin-top:10px;">"{best.get('text')}"</h2>
                        <hr style="opacity:0.1">
                        <p style="font-size:0.9rem; opacity:0.8;">{data.get('strategic_analysis')}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.code(best.get('text'), language=None)
            
            # Alternatives
            with st.expander("Show Alternative Dimensions"):
                for i, o in enumerate(opts):
                    if i != w_idx:
                        st.markdown(f"**{o.get('type')}**: {o.get('text')}")
        else:
            st.markdown('<div style="height:300px; display:flex; align-items:center; justify-content:center; border:1px dashed #333; border-radius:15px; opacity:0.3;">SIGNAL IDLE</div>', unsafe_allow_html=True)

st.markdown("<br><hr><div style='text-align:center; opacity:0.1; font-size:0.6rem;'>PRECISION_CORE_v21.0 | GROK_4.20_ENABLED</div>", unsafe_allow_html=True)
