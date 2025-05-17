import json
import os
import uuid
from typing import Optional, List
from models.token_nft import TokenNFT
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD  
DATA_DIR = "data"
NFT_FILE = os.path.join(DATA_DIR, "nfts.json")

class NFTRepository:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(NFT_FILE):
            with open(NFT_FILE, "w") as f:
                json.dump([], f)

    def guardar_nft(self, token: TokenNFT) -> None:
        with open(NFT_FILE, "r") as f:
            tokens = json.load(f)
        tokens.append(token.to_dict())
        with open(NFT_FILE, "w") as f:
            json.dump(tokens, f, default=str, indent=4)
        with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)).session() as session:
            session.run(
                "MERGE (e:NFT {id: $id}) SET e += {owner: $owner, poll_id: $poll_id, opcion: $opcion, issued_at: $issued_at}",
                token.to_dict()
            )


    def listar_tokens_por_usuario(self, owner: str) -> List[TokenNFT]:
        with open(NFT_FILE, "r") as f:
            tokens = json.load(f)
        return [
            TokenNFT(id = uuid.UUID(data["id"]),owner=data["owner"], poll_id=uuid.UUID(data["poll_id"]), opcion=data["opcion"], issued_at=data["issued_at"])
            for data in tokens if data["owner"] == owner
        ]

    def obtener_token(self, token_id: uuid.UUID) -> Optional[TokenNFT]:
        with open(NFT_FILE, "r") as f:
            tokens = json.load(f)
        for data in tokens:
            if data.get("id") == str(token_id):
                return TokenNFT(
                    id=uuid.UUID(data["id"]),
                    owner=data["owner"],
                    poll_id=uuid.UUID(data["poll_id"]),
                    opcion=data["opcion"],
                    issued_at=data["issued_at"]
                )
        return None