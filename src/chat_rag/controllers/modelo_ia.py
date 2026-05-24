from typing import Optional
from google import genai
from google.genai import errors
import random

from chat_rag.controllers.autorizacion import Autorizacion
from chat_rag.controllers.conversacion import Conversacion
from chat_rag.controllers.manejador_archivo import ManejadorArchivo
from chat_rag.config import config


class ModeloIA:

    _instancia: Optional["ModeloIA"] = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self):
        if getattr(self, "_inicializado", False):
            return
        self._inicializado = True

    def procesar_pregunta(self, pregunta: str, conversacion: Conversacion) -> str:
        if self.__validar_archivo(conversacion):
            contenido_archivo = self.__obtener_contenido_archivo(conversacion)
            respuesta = self.__generar_respuesta(pregunta, contenido_archivo)
            return respuesta
        else:
            raise ValueError("No se ha adjuntado ningún archivo a la conversación.")

    def __validar_archivo(self, conversacion: Conversacion) -> bool:
        return conversacion.archivo is not None
    
    def __obtener_contenido_archivo(self, conversacion: Conversacion) -> str:
        if self.__validar_archivo(conversacion):
            try:
                return ManejadorArchivo.obtener_contenido_archivo(f"{conversacion.id_usuario}/{conversacion.archivo.nombre}")
            except Exception as e:
                raise RuntimeError(f"Error al obtener el contenido del archivo: {e}")
        else:
            raise ValueError("No se ha adjuntado ningún archivo a la conversación.")

    def __generar_respuesta_aleatoria(self, pregunta: str, contenido_archivo: str) -> str:
        contenido_limpio = (contenido_archivo or "").strip()
        vista_previa = contenido_limpio[:120]

        respuestas = [
            f"Según el archivo, una respuesta breve sería: {vista_previa}. Si quieres, puedo ampliarlo por secciones.",
            f"Con base en tu pregunta '{pregunta}', el documento sugiere lo siguiente: {vista_previa}.",
            f"Interpretando el contenido, la idea principal es: {vista_previa}.",
            f"Respuesta simulada de IA: el texto parece indicar que {vista_previa}.",
            f"Buena pregunta. A partir del archivo, te respondería así: {vista_previa}.",
            f"Resumen generado: {vista_previa}. Puedo darte también una versión más técnica.",
        ]

        if not contenido_limpio:
            respuestas = [
                "No encontré contenido en el archivo adjunto. ¿Quieres que revisemos otro archivo?",
                "El archivo parece estar vacío o no se pudo leer su contenido.",
                "No hay texto disponible para generar una respuesta útil en este momento.",
            ]

        return random.choice(respuestas)
        
    def __generar_respuesta(self, pregunta: str, contenido_archivo: str) -> str:
        try:
            respuesta = self.__generar_respuesta_gemini(pregunta, contenido_archivo)
        except Exception as e:
            print("Error al generar respuesta con Gemini", e)
            respuesta = self.__generar_respuesta_aleatoria(pregunta, contenido_archivo)
        return respuesta

    def __generar_respuesta_gemini(self, pregunta: str, contenido_archivo: str) -> str:
        # TIP: Asegúrate de que esta llave sea la que copiaste de AI Studio
        LLAVE_API = config.gemini_api_key
        
        if not isinstance(LLAVE_API, str) or not LLAVE_API.strip():
            raise ValueError("La configuración 'gemini_api_key' no está definida o está vacía.")

        client = genai.Client(api_key=LLAVE_API)

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config={
                    "system_instruction": "Responde la pregunta a partir del siguiente texto: "+contenido_archivo
                },
                contents=""+pregunta
            )
            return response.text

        except errors.ClientError as e:
            # En google-genai se usa .code para obtener el status HTTP
            codigo = e.code

            if codigo == 429:
                raise ValueError("Error 429: Límite de cuota alcanzado. Esperando 60 segundos...")
                # time.sleep(60)
            elif codigo == 400:
                raise ValueError("Error 400: La API Key no es válida. Revisa que esté bien copiada en AI Studio.")
            else:
                raise ValueError(f"Error detectado (Código {codigo}): {e}")
        except Exception as e:
            raise ValueError(f"Ocurrió un error inesperado: {e}")
