import hashlib
from models.usuario import Usuario
from repositories.usuario_repo import UsuarioRepository

class UserService:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo

    def registrar_usuario(self, username: str, password: str) -> Usuario:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        usuario = Usuario(username=username, password_hash=hashed_password)
        self.usuario_repo.guardar_usuario(usuario)
        return usuario

    def autenticar_usuario(self, username: str, password: str) -> bool:
        usuario = self.usuario_repo.obtener_usuario(username)
        if usuario and usuario.password_hash == hashlib.sha256(password.encode()).hexdigest():
            return True
        return False