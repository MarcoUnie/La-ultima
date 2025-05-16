import uuid
from typing import List, Optional
from models.encuesta import Encuesta
from models.voto import Voto
from repositories.encuesta_repo import EncuestaRepository
from datetime import datetime
from .nft_service import NFTService 
class PollService:
    def __init__(self, encuesta_repo: EncuestaRepository):
        self.encuesta_repo = encuesta_repo

    def crear_encuesta(self, pregunta: str, opciones: List[str], duracion_segundos: int, tipo: str = "simple") -> Encuesta:
        encuesta = Encuesta(pregunta=pregunta, opciones=opciones, duracion_segundos=duracion_segundos, tipo=tipo)
        self.encuesta_repo.guardar_encuesta(encuesta)
        return encuesta
    
    def listar_encuestas(self, estado: Optional[str] = None) -> List[Encuesta]:
        encuestas = self.encuesta_repo.listar_encuestas()
        if estado:
            return [e for e in encuestas if e.estado == estado]
        return encuestas

    def votar(self, encuesta_id: uuid.UUID, usuario_id: uuid.UUID, opcion: str) -> Voto:
        encuesta = self.encuesta_repo.obtener_encuesta(encuesta_id)
        if encuesta.es_activa():
            voto = Voto(usuario_id=usuario_id, opcion=opcion, encuesta_id=encuesta_id)
            try:
                encuesta.agregar_voto(voto)
            except ValueError as e:
                raise ValueError(f"Error al agregar voto: {e}")
            self.encuesta_repo.guardar_encuesta(encuesta)
            return voto
        else:
            raise ValueError("Encuesta no encontrada o cerrada")



    def cerrar_encuesta(self, encuesta_id: uuid.UUID) -> None:
        encuesta = self.encuesta_repo.obtener_encuesta(encuesta_id)
        if encuesta and encuesta.es_activa():
            encuesta.cerrar()
            self.encuesta_repo.guardar_encuesta(encuesta)
        else:
            raise ValueError("Encuesta no encontrada o ya cerrada")

    def obtener_resultados(self, encuesta_id: uuid.UUID) -> Optional[dict]:
        encuesta = self.encuesta_repo.obtener_encuesta(encuesta_id)
        if encuesta:
            return encuesta.resultados_parciales()
        return None
    def comprobar_y_cerrar_encuestas_expiradas(self):
        encuestas = self.encuesta_repo.listar_encuestas()
        for encuesta in encuestas:
            if encuesta.es_activa() and datetime.now().timestamp() > encuesta.timestamp_fin:
                encuesta.cerrar()
                self.encuesta_repo.guardar_encuesta(encuesta)
                print(f"Encuesta '{encuesta.pregunta}' cerrada automáticamente por expiración.")