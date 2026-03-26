# --- Verbeterde Engine Core ---

def get_analysis(client, b64, ctx, dark, lang):
    lang_name = "Dutch" if lang == "NL" else "English"
    # We voegen 'Strict JSON' instructie toe aan de prompt
    prompt = f"Role: Sovereign Architect. Respond ONLY in {lang_name} using VALID JSON. Return structure: {{\"success_rate\": int, \"breakdown\": {{\"vibe\": int, \"timing\": int, \"subtext\": int}}, \"green_flags\": [str], \"red_flags\": [str], \"options\": [ {{\"type\": \"str\", \"zin\": \"str\", \"psychology\": \"str\"}} ], \"winner_idx\": int}}"
    
    try:
        res = client.chat.completions.create(
            model="grok-4.20-0309-non-reasoning",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {ctx if ctx else 'No context provided.'}"}, 
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}
            ]
        )
        
        # Veilig laden van JSON
        data = json.loads(res.choices[0].message.content)
        
        # Validatie: Check of de belangrijkste velden bestaan, anders fallback naar defaults
        if 'options' not in data or not data['options']:
             raise ValueError("Geen opties gegenereerd door AI")
             
        return data

    except json.JSONDecodeError:
        st.error("🚨 De AI gaf een ongeldig antwoordformaat. Probeer het opnieuw.")
    except Exception as e:
        st.error(f"⚠️ Systeemfout: {str(e)}")
    return None

# --- Verbeterde Interface Logica ---

# In je 'with col_l:' sectie:
if st.button(t["btn_scan"], use_container_width=True):
    if u_file is not None: # Check of er een bestand is
        with st.spinner("Analyzing Architecture..."):
            try:
                encoded_img = process_img(u_file)
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                result = get_analysis(client, encoded_img, u_ctx, is_dark, lang_choice)
                
                if result:
                    st.session_state.state = result
                    st.rerun()
            except Exception as e:
                st.error(f"Fout bij verwerken afbeelding: {e}")
    else:
        st.warning("⚠️ Upload eerst een screenshot voordat je de analyse start.")
