import unittest
from unittest.mock import patch
from chat_rag.controllers.autorizacion import Autorizacion

class TestLogin(unittest.TestCase):
    """
    Pruebas de modulo autorizacion - Iniciar sesión.
    Cubre: EX001 (Error de conexión BD) y EX002 (Campos inválidos).
    """

    def setUp(self):
        Autorizacion._instancia = None
        self.auth = Autorizacion(salt="test_salt_2026")

    def tearDown(self):
        self.auth.cerrar_sesion()
        Autorizacion._instancia = None

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_error_conexion_bd(self, mock_obtener):
        mock_obtener.side_effect = Exception("connection refused")
        resultado = self.auth.login("usuario_valido", "password_valido")
        self.assertIsNone(resultado)
        self.assertIsNone(self.auth.usuario_actual)

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_username_vacio(self, mock_obtener):
        # EX002: Se valida que el sistema maneje el campo vacío sin crashear
        resultado = self.auth.login("", "password123")
        self.assertIsNone(resultado)

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_password_vacio(self, mock_obtener):
        resultado = self.auth.login("usuario_valido", "")
        self.assertIsNone(resultado)

    @patch("chat_rag.controllers.autorizacion.UsuarioModel.obtener_por_username")
    def test_ambos_campos_vacios(self, mock_obtener):
        resultado = self.auth.login("", "")
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main(verbosity=2)