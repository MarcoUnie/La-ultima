
import json
import os

DEFAULT_CONFIG = {
    "port": 7860,
    "data_dir": "data",
    "ia_model": "facebook/blenderbot-400M-distill",
    "poll_check_interval": 10,  # segundos para chequear cierre automático
}

MONGO_URI = "mongodb+srv://mmagecoyt:JP6loUSzG3CyjGcX@streamingtokens.fvey6d0.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME = "Streaming_data"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return {**DEFAULT_CONFIG, **config}
    else:
        return DEFAULT_CONFIG