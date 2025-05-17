import uuid
class Usuario:
    def __init__(self, username: str, password_hash: str):
        self.id = uuid.uuid4()
        self.username = username
        self.password_hash = password_hash

    def to_dict(self) -> dict:
        return {
            "usuario":str(self.username),
            "usuario_id": str(self.id),
            "password_hash": str(self.password_hash),
        }