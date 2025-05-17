import json
import os
import uuid
from typing import Optional
from models.usuario import Usuario
from repositories.encuesta_repo import DATA_DIR
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD  
USER_FILE = os.path.join(DATA_DIR, "usuarios.json")

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
            
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)).session() as session:
            session.run(
                "MERGE (e:Usuario {usuario: $usuario}) SET e += {usuario_id: $usuario_id, password_hash: $password_hash}",
                usuario.to_dict()
            )


    def obtener_usuario(self, username: str) -> Optional[Usuario]:
        with open(USER_FILE, "r") as f:
            usuarios = json.load(f)
        for data in usuarios:
            if data.get("username") == username:
                user = Usuario(username=data["username"], password_hash=data["password_hash"])
                user.id = uuid.UUID(data["id"])
                return user
        return None