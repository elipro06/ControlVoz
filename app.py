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

# ==== ESTILOS CON TEXTO NEGRO ====
st.markdown("""
    <style>
        .stApp {
            background-color: #f9f9f9;
            font-family: sans-serif;
        }

        h1, h3, p, div, .mensaje {
            color: #000000 !important;
            text-align: center;
        }

        .stButton>button {
            background-color: #005bbb;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .stButton>button:hover {
            background-color: #004999;
        }

        .caja {
            background-color: #ffffff;
            border-left: 5px solid #005bbb;
            padding: 1.2em;
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            margin-top: 1em;
            text-align: center;
        }

        .mensaje {
            margin-top: 1em;
            background-color: #e3f2fd;
            padding: 1em;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ==== INTERFAZ ====
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

# ==== RESULTADO ====
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
