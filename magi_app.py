import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="MAGI System Terminal", layout="wide")

st.title("🔴 MAGI SYSTEM - Terminale Decisionale (Free Edition)")
st.markdown("---")

OPENROUTER_API_KEY = st.sidebar.text_input("OpenRouter API Key (Gratuita)", type="password")

query = st.text_input("Inserisci il quesito o l'equazione da analizzare:", placeholder="Es: Risolvi x^2 + 5x + 6 = 0")

def risposta_ia(model_name, prompt):
    if not OPENROUTER_API_KEY:
        return "Errore: Inserisci la tua API Key nella barra laterale."
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Sei un assistente preciso. Rispondi in modo sintetico introducendo subito la soluzione o risposta finale, seguita da una brevissima spiegazione."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Errore con {model_name}: {str(e)}"

if query:
    if not OPENROUTER_API_KEY:
        st.warning("⚠️ Inserisci la tua OpenRouter API Key nella barra laterale per procedere.")
    else:
        st.write(f"**Analisi in corso per:** {query}")
        
        col1, col2, col3 = st.columns(3)
        
        # Agente 1: Llama 3.3 70B (Gratuito)
        with col1:
            st.subheader("MELCHIOR (Llama 3.3)")
            with st.status("Elaborazione...", expanded=True):
                res1 = risposta_ia("meta-llama/llama-3.3-70b-instruct:free", query)
                st.write(res1)
                st.success("Completato")

        # Agente 2: Mistral Small (Gratuito)
        with col2:
            st.subheader("BALTHASAR (Mistral Small)")
            with st.status("Elaborazione...", expanded=True):
                res2 = risposta_ia("mistralai/mistral-small-24b-instruct-2501:free", query)
                st.write(res2)
                st.success("Completato")

        # Agente 3: Qwen 2.5 72B (Gratuito)
        with col3:
            st.subheader("CASPER (Qwen 2.5)")
            with st.status("Elaborazione...", expanded=True):
                res3 = risposta_ia("qwen/qwen-2.5-72b-instruct:free", query)
                st.write(res3)
                st.success("Completato")

        st.markdown("---")

        # --- FASE DI VALUTAZIONE DEL CONSENSO (GIUDICE) ---
        st.subheader("⚖️ Valutazione del Consenso")
        with st.spinner("Confronto delle risposte in corso..."):
            judge_prompt = f"""
            Analizza le seguenti 3 risposte alla domanda: "{query}"

            Risposta 1 (Melchior): {res1}
            Risposta 2 (Balthasar): {res2}
            Risposta 3 (Casper): {res3}

            Svolgi i seguenti compiti:
            1. Determina se le 3 risposte sono d'accordo sulla soluzione finale (Unanime, Maggioranza o Disaccordo).
            2. Indica la percentuale stimata di accordo (es. 100%, 66%, 0%).
            3. Fornisci la RISPOSTA DEFINITIVA validata dal sistema.
            """
            
            # Giudice Gratuito
            verdetto = risposta_ia("meta-llama/llama-3.3-70b-instruct:free", judge_prompt)
            st.markdown(verdetto)

        with st.expander("Visualizza risposte grezze per debugging"):
            st.write(f"**Melchior:** {res1}")
            st.write(f"**Balthasar:** {res2}")
            st.write(f"**Casper:** {res3}")
