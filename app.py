import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import json
import re

# ==============================================================================
# --- 1. THE PURGE: VERWIJDER ELKE EMOJI UIT HET GEHEUGEN ---
# ==============================================================================

def clean_text_strict(text):
    """
    Forceert tekst naar pure ASCII. 
    Verwijdert de kroon-emoji (\U0001f451) en elk ander non-standard teken.
    """
    if not text:
        return ""
    # We coderen naar ascii en negeren alles wat fout gaat.
    return text.encode("ascii", "ignore").decode("ascii")

# Pagina instellen zonder titels met speciale tekens
st.set_page_config(page_title="Architect v19.8", layout="wide")

if 'result_storage' not in st.session_state:
    st.session_state.result_storage = None

# ==============================================================================
# --- 2. ULTRA-CLEAN UI (STRICT ASCII) ---
# ==============================================================================
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000 !important;
        color: #fff !important;
        font-family: monospace;
    }
    .main-header { font-size: 2rem; font-weight: bold; text-align: center; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 10px; }
    .card { background: #111; border: 1px solid #333; padding: 15px; border-radius: 5px; margin-bottom: 10px; }
    .winner { border: 1px solid #FFD700 !important; }
    .stButton>button { background: #fff !important; color: #000 !important; font-weight: bold; width: 100%; border-radius: 0; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# --- 3. THE ENGINE (NO LOGGING) ---
# ==============================================================================

def img_to_b64(file):
    """Afbeelding naar b64 zonder metadata."""
    try:
        img = Image.open(file).convert('RGB')
        img.thumbnail((800, 800))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode('ascii')
    except:
        return None

def analyze_chat(api_key, b64_img, context):
    """Aanroep naar Grok met extreme fout-isolatie."""
    # Gebruik geen 'with' of complexe logging om codec errors te vermijden
    client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
    
    # Instructies in puur ASCII
    sys_msg = "Role: Expert. Analyze dating chat. Return JSON: {rate:int, pos:[], neg:[], moves:[{type:str, text:str}], best_idx:int, why:str}"

    try:
        # We maken de context 'schoon' voor verzending
        safe_context = clean_text_strict(context)
        
        response = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": clean_text_strict(sys_msg)},
                {"role": "user", "content": [
                    {"type": "text", "text": safe_context},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}}
                ]}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # We vangen de error en strippen hem onmiddellijk van de emoji die de crash veroorzaakt
        raw_error = str(e)
        safe_error = clean_text_strict(raw_error)
        st.error(f"Engine Error: {safe_error}")
        return None

# ==============================================================================
# --- 4. INTERFACE ---
# ==============================================================================

st.markdown('<div class="main-header">RIZZ ARCHITECT 19.8</div>', unsafe_allow_html=True)

with st.sidebar:
    st.write("--- SETTINGS ---")
    key = st.text_input("API Key", type="password")
    if st.button("RESET"):
        st.session_state.clear()
        st.rerun()

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.write("--- INPUT ---")
    up = st.file_uploader("Screenshot", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if up:
        st.image(up, width='stretch')
    
    ctx = st.text_area("CONTEXT", height=100)
    
    if st.button("ANALYZE"):
        if key and up:
            with st.spinner("..."):
                b64 = img_to_b64(up)
                res = analyze_chat(key, b64, ctx)
                if res:
                    st.session_state.result_storage = res
                    st.rerun()

with col2:
    st.write("--- RESULTS ---")
    if st.session_state.result_storage:
        r = st.session_state.result_storage
        
        st.write(f"SUCCESS RATE: {r.get('rate', 0)}%")
        
        st.write("POSITIVE SIGNALS:")
        for p in r.get('pos', []):
            st.write(f"- {clean_text_strict(p)}")
            
        st.write("NEGATIVE SIGNALS:")
        for n in r.get('neg', []):
            st.write(f"- {clean_text_strict(n)}")
            
        st.write("STRATEGY:")
        moves = r.get('moves', [])
        best = r.get('best_idx', 0)
        
        for i, m in enumerate(moves):
            style = "card winner" if i == best else "card"
            st.markdown(f"""
                <div class="{style}">
                    <div style="font-size:0.7rem; color: #888;">{clean_text_strict(m['type'])}</div>
                    <div>{clean_text_strict(m['text'])}</div>
                </div>
            """, unsafe_allow_html=True)
            st.code(m['text'], language=None)
            
        st.info(clean_text_strict(r.get('why', '')))
    else:
        st.write("Awaiting data...")

st.markdown("<br><hr><div style='text-align:center; opacity:0.1; font-size:0.5rem;'>BUILD_19.8_STABLE_NO_UNICODE</div>", unsafe_allow_html=True)
