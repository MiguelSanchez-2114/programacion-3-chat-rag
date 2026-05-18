from chat_rag.db.models.model_base import ModelBase
from datetime import datetime
from chat_rag.db.connection import BaseDeDatos
from typing import Optional

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

    @staticmethod
    def obtener_por_username(username: str) -> Optional['UsuarioModel']:
        conexion = ModelBase.obtener_conexion()
        schema = BaseDeDatos.instancia().schema
        
        try:
            sql = f"""
                SELECT id, username, password, creado_en 
                FROM {schema}.usuario 
                WHERE username = %s
            """
            cursor = conexion.cursor()
            cursor.execute(sql, (username,))
            record = cursor.fetchone()
            
            if record:
                columnas = [desc[0] for desc in cursor.description]
                return UsuarioModel(dict(zip(columnas, record)))
            return None
        except Exception as e:
            print(f"Error al obtener usuario por username: {e}")
            return None
