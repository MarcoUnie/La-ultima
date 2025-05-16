from typing import Optional
import os
from services.user_service import UserService
from services.poll_service import PollService
from services.nft_service import NFTService
from services.chatbot_service import ChatbotService
import uuid
from repositories.encuesta_repo import DATA_DIR
import json
class CLIController:
    def __init__(self, user_service: UserService, poll_service: PollService, nft_service: NFTService, chatbot_service: ChatbotService):
        self.user_service = user_service
        self.poll_service = poll_service
        self.nft_service = nft_service
        self.current_user: Optional[str] = None
        self.chatbot_service = chatbot_service

    def run(self):
        print("Bienvenido al stream")
        while True:
            try:
                command = input(">> ").strip()
                if not command:
                    continue
                parts = command.split()
                cmd = parts[0]

                if cmd == "salir":
                    print("Saliendo...")
                    break

                elif cmd == "registrar":
                    username = input("Username: ")
                    password = input("Password: ")
                    self.user_service.registrar_usuario(username, password)
                    print(f"Usuario '{username}' registrado.")

                elif cmd == "login":
                    username = input("Username: ")
                    password = input("Password: ")
                    with open(os.path.join(DATA_DIR, "usuarios.json"), "r") as f:
                        usuarios = json.load(f)
                    for data in usuarios:
                        usuario_id = uuid.UUID(data["id"])
                    if self.user_service.autenticar_usuario(username, password):
                        self.current_user = username
                        print(f"Usuario '{username}' logueado.")
                    else:
                        print("Credenciales inválidas.")

                elif cmd == "crear_encuesta":
                    if not self._check_login(): continue
                    pregunta = input("Pregunta: ")
                    opciones = input("Opciones (separadas por coma): ").split(",")
                    try:
                        duracion = int(input("Duración (segundos): "))
                    except ValueError:
                        print("Duración inválida. Debe ser un número entero.")
                        continue
                    tipo = input("Tipo (simple/multiple): ").strip()
                    poll_id = self.poll_service.crear_encuesta(pregunta, [o.strip() for o in opciones], duracion, tipo)
                    print(f"Encuesta creada con id: {poll_id}")

                elif cmd == "listar_encuestas":
                    encuestas = self.poll_service.listar_encuestas()
                    for e in encuestas:
                        estado = "ACTIVA" if e.es_activa() else "CERRADA"
                        print(f"{e.id} | {e.pregunta} | Estado: {estado}")

                elif cmd == "votar":
                    if not self._check_login(): continue
                    poll_id = input("ID encuesta: ").strip()
                    opcion = input("Opción: ").strip()
                    try:
                        self.poll_service.votar(poll_id, usuario_id, opcion)
                        print("Voto registrado.")
                    except Exception as e:
                        print(f"Error: {e}")

                elif cmd == "cerrar_encuesta":
                    if not self._check_login(): continue
                    poll_id = input("ID encuesta: ").strip()
                    self.poll_service.cerrar_encuesta(poll_id)
                    print(f"Encuesta {poll_id} cerrada.")

                elif cmd == "ver_resultados":
                    poll_id = input("ID encuesta: ").strip()

                    try:
                        encuesta_id = uuid.UUID(poll_id) 
                        resultados = self.poll_service.obtener_resultados(encuesta_id)

                        if resultados:
                            print("Resultados finales:")
                            for opcion, votos in resultados.items():
                                print(f"{opcion}: {votos}")
                        else:
                            print("No se encontraron resultados para esta encuesta.")
                    except ValueError:
                        print("ID de encuesta no válido. Asegúrate de ingresar un UUID correcto.")

                elif cmd == "mis_tokens":
                    if not self._check_login(): continue
                    tokens = self.nft_service.listar_tokens_por_usuario(self.current_user)
                    for t in tokens:
                        print(f"Token ID: {t.token_id} | Opción: {t.opcion} | Fecha: {t.issued_at} | Propietario: {t.owner}")

                elif cmd == "transferir_token":
                    if not self._check_login(): continue
                    token_id_str = input("Token ID: ").strip()
                    nuevo_owner = input("Nuevo propietario: ").strip()
                    try:
                        token_id = uuid.UUID(token_id_str)
                        self.nft_service.transferir_token(token_id, nuevo_owner)
                        print("Token transferido correctamente.")
                    except ValueError as ve:
                        print(f"Error: {ve}")
                    except Exception as e:
                        print(f"Error inesperado: {e}")
                else:
                    print("Comando no reconocido. Comandos válidos: registrar, login, crear_encuesta, listar_encuestas, votar, cerrar_encuesta, ver_resultados, mis_tokens, transferir_token, salir")

            except KeyboardInterrupt:
                print("\nSaliendo...")
                break

    def _check_login(self) -> bool:
        if not self.current_user:
            print("Debes iniciar sesión primero.")
            return False
        return True