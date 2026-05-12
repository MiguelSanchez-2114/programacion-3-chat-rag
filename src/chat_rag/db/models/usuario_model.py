from chat_rag.db.models.model_base import ModelBase
from datetime import datetime

class UsuarioModel(ModelBase):
    __table_name = "usuario"

    def __init__(self, model: dict[str, object] = None):
        self.__id: int = model.get("id", None) if model else None
        self.__username: str = model.get("username", None) if model else None
        self.__password: str = model.get("password", None) if model else None
        self.__creado_en: datetime = model.get("creado_en", None) if model else None
        super().__init__(self.__table_name, {
            "id": self.__id,
            "username": self.__username,
            "password": self.__password,
            "creado_en": self.__creado_en,
        })

    @staticmethod
    def obtener_todos() -> list["UsuarioModel"]:
        usuarios = ModelBase.obtener_todos(UsuarioModel.__table_name)
        return [UsuarioModel(model=usuario) for usuario in usuarios]

    @property
    def id(self) -> int:
        self.__id = self.model.get("id", None)
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        self.__id = value
        self.model["id"] = value

    @property
    def username(self) -> str:
        self.__username = self.model.get("username", None)
        return self.__username
    
    @username.setter
    def username(self, value: str) -> None:
        self.__username = value
        self.model["username"] = value

    @property
    def password(self) -> str:
        self.__password = self.model.get("password", None)
        return self.__password
    
    @password.setter
    def password(self, value: str) -> None:
        self.__password = value
        self.model["password"] = value

    @property
    def creado_en(self) -> datetime:
        self.__creado_en = self.model.get("creado_en", None)
        return self.__creado_en
    
    @creado_en.setter
    def creado_en(self, value: datetime) -> None:
        self.__creado_en = value
        self.model["creado_en"] = value