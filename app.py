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
            box-shadow: 0 4px 12px rgba(0,0,0,0.1
