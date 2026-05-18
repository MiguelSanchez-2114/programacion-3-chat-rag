import unittest
from unittest.mock import patch
from datetime import datetime
from types import SimpleNamespace

from chat_rag.controllers.autorizacion import Autorizacion
from chat_rag.controllers.usuario import Usuario


class TestRF001_Login(unittest.TestCase):
    """
    Pruebas de excepción para RF001 - Iniciar sesión.
    Cubre: EX001 (Error de conexión BD) y EX002 (Campos inválidos).
    """

    def setUp(self):
        """Preparar entorno antes de cada prueba."""
        # Resetear Singleton para aislamiento entre tests
        Autorizacion._instancia = None
        self.auth = Autorizacion(salt="test_salt_2026")

    def tearDown(self):
        """Limpiar entorno después de cada prueba."""
        self.auth.cerrar_sesion()
        Autorizacion._instancia = None

    # =========================================================================
    # EX001 – Error de conexión a BD
    # =========================================================================
    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_ex001_error_conexion_bd(self, mock_obtener):
        """
        EX001: Cuando la BD no está disponible, login() debe retornar None
        y mostrar mensaje de error, sin crashear la aplicación.
        """
        # Simular excepción de conexión en la capa de datos
        mock_obtener.side_effect = Exception("connection refused")

        # Ejecutar login con credenciales válidas
        resultado = self.auth.login("usuario_valido", "password_valido")

        # Validar reacción esperada del sistema
        self.assertIsNone(resultado, "Login debe retornar None ante error de BD")
        self.assertIsNone(self.auth.usuario_actual, "No debe haber sesión activa")

    # =========================================================================
    # EX002 – Campos vacíos o inválidos
    # =========================================================================
    def test_ex002_username_vacio(self):
        """
        EX002a: Cuando username está vacío, no se debe consultar la BD
        y debe retornar None inmediatamente.
        """
        # Ejecutar login con username vacío
        resultado = self.auth.login("", "password123")

        # Validar: no se consulta BD, retorna fallo
        self.assertIsNone(resultado)
        self.assertIsNone(self.auth.usuario_actual)

    def test_ex002_password_vacio(self):
        """
        EX002b: Cuando password está vacío, no se debe consultar la BD
        y debe retornar None inmediatamente.
        """
        # Ejecutar login con password vacío
        resultado = self.auth.login("usuario_valido", "")

        # Validar: no se consulta BD, retorna fallo
        self.assertIsNone(resultado)
        self.assertIsNone(self.auth.usuario_actual)

    def test_ex002_ambos_campos_vacios(self):
        """
        EX002c: Cuando ambos campos están vacíos, validación temprana.
        """
        resultado = self.auth.login("", "")
        self.assertIsNone(resultado)
        self.assertIsNone(self.auth.usuario_actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)