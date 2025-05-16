import uuid
from datetime import datetime
from typing import List, Dict
from .voto import Voto

class Encuesta:
    def __init__(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple"):
        self.id = uuid.uuid4()
        self.pregunta = pregunta
        self.opciones = {opcion: 0 for opcion in opciones}
        self.votos: List[Voto] = []
        self.tipo = tipo
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.duracion_segundos = duracion_segundos
        self.timestamp_fin = self.timestamp_inicio.timestamp() + duracion_segundos

    def __repr__(self):
        return f"Encuesta(id={self.id}, pregunta='{self.pregunta}', estado='{self.estado}')"

    def __str__(self):
        return str(self.id)

    def agregar_voto(self, voto: Voto) -> None:
        if not self.es_activa():
            raise ValueError("Encuesta cerrada o expirada")

        if voto.opcion not in self.opciones:
            raise ValueError("Opción no válida")
        
        if any(v.usuario_id == voto.usuario_id and v.opcion == voto.opcion for v in self.votos):
            raise ValueError("El usuario ya ha votado esta opción en esta encuesta")
        self.opciones[voto.opcion] += 1
        self.votos.append(voto)



    def cerrar(self) -> None:
        self.estado = "cerrada"

    def resultados_parciales(self) -> Dict[str, int]:
        return self.opciones
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "pregunta": self.pregunta,
            "opciones": self.opciones,
            "tipo": self.tipo,
            "estado": self.estado,
            "timestamp_inicio": self.timestamp_inicio.isoformat(),
            "duracion_segundos": self.duracion_segundos,
            "timestamp_fin": self.timestamp_fin,
            "votos": [voto.to_dict() for voto in self.votos]
        }

    def es_activa(self) -> bool:
        return self.estado == "activa" and datetime.now().timestamp() <= self.timestamp_fin