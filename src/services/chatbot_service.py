import uuid
import re
from typing import Dict
from transformers import AutoModelForCausalLM, AutoTokenizer
from .poll_service import PollService


class ChatbotService:
    def __init__(self, poll_service: PollService, model_name: str = "microsoft/DialoGPT-medium"):
        self.poll_service = poll_service
        self.historial: Dict[str, list] = {}
        self.model_name = model_name

        print(f"Cargando modelo '{self.model_name}'... Esto puede tardar unos minutos.")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def procesar_mensaje(self, username: str, mensaje: str) -> str:
        if self._es_consulta_encuesta(mensaje):
            mensaje = input("Introduce el id o el nombre de la encuesta: ")
            return self._respuesta_encuesta(mensaje)
        else:
            self.historial.setdefault(username, []).append(mensaje)
            respuesta = self._generar_respuesta(username, mensaje)
            self.historial[username].append(respuesta)
            return respuesta

    def _generar_respuesta(self, username: str, prompt: str) -> str:
        historial_texto = " " + " ".join(self.historial[username][-5:])
        input_text = f"{historial_texto} {prompt}"
        inputs = self.tokenizer(input_text, return_tensors="pt")

        outputs = self.model.generate(
            **inputs,
            max_length=100,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(input_text, "").strip()

    def _es_consulta_encuesta(self, mensaje: str) -> bool:
        keywords = ["ganando", "quién va", "cuánto falta", "resultado", "encuesta"]
        mensaje_lower = mensaje.lower()
        return any(kw in mensaje_lower for kw in keywords)

    def _respuesta_encuesta(self, mensaje: str) -> str:
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
