from chat_rag.controllers.autorizacion import Autorizacion
from chat_rag.db.models.mensaje_model import MensajeModel
from chat_rag.controllers.conversacion import Conversacion
from chat_rag.config import config

class Chat:
    sesion: Autorizacion = None
    __conversacion: Conversacion = None
    def __init__(self):
        self.sesion = Autorizacion()

    @property
    def conversacion(self) -> Conversacion:
        if self.__conversacion is None:
            self.__iniciar_conversacion()
        return self.__conversacion

    def obtener_ultimos_mensajes(self):
        usuario_actual = self.sesion.usuario_actual
        if usuario_actual is None:
            raise ValueError("No hay un usuario autenticado.")
        mensajes = MensajeModel.obtener_ultimos_mensajes(self.sesion.usuario_actual.id)
        return mensajes
    
    def agregar_mensaje(self, contenido: str, emisor: str):
        try:
            return self.conversacion.agregar_mensaje(contenido, emisor)
        except Exception as e:
            raise ValueError(f"Error al agregar mensaje: {e}")

    def __iniciar_conversacion(self):
        if self.sesion.usuario_actual is None:
            raise ValueError("No hay un usuario autenticado.")
        if self.__conversacion is None:
            try:
                self.__conversacion = Conversacion(id_usuario=self.sesion.usuario_actual.id)
                self.__conversacion.iniciar_conversacion()
            except Exception as e:
                raise ValueError(f"Error al iniciar conversación: {e}")