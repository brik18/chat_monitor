from fastapi import FastAPI
from services import (stop_monitoring , start_monitoring, analize_chat)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/chat/analize")
def read_item():
    return analize_chat()


@app.post("/start/monitor")
def start_monitor(url:str):
    return start_monitoring(url)


@app.post("/stop/monitor")
def start_monitor():
    return stop_monitoring()