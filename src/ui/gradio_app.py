from services.user_service import UserService
from services.poll_service import PollService
from services.nft_service import NFTService
from services.chatbot_service import ChatbotService
import gradio as gr
from repositories.usuario_repo import UsuarioRepository

with gr.Blocks() as demo:
    gr.Markdown("# Plataforma de Encuestas Streaming")

    with gr.Tab("Autenticación"):
        with gr.Row():
            username = gr.Text(label="Usuario")
            password = gr.Text(label="Contraseña", type="password")
        gr.Button("Registrar").click(UserService.registrar_usuario(username, password), outputs=[gr.Text()])
        gr.Button("Login").click(UserService.autenticar_usuario(username, password), outputs=[gr.Text()])

    with gr.Tab("Encuestas"):
        pregunta = gr.Text(label="Pregunta")
        opciones = gr.Text(label="Opciones (coma)")
        duracion = gr.Number(label="Duración")
        tipo = gr.Text(label="Tipo")
        gr.Button("Crear Encuesta").click(PollService.crear_encuesta(pregunta, opciones, duracion, tipo), outputs=[gr.Text()])
        gr.Button("Listar Encuestas").click(PollService.listar_encuestas(), [], outputs=[gr.Text()])
        poll_id_vote = gr.Text(label="ID Encuesta")
        opcion_vote = gr.Text(label="Opción")
        gr.Button("Votar").click(PollService.votar(poll_id_vote,UsuarioRepository.obtener_usuario(username)[1], opcion_vote), outputs=[gr.Text()])
        poll_id_result = gr.Text(label="ID Encuesta Resultados")
        gr.Button("Ver Resultados").click(PollService.obtener_resultados(poll_id_result), outputs=[gr.Text()])

    with gr.Tab("NFTs"):
        gr.Button("Mis Tokens").click(NFTService.listar_tokens_por_usuario(username), [], outputs=[gr.Text()])
        token_id_transfer = gr.Text(label="Token ID")
        nuevo_owner = gr.Text(label="Nuevo Propietario")
        gr.Button("Transferir Token").click(NFTService.transferir_token(token_id_transfer,UsuarioRepository.obtener_usuario(username)[1], nuevo_owner), outputs=[gr.Text()])

    with gr.Tab("Chatbot"):
        pregunta_chatbot = gr.Text(label="Pregunta al Chatbot")
        gr.Button("Enviar").click(ChatbotService.procesar_mensaje(pregunta_chatbot), outputs=[gr.Text()])

if __name__ == "__main__":
    demo.launch()
