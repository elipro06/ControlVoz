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

# ==== ESTILOS MÁS SIMPLES Y EFECTIVOS ====
st.markdown("""
    <style>
        .stApp {
            background-color: #f9f9f9;
            font-family: sans-serif;
        }

        h1, h3, p {
            color: #222222;
            text-align: center;
        }
