from chat_rag.db.models.model_base import ModelBase

class ConversacionModel(ModelBase):
    __table_name = "conversacion"

    def __init__(self, model: dict[str, object] = None):
        self.__id: int = model.get("id", None) if model else None
        self.__id_usuario: str = model.get("id_usuario", None) if model else None
        super().__init__(self.__table_name, {
            "id": self.__id,
            "id_usuario": self.__id_usuario,
        })

    @staticmethod
    def obtener_todos() -> list["ConversacionModel"]:
        conversaciones = ModelBase.obtener_todos(ConversacionModel.__table_name)
        return [ConversacionModel(model=conversacion) for conversacion in conversaciones]

    @property
    def id(self) -> int:
        self.__id = self.model.get("id", None)
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        self.__id = value
        self.model["id"] = value
    
    @property
    def id_usuario(self) -> str:
        self.__id_usuario = self.model.get("id_usuario", None)
        return self.__id_usuario
    
    @id_usuario.setter
    def id_usuario(self, value: str) -> None:
        self.__id_usuario = value
        self.model["id_usuario"] = value
    
