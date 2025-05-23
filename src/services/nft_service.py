import uuid
import json
import os
from repositories.nft_repo import NFTRepository
from models.token_nft import TokenNFT
from datetime import datetime
from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

class NFTService:
    def __init__(self, nft_repo: NFTRepository):
        self.nft_repo = nft_repo

    def crear_token(self, owner: str, poll_id: uuid.UUID, opcion: str) -> TokenNFT:
        token = TokenNFT(id=uuid.uuid4(),owner=owner, poll_id=poll_id, opcion=opcion, issued_at=datetime.now())
        self.nft_repo.guardar_nft(token)
        return token

    def listar_tokens_por_usuario(self, owner: str) -> list[TokenNFT]:
        return self.nft_repo.listar_tokens_por_usuario(owner)

    def transferir_token(self, token_id: uuid.UUID, actual_owner: str, nuevo_owner: str) -> bool:
        token = self.nft_repo.obtener_token(token_id)
        if token is None:
            raise ValueError(f"El token con ID {token_id} no existe.")
        if token.owner != actual_owner:
            raise ValueError(f"El token con ID {token_id} no pertenece al usuario {actual_owner}.")
        if token.owner != nuevo_owner:
            with open(os.path.join("data", "nfts.json"), "r") as f:
                tokens = json.load(f)
                for token in tokens:
                    if token["id"] == str(token_id):
                        token["owner"] = nuevo_owner
            with open(os.path.join("data", "nfts.json"), "w") as f:
                json.dump(tokens, f, default=str, indent=4)
            db.mongo_db.tokens.update_one(
            {"$set": {"owner": nuevo_owner}}
        )

            return True
        else:
            raise ValueError(f"El token con ID {token_id} ya pertenece al usuario {nuevo_owner}.")