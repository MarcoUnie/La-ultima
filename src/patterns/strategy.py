from abc import ABC, abstractmethod
from typing import Dict, List
import random
from models.encuesta import Encuesta

class DesempateStrategy(ABC):
    @abstractmethod
    def resolver(self, encuesta: Encuesta) -> str:
        pass

class DesempateAlfabetico(DesempateStrategy):
    def resolver(self, encuesta: Encuesta) -> str:
        empate = self._obtener_empate(encuesta)
        return sorted(empate)[0] if empate else None

    def _obtener_empate(self, encuesta: Encuesta) -> List[str]:
        max_votos = max(encuesta.opciones.values())
        return [op for op, votos in encuesta.opciones.items() if votos == max_votos]

class DesempateAleatorio(DesempateStrategy):
    def resolver(self, encuesta: Encuesta) -> str:
        empate = self._obtener_empate(encuesta)
        return random.choice(empate) if empate else None

    def _obtener_empate(self, encuesta: Encuesta) -> List[str]:
        max_votos = max(encuesta.opciones.values())
        return [op for op, votos in encuesta.opciones.items() if votos == max_votos]

class DesempateProrroga(DesempateStrategy):
    def resolver(self) -> str:
        return None


class PresentacionStrategy(ABC):
    @abstractmethod
    def presentar(self, resultados: Dict[str, int]) -> str:
        pass

class PresentacionTexto(PresentacionStrategy):
    def presentar(self, resultados: Dict[str, int]) -> str:
        return "\n".join(f"{opcion}: {votos}" for opcion, votos in resultados.items())

class PresentacionAscii(PresentacionStrategy):
    def presentar(self, resultados: Dict[str, int]) -> str:
        max_votos = max(resultados.values()) if resultados else 1
        barras = [f"{opcion}: {'#' * int((votos / max_votos) * 20)}" for opcion, votos in resultados.items()]
        return "\n".join(barras)

class PresentacionJson(PresentacionStrategy):
    def presentar(self, resultados: Dict[str, int]) -> str:
        import json
        return json.dumps(resultados, indent=4)