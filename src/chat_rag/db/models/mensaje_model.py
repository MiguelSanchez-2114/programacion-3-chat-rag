from chat_rag.db.models.model_base import ModelBase

class MensajeModel(ModelBase):
    __table_name = "mensaje"

    def __init__(self, model: dict[str, object] = None):
        self.__id: int = model.get("id", None) if model else None
        self.__contenido: str = model.get("contenido", None) if model else None
        self.__emisor: str = model.get("emisor", None) if model else None
        self.__fecha: str = model.get("fecha", None) if model else None
        self.__id_conversacion: int = model.get("id_conversacion", None) if model else None
        super().__init__(self.__table_name, {
            "id": self.__id,
            "contenido": self.__contenido,
            "emisor": self.__emisor,
            "fecha": self.__fecha,
            "id_conversacion": self.__id_conversacion,
        })

    @staticmethod
    def obtener_todos() -> list["MensajeModel"]:
        mensajes = ModelBase.obtener_todos(MensajeModel.__table_name)
        return [MensajeModel(model=mensaje) for mensaje in mensajes]

    @property
    def id(self) -> int:
        self.__id = self.model.get("id", None)
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        self.__id = value
        self.model["id"] = value

    @property
    def contenido(self) -> str:
        self.__contenido = self.model.get("contenido", None)
        return self.__contenido

    @contenido.setter
    def contenido(self, value: str) -> None:
        self.__contenido = value
        self.model["contenido"] = value

    @property
    def emisor(self) -> str:
        self.__emisor = self.model.get("emisor", None)
        return self.__emisor

    @emisor.setter
    def emisor(self, value: str) -> None:
        self.__emisor = value
        self.model["emisor"] = value

    @property
    def fecha(self) -> str:
        self.__fecha = self.model.get("fecha", None)
        return self.__fecha

    @fecha.setter
    def fecha(self, value: str) -> None:
        self.__fecha = value
        self.model["fecha"] = value
    
    @property
    def id_conversacion(self) -> int:
        self.__id_conversacion = self.model.get("id_conversacion", None)
        return self.__id_conversacion

    @id_conversacion.setter
    def id_conversacion(self, value: int) -> None:
        self.__id_conversacion = value
        self.model["id_conversacion"] = value
