# src/app.py
import sys
import threading
import time
from config import load_config
from controllers.cli_controller import CLIController
from ui.gradio_app import launch_gradio_app
from services.poll_service import PollService
from services.user_service import UserService
from services.nft_service import NFTService
from services.chatbot_service import ChatbotService
from repositories.encuesta_repo import EncuestaRepository
from repositories.usuario_repo import UsuarioRepository
from repositories.nft_repo import NFTRepository
import firebase_admin
from firebase_admin import credentials
from config import FIREBASE_CREDENTIALS

firebase_admin.initialize_app(credentials.Certificate(FIREBASE_CREDENTIALS))
def main():
    config = load_config()

    # Inicializar servicios
    poll_service = PollService(EncuestaRepository())
    user_service = UserService(UsuarioRepository())
    nft_service = NFTService(NFTRepository())
    chatbot_service = ChatbotService(poll_service)

    # Crear CLI Controller
    cli = CLIController(
        poll_service=poll_service,
        user_service=user_service,
        nft_service=nft_service,
        chatbot_service=chatbot_service
    )

    # Función para cierre automático periódicamente
    def auto_close_polls():
        while True:
            poll_service.comprobar_y_cerrar_encuestas_expiradas()
            time.sleep(config["poll_check_interval"])

    # Arrancar thread para cierre automático
    threading.Thread(target=auto_close_polls, daemon=True).start()

    # Si se pasa --ui, lanzar interfaz Gradio paralelamente
    if "--ui" in sys.argv:
        # Lanzar UI en otro thread
        threading.Thread(target=launch_gradio_app, args=(poll_service, user_service, nft_service, chatbot_service, config), daemon=True).start()
        print("Interfaz Gradio iniciada en http://localhost:{}".format(config["port"]))
        print("Presiona Ctrl+C para salir.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSaliendo...")

    else:
        # Ejecutar CLI en consola
        cli.run()

if __name__ == "__main__":
    main()