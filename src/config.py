
import json
import os
from neo4j import GraphDatabase
DEFAULT_CONFIG = {
    "port": 7860,
    "data_dir": "data",
    "ia_model": "facebook/blenderbot-400M-distill",
    "poll_check_interval": 10,  # segundos para chequear cierre automático
}

NEO4J_URI="neo4j+s://e51e0f54.databases.neo4j.io"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="50ywM50_VHEdy_vb8kMrS5IlJBb3tvSWU2AfHD4iamo"

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return {**DEFAULT_CONFIG, **config}
    else:
        return DEFAULT_CONFIG