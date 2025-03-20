import streamlit as st
import json
import time
import pyautogui
from pynput import mouse
from bs4 import BeautifulSoup
import requests

event_log = []

def on_click(x, y, button, pressed):
    if pressed:
        event_log.append({"x": x, "y": y, "button": str(button), "time": time.time()})
        st.write(f"Click registrado en ({x}, {y}) con {button}")

def start_recording():
    global event_log
    event_log = []
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

def save_recording():
    with open("clics.json", "w") as f:
        json.dump(event_log, f, indent=4)
    st.success("Grabación guardada en clics.json")

def load_and_replay():
    with open("clics.json", "r") as f:
        recorded_events = json.load(f)
    st.success("Reproduciendo los clics grabados...")
    start_time = recorded_events[0]["time"]
    for event in recorded_events:
        time.sleep(event["time"] - start_time)
        pyautogui.click(event["x"], event["y"])
        st.write(f"Click en ({event['x']}, {event['y']})")

def extract_html():
    url = st.text_input("Ingresa la URL para extraer HTML:")
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        with open("pagina.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        st.success("HTML extraído y guardado como 'pagina.html'")

st.title("Grabadora de Clics RPA")
if st.button("Grabar Clics"):
    start_recording()
    save_recording()
if st.button("Reproducir Clics"):
    load_and_replay()
if st.button("Extraer HTML"):
    extract_html()
