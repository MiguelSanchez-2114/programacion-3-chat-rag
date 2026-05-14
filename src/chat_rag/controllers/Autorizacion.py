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
    
    

if __name__ == "__main__":
    print("1.- Iniciando prueba directa...")
    auth = Autorizacion()

    print("\n2. Login de prueba:")
    usuario = auth.login("usuario_prueba", "clave123")
    if usuario:
        print(f"   Exito: {usuario.username} (ID: {usuario.id})")
    else:
        print("   Fallo")
    print("\n3. Usuario actual:")
    print(f"   {auth.usuario_actual}")
    print("\n4. Cerrando sesión...")
    auth.cerrar_sesion()
    print("\n5. Usuario actual después de cerrar sesión:")
    print(f"   {auth.usuario_actual}")
    print("\nPrueba terminada.")