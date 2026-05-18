from pathlib import Path
import shutil

from chat_rag.config import config
from chat_rag.controllers.archivo import Archivo

class ManejadorArchivo:

    tipo_archivo_permitido = config.file_types_allowed
    ruta_base = config.file_storage_path

    @staticmethod
    def validar_archivo(archivo: Path) -> bool:
        if not archivo.exists():
            raise FileNotFoundError("El archivo no existe")
        if not archivo.is_file():
            raise ValueError("La ruta especificada no es un archivo")
        if archivo.suffix.lower() not in ManejadorArchivo.tipo_archivo_permitido:
            raise ValueError("El tipo de archivo no está permitido")
        return True
    
    @staticmethod
    def obtener_informacion_archivo(ruta_archivo: str, id_user: int) -> Archivo:
        archivo_sistema = Path(ruta_archivo)
        ManejadorArchivo.validar_archivo(archivo_sistema)
        nombre_archivo = ManejadorArchivo.almacenar_archivo(archivo_sistema, id_user=str(id_user))
        
        archivo = Archivo(
            id=None,
            nombre=nombre_archivo,
            tipo=archivo_sistema.suffix,
            tamano=str(archivo_sistema.stat().st_size),
            id_conversacion=None
        )
        return archivo
    
    @staticmethod
    def almacenar_archivo(archivo: Path, id_user: str) -> str:
        ruta = f"{ManejadorArchivo.ruta_base.replace('[id_user]', id_user)}"
        ruta_archivo_destino = Path(ruta)
        ruta_archivo_destino.mkdir(parents=True, exist_ok=True)
        ruta_archivo_destino = Path(f"{ruta_archivo_destino}/{archivo.name}")
        if ruta_archivo_destino.exists():
            def generar_nombre_unico(ruta: Path) -> Path:
                contador = 1
                while True:
                    nuevo_nombre = f"{ruta.stem}_{contador}{ruta.suffix}"
                    nueva_ruta = f"{ruta.parent}/{nuevo_nombre}"
                    if not Path(nueva_ruta).exists():
                        return Path(nueva_ruta)
                    contador += 1
            ruta_archivo_destino = generar_nombre_unico(ruta_archivo_destino)
        shutil.copy(archivo.resolve(), ruta_archivo_destino.resolve())
        return ruta_archivo_destino.name