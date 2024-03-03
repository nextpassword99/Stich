# Stich: Tu útil asistente de inteligencia artificial

Stich es un asistente de inteligencia artificial versátil y útil diseñado para hacerte la vida más fácil. Puede realizar una amplia gama de tareas, como realizar llamadas, proporcionar actualizaciones meteorológicas, reproducir música y mucho más.

## Características

- Reconocimiento y síntesis de voz con Whisper
- Dictado usando ElevenLabs
- Reproducción de música en Spotify
- Búsqueda de imágenes y vídeos
- Resúmenes de Wikipedia
- Integración con ChatGPT y Gemini Pro
- Toma de notas
- Enviar mensajes de WhatsApp

## Introducción

Para usar Stich, necesitas tener Python instalado en tu sistema. Después de clonar este repositorio, instala los paquetes necesarios usando pip:

```bash
pip install -r requirements.txt
```

A continuación, configura tus variables de entorno creando un archivo `.env` en la raíz del proyecto:

```makefile
ELEVENLABS_API_KEY=<tu_clave_api_elevenlabs>
OPENAI_API_KEY=<su_clave_openai_api_key>
SPOTIFY_CLIENT_ID=<su_id_cliente_spotify>
SPOTIFY_CLIENT_SECRET=<su_secreto_cliente_spotify>
GEMINI_API_KEY=<tu_gemini_api_key>
```

Sustituye los marcadores de posición por tus claves de API reales.

## Uso

Para iniciar Stich, ejecute el script `main.py`:

``bash
python main.py
```

Stich te dará la bienvenida y esperará tus órdenes. Para interactuar con Stich, simplemente di tus comandos. Stich soporta una amplia gama de comandos, incluyendo:

- Saludos: "Hola", "Hola", "Eh".
- Llamar a un contacto: "Llamar a [nombre_de_contacto]"
- Reproducir música: "Reproducir música", "Reproducir música [nombre_canción]"
- Buscar imágenes: "Mostrar imagen de [palabra clave]"
- Definir un término en Wikipedia: "Definir [término]"
- Reproducir un vídeo: "Reproducir vídeo de [palabra clave]"
- Tomar notas: "Tomar una nota", "Anotar [texto]"
- Enviar un mensaje de WhatsApp: "Enviar mensaje a [número_teléfono] [mensaje]"
- Iniciar una conversación con ChatGPT: "Hablar con ChatGPT"
- Iniciar una conversación con Gemini Pro: "Hablar con Gemini"

## Solución de problemas

Si tiene algún problema al utilizar Stich, asegúrese de que las variables de entorno están configuradas correctamente y de que dispone de las claves API necesarias. Si el problema persiste, puede utilizar la función de notificación de errores de Stich para obtener ayuda:

- Informar de un error: "Informar de un error", "Error [error_description]"

Stich proporcionará entonces una respuesta útil generada por ChatGPT de OpenAI.
