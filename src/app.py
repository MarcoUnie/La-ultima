import sys
import threading
import time
from config import load_config
from controllers.cli_controller import CLIController
from ui.gradio_app import GradioController
from services.poll_service import PollService
from services.user_service import UserService
from services.nft_service import NFTService
from services.chatbot_service import ChatbotService
from repositories.encuesta_repo import EncuestaRepository
from repositories.usuario_repo import UsuarioRepository
from repositories.nft_repo import NFTRepository

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

    gra = GradioController(
        poll_service=poll_service,
        user_service=user_service,
        nft_service=nft_service,
        chatbot_service=chatbot_service,
        user_repo=UsuarioRepository(),
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
        threading.Thread(target=gra.run()).start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSaliendo...")

    else:
        cli.run()

if __name__ == "__main__":
    main()