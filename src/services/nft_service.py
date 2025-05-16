import uuid
from repositories.nft_repo import NFTRepository
from models.token_nft import TokenNFT

class NFTService:
    def __init__(self, nft_repo: NFTRepository):
        self.nft_repo = nft_repo

    def crear_token(self, owner: str, poll_id: uuid.UUID, opcion: str) -> TokenNFT:
        token = TokenNFT(owner=owner, poll_id=poll_id, opcion=opcion)
        self.nft_repo.guardar_nft(token)
        return token

    def listar_tokens_por_usuario(self, owner: str) -> list[TokenNFT]:
        return self.nft_repo.listar_tokens_por_usuario(owner)

    def transferir_token(self, token_id: uuid.UUID, nuevo_owner: str) -> bool:
        token = self.nft_repo.obtener_token(token_id)
        if token is None:
            raise ValueError(f"El token con ID {token_id} no existe.")
        if token.owner != nuevo_owner:
            token.owner = nuevo_owner
            self.nft_repo.guardar_nft(token)
            return True
        else:
            raise ValueError(f"El token con ID {token_id} ya pertenece al usuario {nuevo_owner}.")