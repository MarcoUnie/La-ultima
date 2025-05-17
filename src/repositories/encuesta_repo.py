import json
import os
import uuid
from typing import List, Optional
from datetime import datetime
from models.encuesta import Encuesta
from models.voto import Voto
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

DATA_DIR = "data"
POLL_FILE = os.path.join(DATA_DIR, "encuestas.json")

class EncuestaRepository:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(POLL_FILE):
            with open(POLL_FILE, "w") as f:
                json.dump([], f)

    def guardar_encuesta(self, encuesta: Encuesta) -> None:
        with open(POLL_FILE, "r") as f:
            encuestas = json.load(f)

        encuestas_actualizadas = []
        encuesta_actualizada = False

        for e in encuestas:
            if isinstance(e.get("id"), str) and e["id"] == str(encuesta.id):
                encuestas_actualizadas.append(encuesta.to_dict())
                encuesta_actualizada = True
            else:
                encuestas_actualizadas.append(e)

        if not encuesta_actualizada:
            encuestas_actualizadas.append(encuesta.to_dict())

        with open(POLL_FILE, "w") as f:
            json.dump(encuestas_actualizadas, f, default=str, indent=4)
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)).session() as session:
            session.run(
                "MERGE (e:Encuesta {id: $id}) SET e += {pregunta: $pregunta, tipo: $tipo, estado: $estado, timestamp_inicio: $timestamp_inicio, duracion_segundos: $duracion_segundos, timestamp_fin: $timestamp_fin}",
                encuesta.to_dict()
            )





    def obtener_encuesta(self, encuesta_id: uuid.UUID) -> Optional[Encuesta]:
        with open(POLL_FILE, "r") as f:
            encuestas = json.load(f)

        for data in encuestas:
            if data.get("id") == str(encuesta_id):
                encuesta = Encuesta(
                    pregunta=data["pregunta"],
                    opciones=list(data["opciones"].keys()),
                    duracion_segundos=data["duracion_segundos"],
                    tipo=data["tipo"]
                )

                encuesta.id = uuid.UUID(data["id"])
                encuesta.estado = data["estado"]
                encuesta.timestamp_inicio = datetime.fromisoformat(data["timestamp_inicio"])
                encuesta.timestamp_fin = float(data["timestamp_fin"])

                for v in data.get("votos", []):
                    voto = Voto(
                        usuario_id=uuid.UUID(v["usuario_id"]),
                        opcion=v["opcion"],
                        encuesta_id=uuid.UUID(v["encuesta_id"])
                    )
                    try:
                        encuesta.agregar_voto(voto)
                    except ValueError:
                        pass 

                return encuesta

        return None


    def listar_encuestas(self) -> List[Encuesta]:
        with open(POLL_FILE, "r") as f:
            encuestas = json.load(f)
        return [self.obtener_encuesta(uuid.UUID(e["id"])) for e in encuestas]