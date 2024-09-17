import streamlit as st
import base64
import requests
import json
import os
from dotenv import load_dotenv  

load_dotenv()

# Streamlit title and description
st.title("OrthoMia")
st.write("Carica la tua radiografia e spiega come è avvenuto l'incidente. Ottieni informazioni sulla tua lesione.")

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# Upload image and explanation
uploaded_file = st.file_uploader("Carica la tua radiografia (formato JPEG)", type=["jpg", "jpeg"])
explanation = st.text_area("Spiega come è avvenuto l'incidente", placeholder="Esempio: Ero un portiere e ho ricevuto un tiro forte durante una partita di calcio.")

# Run button to trigger the analysis
if st.button("Esegui"):
    if uploaded_file and explanation:
        # Encode the image to base64
        base64_image = encode_image(uploaded_file)

        # Set headers for the API call
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Create the payload for the API
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": "Sei un esperto di ortopedia e stai aiutando le persone che hanno subito una frattura o una rottura. Queste persone ti inviano radiografie della frattura con una descrizione dell'incidente o di come è successo. Tu devi esaminare la radiografia e la spiegazione per fornire assistenza con informazioni utili. Ricorda che, anche se non sei un medico e devi sempre consigliare ai pazienti di consultare uno specialista, puoi comunque offrire informazioni generali. Devi concentrarti su questi aspetti:\nDove si trova esattamente la frattura?\nQuanto tempo è previsto per il recupero (timeline)?\nConsigli generali per questo periodo.\nAccessori che possono essere utili (ad esempio, plastica speciale per fare la doccia)."
                },
                {
                    "role": "user",
                    "content": explanation
                },
                {
                    "role": "user",
                    "content": f"![radiografia](data:image/jpeg;base64,{base64_image})"
                }
            ],
            "max_tokens": 300
        }

        # Send the request to the OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Process the API response
        if response.status_code == 200:
            result = response.json()
            # Display the response
            st.write("Analisi:")
            st.write(result['choices'][0]['message']['content'])
        else:
            st.write("Errore:", response.status_code)
            st.write(response.text)
    else:
        st.write("Per favore, carica una radiografia e spiega l'incidente.")
