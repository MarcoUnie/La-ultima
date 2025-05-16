import gradio as gr
from services.poll_service import PollService
from services.user_service import UserService
from services.nft_service import NFTService
from services.chatbot_service import ChatbotService

def launch_gradio_app(poll_service: PollService, user_service: UserService, nft_service: NFTService, chatbot_service: ChatbotService, config: dict):
    def crear_encuesta(pregunta, opciones, duracion, tipo):
        opciones_lista = opciones.split(",")
        encuesta = poll_service.create_poll(pregunta, opciones_lista, int(duracion), tipo)
        return f"Encuesta creada: {encuesta.id}"

    def votar(poll_id, username, opcion):
        try:
            poll_service.vote(poll_id, username, opcion)
            return f"Voto registrado para {username} en encuesta {poll_id}"
        except Exception as e:
            return str(e)

    def consultar_encuestas():
        encuestas = poll_service.list_active_polls()
        if not encuestas:
            return "No hay encuestas activas."
        return "\n".join([f"{p.id} - {p.pregunta}" for p in encuestas])

    def consultar_tokens(username):
        user = user_service.get_user(username)
        if not user:
            return "Usuario no encontrado."
        tokens = nft_service.list_tokens_by_user(user.id)
        if not tokens:
            return "No tienes tokens."
        return "\n".join([f"Token {t.token_id} - {t.opcion} ({t.issued_at})" for t in tokens])

    def chatear(usuario, mensaje):
        try:
            response = chatbot_service.respond(usuario, mensaje)
            return response
        except Exception as e:
            return str(e)

    with gr.Blocks() as demo:
        with gr.Tab("Encuestas"):
            gr.Markdown("### Crear Encuesta")
            pregunta = gr.Textbox(label="Pregunta")
            opciones = gr.Textbox(label="Opciones (separadas por coma)")
            duracion = gr.Number(label="Duración en segundos")
            tipo = gr.Dropdown(choices=["simple", "multiple"], label="Tipo")
            crear_btn = gr.Button("Crear Encuesta")
            crear_output = gr.Textbox(label="Resultado")
            crear_btn.click(crear_encuesta, inputs=[pregunta, opciones, duracion, tipo], outputs=crear_output)

            gr.Markdown("### Votar en Encuesta")
            poll_id = gr.Textbox(label="ID de Encuesta")
            username = gr.Textbox(label="Username")
            opcion = gr.Textbox(label="Opción")
            votar_btn = gr.Button("Votar")
            votar_output = gr.Textbox(label="Resultado")
            votar_btn.click(votar, inputs=[poll_id, username, opcion], outputs=votar_output)

            gr.Markdown("### Consultar Encuestas Activas")
            consultar_btn = gr.Button("Consultar Encuestas")
            consultar_output = gr.Textbox(label="Encuestas Activas")
            consultar_btn.click(consultar_encuestas, outputs=consultar_output)

        with gr.Tab("Tokens"):
            gr.Markdown("### Mis Tokens")
            username_tokens = gr.Textbox(label="Username")
            tokens_btn = gr.Button("Consultar Tokens")
            tokens_output = gr.Textbox(label="Tokens")
            tokens_btn.click(consultar_tokens, inputs=[username_tokens], outputs=tokens_output)

        with gr.Tab("Chatbot"):
            gr.Markdown("### Chat con IA")
            chat_user = gr.Textbox(label="Username")
            chat_msg = gr.Textbox(label="Mensaje")
            chat_btn = gr.Button("Enviar")
            chat_output = gr.Textbox(label="Respuesta")
            chat_btn.click(chatear, inputs=[chat_user, chat_msg], outputs=chat_output)

    # Ejecutar el servidor
    demo.launch(server_name="0.0.0.0", server_port=config["port"])
