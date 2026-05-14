from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from chat_rag.db.models.usuario_model import UsuarioModel  

class Usuario:
    
    def __init__(self, id: int, username: str, creado_en: Optional[datetime] = None):
        self.id = id
        self.username = username
        self.creado_en = creado_en or datetime.now()

    @classmethod
    def desde_modelo(cls, modelo: "UsuarioModel") -> "Usuario":
        return cls(
            id=modelo.id,
            username=modelo.username,
            creado_en=modelo.creado_en
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "creado_en": self.creado_en.isoformat() if isinstance(self.creado_en, datetime) else str(self.creado_en)
        }

    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, username='{self.username}')"