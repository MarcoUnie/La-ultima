import uuid
from abc import ABC, abstractmethod
from typing import List
from models.encuesta import Encuesta
from models.token_nft import TokenNFT


class PollFactory(ABC):
    @abstractmethod
    def create_poll(self, pregunta: str, opciones: List[str], duracion_segundos: int) -> Encuesta:
        pass

class SimplePollFactory(PollFactory):
    def create_poll(self, pregunta: str, opciones: List[str], duracion_segundos: int) -> Encuesta:
        return Encuesta(pregunta=pregunta, opciones=opciones, duracion_segundos=duracion_segundos, tipo="simple")

class MultiplePollFactory(PollFactory):
    def create_poll(self, pregunta: str, opciones: List[str], duracion_segundos: int) -> Encuesta:
        return Encuesta(pregunta=pregunta, opciones=opciones, duracion_segundos=duracion_segundos, tipo="multiple")

# Factory para TokenNFT

class TokenNFTFactory(ABC):
    @abstractmethod
    def create_token(self, owner: str, poll_id: uuid.UUID, opcion: str) -> TokenNFT:
        pass

class StandardTokenFactory(TokenNFTFactory):
    def create_token(self, owner: str, poll_id: uuid.UUID, opcion: str) -> TokenNFT:
        return TokenNFT(owner=owner, poll_id=poll_id, opcion=opcion)

class LimitedEditionTokenFactory(TokenNFTFactory):
    def create_token(self, owner: str, poll_id: uuid.UUID, opcion: str) -> TokenNFT:
        token = TokenNFT(owner=owner, poll_id=poll_id, opcion=opcion)
        # agregar metadatos de edición limitada
        token.metadata = {"edition": "limited"}
        return token