import unittest
import tempfile
import os
from pathlib import Path  
from types import SimpleNamespace
from unittest.mock import patch, PropertyMock

from chat_rag.controllers.chat import Chat
from chat_rag.controllers.conversacion import Conversacion
from chat_rag.controllers.modelo_ia import ModeloIA
from chat_rag.controllers.manejador_archivo import ManejadorArchivo
from chat_rag.controllers.exportador import Exportador


class TestChat(unittest.TestCase):
    """
    Pruebas para el módulo Chat (visualización de conversaciones).
    
    Casos de uso:
    1. Manejo de error cuando la base de datos es inaccesible.
    2. Exportación de conversación con metadatos incompletos.
    """

    def setUp(self):
        self.user = SimpleNamespace(id=1)
        
    @patch('chat_rag.controllers.autorizacion.Autorizacion.usuario_actual', new_callable=PropertyMock)
    def test_error_conexion_bd_al_cargar_mensajes(self, mock_usuario):
        """
        Caso: La BD está caída al intentar obtener mensajes.
        El sistema debe propagar la excepción de forma controlada.
        """
        mock_usuario.return_value = self.user
        with patch('chat_rag.db.models.mensaje_model.MensajeModel.obtener_ultimos_mensajes', 
                   side_effect=Exception('DB down')):
            chat = Chat()
            with self.assertRaises(Exception) as exc_info:
                chat.obtener_ultimos_mensajes()
            # Valida que la excepción capturada sea exactamente la simulada
            self.assertEqual(str(exc_info.exception), 'DB down')

    def test_exportar_con_mensajes_sin_fecha_no_falla(self):
        """
        Caso: Mensajes con metadatos incompletos (fecha None).
        El exportador debe manejar el caso y generar JSON válido.
        """
        fake_msg = SimpleNamespace(emisor='user', contenido='hola', fecha=None)
        
        with patch.object(Conversacion, 'mensajes', new_callable=PropertyMock) as mock_mensajes:
            mock_mensajes.return_value = [fake_msg]
            conversacion = Conversacion(id=10, id_usuario=1)
            
            json_text = Exportador.to_json(conversacion)
            self.assertIn('mensajes', json_text)


class TestConversacion(unittest.TestCase):
    """
    Pruebas para el modulo Conversacion (envio y registro de mensajes).
    """

    def setUp(self):
        # Resetear Singleton de ModeloIA para garantizar aislamiento entre pruebas
        ModeloIA._instancia = None

    def tearDown(self):
        # Limpiar estado compartido despues de cada prueba
        ModeloIA._instancia = None

    def test_error_bd_al_guardar_mensaje(self):
        """
        Caso: Fallo de escritura en BD al agregar un mensaje.
        El sistema debe propagar la excepcion para manejo en capa superior.
        """
        conv = Conversacion(id=5, id_usuario=1)
        with patch('chat_rag.db.models.mensaje_model.MensajeModel.guardar', 
                   side_effect=Exception('Write error')):
            with self.assertRaises(Exception) as exc_info:
                conv.agregar_mensaje('hola', 'user')
            # Verificacion estricta del mensaje simulado
            self.assertEqual(str(exc_info.exception), 'Write error')

    def test_error_generar_respuesta_sin_archivo(self):
        """
        Caso: Solicitar respuesta basada en archivo cuando no hay archivo asociado.
        El sistema debe validar el contexto y lanzar ValueError.
        """
        conversacion = Conversacion(id=2, id_usuario=1)
        modelo = ModeloIA()
        with self.assertRaises(ValueError) as exc_info:
            modelo.procesar_pregunta('¿Qué dice el archivo?', conversacion)
        # Verificacion estricta del error generado
        self.assertIn('archivo', str(exc_info.exception).lower())


class TestManejadorArchivo(unittest.TestCase):
    """
    Pruebas para el módulo ManejadorArchivo (carga y validación de archivos).
    
    Casos de uso:
    1. Rechazo de formatos de archivo no permitidos.
    2. Validación de existencia de archivo antes de procesar.
    """

    def test_rechazar_formato_no_permitido(self):
        """
        Caso: Usuario intenta cargar archivo con extension no valida (.exe).
        El sistema debe validar la extension y lanzar ValueError.
        """
        tmp = tempfile.NamedTemporaryFile(suffix='.exe', delete=False)
        tmp.write(b'test')
        tmp.flush()
        tmp.close()
        try:
            with self.assertRaises(ValueError):
                ManejadorArchivo.validar_archivo(Path(tmp.name))
        finally:
            os.unlink(tmp.name)

    def test_error_archivo_no_encontrado(self):
        """
        Caso: Intentar obtener información de un archivo que no existe.
        El sistema debe lanzar FileNotFoundError.
        """
        with self.assertRaises(FileNotFoundError):
            ManejadorArchivo.obtener_informacion_archivo('no_existe.txt', 1)


class TestExportador(unittest.TestCase):
    """
    Pruebas para el módulo Exportador (generación de archivos de exportación).
    
    Casos de uso:
    1. Serialización de conversación a JSON con datos válidos.
    """

    def test_generar_json_con_mensajes_validos(self):
        """
        Caso: Exportar conversación con mensajes bien formados.
        El sistema debe generar JSON con la estructura esperada.
        """
        conversacion = Conversacion(id=9, id_usuario=1)
        fake_msg = SimpleNamespace(emisor='u', contenido='hola', fecha=None)
        conversacion._Conversacion__mensajes = [fake_msg]
        
        txt = Exportador.to_json(conversacion)
        self.assertIn('conversacion_id', txt)


class TestRegistroConversacion(unittest.TestCase):
    """
    Pruebas para el registro de conversaciones en base de datos.
    
    Casos de uso:
    1. Error de conexión al iniciar una nueva conversación.
    """

    def test_error_conexion_bd_al_iniciar_conversacion(self):
        """
        Caso: La BD está inaccesible al crear una nueva conversación.
        El sistema debe propagar la excepción para manejo en capa superior.
        """
        conv = Conversacion(id=None, id_usuario=1)
        with patch('chat_rag.db.models.conversacion_model.ConversacionModel.guardar', 
                   side_effect=Exception('DB down')):
            with self.assertRaises(ValueError):
                conv.iniciar_conversacion()


class TestAsociarArchivo(unittest.TestCase):
    """
    Pruebas para la asociación de archivos a conversaciones.
    
    Casos de uso:
    1. Error de base de datos al registrar la asociación archivo-conversación.
    """

    def test_error_bd_al_registrar_asociacion_archivo(self):
        """
        Caso: Fallo en BD al guardar la relación entre archivo y conversación.
        Se mockea la capa de archivos para evitar escritura en disco y dependencias de configuración.
        """
        # Simular objeto Archivo sin tocar el sistema de archivos
        archivo_mock = SimpleNamespace(
            id=None,
            nombre="prueba_segura.txt",
            ruta="/mock/ruta.txt",
            tipo="text/plain"
        )

        with patch.object(ManejadorArchivo, 'obtener_informacion_archivo', return_value=archivo_mock):
            with patch('chat_rag.db.models.archivo_model.ArchivoModel.guardar', side_effect=Exception('DB error')):
                conv = Conversacion(id=3, id_usuario=1)
                with self.assertRaises(Exception):
                    conv.agregar_archivo(archivo_mock)


if __name__ == '__main__':
    unittest.main(verbosity=2)