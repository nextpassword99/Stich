import speech_recognition as sr
import pyttsx3 as tts
import datetime
import difflib
import random
import webbrowser
import wikipedia as wiki
import pywhatkit as kit
from openai import OpenAI
import google.generativeai as genai
import elevenlabs as lb
from dotenv import load_dotenv
import os
import soundfile as sf
import sounddevice as sd
import whisper
import tempfile
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Archivos externos
import comandos_stich as cmd


name_system = "Stich"

engine = tts.init()
listener = sr.Recognizer()
temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, "temp.wav")


def speak_elevenlabs(text):
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    set_api_key = ELEVENLABS_API_KEY
    audio = lb.generate(
        api_key=set_api_key, text=text, voice="Michael", model="eleven_multilingual_v1"
        # api_key=set_api_key, text=text, voice="Rachel", model="eleven_multilingual_v1"
        )
    audio_file = "audio_elevenlabs.mp3"
    lb.save(audio, audio_file)

    # Reproduce el audio
    data, sample_rate = sf.read(audio_file)
    sd.play(data, sample_rate)
    sd.wait()


def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            with open(save_path, "wb") as file:
                file.write(audio.get_wav_data())
            return save_path
    except Exception as e:
        print(e)
        return None


def recognizer_whisper(audio_path):
    print("Reconociendo...")
    audio_model = whisper.load_model("medium")
    transcription = audio_model.transcribe(
        audio_path, language="es", fp16=False, verbose="True"
    )
    text = transcription["text"].strip()
    return text


def recognition_command():
    try:
        comando = recognizer_whisper(listen())
        print(f"\nTexto reconocido: {comando}")

        lista_comandos = (
            cmd.comando_llamar_lista
            + cmd.comandos_saludo
            + cmd.comando_fecha
            + cmd.comando_imagen
            + cmd.comando_wiki
            + cmd.comando_video
            + cmd.comando_music
            + cmd.comandos_apunte
            + cmd.comando_whats
            + cmd.comando_gpt
            + cmd.comando_gemini
        )

        comando_reconocido = difflib.get_close_matches(
            comando, lista_comandos, 
            cutoff=0.5,
        )

        if len(comando_reconocido) > 0:
            comando_reconocido = comando_reconocido[0]
            print(f"\nComando reconocido: {comando_reconocido}")
            
            if comando_reconocido in cmd.comandos_saludo:
                saludar()
            elif comando_reconocido in cmd.comando_llamar_lista:
                llamar_lista()
            elif comando_reconocido in cmd.comando_fecha:
                fecha()
            elif comando_reconocido in cmd.comando_imagen:
                imagen = comando.lower().replace(comando_reconocido.lower(), "")
                imagen = imagen.strip()
                mostrar_imagen(imagen)
            elif comando_reconocido in cmd.comando_wiki:
                palabra = comando.lower().replace(comando_reconocido.lower(), "")
                palabra = palabra.strip()
                definir_wiki(palabra)
            elif comando_reconocido in cmd.comando_video:
                video = comando.lower().replace(comando_reconocido.lower(), "")
                video = video.strip()
                reproducir_video(video)
            elif comando_reconocido in cmd.comando_music or comando in cmd.comando_music:
                # music = comando.lower().replace(comando_reconocido, "")
                reproducir_music(comando)
            elif comando_reconocido in cmd.comandos_apunte:
                tomar_apuntes()
            elif comando_reconocido in cmd.comando_whats:
                enviar_whats()
            elif comando_reconocido in cmd.comando_gpt:
                chatgpt()
            elif comando_reconocido in cmd.comando_gemini:
                gemine()
            else:
                error_command(comando)
                # print("error no hay lista")

        else:
            error_command(comando)
            # print("error comando no reconocido")

    except sr.UnknownValueError:
        print("Error al reconocer el comando")

    except sr.RequestError as e:
        print(f"Error al realizar la solicitud: {str(e)}")


def recognition_voz():
    inicio = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")

        audio = inicio.listen(source, timeout=20000)
        print("Reconociendo...")
        try:
            text = inicio.recognize_google(audio, language="es-ES")
            print(f"Texto reconocido: {text}")
            return text
        except:
            print("Error en el reconocimiento, intente nuevamente")


def llamar_lista():
    lista_alumnos = ["Edison", "Alfred", "Daniel", "Macias"]
    alumnos_presentes = []
    print("Vamos a llamar lista.")
    speak_elevenlabs("Vamos a llamar lista.")

    for alumno in lista_alumnos:
        speak_elevenlabs(alumno)

        print(alumno)
        response = recognizer_whisper(listen())
        if response == "presente":
            alumnos_presentes.append(alumno)
        elif response == "no vino":
            print("no vino")
    for alumno in alumnos_presentes:
        print(f"{alumno} está presente.")
        speak_elevenlabs(f"{alumno} está presente.")


def saludar():
    lista_saludos = [
        f"Hola, soy {name_system}, ¿en que te puedo ayudar hoy?",
        f"Buen día, me llamo {name_system}, ¿qué necesitas hoy?",
        f"Soy{name_system}. ¿Qué quieres que haga por ti?",
        f"Mi nombre es {name_system}. ¿En que te puedo ayudar hoy?",
    ]
    saludo_random = random.choice(lista_saludos)
    speak_elevenlabs(saludo_random)
    print(saludo_random)


def fecha():
    fecha = datetime.date.today()
    print(f"La fecha de hoy es: {fecha}.")
    speak_elevenlabs(f"La fecha de hoy es: {fecha}.")


def mostrar_imagen(imagen):
    print(f"Mostrando imagen de {imagen}")
    speak_elevenlabs(f"Mostrando imagen de {imagen}")

    imagen_buscar = (
        "https://google.com/search?q="
        + imagen.replace(" ", "+")
        + "&tbm=isch&safe=active&ssui=on"
    )
    webbrowser.open(imagen_buscar)


def definir_wiki(palabra):
    wiki.set_lang("es")
    try:
        palabra = wiki.summary(palabra).split("\n")[0]
        print(palabra)
        speak_elevenlabs(palabra)
    except:
        print("No se encontró la información en Wikipedia")
        speak_elevenlabs("No se encontró la información en Wikipedia")


def reproducir_video(video):
    print(f"Reproduciendo el video de {video}")
    speak_elevenlabs(f"Reproduciendo el video de {video}")
    try:
        kit.playonyt(video)
    except:
        print("Lo siento, no logro reproducir el video.")


def tomar_apuntes():
    print("Anotando la siguiente frase...")
    speak_elevenlabs("Anotando la siguiente frase")

    apunte_text = recognizer_whisper(listen())
    if apunte_text:
        apunte_list = list(apunte_text)

        nm_apunte = ""
        for i in range(20):
            nm_apunte = nm_apunte + apunte_list[i]

        nm_apunte = nm_apunte.replace(" ", "-").lower()
        fecha_actual = str(datetime.datetime.now()).replace(".", "-").replace(":", "-").replace(" ", "-")
        name_file = nm_apunte + fecha_actual

        archivo_apunte = open(f"apuntes_asistente/{name_file}.txt", "w")
        archivo_apunte.write(apunte_text)
        archivo_apunte.close()
        print("Apunte guardado correctamente.")
        speak_elevenlabs("Apunte guardado correctamente.")

        print("¿Deseas que te lea tú apunte?")
        speak_elevenlabs("¿Deseas que te lea tú apunte?")

        if "si" in recognizer_whisper(listen()) :
            print(apunte_text)
            speak_elevenlabs(apunte_text)
    else:
        speak_elevenlabs("Lo siento, no pude capturar lo que dijiste.")

        print("Lo siento, no pude capturar lo que dijiste.")

def reproducir_music(action_music):
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    palabras_music = action_music.split()
    index_music = palabras_music.index("música") + 1
    music_select = " ".join(palabras_music[index_music:])
    print(f"Música detectada {music_select}")

    if music_select:
        main_path = r"D:\User\System\Música"
        list_path = []
        list_music = []
        for root, dirs, files in os.walk(main_path):
            for file in files:
                if file.endswith(".mp3"):
                    ruta_completa = os.path.join(root, file)
                    list_path.append(ruta_completa)
                    list_music.append(file.lower())

        music_reconocida = difflib.get_close_matches(
            music_select.lower(),
            list_music,
            cutoff=0.5
        )

        if len(music_reconocida) > 0:
            music_reconocida_path = list_path[list_music.index(music_reconocida[0])]
            print(f"Reproduciendo la música {music_reconocida[0]}...")
            subprocess.Popen(['start', '', music_reconocida_path], shell=True)

        else:
            print("No se encontró la música en los archivos locales. Buscando en Spotify...")

            sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
            result_music_search = sp.search(music_select)

            list_music_spotify = []
            list_autor_spotify = [[]]
            list_path_spotify = []

            for i in range (len(result_music_search["tracks"]["items"])):
                name_song = result_music_search["tracks"]["items"][i]["name"]
                path_music = result_music_search["tracks"]["items"][i]["uri"]
                for x in range (len(result_music_search["tracks"]["items"][i]["artists"])):
                    autor_song = result_music_search["tracks"]["items"][i]["artists"][x]["name"]
                    list_autor_spotify.append([])
                    list_autor_spotify[i].append(autor_song.lower())
                    

                list_path_spotify.append(path_music)
                list_music_spotify.append(name_song)


            if "de" in palabras_music:
                print("Autor detectado")

                index_autor = palabras_music.index("de") + 1
                autor_select = " ".join(palabras_music[index_autor:])
                print(autor_select)

                if len(list_path_spotify) > 0:
                    for y in range(len(list_autor_spotify)):
                        for autor in list_autor_spotify[y]:
                                print(autor)
                                print(autor_select)
                                if autor_select.lower() == autor.lower():
                                    print(f"Reproduciendo {list_music_spotify[y]} de {autor}")
                                    webbrowser.open(list_path_spotify[y])
                                    
                                    break
            
            else:
                if len(list_music_spotify) > 0:
                    for i in range(len(list_music_spotify)):
                        if music_select.lower() in list_music_spotify[i].lower():
                            print(f"Reproduciendo {list_music_spotify[i]}...")
                            webbrowser.open(list_path_spotify[i])
                            break
                        else:
                            print(f"Reproduciendo {list_music_spotify[0]}...")
                            webbrowser.open(list_path_spotify[0])
                            break


def enviar_whats():
    speak_elevenlabs("Escribiendo el mensaje")

    mensaje = recognizer_whisper(listen())
    if mensaje:
        kit.sendwhatmsg_instantly("+999999999", mensaje, 15, True, 1)


def chatgpt():
    print("Iniciando conversación con chatgpt...")
    speak_elevenlabs("Iniciando conversación con chatgpt")

    print("Escribiendo prompt...")
    speak_elevenlabs("Escribiendo prompt")

    salir_chatgpt = [
        "salir de chatgpt",
        "salir de chat gpt",
        "cerrar chatgpt",
    ]

    chatgpt_active = True
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    while chatgpt_active == True:
        prompt = recognition_voz()
        if prompt.lower() in salir_chatgpt:
            chatgpt_active = False
            print("Saliendo del chat de ChatGPT")
            speak_elevenlabs("Saliendo del chat de ChatGPT")

        else:
            completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )

            print(completion.choices[0].message.content)
            speak_elevenlabs(completion.choices[0].message.content)


def gemine():
    print("Iniciando conversación con Gemini Pro, de Google...")
    speak_elevenlabs("Iniciando conversación con Gemini Pro, de Google")

    gemine_active = True
    GEMINI_API_KEY = os.getenv("GEMINI_API_KYE")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat()

    print("Escribiendo prompt...")
    speak_elevenlabs("Escribiendo prompt...")

    salir_gemini = ["salir de gemini", "salir de google", "salir de géminis"]

    while gemine_active == True:
        prompt = recognizer_whisper(listen())

        if prompt.lower() in salir_gemini:
            gemine_active = False
            print("saliendo de Gemini Pro...")
            speak_elevenlabs("saliendo de Gemini Pro...")
        else:
            response = chat.send_message(prompt)
            print(response.text)
            speak_elevenlabs(response.text)


def error_command(comando):
    prompt = comando

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(completion.choices[0].message.content)
    speak_elevenlabs(completion.choices[0].message.content)


while True:
    recognition_command()
