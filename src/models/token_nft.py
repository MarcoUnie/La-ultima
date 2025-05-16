import uuid

class TokenNFT:
    def __init__(self,id:uuid.UUID, owner:str, poll_id: uuid.UUID, opcion: str, issued_at:str):
        self.id = id
        self.owner = owner
        self.poll_id = poll_id
        self.opcion = opcion
        self.issued_at = issued_at

    def __repr__(self):
        return f"TokenNFT(id={self.id}, owner={self.owner}, poll_id={self.poll_id}, opcion={self.opcion}, issued_at={self.issued_at})"
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "owner": str(self.owner),
            "poll_id": str(self.poll_id),
            "opcion": str(self.opcion),
            "issued_at": str(self.issued_at),
        }