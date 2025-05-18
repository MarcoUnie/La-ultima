
from transformers import pipeline
from typing import Dict
from .poll_service import PollService
import uuid
import re
class ChatbotService:
    def __init__(self, poll_service: PollService):
        self.poll_service = poll_service
        self.chatbot = pipeline("text-generation", model="facebook/blenderbot-400M-distill")
        self.historial: Dict[str, list] = {}

    def procesar_mensaje(self, username: str, mensaje: str) -> str:
        if self._es_consulta_encuesta(mensaje):
            mensaje = input("Introduce el id o el nombre de la encuesta: ")
            return self._respuesta_encuesta(mensaje)
        else:
            self.historial.setdefault(username, []).append(mensaje)
            respuestas = self.chatbot(mensaje)
            respuesta = respuestas[0]['generated_text'].replace(mensaje, "").strip() if respuestas else "Lo siento, no entendí eso."
            self.historial[username].append(respuesta)
            return respuesta

    def _es_consulta_encuesta(self, mensaje: str) -> bool:
        keywords = ["ganando", "quién va", "cuánto falta", "resultado", "encuesta"]
        mensaje_lower = mensaje.lower()
        return any(kw in mensaje_lower for kw in keywords)

    def _respuesta_encuesta(self, mensaje: str) -> str:
        # Extraer poll_id si está en el mensaje (UUID esperado)
        uuid_match = re.search(r"[0-9a-fA-F\-]{36}", mensaje)
        if uuid_match:
            poll_id_str = uuid_match.group(0)
            try:
                poll_id = uuid.UUID(poll_id_str)
            except ValueError:
                return "ID de encuesta inválido."
            resultados = self.poll_service.obtener_resultados(poll_id)
            if resultados:
                texto_resultados = ", ".join(f"{opcion}: {votos}" for opcion, votos in resultados.items())
                return f"Resultados actuales: {texto_resultados}"
            else:
                return "No encontré esa encuesta."
        encuestas = self.poll_service.listar_encuestas()
        for encuesta in encuestas:
            if encuesta.pregunta.lower() in mensaje.lower():
                resultados = self.poll_service.obtener_resultados(encuesta.id)
                if resultados:
                    texto_resultados = ", ".join(f"{opcion}: {votos}" for opcion, votos in resultados.items())
                    return f"Resultados para '{encuesta.pregunta}': {texto_resultados}"
                else:
                    return f"No encontré resultados para '{encuesta.pregunta}'."
        return "Id o nombre de la encuesta no encontrados"
