import streamlit as st
from openai import OpenAI

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="MAGI SYSTEM - NERV HQ Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STILE CSS PERSONALIZZATO (EVANGELION MAGI SYSTEM INTERFACE) ---
magi_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

/* Sfondo Dark Generale */
.stApp {
    background-color: #050303 !important;
    color: #ff5500 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Nasconde elementi predefiniti di Streamlit */
header, footer {
    visibility: hidden;
}

/* Sidebar NERV */
[data-testid="stSidebar"] {
    background-color: #0e0403 !important;
    border-right: 2px solid #ff3300 !important;
}

/* Font e Colori per Headings e Label */
h1, h2, h3, h4, h5, h6, label, p, span {
    font-family: 'Share Tech Mono', monospace !important;
    color: #ff5500 !important;
}

/* Banner Superiore - NERV MAGI HUD Header */
.magi-hud-header {
    border: 2px solid #ff3300;
    padding: 15px 20px;
    background-color: #120302;
    margin-bottom: 25px;
    box-shadow: 0 0 15px rgba(255, 51, 0, 0.4);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.hud-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 32px;
    font-weight: 900;
    color: #ff3300;
    letter-spacing: 3px;
    margin: 0;
    text-shadow: 0 0 12px #ff3300;
}

.hud-code {
    font-size: 13px;
    color: #ffaa00;
    letter-spacing: 1px;
    line-height: 1.4;
}

/* Input di Testo in Stile Terminale */
.stTextInput > div > div > input {
    background-color: #0a0404 !important;
    color: #00ff66 !important;
    border: 2px solid #ff3300 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 16px !important;
    border-radius: 0px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #00ff66 !important;
    box-shadow: 0 0 12px rgba(0, 255, 102, 0.6) !important;
}

/* Carte MAGI Verdi Poligonali (Anime Style) */
.magi-card {
    background-color: #20f070;
    color: #000000;
    padding: 22px;
    margin-bottom: 15px;
    clip-path: polygon(25px 0, 100% 0, 100% calc(100% - 25px), calc(100% - 25px) 100%, 0 100%, 0 25px);
    box-shadow: 0 0 20px rgba(32, 240, 112, 0.5);
    min-height: 280px;
}

.magi-card-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 24px;
    font-weight: 900;
    color: #000000;
    border-bottom: 3px solid #000000;
    padding-bottom: 6px;
    margin-bottom: 15px;
    letter-spacing: 2px;
}

.magi-card-body {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 15px;
    color: #000000;
    line-height: 1.5;
    font-weight: bold;
    white-space: pre-wrap;
}

/* Riquadro di Valutazione del Consenso (Giudice) */
.consensus-box {
    border: 3px solid #ff3300;
    background-color: #0d0202;
    padding: 25px;
    margin-top: 25px;
    box-shadow: 0 0 25px rgba(255, 51, 0, 0.5);
}

.consensus-title {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 22px;
    color: #ffaa00;
    text-shadow: 0 0 10px #ff5500;
    border-bottom: 2px dashed #ff3300;
    padding-bottom: 10px;
    margin-bottom: 15px;
}

.consensus-body {
    font-size: 16px;
    color: #ffcc00;
    line-height: 1.6;
}

/* Badge di Stato */
.badge-green {
    background-color: #00ff66;
    color: #000;
    padding: 3px 8px;
    font-weight: bold;
    font-size: 12px;
    border: 1px solid #000;
}

.badge-orange {
    background-color: #ff9900;
    color: #000;
    padding: 3px 8px;
    font-weight: bold;
    font-size: 12px;
}
</style>
"""

st.markdown(magi_css, unsafe_allow_html=True)

# --- HEADER NERV MAGI ---
st.markdown("""
<div class="magi-hud-header">
    <div>
        <div class="hud-title">MAGI SYSTEM 3.0</div>
        <div style="color: #00ff66; font-size: 12px; font-weight: bold; margin-top: 4px;">● ALL GREEN / 終了</div>
    </div>
    <div class="hud-code">
        CODE : 127 | FILE : AKAGI_CHK<br>
        EXTENTION : 0256 | EX_MODE : ON<br>
        PRIORITY : A-- | NERV HQ TOKYO-3
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar per la configurazione
OPENROUTER_API_KEY = st.sidebar.text_input("OpenRouter API Key (Gratuita)", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size: 12px; color: #ff8800;'>
<b>SISTEMA TRINITA MAGI:</b><br>
• MELCHIOR-1 (Scienziata)<br>
• BALTHASAR-2 (Madre)<br>
• CASPER-3 (Donna)<br>
</div>
""", unsafe_allow_html=True)

query = st.text_input("INSERISCI IL QUESITO PER IL SISTEMA MAGI / 質問入力:", placeholder="Es: Risolvi x^2 + 5x + 6 = 0 oppure poni un dilemma etico...")

def risposta_ia(model_name, prompt):
    if not OPENROUTER_API_KEY:
        return "ERRORE: Inserisci la tua API Key nella barra laterale."
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "Sei un supercomputer MAGI di Evangelion. Rispondi in modo sintetico introducendo subito la soluzione o risposta finale, seguita da una brevissima spiegazione."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback automatico su router libero se il modello specifico va in rate limit
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY,
            )
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {"role": "system", "content": "Sei un supercomputer MAGI di Evangelion. Rispondi in modo sintetico introducendo subito la soluzione o risposta finale, seguita da una brevissima spiegazione."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as inner_e:
            return f"Errore Elaborazione MAGI: {str(inner_e)}"

if query:
    if not OPENROUTER_API_KEY:
        st.warning("⚠️ INSERISCI LA TUA OPENROUTER API KEY NELLA BARRA LATERALE PER PROCEDERE.")
    else:
        st.markdown(f"<div style='color: #ffaa00; margin-bottom: 15px;'><b>ANALISI IN CORSO PER:</b> {query}</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        # --- MELCHIOR-1 ---
        with col1:
            with st.spinner("ELABORAZIONE MELCHIOR-1..."):
                res1 = risposta_ia("openrouter/free", query)
            st.markdown(f"""
            <div class="magi-card">
                <div class="magi-card-title">MELCHIOR · 1</div>
                <div class="magi-card-body">{res1}</div>
            </div>
            """, unsafe_allow_html=True)

        # --- BALTHASAR-2 ---
        with col2:
            with st.spinner("ELABORAZIONE BALTHASAR-2..."):
                res2 = risposta_ia("nvidia/nemotron-3-super-120b-a12b:free", query)
            st.markdown(f"""
            <div class="magi-card">
                <div class="magi-card-title">BALTHASAR · 2</div>
                <div class="magi-card-body">{res2}</div>
            </div>
            """, unsafe_allow_html=True)

        # --- CASPER-3 ---
        with col3:
            with st.spinner("ELABORAZIONE CASPER-3..."):
                res3 = risposta_ia("openrouter/free", query)
            st.markdown(f"""
            <div class="magi-card">
                <div class="magi-card-title">CASPER · 3</div>
                <div class="magi-card-body">{res3}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # --- VALUTAZIONE DEL CONSENSO (GIUDICE MAGI) ---
        with st.spinner("VERIFICA CONSENSO MAGI IN CORSO..."):
            judge_prompt = f"""
            Analizza le seguenti 3 risposte alla domanda: "{query}"

            Risposta 1 (Melchior-1): {res1}
            Risposta 2 (Balthasar-2): {res2}
            Risposta 3 (Casper-3): {res3}

            Svolgi i seguenti compiti:
            1. Determina se le 3 risposte sono d'accordo sulla soluzione finale (Unanime, Maggioranza o Disaccordo).
            2. Indica la percentuale stimata di accordo (es. 100%, 66%, 0%).
            3. Fornisci la RISPOSTA DEFINITIVA validata dal sistema.
            """
            
            verdetto = risposta_ia("openrouter/free", judge_prompt)

        st.markdown(f"""
        <div class="consensus-box">
            <div class="consensus-title">⚖️ VALUTAZIONE DEL CONSENSO / 審議判定</div>
            <div class="consensus-body">{verdetto}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Visualizza dati grezzi per debugging / 生データ"):
            st.write(f"**Melchior-1:** {res1}")
            st.write(f"**Balthasar-2:** {res2}")
            st.write(f"**Casper-3:** {res3}")
```eof

Il codice aggiornato è pronto! Ecco cosa ho aggiunto per riprodurre fedelmente la grafica di Evangelion:

- **Riquadri Poligonali Verdi Aggiustati (`clip-path`):** I blocchi per **MELCHIOR·1**, **BALTHASAR·2** e **CASPER·3** hanno gli angoli smussati a taglio e lo sfondo verde brillante con testo nero in grassetto, proprio come nell'immagine che hai inviato.
- **Header HUD NERV HQ:** In alto appare il pannello di controllo con scritte HUD (`CODE : 127`, `FILE : AKAGI_CHK`, `ALL GREEN / 終了`).
- **Pannello del Consenso:** Il riquadro in basso per la decisione finale ha un bordo arancione/rosso al neon con ombra radiante.
- **Font Retrò/Tech:** Ho caricato da Google Fonts le famiglie di caratteri *Orbitron* e *Share Tech Mono* per ricreare la tipografia dell'anime.

Ti basterà copiare e incollare questo codice nel tuo file `magi_app.py` su GitHub e fare il **Commit changes**: la tua app si aggiornerà con la nuova grafica in pochissimi secondi!
