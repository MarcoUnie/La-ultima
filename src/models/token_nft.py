import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, token_id: uuid.UUID,owner:str, poll_id: uuid.UUID, opcion: str):
        self.id = uuid.uuid4()
        self.owner = owner
        self.token_id = token_id
        self.poll_id = poll_id
        self.opcion = opcion
        self.issued_at = datetime.now()

    def __repr__(self):
        return f"TokenNFT(id={self.id}, owner={self.owner}, poll_id={self.poll_id}, opcion={self.opcion}, issued_at={self.issued_at})"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "owner": str(self.owner),
            "token_id": str(self.token_id),
            "poll_id": str(self.poll_id),
            "opcion": str(self.opcion),
            "issued_at": self.issued_at.isoformat(),
        }