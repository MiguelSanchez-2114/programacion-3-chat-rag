from chat_rag.controllers.autorizacion import Autorizacion
from chat_rag.db.models.mensaje_model import MensajeModel
from chat_rag.config import config


class Chat:
    auth: Autorizacion = None
    def __init__(self):
        self.auth = Autorizacion()

    def obtener_ultimos_mensajes(self):
        mensajes = MensajeModel.obtener_ultimos_mensajes(self.auth.usuario_actual.id)
        return mensajes