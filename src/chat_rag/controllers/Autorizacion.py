import hashlib
from datetime import datetime
from typing import Optional
from .usuario import Usuario

from chat_rag.db.models.usuario_model import UsuarioModel  

class Autorizacion:

    def __init__(self, salt: str = "chat_rag_seguro_2026"):
        self._usuario_sesion: Optional[Usuario] = None
        self._salt = salt

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(f"{self._salt}{password}".encode()).hexdigest()

    def login(self, username: str, password: str) -> Optional[Usuario]:
        try:
            usuarios = UsuarioModel.obtener_todos()
            for user_obj in usuarios:
                if user_obj.username == username and user_obj.password == self._hash_password(password):
                    creado_en = user_obj.creado_en
                    if isinstance(creado_en, str):
                        creado_en = datetime.fromisoformat(creado_en)

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

    def registrar(self, username: str, password: str) -> bool:
        try:
            usuarios = UsuarioModel.obtener_todos()
            if any(u.username == username.strip() for u in usuarios):
                print("El nombre de usuario ya esta registrado.")
                return False

            nuevo = UsuarioModel({
                "username": username.strip(),
                "password": self._hash_password(password),
                "creado_en": datetime.now()
            })
            nuevo_id = nuevo.guardar()
            return nuevo_id is not None
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False

    def cerrar_sesion(self) -> None:
        self._usuario_sesion = None

    @property
    def usuario_actual(self) -> Optional[Usuario]:
        return self._usuario_sesion
    
    

if __name__ == "__main__":
    print("Iniciando prueba directa...")
    auth = Autorizacion()

    print("\n1. Registro de prueba:")
    auth.registrar("usuario_prueba", "clave123")

    print("\n2. Login de prueba:")
    usuario = auth.login("usuario_prueba", "clave123")
    if usuario:
        print(f"   Exito: {usuario.username} (ID: {usuario.id})")
    else:
        print("   Fallo")

    auth.cerrar_sesion()
    print("\nPrueba terminada.")