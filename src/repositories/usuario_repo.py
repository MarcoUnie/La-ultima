import json
import os
import uuid
from typing import Optional
from models.usuario import Usuario
from repositories.encuesta_repo import DATA_DIR
from config import MONGO_URI, MONGO_DB_NAME
from pymongo import MongoClient

USER_FILE = os.path.join(DATA_DIR, "usuarios.json")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
DATA_DIR = "data"
POLL_FILE = os.path.join(DATA_DIR, "encuestas.json")
USER_FILE = os.path.join(DATA_DIR, "usuarios.json")
NFT_FILE = os.path.join(DATA_DIR, "nfts.json")


class UsuarioRepository:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, "w") as f:
                json.dump([], f)

    def guardar_usuario(self, usuario: Usuario) -> None:
        with open(USER_FILE, "r") as f:
            usuarios = json.load(f)
        usuarios.append(usuario.__dict__)
        with open(USER_FILE, "w") as f:
            json.dump(usuarios, f, default=str, indent=4)
        db.usuarios.replace_one({"id": str(usuario.id)}, usuario.to_dict(), upsert=True)

    def obtener_usuario(self, username: str) -> Optional[Usuario]:
        with open(USER_FILE, "r") as f:
            usuarios = json.load(f)
        for data in usuarios:
            if data.get("username") == username:
                user = Usuario(username=data["username"], password_hash=data["password_hash"])
                user.id = uuid.UUID(data["id"])
                return user
        return None