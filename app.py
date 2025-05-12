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

# ======= ESTILOS MEJORADOS =======
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

        .stApp {
            background-color: #ffffff;
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3, p {
            color: #1a1a1a;
            font-size: 1.3rem;
            text-align: center;
        }

        .stButton>button {
            background-color: #4a90e2;
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 0.75em 1.5em;
            font-size: 1rem;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #357ABD;
            transform: scale(1.05);
        }

        .caja {
            background-color: #f2f6fa;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #4a90e2;
            margin-top: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .mensaje {
            margin-top: 1.5rem;
            padding: 1rem;
            background-color: #e8f0fe;
            color: #1a237e;
            font-size: 1.2rem;
            font-weight: 600;
            text-align: center;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ======= CONTENIDO DE LA APP =======
st.markdown("<h1>Sistema de Control de Voz</h1>", unsafe_allow_html=True)
st.markdown("<h3>Interacción mediante audio</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    image = Image.open("voz.png")
    st.image(image, use_container_width=True)

with col2:
    st.markdown("<div class='caja'>", unsafe_allow_html=True)
    st.markdown("<p>Presiona el botón y habla claramente para controlar el sistema</p>", unsafe_allow_html=True)

    stt_button = Button(label="🎙️ Iniciar Reconocimiento", width=260)

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
    st.markdown(f"<div class='mensaje'>{text_result}</div>", unsafe_allow_html=True)
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": text_result.strip()})
    ret = client1.publish("voice_ctrl", message)

    try:
        os.mkdir("temp")
    except:
        pass

