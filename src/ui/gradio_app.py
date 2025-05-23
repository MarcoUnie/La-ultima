from services.user_service import UserService
from services.poll_service import PollService
from services.nft_service import NFTService
from services.chatbot_service import ChatbotService
import gradio as gr
from repositories.usuario_repo import UsuarioRepository
import uuid
class GradioController:
    def __init__(self, poll_service: PollService, user_service: UserService, nft_service: NFTService, chatbot_service: ChatbotService,user_repo: UsuarioRepository):
        self.user_repo = user_repo
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
        self.chatbot_service = chatbot_service

    def run(self):
        def votar_fn(encuesta_id, username_input, voto):
            user_id = self.user_repo.obtener_usuario(username_input)
            try:
                self.poll_service.votar(encuesta_id, user_id.id, voto)
                self.nft_service.crear_token(username_input, encuesta_id, voto)
                return "Votro registrado, tienes un nuevo token"
            except ValueError as e:
                return f"Error al votar: {e}"
        
        def crear_encuesta_fn(pregunta, opciones_str, duracion, tipo):
            opciones_list = [o.strip() for o in opciones_str.split(",") if o.strip()]
            print(opciones_list)
            return self.poll_service.crear_encuesta(pregunta, opciones_list, duracion, tipo)
        
        def transferir_token_fn(token_id_str: str, username: str, nuevo_owner: str):
            try:
                token_id = uuid.UUID(token_id_str)
            except ValueError:
                return "El Token ID es incorrecto"
            except Exception as e:
                return f"Error inesperado: {e}"

            try:
                return self.nft_service.transferir_token(token_id, username, nuevo_owner)
            except Exception as e:
                return f"Error al transferir el token: {e}"

        

            
        with gr.Blocks() as demo:
            gr.Markdown("# Plataforma de Encuestas Streaming")

            with gr.Tab("Autenticación"):
                with gr.Row():
                    username = gr.Text(label="Usuario")
                    password = gr.Text(label="Contraseña", type="password")
                registrar = gr.Button("Registrar")
                registrar.click(fn=self.user_service.registrar_usuario, inputs=[username, password], outputs=gr.Text())
                login = gr.Button("iniciar sesión")
                login.click(fn=self.user_service.autenticar_usuario, inputs=[username, password], outputs=gr.Text())
                

            with gr.Tab("Encuestas"):
                pregunta = gr.Text(label="Pregunta")
                opciones = gr.Text(label="Opciones (coma)")
                duracion = gr.Number(label="Duración")
                tipo = gr.Radio(choices=["simple", "multiple"], label="Tipo de encuesta")
                encuesta_crear = gr.Button("Crear encuesta")
                encuesta_crear.click(fn=crear_encuesta_fn, inputs=[pregunta,opciones,duracion,tipo], outputs=gr.Text())
                encuesta_listar = gr.Button("Listar Encuestas")
                encuesta_listar.click(fn=self.poll_service.listar_encuestas, inputs=[], outputs=gr.Text())
                poll_id_vote = gr.Text(label="ID Encuesta")
                opcion_vote = gr.Text(label="voto")
                votar = gr.Button("Votar")
                votar.click(fn=votar_fn, inputs=[poll_id_vote,username, opcion_vote], outputs=gr.Text())
                poll_id_result = gr.Text(label="ID Encuesta Resultados")
                Resultados = gr.Button("Ver resultados")
                Resultados.click(fn=self.poll_service.obtener_resultados, inputs=[poll_id_result], outputs=gr.Text())

            with gr.Tab("NFTs"):
                Tokens = gr.Button("Mis tokens")
                Tokens.click(fn=self.nft_service.listar_tokens_por_usuario, inputs=[username], outputs=gr.Text())
                token_id_transfer = gr.Text(label="Token ID")
                nuevo_owner = gr.Text(label="Nuevo Propietario")
                Transferir = gr.Button("Transferir Token")
                Transferir.click(fn=transferir_token_fn, inputs=[token_id_transfer,username, nuevo_owner], outputs=gr.Text())

            with gr.Tab("Chatbot"):
                pregunta_chatbot = gr.Text(label="Pregunta al Chatbot")
                preguntar = gr.Button("Enviar")
                preguntar.click(fn=self.chatbot_service.procesar_mensaje, inputs=[username,pregunta_chatbot], outputs=gr.Text())
        demo.launch()