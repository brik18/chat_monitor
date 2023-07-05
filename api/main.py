from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import stop_monitoring, start_monitoring, analize_chat

app = FastAPI()

# Agregar el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/chat/analize")
def read_item():
    return analize_chat()


@app.post("/start/monitor")
def start_monitor(url: str):
    return start_monitoring(url)


@app.post("/stop/monitor")
def start_monitor():
    return stop_monitoring()
