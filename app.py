import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json

def on_publish(client, userdata, result):
    print("Mensaje enviado correctamente")

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.markdown(f"<div class='mensaje'>{message_received}</div>", unsafe_allow_html=True)

broker = "157.230.214.127"
port = 1883
client1 = paho.Client("VOICE-CLIENT")
client1.on_message = on_message

# Estilos actualizados
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        .stApp {
            background-color: #f1f8f6;
            font-family: 'Inter', sans-serif;
            padding: 1rem;
        }

        h1, h2, h3, p {
            color: #003d33;
            text-align: center;
        }

        .stButton>button {
            background: linear-gradient(to right, #009688, #00796b);
            color: white;
            border-radius: 12px;
            padding: 0.5em 1.5em;
            border: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .stButton>button:hover {
            background: #004d40;
            transform: scale(1.05);
        }

        .caja {
            background-color: #ffffff;
            border-left: 5px solid #009688;
            padding: 1.8em;
            border-radius: 14px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            margin-top: 1em;
        }

        .mensaje {
            background-color: #c8e6c9;
            padding: 1em;
            border-radius: 10px;
            margin-top: 1em;
            text-align: center;
            font-weight: 600;
            font-size: 1rem;
            color: #2e7d32;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🗣️ Sistema de Control por Voz</h1>", unsafe_allow_html=True)
st.markdown("<h3>Interactúa con comandos hablados</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    image = Image.open("voz.png")
    st.image(image, use_container_width=True)

with col2:
    st.markdown("<div class='caja'>", unsafe_allow_html=True)
    st.markdown("<p>Presiona el botón y habla claramente para controlar el sistema</p>", unsafe_allow_html=True)

    stt_button = Button(label="🎤 Iniciar Reconocimiento", width=260)

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
    """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="speech_control",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0
    )

    st.markdown("</div>", unsafe_allow_html=True)

if result and "GET_TEXT" in result:
    text_result = result.get("GET_TEXT")
    st.markdown(f"<div class='mensaje'>📢 {text_result}</div>", unsafe_allow_html=True)
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": text_result.strip()})
    ret = client1.publish("voice_ctrl", message)

    try:
        os.mkdir("temp")
    except:
        pass
