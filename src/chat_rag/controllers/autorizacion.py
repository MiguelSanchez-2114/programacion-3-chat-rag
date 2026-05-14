import hashlib
from datetime import datetime
from typing import Optional
from chat_rag.controllers.usuario import Usuario
from chat_rag.db.models.usuario_model import UsuarioModel  
from chat_rag.config import config

class Autorizacion:

    _instancia: Optional["Autorizacion"] = None

    def __new__(cls, salt: str = None):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializado = False
        return cls._instancia

    def __init__(self, salt: str = None):
        if getattr(self, "_inicializado", False):
            return
        self._usuario_sesion: Optional[Usuario] = None
        self._salt = salt or config.auth["salt"]
        self._inicializado = True

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(f"{self._salt}{password}".encode()).hexdigest()
    
    def login(self, username: str, password: str) -> Optional[Usuario]:
        try:
            user_obj = UsuarioModel.obtener_por_username(username)
            
            if user_obj and user_obj.password == self._hash_password(password):
                creado_en = user_obj.creado_en
                if isinstance(creado_en, str):
                    creado_en = datetime.fromisoformat(creado_en)

                # FIX: Guardar en sesión antes de retornar
                self._usuario_sesion = Usuario(
                    id=user_obj.id,
                    username=user_obj.username,
                    creado_en=creado_en
                )
                return self._usuario_sesion
            return None
        except Exception as e:
            print(f"Error en login: {e}")
            return None

    def cerrar_sesion(self) -> None:
        self._usuario_sesion = None

    @property
    def usuario_actual(self) -> Optional[Usuario]:
        return self._usuario_sesion
