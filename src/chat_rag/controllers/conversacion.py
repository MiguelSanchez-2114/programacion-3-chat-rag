from typing import Optional

from chat_rag.controllers.archivo import Archivo
from chat_rag.db.models.conversacion_model import ConversacionModel
from chat_rag.db.models.mensaje_model import MensajeModel

class Conversacion:
    
    def __init__(self, id: Optional[int] = None, id_usuario: Optional[int] = None):
        self.id = id
        self.id_usuario = id_usuario
        self.__mensajes: list[MensajeModel] = []
        self.__archivo: Archivo = None

    @classmethod
    def desde_modelo(cls, modelo: "ConversacionModel") -> "Conversacion":
        return cls(
            id=modelo.id,
            id_usuario=modelo.id_usuario
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "mensajes": [mensaje.model for mensaje in self.mensajes],
            "archivo": self.__archivo.to_dict() if self.__archivo else None
        }

    def __repr__(self) -> str:
        return f"Conversacion(id={self.id}, id_usuario={self.id_usuario})"
    
    @property
    def mensajes(self) -> list[MensajeModel]:
        return self.__mensajes

    @property
    def archivo(self) -> Optional[Archivo]:
        return self.__archivo

    def iniciar_conversacion(self):
        try:
            conversacion = ConversacionModel({
                "id_usuario": self.id_usuario
            })
            conversacion.guardar()
            self.id = conversacion.id
            self.id_usuario = conversacion.id_usuario
            self.__mensajes = []
            self.__archivo = None
        except Exception as e:
            raise ValueError(f"Error al iniciar conversación: {e}")
        
    def agregar_mensaje(self, contenido: str, emisor: str):
        if self.id is None:
            self.iniciar_conversacion()
        mensaje = MensajeModel({
            "contenido": contenido,
            "emisor": emisor,
            "id_conversacion": self.id
        })
        mensaje.guardar()
        self.__mensajes.append(mensaje)
        return mensaje
    
    def agregar_archivo(self, archivo: Archivo):
        if self.id is None:
            self.iniciar_conversacion()
        if self.archivo is None:
            archivo.guardar(self.id)
        else:
            archivo.actualizar(self.id)
        self.__archivo = archivo