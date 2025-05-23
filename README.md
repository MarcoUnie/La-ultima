# La-ultima
https://github.com/MarcoUnie/La-ultima.git

Para instalar dependencias:
pip install -r requirements.txt
Ejecuta la aplicación desde terminal:
python src/app.py
Para lanzar la interfaz gráfica:
python src/app.py --ui

Factory (factory.py)
Encapsula la lógica de creación de objetos (como encuestas o tokens NFT) dependiendo de parámetros como tipo o contexto. Facilita la extensión de nuevas variantes sin modificar código existente.

Observer (observer.py)
Permite que componentes (por ejemplo, el sistema de notificaciones o el sistema de tokens) reaccionen automáticamente a eventos como la creación de votos o encuestas sin acoplar directamente las clases.

Strategy (strategy.py)
Define una familia de algoritmos intercambiables para operaciones como validación de votos, estilos de votación o reglas de puntuación, separando la lógica del objeto principal.

Este proyecto utiliza pytest para validar la funcionalidad de los servicios y componentes principales.

Estructura de pruebas

Las pruebas están organizadas dentro de una carpeta tests/, y siguen la nomenclatura test_*.py para ser detectadas automáticamente por pytest. Cada módulo tiene pruebas unitarias independientes, por ejemplo:

test_user_service.py: verifica el registro, autenticación y duplicados.

test_poll_service.py: valida creación de encuestas, votación, y cierres por tiempo.

test_nft_service.py: comprueba la creación y transferencia de NFTs.

test_chatbot_service.py: simula mensajes y respuestas usando un modelo local o de Hugging Face
