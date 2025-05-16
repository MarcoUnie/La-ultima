import uuid
from datetime import datetime

class Voto:
    def __init__(self, usuario_id: uuid.UUID, opcion: str, encuesta_id: uuid.UUID):
        self.id = uuid.uuid4()
        self.usuario_id = usuario_id
        self.opcion = opcion
        self.encuesta_id = encuesta_id
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        return {
            "usuario_id": str(self.usuario_id),
            "opcion": str(self.opcion),
            "encuesta_id": str(self.encuesta_id),
            "timestamp": self.timestamp.isoformat(),
        }