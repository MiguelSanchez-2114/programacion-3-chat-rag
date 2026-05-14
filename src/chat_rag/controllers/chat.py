from chat_rag.controllers.autorizacion import Autorizacion
from chat_rag.db.models.mensaje_model import MensajeModel


class Chat:
    auth: Autorizacion = None
    def __init__(self):
        self.auth = Autorizacion()

    def obtener_ultimos_mensajes(self):
        usuario_actual = self.auth.usuario_actual
        if usuario_actual is None:
            raise ValueError("No hay un usuario autenticado.")
        mensajes = MensajeModel.obtener_ultimos_mensajes(self.auth.usuario_actual.id)
        return mensajes