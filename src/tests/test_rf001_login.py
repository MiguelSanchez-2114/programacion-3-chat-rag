import unittest
from unittest.mock import patch
from chat_rag.controllers.autorizacion import Autorizacion

class TestRF001_Login(unittest.TestCase):
    """
    Pruebas de excepción para RF001 - Iniciar sesión.
    Cubre: EX001 (Error de conexión BD) y EX002 (Campos inválidos).
    """

    def setUp(self):
        Autorizacion._instancia = None
        self.auth = Autorizacion(salt="test_salt_2026")

    def tearDown(self):
        self.auth.cerrar_sesion()
        Autorizacion._instancia = None

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_ex001_error_conexion_bd(self, mock_obtener):
        mock_obtener.side_effect = Exception("connection refused")
        resultado = self.auth.login("usuario_valido", "password_valido")
        self.assertIsNone(resultado)
        self.assertIsNone(self.auth.usuario_actual)

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_ex002_username_vacio(self, mock_obtener):
        # EX002: Se valida que el sistema maneje el campo vacío sin crashear
        resultado = self.auth.login("", "password123")
        self.assertIsNone(resultado)

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_ex002_password_vacio(self, mock_obtener):
        resultado = self.auth.login("usuario_valido", "")
        self.assertIsNone(resultado)

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_ex002_ambos_campos_vacios(self, mock_obtener):
        resultado = self.auth.login("", "")
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main(verbosity=2)